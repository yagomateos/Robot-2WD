// Leer IP del robot desde variables de entorno
// Si no está definida, usar localhost como fallback
export const API_URL = import.meta.env.VITE_ROBOT_IP || "http://localhost";

// Token de seguridad para endpoints protegidos
// Debe coincidir con SECURITY_TOKEN en config.py del ESP32
export const SECURITY_TOKEN = import.meta.env.VITE_SECURITY_TOKEN || "robot2wd-secure-token-2025";

// Helper para agregar token a URL
function addToken(path) {
  const separator = path.includes('?') ? '&' : '?';
  return `${path}${separator}token=${SECURITY_TOKEN}`;
}

export async function apiGet(path, requiresAuth = false) {
  try {
    // Agregar token si el endpoint lo requiere
    const finalPath = requiresAuth ? addToken(path) : path;
    const res = await fetch(API_URL + finalPath);
    if (!res.ok) {
      console.error(`HTTP ${res.status}: ${finalPath}`);
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
export async function restartESP32() { return apiGet("/restart", true); } // Requiere autenticación