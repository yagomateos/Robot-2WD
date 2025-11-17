import { move } from "../hooks/useRobotApi";

const btn = { padding: "12px 20px", margin: "8px", fontSize: "16px", cursor: "pointer" };

export default function MoveButtons() {
  return (
    <div>
      <h2>Movimiento</h2>
      <div><button style={btn} onClick={() => move("F")}>Adelante</button></div>
      <div>
        <button style={btn} onClick={() => move("L")}>Izquierda</button>
        <button style={btn} onClick={() => move("S")}>Parar</button>
        <button style={btn} onClick={() => move("R")}>Derecha</button>
      </div>
      <div><button style={btn} onClick={() => move("B")}>Atrás</button></div>
    </div>
  );
}