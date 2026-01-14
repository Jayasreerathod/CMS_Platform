import axios from "axios";

//  Correct environment variable name and fallback
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

console.log("Using API base URL:", API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
});

export async function getPrograms() {
  const res = await api.get("/catalog/programs");
  return res.data;
}

export default api;
