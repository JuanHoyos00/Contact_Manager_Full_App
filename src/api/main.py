import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.api.routers.contacts import router as contacts_router
from src.exceptions import (
    ContactAlreadyExistError,
    ContactNameNotFoundError,
    ContactNotFoundError,
    InvalidIdError,
    InvalidNumberDataError,
)

app: FastAPI = FastAPI(
    title="Contact Manager API",
    description="Backend modular con integración a Supabase para la gestión de contactos relacionales.",
    version="1.0.0"
)


@app.exception_handler(ContactNotFoundError)
@app.exception_handler(ContactNameNotFoundError)
def contact_not_found_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles exceptions related to missing contact resources within the system.

    Args:
        request (Request): The incoming HTTP request context.
        exc (Exception): The raised domain exception instance.

    Returns:
        JSONResponse: A structured 404 Not Found JSON response payload.
    """
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={"detail": str(exc)}
    )


@app.exception_handler(ContactAlreadyExistError)
@app.exception_handler(InvalidNumberDataError)
@app.exception_handler(InvalidIdError)
def contact_conflict_and_validation_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handles exceptions related to data duplication, formatting validation, or structural domain integrity.

    Args:
        request (Request): The incoming HTTP request context.
        exc (Exception): The raised validation or constraint exception instance.

    Returns:
        JSONResponse: A structured 400 Bad Request JSON response payload.
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": str(exc)}
    )


app.include_router(contacts_router, prefix="/api")


@app.get("/", tags=["Root"])
def read_root() -> dict:
    """Provides a basic health check and welcome entry point message for the service root URL.

    Returns:
        dict: A simple operational health dictionary payload status.
    """
    return {
        "status": "healthy",
        "message": "Welcome to the Contact Manager API. Go to /docs for interactive documentation."
    }


def start_server() -> None:
    """Initializes and runs the ASGI application server infrastructure utilizing Uvicorn configurations."""
    uvicorn.run("src.api.main:app", host="127.0.0.1", port=8000, reload=True)


if __name__ == "__main__":
    start_server()