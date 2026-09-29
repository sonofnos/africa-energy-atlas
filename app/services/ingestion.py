"""Turns the raw OWID energy-data CSV into rows for our schema.

Split deliberately into pure parsing (testable with a small fixture, no
network or database) and a separate upsert step (testable against a real
Postgres, no network) -- the two things that actually need verifying are
"did we parse this correctly" and "is a re-run of the same data safe",
and neither needs the other to be tested.
"""

import csv
import hashlib
import io
from dataclasses import dataclass
from datetime import datetime, timezone

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.africa import AFRICAN_COUNTRIES
from app.indicators import INDICATORS
from app.models import Country, EnergyFact, IngestionRun


@dataclass(frozen=True)
class FactRow:
    country_iso: str
    year: int
    indicator: str
    value: float


def checksum(raw_csv: str) -> str:
    return hashlib.sha256(raw_csv.encode("utf-8")).hexdigest()


def parse_african_energy_facts(raw_csv: str) -> list[FactRow]:
    """Filters the OWID CSV to African Union member states and the
    indicators this platform tracks, dropping rows with no ISO code
    (aggregates like "Africa (BP)" or "World") or a blank value."""
    reader = csv.DictReader(io.StringIO(raw_csv))
    rows: list[FactRow] = []

    for record in reader:
        iso = record.get("iso_code", "")
        if iso not in AFRICAN_COUNTRIES:
            continue

        year_raw = record.get("year")
        if not year_raw:
            continue
        year = int(year_raw)

        for indicator in INDICATORS:
            value_raw = record.get(indicator)
            if value_raw in (None, ""):
                continue
            rows.append(FactRow(country_iso=iso, year=year, indicator=indicator, value=float(value_raw)))

    return rows


def upsert_facts(db: Session, rows: list[FactRow], source: str) -> int:
    """Idempotent on (country_iso, year, indicator): re-ingesting the same
    source data updates values in place instead of duplicating rows."""
    for iso, name in AFRICAN_COUNTRIES.items():
        db.execute(
            insert(Country)
            .values(iso_code=iso, name=name)
            .on_conflict_do_nothing(index_elements=["iso_code"])
        )

    if not rows:
        db.commit()
        return 0

    for i in range(0, len(rows), 500):
        batch = rows[i : i + 500]
        values = [
            {
                "country_iso": r.country_iso,
                "year": r.year,
                "indicator": r.indicator,
                "value": r.value,
                "source": source,
            }
            for r in batch
        ]
        batch_stmt = insert(EnergyFact).values(values)
        batch_stmt = batch_stmt.on_conflict_do_update(
            index_elements=["country_iso", "year", "indicator"],
            set_={"value": batch_stmt.excluded.value, "source": batch_stmt.excluded.source},
        )
        db.execute(batch_stmt)

    db.commit()
    return len(rows)


def record_ingestion_run(
    db: Session, source_url: str, raw_csv: str, row_count: int, started_at: datetime
) -> IngestionRun:
    run = IngestionRun(
        source_url=source_url,
        checksum=checksum(raw_csv),
        row_count=row_count,
        started_at=started_at,
        completed_at=datetime.now(timezone.utc),
    )
    db.add(run)
    db.commit()
    db.refresh(run)
    return run
