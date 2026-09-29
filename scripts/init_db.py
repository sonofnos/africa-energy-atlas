"""Creates all tables. A production system would use Alembic migrations;
this project keeps the schema simple enough that create_all is honest."""

from app.database import Base, engine
from app.models import Country, EnergyFact, IngestionRun  # noqa: F401 (registers models)

if __name__ == "__main__":
    Base.metadata.create_all(engine)
    print("Schema created.")
