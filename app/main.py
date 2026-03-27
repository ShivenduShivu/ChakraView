from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.core.middleware import LoggingMiddleware
from app.api.routes import router
from app.registry.loader import load_agents, load_tasks, get_agent, get_task


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    load_agents()
    load_tasks()

    # Verify: print one agent and one task
    sample_agent = get_agent("research_agent")
    sample_task  = get_task("generate_report")
    print(f"[startup] sample agent  : {sample_agent}")
    print(f"[startup] sample task   : {sample_task}")

    yield
    # --- Shutdown (nothing to clean up yet) ---


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan,
    )

    app.add_middleware(LoggingMiddleware)
    app.include_router(router, prefix="/api/v1")

    @app.get("/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    return app


app = create_app()
