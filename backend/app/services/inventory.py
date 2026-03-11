from sqlalchemy.orm import Session

from app.repositories.inventory import InventoryRepository
from app.schemas.inventory import InventoryBalanceSummary


class InventoryService:
    def __init__(self, db: Session) -> None:
        self.repository = InventoryRepository(db)

    def list_balances(self, query: str | None = None, low_stock_only: bool = False) -> list[InventoryBalanceSummary]:
        balances = self.repository.list_balances(query=query, low_stock_only=low_stock_only)
        return [
            InventoryBalanceSummary(
                id=balance.id,
                item_id=balance.item_id,
                item_name=balance.item.name,
                sku=balance.item.sku,
                warehouse_name=balance.warehouse_name,
                on_hand_quantity=float(balance.on_hand_quantity),
                reserved_quantity=float(balance.reserved_quantity),
                available_quantity=float(balance.on_hand_quantity - balance.reserved_quantity),
                unit_of_measure=balance.item.unit_of_measure,
                storage_location=balance.item.storage_location,
            )
            for balance in balances
        ]
