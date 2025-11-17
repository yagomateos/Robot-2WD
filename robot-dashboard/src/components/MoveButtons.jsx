import { move } from "../hooks/useRobotApi";

export default function MoveButtons() {
  return (
    <div className="card">
      <div className="card-header">
        <div className="card-icon">🎮</div>
        <h2 className="card-title">Control</h2>
      </div>
      <div className="move-container">
        <div className="move-row">
          <button className="move-btn forward" onClick={() => move("F")}>↑</button>
        </div>
        <div className="move-row">
          <button className="move-btn left" onClick={() => move("L")}>←</button>
          <button className="move-btn stop" onClick={() => move("S")}>■</button>
          <button className="move-btn right" onClick={() => move("R")}>→</button>
        </div>
        <div className="move-row">
          <button className="move-btn backward" onClick={() => move("B")}>↓</button>
        </div>
      </div>
    </div>
  );
}