import { useEffect, useState } from "react";
import PropTypes from 'prop-types';
import { apiGet, restartESP32 } from "../hooks/useRobotApi";

function SecurityPanel({ isRestarting, setIsRestarting }) {
  const [sec, setSec] = useState(null);

  async function refresh(){
    if (!isRestarting) {
      setSec(await apiGet("/security"));
    }
  }

  async function clearSafe(){ await apiGet("/clear"); refresh(); }

  async function handleRestart(){
    if (confirm("¿Estás seguro de que quieres reiniciar el ESP32?")) {
      setIsRestarting(true);
      await restartESP32();
      // Esperar 5 segundos antes de volver a intentar conectar
      setTimeout(() => {
        setIsRestarting(false);
      }, 5000);
    }
  }

  useEffect(()=>{
    if (!isRestarting) {
      refresh();
      const id=setInterval(refresh,1500);
      return()=>clearInterval(id);
    }
  },[isRestarting]);

  if (isRestarting) return (
    <div className="card">
      <div className="card-header">
        <div className="card-icon">🛡️</div>
        <h2 className="card-title">Seguridad</h2>
      </div>
      <div className="security-alert" style={{background: '#f59e0b'}}>
        🔄 Reiniciando ESP32...
      </div>
      <div className="loading">Esperando reconexión...</div>
    </div>
  );

  if (!sec) return (
    <div className="card">
      <div className="loading">Cargando seguridad</div>
    </div>
  );

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-icon">🛡️</div>
        <h2 className="card-title">Seguridad</h2>
      </div>

      {sec.safe_mode && (
        <div className="security-alert">
          ⚠️ Modo Seguro Activado
        </div>
      )}

      <div className="security-stats">
        <div className="security-stat">
          <span className="security-stat-label">Errores detectados</span>
          <span className="security-stat-value">{sec.fail_count}</span>
        </div>
        <div className="security-stat">
          <span className="security-stat-label">Modo seguro</span>
          <span className="security-stat-value">
            {sec.safe_mode ? "🔒 Activado" : "🔓 Desactivado"}
          </span>
        </div>
        <div className="security-stat">
          <span className="security-stat-label">Último error</span>
          <span className="security-stat-value">{sec.last_error || "Ninguno"}</span>
        </div>
        {sec.last_ip && (
          <div className="security-stat">
            <span className="security-stat-label">IP origen</span>
            <span className="security-stat-value">{sec.last_ip}</span>
          </div>
        )}
      </div>

      <button className="btn-reset" onClick={handleRestart}>
        Reiniciar ESP32
      </button>
    </div>
  );
}

SecurityPanel.propTypes = {
  isRestarting: PropTypes.bool.isRequired,
  setIsRestarting: PropTypes.func.isRequired
};

export default SecurityPanel;