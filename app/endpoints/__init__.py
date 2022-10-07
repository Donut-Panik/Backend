from app.endpoints.auth import registr_router
from app.endpoints.product import product_router
from app.endpoints.categories import categories_router


list_of_routes = [
    registr_router,
    product_router,
    categories_router,
]

__all__ = [
    "list_of_routes",
]
