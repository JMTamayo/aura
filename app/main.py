from fastapi import FastAPI

from app.api.router import server_router
from app.config.conf import CONFIG

app: FastAPI = FastAPI(
    title=CONFIG.SERVER_API_NAME,
    description=CONFIG.SERVER_API_DESCRIPTION,
    version=CONFIG.SERVER_API_VERSION,
)

app.include_router(server_router)
