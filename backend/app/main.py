import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routers import upload, chat, extraction

logger = logging.getLogger(__name__)

# Attempt to configure Logfire if token exists — fully optional
_logfire_enabled = False
try:
    import logfire

    if settings.logfire_token:
        os.environ["LOGFIRE_TOKEN"] = settings.logfire_token
        logfire.configure(pydantic_plugin=logfire.PydanticPlugin(record="all"))
        _logfire_enabled = True
        logger.info("Logfire observability enabled.")
    else:
        logger.info("Logfire token not set — observability disabled.")
except ImportError:
    logger.warning("logfire package not installed — observability disabled.")
except Exception as e:
    logger.warning(f"Failed to configure Logfire: {e}")

app = FastAPI(
    title="Mittelstand Document Agent API",
    description="Backend for querying and extracting data from German business PDFs",
    version="1.0.0",
)

if _logfire_enabled:
    try:
        logfire.instrument_fastapi(app)
    except Exception as e:
        logger.warning(f"Failed to instrument FastAPI with Logfire: {e}")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(upload.router, prefix="/api")
app.include_router(chat.router, prefix="/api")
app.include_router(extraction.router, prefix="/api")

@app.get("/api/health")
async def health_check():
    return {"status": "ok", "llm": settings.ollama_chat_model}
