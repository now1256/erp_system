from decimal import Decimal

from app.models.inventory import InventoryBalance
from app.repositories.inventory import InventoryRepository


class InventoryBalanceService:
    def __init__(self, repository: InventoryRepository) -> None:
        self.repository = repository

    def get_or_create_balance(self, item_id: int, warehouse_name: str) -> InventoryBalance:
        balance = self.repository.get_balance(item_id=item_id, warehouse_name=warehouse_name)
        if balance:
            return balance

        balance = InventoryBalance(
            item_id=item_id,
            warehouse_name=warehouse_name,
            on_hand_quantity=Decimal("0"),
            reserved_quantity=Decimal("0"),
        )
        return self.repository.save(balance)
