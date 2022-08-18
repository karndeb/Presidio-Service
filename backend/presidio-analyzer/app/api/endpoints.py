"""FASTAPI SERVER """
import json
import logging
import os
import sys
from logging.config import fileConfig
from pathlib import Path
from .models import request_models
from fastapi import FastAPI, Request
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.responses import JSONResponse

from presidio_analyzer.analyzer_engine import AnalyzerEngine
# from presidio_analyzer.analyzer_request import AnalyzerRequest

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
    """HTTP Server for calling Presidio Analyzer."""

    def __init__(self):
        fileConfig(Path(Path(__file__).parent, LOGGING_CONF_FILE))
        self.logger = logging.getLogger("presidio-analyzer")
        self.logger.setLevel(os.environ.get("LOG_LEVEL", self.logger.level))
        self.logger.info("Starting analyzer engine")
        self.engine = AnalyzerEngine()
        self.logger.info(WELCOME_MESSAGE)

    @router.get("/health")
    def health(self):
        """Return basic health probe result."""
        message = "Presidio Analyzer service is up"
        return self.logger.info(message)

    @router.post("/analyze")
    def analyze(self, request: request_models.AnalyzeRequest):
        """Execute the analyzer function."""
        # Parse the request params
        try:
            req_data = request
            if not req_data.text:
                raise Exception("No text provided")

            if not req_data.language:
                raise Exception("No language provided")

            recognizer_result_list = self.engine.analyze(
                text=req_data.text,
                language=req_data.language,
                correlation_id=req_data.correlation_id,
                score_threshold=req_data.score_threshold,
                entities=req_data.entities,
                return_decision_process=req_data.return_decision_process,
                ad_hoc_recognizers=req_data.ad_hoc_recognizers,
                context=req_data.context,
            )

            return json.dumps(recognizer_result_list, default=lambda o: o.to_dict(), sort_keys=True)
        except TypeError as te:
            error_msg = (
                f"Failed to parse /analyze request "
                f"for AnalyzerEngine.analyze(). {te.args[0]}"
            )
            self.logger.error(error_msg)
            return error_msg, 400

        except Exception as e:
            self.logger.error(
                f"A fatal error occurred during execution of "
                f"AnalyzerEngine.analyze(). {e}"
            )
            return e.args[0], 500

    @router.get("/recognizers")
    def recognizers(self, request: Request, language: str):
        """Return a list of supported recognizers."""
        language = request.get(language)
        try:
            recognizers_list = self.engine.get_recognizers(language)
            names = [o.name for o in recognizers_list]
            return names, 200
        except Exception as e:
            self.logger.error(
                f"A fatal error occurred during execution of "
                f"AnalyzerEngine.get_recognizers(). {e}"
            )
            return e.args[0], 500

    @router.get("/supportedentities")
    def supported_entities(self, request: Request, language: str):
        """Return a list of supported entities."""
        language = request.get(language)
        try:
            entities_list = self.engine.get_supported_entities(language)
            return entities_list, 200
        except Exception as e:
            self.logger.error(
                f"A fatal error occurred during execution of "
                f"AnalyzerEngine.supported_entities(). {e}"
            )
            return e.args[0], 500

    # @staticmethod
    # def http_exception(e):
    #     return JSONResponse(e.description, e.code)


# if __name__ == "__main__":
#     port = int(os.environ.get("PORT", DEFAULT_PORT))
#     server = Server()
#     server.app.run(host="0.0.0.0", port=port)