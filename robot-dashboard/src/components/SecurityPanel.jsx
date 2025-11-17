import { useEffect, useState } from "react";
import { apiGet } from "../hooks/useRobotApi";

export default function SecurityPanel() {
  const [sec, setSec] = useState(null);
  async function refresh(){ setSec(await apiGet("/security")); }
  async function clearSafe(){ await apiGet("/clear"); refresh(); }

  useEffect(()=>{ refresh(); const id=setInterval(refresh,1500); return()=>clearInterval(id);},[]);
  if (!sec) return <p>Cargando seguridad...</p>;

  return (
    <div style={{ border: "1px solid #f00", padding: "15px", borderRadius: "8px" }}>
      <h2>Seguridad</h2>
      <p><strong>Fallos:</strong> {sec.fail_count}</p>
      <p><strong>Modo seguro:</strong> {sec.safe_mode ? "Sí" : "No"}</p>
      <p><strong>Último error:</strong> {sec.last_error || "-"}</p>
      <button onClick={clearSafe}>Reiniciar seguridad</button>
    </div>
  );
}