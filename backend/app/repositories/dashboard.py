from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import ItemCategory, MovementType
from app.models.inventory import InventoryBalance
from app.models.item import Item
from app.models.stock_movement import StockMovement


class DashboardRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def total_items(self) -> int:
        return self.db.scalar(select(func.count(Item.id))) or 0

    def total_stock_on_hand(self) -> float:
        value = self.db.scalar(select(func.coalesce(func.sum(InventoryBalance.on_hand_quantity), 0)))
        return float(value or 0)

    def low_stock_count(self) -> int:
        stmt = (
            select(func.count(func.distinct(Item.id)))
            .join(InventoryBalance, InventoryBalance.item_id == Item.id)
            .where(InventoryBalance.on_hand_quantity <= Item.reorder_threshold)
        )
        return self.db.scalar(stmt) or 0
    def category_breakdown(self) -> list[dict[str, str | int]]:
        stmt = select(Item.category, func.count(Item.id)).group_by(Item.category).order_by(Item.category)
        return [{"category": category.value, "count": count} for category, count in self.db.execute(stmt).all()]

    def recent_movements(self) -> list[dict[str, str | float]]:
        stmt = (
            select(
                StockMovement.id,
                Item.name,
                StockMovement.movement_type,
                StockMovement.quantity,
                StockMovement.warehouse_name,
                StockMovement.moved_at,
            )
            .join(Item, Item.id == StockMovement.item_id)
            .order_by(StockMovement.moved_at.desc())
            .limit(5)
        )
        rows = self.db.execute(stmt).all()
        return [
            {
                "id": movement_id,
                "item_name": item_name,
                "movement_type": movement_type.value,
                "quantity": float(quantity),
                "warehouse_name": warehouse_name,
                "moved_at": moved_at.isoformat(),
            }
            for movement_id, item_name, movement_type, quantity, warehouse_name, moved_at in rows
        ]

    def inventory_snapshot(self) -> list[dict[str, str | float]]:
        stmt = (
            select(
                Item.sku,
                Item.name,
                Item.category,
                Item.storage_location,
                InventoryBalance.on_hand_quantity,
                Item.unit_of_measure,
            )
            .join(InventoryBalance, InventoryBalance.item_id == Item.id)
            .order_by(Item.category, Item.name)
        )
        rows = self.db.execute(stmt).all()
        return [
            {
                "sku": sku,
                "name": name,
                "category": category.value,
                "storage_location": storage_location or "-",
                "on_hand_quantity": float(on_hand_quantity),
                "unit_of_measure": unit_of_measure,
            }
            for sku, name, category, storage_location, on_hand_quantity, unit_of_measure in rows
        ]
