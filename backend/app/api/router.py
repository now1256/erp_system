from fastapi import APIRouter

from app.api.v1.endpoints import auth, dashboard, health, inventory, items, partners, stock_movements

api_router = APIRouter()
api_router.include_router(health.router, tags=["health"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(stock_movements.router, prefix="/stock-movements", tags=["stock-movements"])
api_router.include_router(partners.router, prefix="/partners", tags=["partners"])
