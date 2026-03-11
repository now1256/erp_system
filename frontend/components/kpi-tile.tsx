type KpiTileProps = {
  label: string;
  value: string;
  tone?: "default" | "warning";
};

export function KpiTile({ label, value, tone = "default" }: KpiTileProps) {
  return (
    <div className={`kpi-tile ${tone === "warning" ? "kpi-tile-warning" : ""}`}>
      <span className="kpi-label">{label}</span>
      <strong className="kpi-value">{value}</strong>
    </div>
  );
}
