from decimal import Decimal

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.enums import MovementType
from app.models.stock_movement import StockMovement
from app.repositories.inventory import InventoryRepository
from app.repositories.items import ItemRepository
from app.repositories.partners import PartnerRepository
from app.repositories.stock_movements import StockMovementRepository
from app.schemas.stock_movement import StockMovementCreate, StockMovementSummary
from app.services.inventory_balance import InventoryBalanceService


class StockMovementService:
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repository = StockMovementRepository(db)
        self.item_repository = ItemRepository(db)
        self.partner_repository = PartnerRepository(db)
        self.balance_service = InventoryBalanceService(InventoryRepository(db))

    def list_movements(self, query: str | None = None, movement_type: str | None = None) -> list[StockMovementSummary]:
        movements = self.repository.list_movements(query=query, movement_type=movement_type)
        return [self._to_summary(movement) for movement in movements]

    def create_movement(self, payload: StockMovementCreate) -> StockMovementSummary:
        item = self.item_repository.get_by_id(payload.item_id)
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="품목을 찾을 수 없습니다.")

        partner = None
        if payload.partner_id is not None:
            partner = self.partner_repository.get_by_id(payload.partner_id)
            if not partner:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="거래처를 찾을 수 없습니다.")

        balance = self.balance_service.get_or_create_balance(item_id=item.id, warehouse_name=payload.warehouse_name)
        quantity = Decimal(str(payload.quantity))
        current_on_hand = Decimal(str(balance.on_hand_quantity))

        if payload.movement_type == MovementType.inbound:
            new_on_hand = current_on_hand + quantity
            movement_quantity = quantity
        elif payload.movement_type == MovementType.outbound:
            if current_on_hand < quantity:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="출고 수량이 현재고보다 큽니다.")
            new_on_hand = current_on_hand - quantity
            movement_quantity = quantity
        else:
            new_on_hand = quantity
            movement_quantity = quantity - current_on_hand

        balance.on_hand_quantity = new_on_hand

        movement = StockMovement(
            item_id=item.id,
            partner_id=partner.id if partner else None,
            movement_type=payload.movement_type,
            warehouse_name=payload.warehouse_name,
            quantity=movement_quantity,
            reference=payload.reference,
            reason=payload.reason,
            memo=payload.memo,
        )
        self.repository.save(movement)
        self.db.commit()
        self.db.refresh(movement)
        return self._to_summary(movement)

    def _to_summary(self, movement: StockMovement) -> StockMovementSummary:
        return StockMovementSummary(
            id=movement.id,
            item_name=movement.item.name,
            sku=movement.item.sku,
            movement_type=movement.movement_type.value,
            quantity=float(movement.quantity),
            warehouse_name=movement.warehouse_name,
            reference=movement.reference,
            reason=movement.reason,
            moved_at=movement.moved_at.isoformat(),
            partner_name=movement.partner.name if movement.partner else None,
        )
