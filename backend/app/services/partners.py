from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.partner import Partner
from app.repositories.partners import PartnerRepository
from app.schemas.partner import PartnerCreate, PartnerSummary, PartnerUpdate


class PartnerService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = PartnerRepository(db)

    def list_partners(self, query: str | None = None, partner_type: str | None = None) -> list[PartnerSummary]:
        return [PartnerSummary.model_validate(partner) for partner in self.repository.list_partners(query=query, partner_type=partner_type)]

    def create_partner(self, payload: PartnerCreate) -> PartnerSummary:
        partner = Partner()
        self._assign_partner(partner, payload)
        self.repository.save(partner)
        self.db.commit()
        self.db.refresh(partner)
        return PartnerSummary.model_validate(partner)

    def update_partner(self, partner_id: int, payload: PartnerUpdate) -> PartnerSummary:
        partner = self.repository.get_by_id(partner_id)
        if not partner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="거래처를 찾을 수 없습니다.")
        self._assign_partner(partner, payload)
        self.db.commit()
        self.db.refresh(partner)
        return PartnerSummary.model_validate(partner)

    def delete_partner(self, partner_id: int) -> None:
        partner = self.repository.get_by_id(partner_id)
        if not partner:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="거래처를 찾을 수 없습니다.")
        self.repository.delete(partner)
        self.db.commit()

    def _assign_partner(self, partner: Partner, payload: PartnerCreate | PartnerUpdate) -> None:
        partner.name = payload.name.strip()
        partner.partner_type = payload.partner_type
        partner.contact_name = payload.contact_name
        partner.phone = payload.phone
        partner.address = payload.address
