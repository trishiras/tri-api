from typing import Any
from fastapi import FastAPI
from beanie import init_beanie
from tri_api.core.logger import logger
from tri_api.models.trove.cve import CVE
from tri_api.support.enums import APIenum
from contextlib import asynccontextmanager
from tri_api.__version__ import __version__
from tri_api.models.tenant.user import User
from tri_api.models.super.user import SuperUser
from tri_api.support.config import CONFIGURATION
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.middleware.cors import CORSMiddleware
from tri_api.models.tenant.tenant import InviteToken
from tri_api.models.trove.taxonomy import CWE, CAPEC
from tri_api.models.scanner.task import ScannerTask


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """
    Initialize and cleanup application services.

    Args:
        app: FastAPI application instance
    """
    client = None
    try:
        # Initialize MongoDB client
        client = AsyncIOMotorClient(CONFIGURATION.mongo_uri)
        # client = connect_to_mongodb()
        app.mongodb_client = client
        app.mongodb = client.account

        # Initialize Beanie with models
        await init_beanie(
            database=app.mongodb,
            document_models=[
                CVE,
                CWE,
                User,
                CAPEC,
                SuperUser,
                InviteToken,
                ScannerTask,
            ],
        )

        logger.info("MongoDB connection established")
        logger.info("|||---Startup complete---|||")

        yield

    except Exception as e:
        logger.error(f"Startup Error: {str(e)}")
        raise

    finally:
        # Cleanup
        if client:
            client.close()
            logger.info("MongoDB connection closed")
        logger.info("|||---Shutdown complete---|||")


def create_application() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        FastAPI: Configured FastAPI application instance
    """
    application = FastAPI(
        title=APIenum.title.value,
        description=APIenum.description.value,
        version=__version__,
        contact=APIenum.contact.value,
        lifespan=lifespan,
        docs_url="/api/docs",
        openapi_url="/api/openapi.json",
    )

    # Add CORS middleware
    application.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return application


# Create the FastAPI application instance
app = create_application()


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "version": __version__,
        "mongodb_status": "connected" if app.mongodb_client else "disconnected",
    }


@app.on_event("startup")
async def startup_event():
    """Startup event handler"""
    logger.info(f"Starting {APIenum.title.value} version {__version__}")


@app.on_event("shutdown")
async def shutdown_event():
    """Shutdown event handler"""
    logger.info(f"Shutting down {APIenum.title.value}")
