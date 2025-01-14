from contextlib import asynccontextmanager
from fastapi import FastAPI
from src.api.v1.routes import router as v1_router
from src.services.external_api import ExternalAPIService


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage the lifespan of FastAPI application services."""
    app.state.api_service = ExternalAPIService()
    yield
    await app.state.api_service.close()


app = FastAPI(
    title="API Wrapper Example",
    description="A versioned API wrapper example",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount v1 routes
app.include_router(v1_router, prefix="/v1")


@app.get("/")
async def root():
    return {
        "message": "Welcome to the API Wrapper Example",
        "versions": {"v1": "/v1"},
    }
