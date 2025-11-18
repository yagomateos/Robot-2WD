// Leer IP del robot desde variables de entorno
// Si no está definida, usar localhost como fallback
export const API_URL = import.meta.env.VITE_ROBOT_IP || "http://localhost";

export async function apiGet(path) {
  try {
    const res = await fetch(API_URL + path);
    if (!res.ok) {
      console.error(`HTTP ${res.status}: ${path}`);
      return null;
    }
    return await res.json();
  } catch (e) {
    // No mostrar error si es durante desarrollo
    if (import.meta.env.DEV) {
      console.error('Error en fetch:', path, e.message);
    }
    return null;
  }
}

export async function move(dir) { return apiGet("/move?dir=" + dir); }
export async function toggleAuto(flag) { return apiGet("/auto?enabled=" + flag); }
export async function restartESP32() { return apiGet("/restart"); }