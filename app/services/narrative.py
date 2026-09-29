"""Generates a short, grounded summary of one country/indicator series.

The number-bearing sentence is built entirely from real computed values --
never handed to an LLM to "fill in." A swappable client may rephrase the
wording, but `render_narrative`'s caller can verify every number quoted in
the final text is one of the numbers actually computed here (see
tests/test_narrative.py), the same "don't let the model invent the fact"
discipline as docwise's citation grounding.
"""

from dataclasses import dataclass
from typing import Protocol

from app.indicators import INDICATORS


@dataclass(frozen=True)
class TrendStats:
    country_name: str
    indicator: str
    unit: str
    first_year: int
    first_value: float
    last_year: int
    last_value: float

    @property
    def pct_change(self) -> float:
        if self.first_value == 0:
            return 0.0
        return ((self.last_value - self.first_value) / abs(self.first_value)) * 100

    @property
    def direction(self) -> str:
        if self.last_value > self.first_value:
            return "risen"
        if self.last_value < self.first_value:
            return "fallen"
        return "held steady"

    def numbers_used(self) -> set[str]:
        """Every numeric token that legitimately appears in the narrative,
        for a caller to check the final text against."""
        return {
            str(self.first_year),
            str(self.last_year),
            f"{self.first_value:.1f}",
            f"{self.last_value:.1f}",
            f"{abs(self.pct_change):.0f}",
        }


def compute_trend_stats(
    country_name: str, indicator: str, series: list[tuple[int, float]]
) -> TrendStats | None:
    if len(series) < 2:
        return None

    ordered = sorted(series, key=lambda point: point[0])
    first_year, first_value = ordered[0]
    last_year, last_value = ordered[-1]

    return TrendStats(
        country_name=country_name,
        indicator=indicator,
        unit=INDICATORS[indicator]["unit"],
        first_year=first_year,
        first_value=first_value,
        last_year=last_year,
        last_value=last_value,
    )


def render_template(stats: TrendStats) -> str:
    label = INDICATORS[stats.indicator]["label"].lower()
    return (
        f"{stats.country_name}'s {label} has {stats.direction} from "
        f"{stats.first_value:.1f}{stats.unit} in {stats.first_year} to "
        f"{stats.last_value:.1f}{stats.unit} in {stats.last_year}, "
        f"a change of {abs(stats.pct_change):.0f}%."
    )


class NarrativeClient(Protocol):
    def polish(self, text: str) -> str: ...


class PassthroughNarrativeClient:
    """Default: no LLM configured, the template sentence is returned as-is."""

    def polish(self, text: str) -> str:
        return text


def render_narrative(stats: TrendStats, client: NarrativeClient | None = None) -> str:
    client = client or PassthroughNarrativeClient()
    return client.polish(render_template(stats))
