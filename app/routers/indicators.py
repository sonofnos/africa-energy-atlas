from fastapi import APIRouter

from app.indicators import INDICATORS
from app.schemas import IndicatorOut

router = APIRouter(prefix="/api/indicators", tags=["indicators"])


@router.get("", response_model=list[IndicatorOut])
def list_indicators():
    return [IndicatorOut(key=key, label=meta["label"], unit=meta["unit"]) for key, meta in INDICATORS.items()]
