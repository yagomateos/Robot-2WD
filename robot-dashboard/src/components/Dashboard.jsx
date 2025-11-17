import MoveButtons from "./MoveButtons";
import TelemetryCard from "./TelemetryCard";
import SecurityPanel from "./SecurityPanel";
import LogsPanel from "./LogsPanel";

export default function Dashboard({ robotIP }) {
  if (!robotIP) {
    return (
      <div className="dashboard-grid">
        <div className="loading-box">
          <h2>Conectando con el robot...</h2>
          <p>Esperando respuesta de /status</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-grid">
      {/* Pasamos la IP a todos los componentes */}
      <TelemetryCard robotIP={robotIP} />
      <MoveButtons robotIP={robotIP} />
      <SecurityPanel robotIP={robotIP} />
      <LogsPanel robotIP={robotIP} />
    </div>
  );
}
