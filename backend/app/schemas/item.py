from datetime import date

from pydantic import BaseModel, Field


class ItemSummary(BaseModel):
    id: int
    sku: str
    name: str
    category: str
    manufacturer: str | None
    unit_of_measure: str
    package_size: str | None
    storage_location: str | None
    lot_code: str | None
    expiration_date: date | None
    reorder_threshold: float
    epa_registration_number: str | None
    active_ingredient: str | None
    signal_word: str | None
    npk_grade: str | None
    guaranteed_analysis: str | None

    model_config = {"from_attributes": True}


class ItemCreate(BaseModel):
    sku: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    category: str
    manufacturer: str | None = None
    unit_of_measure: str = "개"
    package_size: str | None = None
    storage_location: str | None = None
    lot_code: str | None = None
    expiration_date: date | None = None
    reorder_threshold: float = 0
    notes: str | None = None
    epa_registration_number: str | None = None
    active_ingredient: str | None = None
    signal_word: str | None = None
    npk_grade: str | None = None
    guaranteed_analysis: str | None = None


class ItemUpdate(BaseModel):
    sku: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=200)
    category: str
    manufacturer: str | None = None
    unit_of_measure: str = "개"
    package_size: str | None = None
    storage_location: str | None = None
    lot_code: str | None = None
    expiration_date: date | None = None
    reorder_threshold: float = 0
    notes: str | None = None
    epa_registration_number: str | None = None
    active_ingredient: str | None = None
    signal_word: str | None = None
    npk_grade: str | None = None
    guaranteed_analysis: str | None = None
