from pydantic import BaseModel


class PartnerSummary(BaseModel):
    id: int
    name: str
    partner_type: str
    contact_name: str | None
    phone: str | None
    address: str | None

    model_config = {"from_attributes": True}


class PartnerCreate(BaseModel):
    name: str
    partner_type: str
    contact_name: str | None = None
    phone: str | None = None
    address: str | None = None


class PartnerUpdate(BaseModel):
    name: str
    partner_type: str
    contact_name: str | None = None
    phone: str | None = None
    address: str | None = None
