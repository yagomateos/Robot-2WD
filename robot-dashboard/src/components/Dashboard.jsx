import MoveButtons from "./MoveButtons";
import TelemetryCard from "./TelemetryCard";
import SecurityPanel from "./SecurityPanel";
import LogsPanel from "./LogsPanel";

export default function Dashboard() {
  return (
    <div style={{ display: "grid", gap: "20px", gridTemplateColumns: "1fr 1fr" }}>
      <TelemetryCard />
      <MoveButtons />
      <SecurityPanel />
      <LogsPanel />
    </div>
  );
}