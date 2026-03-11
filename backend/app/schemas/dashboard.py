from pydantic import BaseModel


class CategoryBreakdown(BaseModel):
    category: str
    count: int


class RecentMovement(BaseModel):
    id: int
    item_name: str
    movement_type: str
    quantity: float
    warehouse_name: str
    moved_at: str


class InventorySnapshot(BaseModel):
    sku: str
    name: str
    category: str
    storage_location: str
    on_hand_quantity: float
    unit_of_measure: str


class DashboardOverview(BaseModel):
    total_items: int
    total_stock_on_hand: float
    low_stock_count: int
    category_breakdown: list[CategoryBreakdown]
    recent_movements: list[RecentMovement]
    inventory_snapshot: list[InventorySnapshot]
