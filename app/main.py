from fastapi import FastAPI

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.core.middleware import TraceIDMiddleware

configure_logging()
settings = get_settings()

app = FastAPI(title=settings.app_name)

app.add_middleware(TraceIDMiddleware)


@app.get("/")
def root():
    return {"message": settings.app_name}


@app.get("/health")
def health():
    return {"status": "ok", "environment": settings.app_env}


@app.get("/version")
def version():
    return {"version": settings.api_version}