from app.endpoints.auth import registr_router
from app.endpoints.product import product_router
from app.endpoints.categories import categories_router
from app.endpoints.wallet import wallet_router

list_of_routes = [
    registr_router,
    product_router,
    categories_router,
    wallet_router,
]

__all__ = [
    "list_of_routes",
]
