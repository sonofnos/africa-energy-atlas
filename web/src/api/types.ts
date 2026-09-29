export interface Country {
  iso_code: string;
  name: string;
}

export interface Indicator {
  key: string;
  label: string;
  unit: string;
}

export interface DataPoint {
  year: number;
  value: number;
}

export interface Series {
  country: Country;
  indicator: Indicator;
  points: DataPoint[];
}

export interface ComparisonPoint {
  country: Country;
  value: number;
}

export interface Narrative {
  country: Country;
  indicator: Indicator;
  text: string;
}
