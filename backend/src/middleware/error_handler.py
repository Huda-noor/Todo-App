from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from typing import Callable, Awaitable
import traceback
import logging


class ErrorHandlerMiddleware:
    """
    Middleware to handle errors globally.
    """

    def __init__(self, app):
        self.app = app
        self.logger = logging.getLogger(__name__)

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        async def send_with_error_handling(message):
            try:
                await send(message)
            except Exception as e:
                self.logger.error(f"Error sending response: {str(e)}")

        request = Request(scope)
        try:
            # Call the app and handle the response
            await self.app(scope, receive, send_with_error_handling)
        except HTTPException as e:
            # Log the error
            self.logger.error(f"HTTPException: {e.status_code} - {e.detail}")

            # Create and send error response
            response = JSONResponse(
                status_code=e.status_code,
                content={
                    "error": e.detail,
                    "type": "http_exception"
                }
            )
            await response(scope, receive, send_with_error_handling)
        except Exception as e:
            # Log the error with traceback
            self.logger.error(f"Unhandled exception: {str(e)}")
            self.logger.error(traceback.format_exc())

            # Create and send generic error response
            response = JSONResponse(
                status_code=500,
                content={
                    "error": "An unexpected error occurred",
                    "type": "internal_server_error"
                }
            )
            await response(scope, receive, send_with_error_handling)


def handle_validation_error(exc):
    """
    Handle validation errors specifically.
    """
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation error",
            "details": exc.errors(),
            "type": "validation_error"
        }
    )


def handle_authentication_error():
    """
    Handle authentication errors specifically.
    """
    return JSONResponse(
        status_code=401,
        content={
            "error": "Authentication required",
            "type": "authentication_error"
        }
    )


def handle_authorization_error():
    """
    Handle authorization errors specifically.
    """
    return JSONResponse(
        status_code=403,
        content={
            "error": "Access forbidden",
            "type": "authorization_error"
        }
    )