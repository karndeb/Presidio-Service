from fastapi import FastAPI
from app.api.endpoints import router
import uvicorn

app = FastAPI(openapi_url="/api/presidio_analyzer/openapi.json", docs_url="/api/presidio_analyzer/docs")

app.include_router(router, prefix="/api/presidio_analyzer", tags=["presidio_analyzer"])

# if __name__ == "__main__":
#     uvicorn.run("main:app", host="0.0.0.0", port=3000)

