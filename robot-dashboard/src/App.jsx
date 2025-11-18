import { useEffect, useState } from "react";
import Dashboard from "./components/Dashboard";
import { API_URL } from "./hooks/useRobotApi";
import "./styles.css";

export default function App() {
  const [robotIP, setRobotIP] = useState(null);
  const [isRestarting, setIsRestarting] = useState(false);
  const [statusData, setStatusData] = useState(null);

  // Obtener IP del robot desde /status
  const loadRobotIP = async () => {
    try {
      const res = await fetch(`${API_URL}/status`);
      const data = await res.json();
      if (data.ip) setRobotIP(data.ip);
    } catch (e) {
      if (import.meta.env.DEV) {
        console.log("No se pudo obtener la IP del robot");
      }
    }
  };

  // Polling de status - pausado durante reinicio
  useEffect(() => {
    if (!isRestarting) {
      const checkStatus = async () => {
        try {
          const res = await fetch(`${API_URL}/status`);
          const data = await res.json();
          setStatusData(data);
        } catch (e) {
          setStatusData(null);
        }
      };
      checkStatus();
      const id = setInterval(checkStatus, 1000);
      return () => clearInterval(id);
    }
  }, [isRestarting]);

  useEffect(() => {
    loadRobotIP();
  }, []);

  // Determinar si está conectado
  const isConnected = !isRestarting && statusData !== null;

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">🤖 Robot ESP32</h1>
        <p className="app-subtitle">Control Dashboard</p>
        <span className={`status-badge ${isRestarting ? 'restarting' : (isConnected ? 'connected' : 'disconnected')}`}>
          ● {isRestarting ? 'Reiniciando...' : (isConnected ? 'Conectado' : 'Desconectado')}
        </span>
      </header>

      {/* Pasamos la IP y el control de reinicio al Dashboard */}
      <Dashboard robotIP={robotIP} isRestarting={isRestarting} setIsRestarting={setIsRestarting} />
    </div>
  );
}
