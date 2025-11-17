import { useEffect, useState } from "react";
import { apiGet } from "./useRobotApi";

export default function useTelemetry() {
  const [telemetry, setTelemetry] = useState(null);

  useEffect(() => {
    const f = async () => setTelemetry(await apiGet("/telemetry"));
    f();
    const id = setInterval(f, 800);
    return () => clearInterval(id);
  }, []);

  return telemetry;
}