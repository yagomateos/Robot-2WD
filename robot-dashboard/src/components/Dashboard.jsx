import PropTypes from 'prop-types';
import MoveButtons from "./MoveButtons";
import TelemetryCard from "./TelemetryCard";
import SecurityPanel from "./SecurityPanel";
import LogsPanel from "./LogsPanel";

function Dashboard({ robotIP, isRestarting, setIsRestarting }) {
  if (!robotIP) {
    return (
      <div className="dashboard-grid">
        <div className="loading-box">
          <h2>Conectando con el robot...</h2>
          <p>Esperando respuesta de /status</p>
        </div>
      </div>
    );
  }

  return (
    <div className="dashboard-grid">
      {/* Pasamos la IP y el estado de reinicio a todos los componentes */}
      <TelemetryCard robotIP={robotIP} isRestarting={isRestarting} />
      <MoveButtons robotIP={robotIP} isRestarting={isRestarting} />
      <SecurityPanel robotIP={robotIP} isRestarting={isRestarting} setIsRestarting={setIsRestarting} />
      <LogsPanel robotIP={robotIP} isRestarting={isRestarting} />
    </div>
  );
}

Dashboard.propTypes = {
  robotIP: PropTypes.string,
  isRestarting: PropTypes.bool.isRequired,
  setIsRestarting: PropTypes.func.isRequired
};

export default Dashboard;
