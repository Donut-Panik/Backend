from app.endpoints.auth import registr_router
from app.endpoints.product import product_router

list_of_routes = [
    registr_router,
    product_router,
]

__all__ = [
    "list_of_routes",
]
