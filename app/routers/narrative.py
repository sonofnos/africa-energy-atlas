from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.indicators import INDICATORS
from app.models import Country, EnergyFact
from app.schemas import CountryOut, IndicatorOut, NarrativeOut
from app.services.narrative import compute_trend_stats, render_narrative

router = APIRouter(prefix="/api", tags=["narrative"])


@router.get("/narrative", response_model=NarrativeOut)
def get_narrative(country: str = Query(...), indicator: str = Query(...), db: Session = Depends(get_db)):
    if indicator not in INDICATORS:
        raise HTTPException(status_code=404, detail=f"Unknown indicator '{indicator}'")

    country_row = db.get(Country, country.upper())
    if country_row is None:
        raise HTTPException(status_code=404, detail=f"Unknown country '{country}'")

    facts = db.scalars(
        select(EnergyFact)
        .where(EnergyFact.country_iso == country_row.iso_code, EnergyFact.indicator == indicator)
        .order_by(EnergyFact.year)
    ).all()

    stats = compute_trend_stats(country_row.name, indicator, [(f.year, f.value) for f in facts])
    if stats is None:
        raise HTTPException(status_code=404, detail="Not enough data points for a narrative")

    text = render_narrative(stats)
    meta = INDICATORS[indicator]

    return NarrativeOut(
        country=CountryOut(iso_code=country_row.iso_code, name=country_row.name),
        indicator=IndicatorOut(key=indicator, label=meta["label"], unit=meta["unit"]),
        text=text,
    )
