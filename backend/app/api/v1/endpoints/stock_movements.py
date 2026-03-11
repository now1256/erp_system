from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.stock_movement import StockMovementCreate, StockMovementSummary
from app.services.stock_movements import StockMovementService

router = APIRouter()


@router.get("", response_model=list[StockMovementSummary])
def list_stock_movements(
    db: Session = Depends(get_db),
    query: str | None = Query(default=None, alias="q"),
    movement_type: str | None = Query(default=None),
) -> list[StockMovementSummary]:
    return StockMovementService(db).list_movements(query=query, movement_type=movement_type)


@router.post("", response_model=StockMovementSummary, status_code=status.HTTP_201_CREATED)
def create_stock_movement(
    payload: StockMovementCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> StockMovementSummary:
    return StockMovementService(db).create_movement(payload)
