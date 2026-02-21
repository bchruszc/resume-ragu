"""FastAPI application entry point."""

import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import JSONResponse

from app.config import settings
from app.errors import AppError, app_error_handler
from app.logging_setup import request_id_var, setup_logging
from app.routes import profile, chat

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: setup logging at startup."""
    setup_logging(settings.LOG_LEVEL)
    logger.info("Resume Ragu API started")
    yield


app = FastAPI(title="Resume Ragu API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Exception handlers
app.add_exception_handler(AppError, app_error_handler)


# Request ID middleware
@app.middleware("http")
async def add_request_id(request: Request, call_next):
    """Generate request ID and add to context and response headers."""
    request_id = str(uuid.uuid4())
    request_id_var.set(request_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id
    return response


# Include routers
app.include_router(profile.router, prefix="/api")
app.include_router(chat.router, prefix="/api")


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "ok"}
