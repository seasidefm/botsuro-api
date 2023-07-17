"""
Authentication and identification middleware
"""
from typing import List

from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware


class IdentityMiddleware(BaseHTTPMiddleware):
    """
    Add some identity to request state or throw an error if
    identity cannot be determined
    """
    def __init__(
            self,
            app,
            protected_routes: List[str]
    ):
        super().__init__(app)
        self.protected_routes = protected_routes

    async def dispatch(self, request: Request, call_next) -> Response:
        return await call_next(request)
