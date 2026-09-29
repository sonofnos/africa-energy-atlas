from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Country(Base):
    __tablename__ = "countries"

    iso_code: Mapped[str] = mapped_column(String(3), primary_key=True)
    name: Mapped[str] = mapped_column(String(120), nullable=False)

    facts = relationship("EnergyFact", back_populates="country", cascade="all, delete-orphan")
