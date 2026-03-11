from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models.partner import Partner


class PartnerRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def list_partners(self, query: str | None = None, partner_type: str | None = None) -> list[Partner]:
        stmt = select(Partner)
        if query:
            pattern = f"%{query}%"
            stmt = stmt.where(or_(Partner.name.ilike(pattern), Partner.contact_name.ilike(pattern), Partner.phone.ilike(pattern)))
        if partner_type:
            stmt = stmt.where(Partner.partner_type == partner_type)
        stmt = stmt.order_by(Partner.partner_type, Partner.name)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, partner_id: int) -> Partner | None:
        stmt = select(Partner).where(Partner.id == partner_id)
        return self.db.scalar(stmt)

    def save(self, partner: Partner) -> Partner:
        self.db.add(partner)
        self.db.flush()
        return partner

    def delete(self, partner: Partner) -> None:
        self.db.delete(partner)
