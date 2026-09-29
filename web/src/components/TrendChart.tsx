import { CartesianGrid, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { Series } from "../api/types";

export function TrendChart({ series }: { series: Series }) {
  if (series.points.length === 0) {
    return <p className="empty">No data available for {series.country.name} on this indicator.</p>;
  }

  return (
    <ResponsiveContainer width="100%" height={280}>
      <LineChart data={series.points} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#2a3038" />
        <XAxis dataKey="year" stroke="#a9b1bc" fontSize={12} />
        <YAxis stroke="#a9b1bc" fontSize={12} />
        <Tooltip
          contentStyle={{ background: "#161b22", border: "1px solid #2a3038", fontSize: 13 }}
          labelStyle={{ color: "#e6e6e6" }}
          formatter={(value) => [`${value} ${series.indicator.unit}`, series.indicator.label]}
        />
        <Line type="monotone" dataKey="value" stroke="#2f81f7" strokeWidth={2} dot={false} isAnimationActive={false} />
      </LineChart>
    </ResponsiveContainer>
  );
}
