import { describe, expect, it } from "vitest";
import { formatValue, latestYear } from "./format";

describe("formatValue", () => {
  it("formats small values, including percentages, with one decimal place", () => {
    expect(formatValue(3.648, "%")).toBe("3.6%");
    expect(formatValue(3.648, "TWh")).toBe("3.6 TWh");
  });

  it("rounds large values to whole numbers", () => {
    expect(formatValue(2345.254, "kWh")).toBe("2345 kWh");
  });
});

describe("latestYear", () => {
  it("returns the maximum year in a points array", () => {
    expect(latestYear([{ year: 2019 }, { year: 2022 }, { year: 2020 }])).toBe(2022);
  });

  it("returns null for an empty array", () => {
    expect(latestYear([])).toBeNull();
  });
});
