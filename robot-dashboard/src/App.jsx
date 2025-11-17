import Dashboard from "./components/Dashboard";
import "./styles.css";

export default function App() {
  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">🤖 Robot ESP32</h1>
        <p className="app-subtitle">Control Dashboard</p>
        <span className="status-badge">● Conectado</span>
      </header>
      <Dashboard />
    </div>
  );
}