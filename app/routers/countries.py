from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Country
from app.schemas import CountryOut

router = APIRouter(prefix="/api/countries", tags=["countries"])


@router.get("", response_model=list[CountryOut])
def list_countries(db: Session = Depends(get_db)):
    countries = db.scalars(select(Country).order_by(Country.name)).all()
    return [CountryOut(iso_code=c.iso_code, name=c.name) for c in countries]
