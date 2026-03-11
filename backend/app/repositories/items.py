from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.item import Item
from app.models.enums import ItemCategory


class ItemRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_items(self, query: str | None = None, category: str | None = None) -> list[Item]:
        stmt = select(Item)
        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(or_(Item.name.ilike(pattern), Item.sku.ilike(pattern), Item.manufacturer.ilike(pattern)))
        if category:
            stmt = stmt.where(Item.category == ItemCategory(category))
        stmt = stmt.order_by(Item.category, Item.name)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, item_id: int) -> Item | None:
        stmt = select(Item).where(Item.id == item_id)
        return self.db.scalar(stmt)

    def get_by_sku(self, sku: str) -> Item | None:
        stmt = select(Item).where(Item.sku == sku)
        return self.db.scalar(stmt)

    def save(self, item: Item) -> Item:
        self.db.add(item)
        self.db.flush()
        return item

    def delete(self, item: Item) -> None:
        self.db.delete(item)
