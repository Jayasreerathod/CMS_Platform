import axios from "axios";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL?.trim() ||
  "https://cms-platform-backend.onrender.com"; // fallback for production

console.log("Using API base URL:", API_BASE);

export const api = axios.create({
  baseURL: API_BASE,
});

export async function getPrograms() {
  const res = await api.get("/cms/programs");
  return res.data;
}

export default api;
