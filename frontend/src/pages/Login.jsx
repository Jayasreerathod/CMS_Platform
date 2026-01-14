import { useState } from "react";
import api from "../api";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  async function handleLogin(e) {
    e.preventDefault();
    try {
      const res = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      localStorage.setItem("role", res.data.role);
      alert(`Welcome ${res.data.role.toUpperCase()}!`);
      window.location.href = "/programs";
    } catch (err) {
      alert("Invalid credentials");
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-br from-indigo-700 to-black">
      <div className="bg-gray-900 p-8 rounded-xl shadow-xl w-full max-w-md border border-gray-700">
        <h1 className="text-3xl font-bold text-center text-indigo-400 mb-6">
          LessonCMS Login
        </h1>
        <form onSubmit={handleLogin} className="space-y-4">
          <input
            type="email"
            placeholder="Email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full p-3 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500"
            required
          />
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-3 rounded bg-gray-800 border border-gray-700 focus:outline-none focus:border-indigo-500"
            required
          />
          <button
            type="submit"
            className="w-full py-3 bg-indigo-600 hover:bg-indigo-700 rounded text-white font-semibold"
          >
            Login
          </button>
        </form>
      </div>
    </div>
  );
}
