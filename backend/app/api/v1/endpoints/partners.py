from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import require_admin
from app.db.session import get_db
from app.models.user import User
from app.schemas.partner import PartnerCreate, PartnerSummary, PartnerUpdate
from app.services.partners import PartnerService

router = APIRouter()


@router.get("", response_model=list[PartnerSummary])
def list_partners(
    db: Session = Depends(get_db),
    query: str | None = Query(default=None, alias="q"),
    partner_type: str | None = Query(default=None),
) -> list[PartnerSummary]:
    return PartnerService(db).list_partners(query=query, partner_type=partner_type)


@router.post("", response_model=PartnerSummary, status_code=status.HTTP_201_CREATED)
def create_partner(
    payload: PartnerCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> PartnerSummary:
    return PartnerService(db).create_partner(payload)


@router.put("/{partner_id}", response_model=PartnerSummary)
def update_partner(
    partner_id: int,
    payload: PartnerUpdate,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> PartnerSummary:
    return PartnerService(db).update_partner(partner_id, payload)


@router.delete("/{partner_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_partner(
    partner_id: int,
    db: Session = Depends(get_db),
    _: User = Depends(require_admin),
) -> Response:
    PartnerService(db).delete_partner(partner_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
