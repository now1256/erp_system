from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Numeric, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.models.enums import MovementType


class StockMovement(Base):
    __tablename__ = "stock_movements"

    id: Mapped[int] = mapped_column(primary_key=True)
    item_id: Mapped[int] = mapped_column(ForeignKey("items.id", ondelete="CASCADE"), index=True)
    partner_id: Mapped[int | None] = mapped_column(ForeignKey("partners.id", ondelete="SET NULL"))
    movement_type: Mapped[MovementType] = mapped_column(Enum(MovementType))
    warehouse_name: Mapped[str] = mapped_column(String(80), default="Main Yard")
    quantity: Mapped[float] = mapped_column(Numeric(12, 2))
    reference: Mapped[str | None] = mapped_column(String(80))
    reason: Mapped[str | None] = mapped_column(String(120))
    memo: Mapped[str | None] = mapped_column(Text)
    moved_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    item = relationship("Item", back_populates="stock_movements")
    partner = relationship("Partner", back_populates="stock_movements")
