from pydantic import BaseModel


class InventoryBalanceSummary(BaseModel):
    id: int
    item_id: int
    item_name: str
    sku: str
    warehouse_name: str
    on_hand_quantity: float
    reserved_quantity: float
    available_quantity: float
    unit_of_measure: str
    storage_location: str | None

