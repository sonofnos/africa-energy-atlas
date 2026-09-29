from app.models import Country, EnergyFact
from app.services.ingestion import checksum, parse_african_energy_facts, upsert_facts


def test_parses_only_african_countries(sample_csv):
    rows = parse_african_energy_facts(sample_csv)
    isos = {r.country_iso for r in rows}

    assert isos == {"NGA", "ZAF"}  # World is excluded: no ISO code


def test_skips_blank_indicator_values(sample_csv):
    rows = parse_african_energy_facts(sample_csv)

    nga_renewables = [r for r in rows if r.country_iso == "NGA" and r.indicator == "renewables_share_energy"]
    assert nga_renewables == []  # real data gap: OWID has no renewables split for Nigeria

    zaf_renewables = [r for r in rows if r.country_iso == "ZAF" and r.indicator == "renewables_share_energy"]
    assert len(zaf_renewables) == 4


def test_checksum_is_stable():
    assert checksum("abc") == checksum("abc")
    assert checksum("abc") != checksum("abd")


def test_upsert_is_idempotent(db, sample_csv):
    rows = parse_african_energy_facts(sample_csv)

    first_count = upsert_facts(db, rows, source="test")
    second_count = upsert_facts(db, rows, source="test")

    assert first_count == second_count
    assert db.query(EnergyFact).count() == len(rows)  # no duplicates on re-run


def test_upsert_updates_changed_values(db, sample_csv):
    rows = parse_african_energy_facts(sample_csv)
    upsert_facts(db, rows, source="test")

    revised = [
        rows[0].__class__(
            country_iso=rows[0].country_iso, year=rows[0].year, indicator=rows[0].indicator, value=999.0
        )
    ]
    upsert_facts(db, revised, source="test-v2")

    updated = (
        db.query(EnergyFact)
        .filter_by(country_iso=revised[0].country_iso, year=revised[0].year, indicator=revised[0].indicator)
        .one()
    )
    assert updated.value == 999.0
    assert updated.source == "test-v2"


def test_upsert_seeds_all_african_countries_even_with_no_data(db):
    upsert_facts(db, [], source="test")

    assert db.query(Country).count() == 55
