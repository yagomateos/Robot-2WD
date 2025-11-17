import { useEffect, useState } from "react";
import { apiGet } from "../hooks/useRobotApi";

export default function LogsPanel({ robotIP }) {
  const [logs, setLogs] = useState([]);

  const load = async () => {
    if (!robotIP) return;

    const d = await apiGet("/logs");
    if (d && d.logs) setLogs(d.logs);
  };

  useEffect(() => {
    load();
    const interval = setInterval(load, 1000); // refresco实时
    return () => clearInterval(interval);
  }, [robotIP]);

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-icon">📝</div>
        <h2 className="card-title">Registros</h2>
      </div>

      <div className="logs-container">
        {logs.length === 0 ? (
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
