import { useEffect, useState } from "react";
import { apiGet } from "./useRobotApi";

export default function useStatus() {
  const [data, setData] = useState(null);

  useEffect(() => {
    const f = async () => setData(await apiGet("/status"));
    f();
    const id = setInterval(f, 1000);
    return () => clearInterval(id);
  }, []);

  return data;
}