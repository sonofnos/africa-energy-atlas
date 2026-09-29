import type { ComparisonPoint, Country, Indicator, Narrative, Series } from "./types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

async function get<T>(path: string): Promise<T> {
  const response = await fetch(`${API_URL}${path}`);
  if (!response.ok) {
    const body = await response.json().catch(() => null);
    throw new Error(body?.detail ?? `Request failed with status ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export const api = {
  countries: () => get<Country[]>("/api/countries"),
  indicators: () => get<Indicator[]>("/api/indicators"),
  series: (country: string, indicator: string) =>
    get<Series>(`/api/data?country=${country}&indicator=${indicator}`),
  compare: (indicator: string, year: number) =>
    get<ComparisonPoint[]>(`/api/compare?indicator=${indicator}&year=${year}`),
  narrative: (country: string, indicator: string) =>
    get<Narrative>(`/api/narrative?country=${country}&indicator=${indicator}`),
};
