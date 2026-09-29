from pydantic import BaseModel


class CountryOut(BaseModel):
    iso_code: str
    name: str


class IndicatorOut(BaseModel):
    key: str
    label: str
    unit: str


class DataPointOut(BaseModel):
    year: int
    value: float


class SeriesOut(BaseModel):
    country: CountryOut
    indicator: IndicatorOut
    points: list[DataPointOut]


class ComparisonPointOut(BaseModel):
    country: CountryOut
    value: float


class NarrativeOut(BaseModel):
    country: CountryOut
    indicator: IndicatorOut
    text: str
