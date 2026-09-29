from pathlib import Path

import pytest
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import Base, SessionLocal, engine
from app.models import Country, EnergyFact, IngestionRun  # noqa: F401


@pytest.fixture(scope="session", autouse=True)
def _create_schema():
    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture(autouse=True)
def _clean_tables():
    with engine.begin() as conn:
        conn.execute(text("TRUNCATE energy_facts, ingestion_runs, countries RESTART IDENTITY CASCADE"))
    yield


@pytest.fixture
def db() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def sample_csv() -> str:
    return (Path(__file__).parent / "fixtures" / "sample_owid.csv").read_text()
