from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.dashboard import DashboardOverview
from app.services.dashboard import DashboardService

router = APIRouter()


@router.get("/overview", response_model=DashboardOverview)
def get_overview(db: Session = Depends(get_db)) -> DashboardOverview:
    return DashboardService(db).get_overview()
