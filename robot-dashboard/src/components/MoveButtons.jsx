import PropTypes from 'prop-types';
import { move } from "../hooks/useRobotApi";

function MoveButtons({ isRestarting }) {
  const handleMove = (dir) => {
    if (!isRestarting) {
      move(dir);
    }
  };

  return (
    <div className="card">
      <div className="card-header">
        <div className="card-icon">🎮</div>
        <h2 className="card-title">Control</h2>
      </div>
      {isRestarting && (
        <div className="loading">Esperando reconexión...</div>
      )}
      <div className="move-container" role="group" aria-label="Controles de movimiento del robot">
        <div className="move-row">
          <button
            className="move-btn forward"
            onClick={() => handleMove("F")}
            disabled={isRestarting}
            aria-label="Mover adelante"
            title="Mover adelante (W o Flecha Arriba)"
          >
            ↑
          </button>
        </div>
        <div className="move-row">
          <button
            className="move-btn left"
            onClick={() => handleMove("L")}
            disabled={isRestarting}
            aria-label="Girar a la izquierda"
            title="Girar izquierda (A o Flecha Izquierda)"
          >
            ←
          </button>
          <button
            className="move-btn stop"
            onClick={() => handleMove("S")}
            disabled={isRestarting}
            aria-label="Detener"
            title="Detener (S o Espacio)"
          >
            ■
          </button>
          <button
            className="move-btn right"
            onClick={() => handleMove("R")}
            disabled={isRestarting}
            aria-label="Girar a la derecha"
            title="Girar derecha (D o Flecha Derecha)"
          >
            →
          </button>
        </div>
        <div className="move-row">
          <button
            className="move-btn backward"
            onClick={() => handleMove("B")}
            disabled={isRestarting}
            aria-label="Mover atrás"
            title="Mover atrás (X o Flecha Abajo)"
          >
            ↓
          </button>
        </div>
      </div>
    </div>
  );
}

MoveButtons.propTypes = {
  isRestarting: PropTypes.bool.isRequired
};

export default MoveButtons;