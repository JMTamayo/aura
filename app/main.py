from fastapi import FastAPI

from app.api.router import server_router
from app.config.conf import CONFIG


app: FastAPI = FastAPI(
    title=CONFIG.API_NAME,
    description=CONFIG.API_DESCRIPTION,
    version=CONFIG.API_VERSION,
)

app.include_router(server_router)
