import { Bar, BarChart, CartesianGrid, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";
import type { ComparisonPoint, Indicator } from "../api/types";

export function ComparisonChart({ points, indicator }: { points: ComparisonPoint[]; indicator: Indicator }) {
  if (points.length === 0) {
    return <p className="empty">No comparison data available for this year.</p>;
  }

  const top = points.slice(0, 12).map((p) => ({ name: p.country.iso_code, fullName: p.country.name, value: p.value }));

  return (
    <ResponsiveContainer width="100%" height={280}>
      <BarChart data={top} margin={{ top: 8, right: 16, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="#2a3038" />
        <XAxis dataKey="name" stroke="#a9b1bc" fontSize={12} />
        <YAxis stroke="#a9b1bc" fontSize={12} />
        <Tooltip
          contentStyle={{ background: "#161b22", border: "1px solid #2a3038", fontSize: 13 }}
          labelStyle={{ color: "#e6e6e6" }}
          formatter={(value) => [`${value} ${indicator.unit}`, indicator.label]}
          labelFormatter={(_, entry) => entry?.[0]?.payload?.fullName ?? ""}
        />
        <Bar dataKey="value" fill="#2f81f7" radius={[3, 3, 0, 0]} isAnimationActive={false} />
      </BarChart>
    </ResponsiveContainer>
  );
}
