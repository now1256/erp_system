from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.stock_movement import StockMovement
from app.models.item import Item


class StockMovementRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_movements(self, query: str | None = None, movement_type: str | None = None) -> list[StockMovement]:
        stmt = select(StockMovement).join(Item, Item.id == StockMovement.item_id)
        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(or_(Item.name.ilike(pattern), Item.sku.ilike(pattern), StockMovement.reference.ilike(pattern)))
        if movement_type:
            stmt = stmt.where(StockMovement.movement_type == movement_type)
        stmt = stmt.order_by(StockMovement.moved_at.desc(), StockMovement.id.desc())
        return list(self.db.scalars(stmt).all())

    def save(self, movement: StockMovement) -> StockMovement:
        self.db.add(movement)
        self.db.flush()
        return movement
