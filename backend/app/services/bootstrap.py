from datetime import date, timedelta
from decimal import Decimal

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ItemCategory, ItemStatus, MovementType
from app.models.inventory import InventoryBalance
from app.models.item import Item
from app.models.partner import Partner
from app.models.stock_movement import StockMovement
from app.models.user import User


def seed_demo_data(db: Session) -> None:
    _seed_users(db)
    existing_partners = {partner.name: partner for partner in db.scalars(select(Partner)).all()}
    existing_items = {item.sku: item for item in db.scalars(select(Item)).all()}

    supplier = existing_partners.get("그린스케이프 자재상사") or existing_partners.get("GreenScape Supply") or Partner(
        name="그린스케이프 자재상사",
        partner_type="supplier",
    )
    supplier.name = "그린스케이프 자재상사"
    supplier.partner_type = "supplier"
    supplier.contact_name = "김서준"
    supplier.phone = "010-5555-0101"
    supplier.address = "경기 자재물류센터"

    customer = existing_partners.get("리버파크 아파트 현장") or existing_partners.get("River Park Apartment") or Partner(
        name="리버파크 아파트 현장",
        partner_type="customer",
    )
    customer.name = "리버파크 아파트 현장"
    customer.partner_type = "customer"
    customer.contact_name = "이지은"
    customer.phone = "010-8888-2020"
    customer.address = "서울 현장사무소"

    pesticide = existing_items.get("PST-2401") or Item(
        sku="PST-2401",
    )
    pesticide.name = "광엽잡초 방제제 1L"
    pesticide.category = ItemCategory.pesticide
    pesticide.status = ItemStatus.active
    pesticide.manufacturer = "한농자재"
    pesticide.unit_of_measure = "병"
    pesticide.package_size = "1L"
    pesticide.storage_location = "위험물 선반 A1"
    pesticide.lot_code = "LOT-HA-2402"
    pesticide.expiration_date = date.today() + timedelta(days=420)
    pesticide.reorder_threshold = Decimal("8.00")
    pesticide.epa_registration_number = "KR-EPA-DEMO-1024"
    pesticide.active_ingredient = "2,4-D amine"
    pesticide.signal_word = "CAUTION"
    pesticide.restricted_use = False
    pesticide.reentry_interval_hours = 12
    pesticide.sds_url = "https://example.com/sds/herbicide-1l"
    pesticide.notes = "봄철 잔디 및 광엽잡초 방제용"

    fertilizer = existing_items.get("FRT-161616") or Item(
        sku="FRT-161616",
    )
    fertilizer.name = "잔디용 복합비료 20kg"
    fertilizer.category = ItemCategory.fertilizer
    fertilizer.status = ItemStatus.active
    fertilizer.manufacturer = "블루필드 뉴트리언츠"
    fertilizer.unit_of_measure = "포"
    fertilizer.package_size = "20kg"
    fertilizer.storage_location = "건식창고 B2"
    fertilizer.lot_code = "LOT-BF-0310"
    fertilizer.expiration_date = date.today() + timedelta(days=365)
    fertilizer.reorder_threshold = Decimal("20.00")
    fertilizer.npk_grade = "16-16-16"
    fertilizer.guaranteed_analysis = "질소 16%, 인산 16%, 칼리 16%"
    fertilizer.slow_release = True
    fertilizer.coverage_area_sq_m = Decimal("650.00")
    fertilizer.notes = "조경 유지관리용 일반 복합비료"

    material = existing_items.get("MAT-MULCH-01") or Item(
        sku="MAT-MULCH-01",
    )
    material.name = "소나무 수피 멀칭재"
    material.category = ItemCategory.material
    material.status = ItemStatus.active
    material.manufacturer = "포레스트어스"
    material.unit_of_measure = "포"
    material.package_size = "40L"
    material.storage_location = "외부야적장 C3"
    material.reorder_threshold = Decimal("15.00")

    db.add_all([supplier, customer, pesticide, fertilizer, material])
    db.flush()

    existing_balances = {
        (balance.item_id, balance.warehouse_name): balance
        for balance in db.scalars(select(InventoryBalance)).all()
    }
    for item, quantity in [
        (pesticide, Decimal("14.00")),
        (fertilizer, Decimal("42.00")),
        (material, Decimal("11.00")),
    ]:
        balance = existing_balances.get((item.id, "본사 창고")) or InventoryBalance(
            item_id=item.id,
            warehouse_name="본사 창고",
        )
        balance.on_hand_quantity = quantity
        balance.reserved_quantity = Decimal("0.00")
        db.add(balance)

    existing_references = {
        reference
        for reference in db.scalars(select(StockMovement.reference).where(StockMovement.reference.is_not(None))).all()
    }
    movement_specs = [
        {
            "item_id": pesticide.id,
            "partner_id": supplier.id,
            "movement_type": MovementType.inbound,
            "warehouse_name": "본사 창고",
            "quantity": Decimal("20.00"),
            "reference": "PO-2026-001",
            "reason": "봄철 제초제 입고",
        },
        {
            "item_id": pesticide.id,
            "partner_id": customer.id,
            "movement_type": MovementType.outbound,
            "warehouse_name": "본사 창고",
            "quantity": Decimal("6.00"),
            "reference": "WO-2026-003",
            "reason": "아파트 잔디 병해충 방제",
        },
        {
            "item_id": fertilizer.id,
            "partner_id": supplier.id,
            "movement_type": MovementType.inbound,
            "warehouse_name": "본사 창고",
            "quantity": Decimal("50.00"),
            "reference": "PO-2026-002",
            "reason": "정기 비료 입고",
        },
        {
            "item_id": material.id,
            "partner_id": None,
            "movement_type": MovementType.adjustment,
            "warehouse_name": "본사 창고",
            "quantity": Decimal("-4.00"),
            "reference": "ADJ-2026-001",
            "reason": "실사 차이 조정",
        },
    ]
    for spec in movement_specs:
        if spec["reference"] in existing_references:
            continue
        db.add(StockMovement(**spec))

    _normalize_demo_movements(db, supplier_id=supplier.id, customer_id=customer.id)
    _migrate_legacy_demo_data(db, supplier_id=supplier.id, customer_id=customer.id)
    db.commit()


def _seed_users(db: Session) -> None:
    admin = db.scalar(select(User).where(User.username == "admin"))
    if not admin:
        admin = User(username="admin", password="admin1234", full_name="시스템 관리자", role="admin")
        db.add(admin)

    manager = db.scalar(select(User).where(User.username == "manager"))
    if not manager:
        manager = User(username="manager", password="manager1234", full_name="재고 담당자", role="manager")
        db.add(manager)
    db.flush()


def _migrate_legacy_demo_data(db: Session, supplier_id: int, customer_id: int) -> None:
    legacy_partner_names = {
        "GreenScape Supply": supplier_id,
        "River Park Apartment": customer_id,
    }
    partners_by_name = {partner.name: partner for partner in db.scalars(select(Partner)).all()}
    for legacy_name, target_id in legacy_partner_names.items():
        legacy_partner = partners_by_name.get(legacy_name)
        if not legacy_partner or legacy_partner.id == target_id:
            continue

        for movement in db.scalars(select(StockMovement).where(StockMovement.partner_id == legacy_partner.id)).all():
            movement.partner_id = target_id
        db.delete(legacy_partner)

    balances = db.scalars(select(InventoryBalance)).all()
    canonical_balance_map: dict[int, InventoryBalance] = {}
    for balance in balances:
        if balance.warehouse_name == "본사 창고":
            canonical_balance_map[balance.item_id] = balance

    for balance in balances:
        if balance.warehouse_name != "Main Yard":
            continue

        canonical = canonical_balance_map.get(balance.item_id)
        if canonical:
            db.delete(balance)
        else:
            balance.warehouse_name = "본사 창고"

    for movement in db.scalars(select(StockMovement)).all():
        if movement.warehouse_name == "Main Yard":
            movement.warehouse_name = "본사 창고"


def _normalize_demo_movements(db: Session, supplier_id: int, customer_id: int) -> None:
    normalized_specs = {
        "PO-2026-001": {"partner_id": supplier_id, "warehouse_name": "본사 창고", "reason": "봄철 제초제 입고"},
        "WO-2026-003": {"partner_id": customer_id, "warehouse_name": "본사 창고", "reason": "아파트 잔디 병해충 방제"},
        "PO-2026-002": {"partner_id": supplier_id, "warehouse_name": "본사 창고", "reason": "정기 비료 입고"},
        "ADJ-2026-001": {"partner_id": None, "warehouse_name": "본사 창고", "reason": "실사 차이 조정"},
    }
    for movement in db.scalars(select(StockMovement)).all():
        if movement.reference not in normalized_specs:
            continue
        spec = normalized_specs[movement.reference]
        movement.partner_id = spec["partner_id"]
        movement.warehouse_name = spec["warehouse_name"]
        movement.reason = spec["reason"]
