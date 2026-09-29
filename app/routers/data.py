from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.indicators import INDICATORS
from app.models import Country, EnergyFact
from app.schemas import ComparisonPointOut, CountryOut, DataPointOut, IndicatorOut, SeriesOut

router = APIRouter(prefix="/api", tags=["data"])


def _require_indicator(indicator: str) -> None:
    if indicator not in INDICATORS:
        raise HTTPException(status_code=404, detail=f"Unknown indicator '{indicator}'")


def _get_country(db: Session, iso_code: str) -> Country:
    country = db.get(Country, iso_code.upper())
    if country is None:
        raise HTTPException(status_code=404, detail=f"Unknown country '{iso_code}'")
    return country


@router.get("/data", response_model=SeriesOut)
def get_series(
    country: str = Query(...),
    indicator: str = Query(...),
    from_year: int | None = Query(default=None),
    to_year: int | None = Query(default=None),
    db: Session = Depends(get_db),
):
    _require_indicator(indicator)
    country_row = _get_country(db, country)

    stmt = select(EnergyFact).where(
        EnergyFact.country_iso == country_row.iso_code, EnergyFact.indicator == indicator
    )
    if from_year is not None:
        stmt = stmt.where(EnergyFact.year >= from_year)
    if to_year is not None:
        stmt = stmt.where(EnergyFact.year <= to_year)
    stmt = stmt.order_by(EnergyFact.year)

    facts = db.scalars(stmt).all()
    meta = INDICATORS[indicator]

    return SeriesOut(
        country=CountryOut(iso_code=country_row.iso_code, name=country_row.name),
        indicator=IndicatorOut(key=indicator, label=meta["label"], unit=meta["unit"]),
        points=[DataPointOut(year=f.year, value=f.value) for f in facts],
    )


@router.get("/compare", response_model=list[ComparisonPointOut])
def compare_countries(
    indicator: str = Query(...),
    year: int = Query(...),
    db: Session = Depends(get_db),
):
    _require_indicator(indicator)

    stmt = (
        select(EnergyFact, Country)
        .join(Country, Country.iso_code == EnergyFact.country_iso)
        .where(EnergyFact.indicator == indicator, EnergyFact.year == year)
        .order_by(EnergyFact.value.desc())
    )
    rows = db.execute(stmt).all()

    return [
        ComparisonPointOut(country=CountryOut(iso_code=c.iso_code, name=c.name), value=f.value)
        for f, c in rows
    ]
