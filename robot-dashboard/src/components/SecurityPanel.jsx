import { useEffect, useState } from "react";
import PropTypes from 'prop-types';
import { apiGet, restartESP32, API_URL } from "../hooks/useRobotApi";

function SecurityPanel({ isRestarting, setIsRestarting }) {
  const [sec, setSec] = useState(null);

  async function refresh(){
    if (!isRestarting) {
      setSec(await apiGet("/security"));
    }
  }

  async function clearSafe(){ await apiGet("/clear", true); refresh(); } // Requiere autenticación

  async function handleRestart(){
    if (confirm("¿Estás seguro de que quieres reiniciar el ESP32?")) {
      setIsRestarting(true);
      await restartESP32();

      // Polling inteligente: intentar reconectar cada 2s
      let attempts = 0;
      const maxAttempts = 15; // 15 intentos = 30 segundos máximo

      const checkConnection = async () => {
        attempts++;

        try {
          const response = await fetch(API_URL + "/status");
          if (response.ok) {
            // ESP32 respondió, reconectado exitosamente
            console.log(`ESP32 reconectado después de ${attempts * 2}s`);
            setIsRestarting(false);
            refresh();
            return;
          }
        } catch (e) {
          // Todavía no responde
        }

        // Si no ha respondido y no hemos alcanzado el límite, reintentar
        if (attempts < maxAttempts) {
          setTimeout(checkConnection, 2000);
        } else {
          // Timeout alcanzado, dejar de intentar
          console.log("Timeout: ESP32 no respondió después de 30s");
          setIsRestarting(false);
        }
      };

      // Esperar 5s antes del primer intento (tiempo mínimo de arranque)
      setTimeout(checkConnection, 5000);
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

      <div style={{display: 'flex', gap: '10px', flexDirection: 'column'}}>
        {sec.safe_mode && (
          <button className="btn-reset" onClick={clearSafe} style={{background: '#10b981'}}>
            Desactivar Modo Seguro
          </button>
        )}
        <button className="btn-reset" onClick={handleRestart}>
          Reiniciar ESP32
        </button>
      </div>
    </div>
  );
}

SecurityPanel.propTypes = {
  isRestarting: PropTypes.bool.isRequired,
  setIsRestarting: PropTypes.func.isRequired
};

export default SecurityPanel;