import { useEffect, useState } from "react";
import { apiGet } from "../hooks/useRobotApi";

export default function LogsPanel({ robotIP, isRestarting }) {
  const [logs, setLogs] = useState([]);

  const load = async () => {
    if (!robotIP || isRestarting) return;

    const d = await apiGet("/logs");
    if (d && d.logs) setLogs(d.logs);
  };

  useEffect(() => {
    if (!isRestarting) {
      load();
      const interval = setInterval(load, 1000);
      return () => clearInterval(interval);
    }
  }, [robotIP, isRestarting]);

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-icon">📝</div>
        <h2 className="card-title">Registros</h2>
      </div>

      <div className="logs-container">
        {isRestarting ? (
          <div className="empty-logs">Esperando reconexión...</div>
        ) : logs.length === 0 ? (
          <div className="empty-logs">No hay registros aún...</div>
        ) : (
          <ul className="logs-list">
            {logs.map((log, i) => (
              <li
                key={i}
                className={`log-item ${
                  log.includes("ERROR") ? "error" : ""
                }`}
              >
                {log}
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  );
}
