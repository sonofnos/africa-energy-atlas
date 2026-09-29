"""Downloads OWID's public energy-data CSV, filters it to African Union
member states and the indicators this platform tracks, and upserts the
result into Postgres. Idempotent -- safe to re-run on a schedule.

Usage: python -m scripts.ingest
"""

from datetime import datetime, timezone

import httpx

from app.config import settings
from app.database import SessionLocal
from app.services.ingestion import parse_african_energy_facts, record_ingestion_run, upsert_facts


def run() -> None:
    started_at = datetime.now(timezone.utc)
    print(f"Fetching {settings.owid_source_url} ...")

    response = httpx.get(settings.owid_source_url, timeout=60, follow_redirects=True)
    response.raise_for_status()
    raw_csv = response.text

    rows = parse_african_energy_facts(raw_csv)
    print(f"Parsed {len(rows)} African data points.")

    db = SessionLocal()
    try:
        upsert_facts(db, rows, source=settings.owid_source_url)
        ingestion_run = record_ingestion_run(db, settings.owid_source_url, raw_csv, len(rows), started_at)
        print(
            f"Ingestion run {ingestion_run.id} complete: {ingestion_run.row_count} rows, "
            f"checksum {ingestion_run.checksum[:12]}..."
        )
    finally:
        db.close()


if __name__ == "__main__":
    run()
