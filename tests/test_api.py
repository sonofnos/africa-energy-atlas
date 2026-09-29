from fastapi.testclient import TestClient

from app.main import app
from app.services.ingestion import parse_african_energy_facts, upsert_facts

client = TestClient(app)


def _seed(db, sample_csv):
    rows = parse_african_energy_facts(sample_csv)
    upsert_facts(db, rows, source="test")


def test_healthz():
    assert client.get("/healthz").json() == {"status": "ok"}


def test_list_countries_includes_seeded_data(db, sample_csv):
    _seed(db, sample_csv)

    response = client.get("/api/countries")

    assert response.status_code == 200
    codes = {c["iso_code"] for c in response.json()}
    assert "NGA" in codes and "ZAF" in codes


def test_list_indicators():
    response = client.get("/api/indicators")

    assert response.status_code == 200
    keys = {i["key"] for i in response.json()}
    assert "per_capita_electricity" in keys


def test_get_series_for_a_country(db, sample_csv):
    _seed(db, sample_csv)

    response = client.get("/api/data", params={"country": "NGA", "indicator": "per_capita_electricity"})

    assert response.status_code == 200
    body = response.json()
    assert body["country"]["iso_code"] == "NGA"
    assert len(body["points"]) == 4
    assert body["points"] == sorted(body["points"], key=lambda p: p["year"])


def test_get_series_year_filter(db, sample_csv):
    _seed(db, sample_csv)

    response = client.get(
        "/api/data", params={"country": "NGA", "indicator": "per_capita_electricity", "from_year": 2021}
    )

    years = [p["year"] for p in response.json()["points"]]
    assert years == [2021, 2022]


def test_get_series_unknown_country_is_404(db, sample_csv):
    _seed(db, sample_csv)

    response = client.get("/api/data", params={"country": "ZZZ", "indicator": "per_capita_electricity"})

    assert response.status_code == 404


def test_get_series_unknown_indicator_is_404(db, sample_csv):
    _seed(db, sample_csv)

    response = client.get("/api/data", params={"country": "NGA", "indicator": "not_a_real_indicator"})

    assert response.status_code == 404


def test_compare_countries_for_a_year(db, sample_csv):
    _seed(db, sample_csv)

    response = client.get("/api/compare", params={"indicator": "per_capita_electricity", "year": 2022})

    assert response.status_code == 200
    isos = {p["country"]["iso_code"] for p in response.json()}
    assert isos == {"NGA", "ZAF"}


def test_narrative_is_grounded_in_real_numbers(db, sample_csv):
    _seed(db, sample_csv)

    response = client.get("/api/narrative", params={"country": "ZAF", "indicator": "renewables_share_energy"})

    assert response.status_code == 200
    text = response.json()["text"]
    assert "2019" in text and "2022" in text
    assert "South Africa" in text


def test_narrative_404s_with_insufficient_data(db, sample_csv):
    _seed(db, sample_csv)

    # Nigeria has no renewables_share_energy points in the fixture at all.
    response = client.get("/api/narrative", params={"country": "NGA", "indicator": "renewables_share_energy"})

    assert response.status_code == 404
