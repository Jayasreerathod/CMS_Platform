import axios from "axios";

const API_BASE = "http://127.0.0.1:8000";

export const api = axios.create({
  baseURL: API_BASE,
});

export async function getPrograms() {
  const res = await api.get("/cms/programs");
  return res.data;
}

export default api;
