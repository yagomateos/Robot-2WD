import useTelemetry from "../hooks/useTelemetry";

export default function TelemetryCard() {
  const t = useTelemetry();

  if (!t) return (
    <div className="card">
      <div className="loading">Cargando telemetría</div>
    </div>
  );

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-icon">📊</div>
        <h2 className="card-title">Telemetría</h2>
      </div>
      <div className="telemetry-grid">
        <div className="metric">
          <div className="metric-label">Uptime</div>
          <div className="metric-value">
            {t.uptime}
            <span className="metric-unit">s</span>
          </div>
        </div>
        <div className="metric">
          <div className="metric-label">Distancia</div>
          <div className="metric-value">
            {t.distance_cm >= 0 ? t.distance_cm : "--"}
            <span className="metric-unit">cm</span>
          </div>
        </div>
        <div className="metric">
          <div className="metric-label">Obstáculo</div>
          <div className="metric-value">
            <span className={`metric-badge ${t.obstacle ? 'danger' : 'success'}`}>
              {t.obstacle ? "⚠️ Detectado" : "✓ Libre"}
            </span>
          </div>
        </div>
        <div className="metric">
          <div className="metric-label">Modo Auto</div>
          <div className="metric-value">
            <span className={`metric-badge ${t.auto_enabled ? 'info' : 'success'}`}>
              {t.auto_enabled ? "⚡ Activo" : "○ Inactivo"}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
}