# Africa Energy Atlas

A data platform for African Union member states' energy transition: a
Python/FastAPI ingestion pipeline over a real public dataset, a Postgres
schema built for provenance and reproducibility, and a React dashboard with
real charts (trend lines, cross-country comparisons) plus a narrative
summary that's grounded in the underlying numbers, never invented.

## Data

Source: [Our World in Data's energy dataset](https://github.com/owid/energy-data)
(`owid-energy-data.csv`), public domain, updated regularly. `scripts/ingest.py`
downloads it, filters to the 55 African Union member states (by ISO code,
not a fuzzy name match — aggregates like "Africa" or "World" have no ISO
code and are dropped automatically), and upserts six indicators relevant to
the energy transition: renewables and fossil shares of primary energy,
electricity generation (total and per capita), primary energy per capita,
and energy-sector greenhouse gas emissions.

**Real, honestly-documented data gap:** OWID's renewables/fossil energy-share
split only has coverage for 4 African countries (Algeria, Egypt, Morocco,
South Africa) — it's sourced from the Energy Institute's Statistical Review,
which tracks major economies, not a platform bug. The other four indicators
have much broader African coverage. The API returns an empty series rather
than fabricating a number for a country/indicator pair with no data.

## Provenance and reproducibility

Every ingestion run is recorded (`ingestion_runs`: source URL, a SHA-256
checksum of the raw file, row count, timestamps) so a given dataset snapshot
is traceable. Ingestion is idempotent on `(country_iso, year, indicator)` —
re-running it updates values in place rather than duplicating rows, so it's
safe to run on a schedule as OWID's upstream file changes.

## Grounded narratives, not generated ones

`/api/narrative` computes a real trend (first year, last year, % change,
direction) from the actual stored data points and renders it into a
sentence. A pluggable `NarrativeClient` can rephrase the wording, but it
never sees or invents the numbers — `tests/test_narrative.py` proves this by
asserting every numeric token in the final text is one of the numbers this
module actually computed, even when a client "polishes" the wording. Same
discipline as grounding a citation: state only what the data actually says.

## Stack

- FastAPI, SQLAlchemy, PostgreSQL.
- React 19 + TypeScript + Vite, Recharts for real chart rendering (line and
  bar), not just tables.
- pytest (backend, against a real Postgres) + Vitest (frontend).

## Running it

```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
createdb energy_atlas_dev
cp .env.example .env
python -m scripts.init_db
python -m scripts.ingest        # pulls the real OWID CSV, ~7k African data points
uvicorn app.main:app --reload

cd web
npm install
cp .env.example .env.local      # VITE_API_URL=http://localhost:8000
npm run dev
```

## Tests

```
python -m pytest              # 21 examples
cd web && npx vitest run      # 4 examples
```
