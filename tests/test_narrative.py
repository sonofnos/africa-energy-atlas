import re

from app.services.narrative import PassthroughNarrativeClient, compute_trend_stats, render_narrative


def test_computes_direction_and_pct_change():
    stats = compute_trend_stats("Nigeria", "per_capita_electricity", [(2019, 174.0), (2022, 170.3)])

    assert stats.direction == "fallen"
    assert round(stats.pct_change, 1) == round(((170.3 - 174.0) / 174.0) * 100, 1)


def test_returns_none_with_fewer_than_two_points():
    assert compute_trend_stats("Nigeria", "per_capita_electricity", [(2022, 170.3)]) is None
    assert compute_trend_stats("Nigeria", "per_capita_electricity", []) is None


def test_narrative_uses_only_computed_numbers():
    """The grounding invariant: every number in the rendered narrative must
    be one this module actually computed from the data, not something a
    client injected while 'polishing' the text."""
    stats = compute_trend_stats("South Africa", "renewables_share_energy", [(2019, 2.24), (2022, 3.65)])
    text = render_narrative(stats)

    numbers_in_text = set(re.findall(r"\d+\.?\d*", text))
    assert numbers_in_text <= stats.numbers_used()


class _RephrasingClient:
    """A client that changes wording but must never introduce new numbers."""

    def polish(self, text: str) -> str:
        return f"In short: {text}"


def test_a_rephrasing_client_cannot_add_numbers():
    stats = compute_trend_stats("Egypt", "fossil_share_energy", [(2019, 92.1), (2022, 89.4)])
    text = render_narrative(stats, client=_RephrasingClient())

    numbers_in_text = set(re.findall(r"\d+\.?\d*", text))
    assert numbers_in_text <= stats.numbers_used()


def test_passthrough_client_is_the_default():
    stats = compute_trend_stats("Kenya", "energy_per_capita", [(2019, 500.0), (2022, 520.0)])

    assert render_narrative(stats) == render_narrative(stats, client=PassthroughNarrativeClient())
