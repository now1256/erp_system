from sqlalchemy.orm import Session

from app.repositories.dashboard import DashboardRepository
from app.schemas.dashboard import DashboardOverview


class DashboardService:
    def __init__(self, db: Session) -> None:
        self.repository = DashboardRepository(db)

    def get_overview(self) -> DashboardOverview:
        return DashboardOverview(
            total_items=self.repository.total_items(),
            total_stock_on_hand=self.repository.total_stock_on_hand(),
            low_stock_count=self.repository.low_stock_count(),
            category_breakdown=self.repository.category_breakdown(),
            recent_movements=self.repository.recent_movements(),
            inventory_snapshot=self.repository.inventory_snapshot(),
        )
