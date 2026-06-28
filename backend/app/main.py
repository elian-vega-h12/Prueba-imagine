from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.controllers.clients import router as clients_router
from app.controllers.health import router as health_router
from app.controllers.tickets import router as tickets_router
from app.core.config import get_settings


def create_app() -> FastAPI:
    settings = get_settings()
    application = FastAPI(title=settings.app_name)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.exception_handler(RequestValidationError)
    async def validation_exception_handler(request, exc):
        print(f"--- VALIDATION ERROR ---")
        print(f"URL: {request.url}")
        print(f"Errors: {exc.errors()}")
        try:
            body = await request.body()
            print(f"Body: {body.decode()}")
        except Exception:
            pass
        print(f"------------------------")
        
        # Clean up bytes in errors to prevent json serialization issues
        cleaned_errors = []
        for err in exc.errors():
            cleaned_err = dict(err)
            if "input" in cleaned_err and isinstance(cleaned_err["input"], bytes):
                cleaned_err["input"] = cleaned_err["input"].decode(errors="ignore")
            cleaned_errors.append(cleaned_err)
            
        return JSONResponse(
            status_code=422,
            content={"detail": cleaned_errors}
        )

    application.include_router(health_router)
    application.include_router(clients_router)
    application.include_router(tickets_router)

    return application


app = create_app()
