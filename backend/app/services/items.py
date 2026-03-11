from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.models.enums import ItemCategory
from app.models.item import Item
from app.repositories.items import ItemRepository
from app.schemas.item import ItemCreate, ItemSummary, ItemUpdate


class ItemService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = ItemRepository(db)

    def list_items(self, query: str | None = None, category: str | None = None) -> list[ItemSummary]:
        items = self.repository.list_items(query=query, category=category)
        return [
            ItemSummary(
                id=item.id,
                sku=item.sku,
                name=item.name,
                category=item.category.value,
                manufacturer=item.manufacturer,
                unit_of_measure=item.unit_of_measure,
                package_size=item.package_size,
                storage_location=item.storage_location,
                lot_code=item.lot_code,
                expiration_date=item.expiration_date,
                reorder_threshold=float(item.reorder_threshold),
                epa_registration_number=item.epa_registration_number,
                active_ingredient=item.active_ingredient,
                signal_word=item.signal_word,
                npk_grade=item.npk_grade,
                guaranteed_analysis=item.guaranteed_analysis,
            )
            for item in items
        ]

    def create_item(self, payload: ItemCreate) -> ItemSummary:
        if self.repository.get_by_sku(payload.sku):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 품목코드입니다.")

        item = Item()
        self._assign_item(item, payload)
        self.repository.save(item)
        self.db.commit()
        self.db.refresh(item)
        return self._to_summary(item)

    def update_item(self, item_id: int, payload: ItemUpdate) -> ItemSummary:
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="품목을 찾을 수 없습니다.")

        existing = self.repository.get_by_sku(payload.sku)
        if existing and existing.id != item_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="이미 존재하는 품목코드입니다.")

        self._assign_item(item, payload)
        self.db.commit()
        self.db.refresh(item)
        return self._to_summary(item)

    def delete_item(self, item_id: int) -> None:
        item = self.repository.get_by_id(item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="품목을 찾을 수 없습니다.")
        self.repository.delete(item)
        self.db.commit()

    def _assign_item(self, item: Item, payload: ItemCreate | ItemUpdate) -> None:
        item.sku = payload.sku.strip()
        item.name = payload.name.strip()
        item.category = ItemCategory(payload.category)
        item.manufacturer = payload.manufacturer
        item.unit_of_measure = payload.unit_of_measure
        item.package_size = payload.package_size
        item.storage_location = payload.storage_location
        item.lot_code = payload.lot_code
        item.expiration_date = payload.expiration_date
        item.reorder_threshold = payload.reorder_threshold
        item.notes = payload.notes
        item.epa_registration_number = payload.epa_registration_number
        item.active_ingredient = payload.active_ingredient
        item.signal_word = payload.signal_word
        item.npk_grade = payload.npk_grade
        item.guaranteed_analysis = payload.guaranteed_analysis

    def _to_summary(self, item: Item) -> ItemSummary:
        return ItemSummary(
            id=item.id,
            sku=item.sku,
            name=item.name,
            category=item.category.value,
            manufacturer=item.manufacturer,
            unit_of_measure=item.unit_of_measure,
            package_size=item.package_size,
            storage_location=item.storage_location,
            lot_code=item.lot_code,
            expiration_date=item.expiration_date,
            reorder_threshold=float(item.reorder_threshold),
            epa_registration_number=item.epa_registration_number,
            active_ingredient=item.active_ingredient,
            signal_word=item.signal_word,
            npk_grade=item.npk_grade,
            guaranteed_analysis=item.guaranteed_analysis,
        )
