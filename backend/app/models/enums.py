import enum


class ItemCategory(str, enum.Enum):
    pesticide = "pesticide"
    fertilizer = "fertilizer"
    seed = "seed"
    material = "material"


class ItemStatus(str, enum.Enum):
    active = "active"
    inactive = "inactive"


class MovementType(str, enum.Enum):
    inbound = "inbound"
    outbound = "outbound"
    adjustment = "adjustment"
