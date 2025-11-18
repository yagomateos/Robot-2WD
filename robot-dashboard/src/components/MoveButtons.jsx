import { move } from "../hooks/useRobotApi";

export default function MoveButtons({ isRestarting }) {
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
      <div className="move-container">
        <div className="move-row">
          <button className="move-btn forward" onClick={() => handleMove("F")} disabled={isRestarting}>↑</button>
        </div>
        <div className="move-row">
          <button className="move-btn left" onClick={() => handleMove("L")} disabled={isRestarting}>←</button>
          <button className="move-btn stop" onClick={() => handleMove("S")} disabled={isRestarting}>■</button>
          <button className="move-btn right" onClick={() => handleMove("R")} disabled={isRestarting}>→</button>
        </div>
        <div className="move-row">
          <button className="move-btn backward" onClick={() => handleMove("B")} disabled={isRestarting}>↓</button>
        </div>
      </div>
    </div>
  );
}