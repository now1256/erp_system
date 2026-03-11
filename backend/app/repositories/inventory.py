from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.inventory import InventoryBalance
from app.models.item import Item


class InventoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_balances(self, query: str | None = None, low_stock_only: bool = False) -> list[InventoryBalance]:
        stmt = select(InventoryBalance).join(Item, Item.id == InventoryBalance.item_id)
        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(or_(Item.name.ilike(pattern), Item.sku.ilike(pattern), InventoryBalance.warehouse_name.ilike(pattern)))
        if low_stock_only:
            stmt = stmt.where(InventoryBalance.on_hand_quantity <= Item.reorder_threshold)
        stmt = stmt.order_by(InventoryBalance.warehouse_name, InventoryBalance.id)
        return list(self.db.scalars(stmt).all())

    def get_balance(self, item_id: int, warehouse_name: str) -> InventoryBalance | None:
        stmt = select(InventoryBalance).where(
            InventoryBalance.item_id == item_id,
            InventoryBalance.warehouse_name == warehouse_name,
        )
        return self.db.scalar(stmt)

    def save(self, balance: InventoryBalance) -> InventoryBalance:
        self.db.add(balance)
        self.db.flush()
        return balance
