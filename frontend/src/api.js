import axios from "axios";

const API_BASE_URL = import.meta.env.VITE_API_URL || "http://127.0.0.1:8000"; // fallback for production

console.log("Using API base URL:", API_BASE_URL);

const api = axios.create({
  baseURL: API_BASE_URL,
});

export async function getPrograms() {
  const res = await api.get("/cms/programs");
  return res.data;
}

export default api;
