export function formatValue(value: number, unit: string): string {
  const rounded = Math.abs(value) >= 100 ? Math.round(value).toString() : value.toFixed(1);
  return unit === "%" ? `${rounded}%` : `${rounded} ${unit}`;
}

export function latestYear(points: { year: number }[]): number | null {
  if (points.length === 0) return null;
  return points.reduce((max, p) => Math.max(max, p.year), points[0].year);
}
