from fastapi import FastAPI
from fastapi_swagger import patch_fastapi

app = FastAPI(docs_url=None,swagger_ui_oauth2_redirect_url=None)
patch_fastapi(app,docs_url="/docs")

@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}
