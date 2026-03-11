from datetime import date

from sqlalchemy import Boolean, Date, Enum, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.enums import ItemCategory, ItemStatus


class Item(Base, TimestampMixin):
    __tablename__ = "items"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    category: Mapped[ItemCategory] = mapped_column(Enum(ItemCategory))
    status: Mapped[ItemStatus] = mapped_column(Enum(ItemStatus), default=ItemStatus.active)
    manufacturer: Mapped[str | None] = mapped_column(String(120))
    unit_of_measure: Mapped[str] = mapped_column(String(30), default="ea")
    package_size: Mapped[str | None] = mapped_column(String(80))
    storage_location: Mapped[str | None] = mapped_column(String(120))
    lot_code: Mapped[str | None] = mapped_column(String(80))
    expiration_date: Mapped[date | None] = mapped_column(Date)
    reorder_threshold: Mapped[float] = mapped_column(Numeric(12, 2), default=0)
    notes: Mapped[str | None] = mapped_column(Text)

    # Pesticide-specific
    epa_registration_number: Mapped[str | None] = mapped_column(String(80))
    active_ingredient: Mapped[str | None] = mapped_column(String(200))
    signal_word: Mapped[str | None] = mapped_column(String(40))
    restricted_use: Mapped[bool] = mapped_column(Boolean, default=False)
    reentry_interval_hours: Mapped[int | None]
    sds_url: Mapped[str | None] = mapped_column(String(255))

    # Fertilizer-specific
    npk_grade: Mapped[str | None] = mapped_column(String(40))
    guaranteed_analysis: Mapped[str | None] = mapped_column(Text)
    slow_release: Mapped[bool] = mapped_column(Boolean, default=False)
    coverage_area_sq_m: Mapped[float | None] = mapped_column(Numeric(12, 2))

    inventory_balances = relationship("InventoryBalance", back_populates="item", cascade="all, delete-orphan")
    stock_movements = relationship("StockMovement", back_populates="item", cascade="all, delete-orphan")
