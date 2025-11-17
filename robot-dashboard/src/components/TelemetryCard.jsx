import useTelemetry from "../hooks/useTelemetry";

export default function TelemetryCard() {
  const t = useTelemetry();
  if (!t) return <p>Cargando datos...</p>;

  return (
    <div style={{ border: "1px solid #ccc", padding: "15px", borderRadius: "8px" }}>
      <h2>Telemetría</h2>
      <p><strong>Uptime:</strong> {t.uptime}s</p>
      <p><strong>Distancia:</strong> {t.distance_cm} cm</p>
      <p><strong>Obstáculo:</strong> {t.obstacle ? "Sí" : "No"}</p>
      <p><strong>Auto:</strong> {t.auto_enabled ? "Activo" : "Inactivo"}</p>
    </div>
  );
}