from fastapi import FastAPI
from app.api.endpoints import router
import uvicorn

app = FastAPI(openapi_url="/api/presidio_anonymizer/openapi.json", docs_url="/api/presidio_anonymizer/docs")

app.include_router(router, prefix="/api/presidio_anonymizer", tags=["presidio_anonymizer"])

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=3000)