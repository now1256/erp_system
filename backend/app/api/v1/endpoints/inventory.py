from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.inventory import InventoryBalanceSummary
from app.services.inventory import InventoryService

router = APIRouter()


@router.get("/balances", response_model=list[InventoryBalanceSummary])
def list_inventory_balances(
    db: Session = Depends(get_db),
    query: str | None = Query(default=None, alias="q"),
    low_stock_only: bool = Query(default=False),
) -> list[InventoryBalanceSummary]:
    return InventoryService(db).list_balances(query=query, low_stock_only=low_stock_only)
