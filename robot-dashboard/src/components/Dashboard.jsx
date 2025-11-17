import MoveButtons from "./MoveButtons";
import TelemetryCard from "./TelemetryCard";
import SecurityPanel from "./SecurityPanel";
import LogsPanel from "./LogsPanel";

export default function Dashboard() {
  return (
    <div className="dashboard-grid">
      <TelemetryCard />
      <MoveButtons />
      <SecurityPanel />
      <LogsPanel />
    </div>
  );
}