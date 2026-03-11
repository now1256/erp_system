from pydantic import BaseModel, Field, field_validator

from app.models.enums import MovementType


class StockMovementCreate(BaseModel):
    item_id: int
    movement_type: MovementType
    quantity: float = Field(gt=0)
    warehouse_name: str = Field(min_length=1, max_length=80)
    partner_id: int | None = None
    reference: str | None = Field(default=None, max_length=80)
    reason: str | None = Field(default=None, max_length=120)
    memo: str | None = None

    @field_validator("warehouse_name", "reference", "reason", "memo", mode="before")
    @classmethod
    def strip_text(cls, value: str | None) -> str | None:
        if value is None:
            return None
        stripped = value.strip()
        return stripped or None


class StockMovementSummary(BaseModel):
    id: int
    item_name: str
    sku: str
    movement_type: str
    quantity: float
    warehouse_name: str
    reference: str | None
    reason: str | None
    moved_at: str
    partner_name: str | None
