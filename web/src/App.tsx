import { useEffect, useMemo, useState } from "react";
import { api } from "./api/client";
import type { ComparisonPoint, Country, Indicator, Narrative, Series } from "./api/types";
import { TrendChart } from "./components/TrendChart";
import { ComparisonChart } from "./components/ComparisonChart";
import { latestYear } from "./lib/format";

export default function App() {
  const [countries, setCountries] = useState<Country[]>([]);
  const [indicators, setIndicators] = useState<Indicator[]>([]);
  const [countryIso, setCountryIso] = useState("NGA");
  const [indicatorKey, setIndicatorKey] = useState("per_capita_electricity");

  const [series, setSeries] = useState<Series | null>(null);
  const [comparison, setComparison] = useState<ComparisonPoint[]>([]);
  const [narrative, setNarrative] = useState<Narrative | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api.countries().then(setCountries).catch((e) => setError(e.message));
    api.indicators().then(setIndicators).catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    if (!countryIso || !indicatorKey) return;
    setError(null);

    api
      .series(countryIso, indicatorKey)
      .then((data) => {
        setSeries(data);
        const year = latestYear(data.points);
        if (year !== null) {
          api.compare(indicatorKey, year).then(setComparison).catch(() => setComparison([]));
        } else {
          setComparison([]);
        }
      })
      .catch((e) => {
        setError(e.message);
        setSeries(null);
      });

    api
      .narrative(countryIso, indicatorKey)
      .then(setNarrative)
      .catch(() => setNarrative(null));
  }, [countryIso, indicatorKey]);

  const currentIndicator = useMemo(
    () => indicators.find((i) => i.key === indicatorKey),
    [indicators, indicatorKey],
  );

  return (
    <div className="page">
      <header>
        <h1>Africa Energy Atlas</h1>
        <p className="subtitle">
          Energy transition indicators for African Union member states, from public data
        </p>
      </header>

      <div className="controls">
        <label>
          Country
          <select value={countryIso} onChange={(e) => setCountryIso(e.target.value)}>
            {countries.map((c) => (
              <option key={c.iso_code} value={c.iso_code}>
                {c.name}
              </option>
            ))}
          </select>
        </label>
        <label>
          Indicator
          <select value={indicatorKey} onChange={(e) => setIndicatorKey(e.target.value)}>
            {indicators.map((i) => (
              <option key={i.key} value={i.key}>
                {i.label}
              </option>
            ))}
          </select>
        </label>
      </div>

      {error && <p className="error">{error}</p>}

      {narrative && <p className="narrative">{narrative.text}</p>}

      <section className="card">
        <h2>Trend over time</h2>
        {series && <TrendChart series={series} />}
      </section>

      <section className="card">
        <h2>
          {currentIndicator?.label} — cross-country comparison
          {series && series.points.length > 0 && ` (${latestYear(series.points)})`}
        </h2>
        {currentIndicator && <ComparisonChart points={comparison} indicator={currentIndicator} />}
      </section>

      <footer>
        Data: Our World in Data energy dataset (owid/energy-data), public domain.
      </footer>
    </div>
  );
}
