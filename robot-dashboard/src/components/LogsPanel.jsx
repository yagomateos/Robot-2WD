import { useEffect, useState } from "react";
import { apiGet } from "../hooks/useRobotApi";

export default function LogsPanel() {
  const [logs, setLogs] = useState([]);
  const load = async () => { const d = await apiGet("/logs"); if (d && d.logs) setLogs(d.logs); };

  useEffect(()=>{ load(); const id=setInterval(load,1500); return()=>clearInterval(id);},[]);

  return (
    <div style={{ border: "1px solid #888", padding: "15px", borderRadius: "8px" }}>
      <h2>Registros</h2>
      <ul>{logs.map((l,i)=>(<li key={i}>{l}</li>))}</ul>
    </div>
  );
}