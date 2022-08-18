import logging
import os
from logging.config import fileConfig
from pathlib import Path
from .models import request_models
from fastapi import FastAPI
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.encoders import jsonable_encoder

from presidio_anonymizer import AnonymizerEngine, DeanonymizeEngine
# from presidio_anonymizer.entities import InvalidParamException
from presidio_anonymizer.services.app_entities_convertor import AppEntitiesConvertor

DEFAULT_PORT = "3000"

LOGGING_CONF_FILE = "../../logging.ini"

WELCOME_MESSAGE = r"""
 _______  _______  _______  _______ _________ ______  _________ _______
(  ____ )(  ____ )(  ____ \(  ____ \\__   __/(  __  \ \__   __/(  ___  )
| (    )|| (    )|| (    \/| (    \/   ) (   | (  \  )   ) (   | (   ) |
| (____)|| (____)|| (__    | (_____    | |   | |   ) |   | |   | |   | |
|  _____)|     __)|  __)   (_____  )   | |   | |   | |   | |   | |   | |
| (      | (\ (   | (            ) |   | |   | |   ) |   | |   | |   | |
| )      | ) \ \__| (____/\/\____) |___) (___| (__/  )___) (___| (___) |
|/       |/   \__/(_______/\_______)\_______/(______/ \_______/(_______)
"""
app = FastAPI()
router = InferringRouter()


@cbv(router)
class Server:
    """FastAPI server for anonymizer."""

    def __init__(self):
        fileConfig(Path(Path(__file__).parent, LOGGING_CONF_FILE))
        self.logger = logging.getLogger("presidio-anonymizer")
        self.logger.setLevel(os.environ.get("LOG_LEVEL", self.logger.level))
        self.logger.info("Starting anonymizer engine")
        self.anonymizer = AnonymizerEngine()
        self.deanonymize = DeanonymizeEngine()
        self.logger.info(WELCOME_MESSAGE)

    @router.get("/health")
    def health(self):
        """Return basic health probe result."""
        message = "Presidio Anonymizer service is up"
        return self.logger.info(message)

    @router.post("/anonymize")
    def anonymize(self, request: request_models.AnonymizeRequest):
        content = request
        if not content:
            raise self.logger.error("Invalid request json")

        anonymizers_config = AppEntitiesConvertor.operators_config_from_json(content.anonymizers)
        if AppEntitiesConvertor.check_custom_operator(anonymizers_config):
            raise self.logger.error("Custom type anonymizer is not supported")

        analyzer_results = AppEntitiesConvertor.analyzer_results_from_json(
            content.analyzer_results
        )
        anoymizer_result = self.anonymizer.anonymize(
            text=content.text,
            analyzer_results=analyzer_results,
            operators=anonymizers_config,
        )
        return anoymizer_result

    @router.post("/deanonymize")
    def deanonymize(self, request: request_models.DeanonymizeRequest):
        content = request
        if not content:
            raise self.logger.error("Invalid request json")
        text = content.text
        deanonymize_entities = AppEntitiesConvertor.deanonymize_entities_from_json(jsonable_encoder(content))
        deanonymize_config = AppEntitiesConvertor.operators_config_from_json(content.deanonymizers)
        deanonymized_response = self.deanonymize.deanonymize(
            text=text, entities=deanonymize_entities, operators=deanonymize_config)
        return deanonymized_response

    @router.get("/anonymizers")
    def anonymizers(self):
        """Return a list of supported anonymizers."""
        return self.anonymizer.get_anonymizers()

    @router.get("/deanonymizers")
    def deanonymizers(self):
        """Return a list of supported deanonymizers."""
        return self.deanonymize.get_deanonymizers()

    # @self.app.errorhandler(InvalidParamException)
    # def invalid_param(err):
    #     self.logger.warning(
    #         f"Request failed with parameter validation error: {err.err_msg}"
    #     )
    #     return jsonify(error=err.err_msg), 422
    #
    # @self.app.errorhandler(HTTPException)
    # def http_exception(e):
    #     return jsonify(error=e.description), e.code
    #
    # @self.app.errorhandler(Exception)
    # def server_error(e):
    #     self.logger.error(f"A fatal error occurred during execution: {e}")
    #     return jsonify(error="Internal server error"), 500


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", DEFAULT_PORT))
#     server = Server()
#     server.app.run(host="0.0.0.0", port=port)
