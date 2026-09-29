from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class EnergyFact(Base):
    __tablename__ = "energy_facts"
    __table_args__ = (
        UniqueConstraint("country_iso", "year", "indicator", name="uq_energy_fact_point"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    country_iso: Mapped[str] = mapped_column(String(3), ForeignKey("countries.iso_code"), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    indicator: Mapped[str] = mapped_column(String(64), nullable=False)
    value: Mapped[float] = mapped_column(Float, nullable=False)
    source: Mapped[str] = mapped_column(String(255), nullable=False)
    ingested_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    country = relationship("Country", back_populates="facts")
