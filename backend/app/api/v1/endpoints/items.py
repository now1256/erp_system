from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.item import ItemCreate, ItemSummary, ItemUpdate
from app.services.items import ItemService

router = APIRouter()


@router.get("", response_model=list[ItemSummary])
def list_items(
    db: Session = Depends(get_db),
    query: str | None = Query(default=None, alias="q"),
    category: str | None = Query(default=None),
) -> list[ItemSummary]:
    return ItemService(db).list_items(query=query, category=category)


@router.post("", response_model=ItemSummary, status_code=status.HTTP_201_CREATED)
def create_item(
    payload: ItemCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> ItemSummary:
    return ItemService(db).create_item(payload)


@router.put("/{item_id}", response_model=ItemSummary)
def update_item(
    item_id: int,
    payload: ItemUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> ItemSummary:
    return ItemService(db).update_item(item_id, payload)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(
    item_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Response:
    ItemService(db).delete_item(item_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
