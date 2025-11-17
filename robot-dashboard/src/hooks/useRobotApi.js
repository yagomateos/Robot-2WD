export const API_URL = "http://10.184.61.174";

export async function apiGet(path) {
  try {
    const res = await fetch(API_URL + path);
    return await res.json();
  } catch (e) {
    return null;
  }
}

export async function move(dir) { return apiGet("/move?dir=" + dir); }
export async function toggleAuto(flag) { return apiGet("/auto?enabled=" + flag); }