from sqlalchemy import ForeignKey, Numeric, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class InventoryBalance(Base, TimestampMixin):
    __tablename__ = "inventory_balances"
    __table_args__ = (UniqueConstraint("item_id", "warehouse_name", name="uq_inventory_item_warehouse"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), index=True)
    warehouse_name: Mapped[str] = mapped_column(String(80), default="Main Yard")
    on_hand_quantity: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    reserved_quantity: Mapped[float] = mapped_column(Numeric(12, 2), default=0)

    item = relationship("Item", back_populates="inventory_balances")
