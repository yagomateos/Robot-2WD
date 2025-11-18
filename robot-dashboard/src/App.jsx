import { useEffect, useState } from "react";
import Dashboard from "./components/Dashboard";
import useStatus from "./hooks/useStatus";
import "./styles.css";

export default function App() {
  const [robotIP, setRobotIP] = useState(null);
  const statusData = useStatus();

  // Obtener IP del robot desde /status
  const loadRobotIP = async () => {
    try {
      const res = await fetch("http://10.184.61.174/status");
      const data = await res.json();
      if (data.ip) setRobotIP(data.ip);
    } catch (e) {
      console.log("No se pudo obtener la IP del robot");
    }
  };

  useEffect(() => {
    loadRobotIP();
  }, []);

  // Determinar si está conectado
  const isConnected = statusData !== null;

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">🤖 Robot ESP32</h1>
        <p className="app-subtitle">Control Dashboard</p>
        <span className={`status-badge ${isConnected ? 'connected' : 'disconnected'}`}>
          ● {isConnected ? 'Conectado' : 'Desconectado'}
        </span>
      </header>

      {/* Pasamos la IP al Dashboard */}
      <Dashboard robotIP={robotIP} />
    </div>
  );
}
