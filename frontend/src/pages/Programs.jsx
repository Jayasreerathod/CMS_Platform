import { useState, useEffect } from "react";
import api from "../api";
import { Link } from "react-router-dom";

export default function Programs() {
  const [programs, setPrograms] = useState([]);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const role = localStorage.getItem("role");
  const token = localStorage.getItem("token");

  useEffect(() => {
    async function fetchPrograms() {
      try {
        const res = await api.get("/cms/programs");
        setPrograms(res.data);
      } catch (err) {
        console.error(err);
      }
    }
    fetchPrograms();
  }, []);

  async function handleAdd() {
    if (!title) return alert("Please enter a title");
    await api.post(
      "/cms/programs",
      { title, description },
      { headers: { Authorization: `Bearer ${token}` } }
    );
    alert("Program added!");
    window.location.reload();
  }

  async function handlePublish(id) {
    await api.post(
      `/cms/programs/${id}/publish`,
      {},
      { headers: { Authorization: `Bearer ${token}` } }
    );
    alert("Published!");
    window.location.reload();
  }

  async function handleDelete(id) {
    if (!window.confirm("Delete program?")) return;
    await api.delete(`/cms/programs/${id}`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    window.location.reload();
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-gray-800 text-white p-8">
      <h1 className="text-4xl font-extrabold text-indigo-400 mb-6">
        🎓 LessonCMS Dashboard
      </h1>

      {(role === "admin" || role === "editor") && (
        <div className="bg-gray-800 p-4 rounded-xl mb-8 shadow-lg border border-gray-700 flex gap-4 flex-wrap">
          <input
            placeholder="Program Title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="p-2 rounded bg-gray-900 border border-gray-700"
          />
          <input
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="p-2 rounded bg-gray-900 border border-gray-700 flex-1"
          />
          <button
            onClick={handleAdd}
            className="bg-indigo-600 hover:bg-indigo-700 px-4 py-2 rounded text-white"
          >
            ➕ Add Program
          </button>
        </div>
      )}

      <div className="grid md:grid-cols-3 sm:grid-cols-2 gap-6">
        {programs.map((p) => (
          <div
            key={p.id}
            className="bg-gray-900 p-5 rounded-xl shadow-lg hover:border-indigo-500 border border-gray-700 transition"
          >
            <h2 className="text-xl font-semibold text-indigo-400 mb-2">{p.title}</h2>
            <p className="text-gray-400 mb-4 text-sm">{p.description}</p>

            <div className="flex justify-between items-center mb-3">
              <span
                className={`px-2 py-1 rounded text-xs font-semibold ${
                  p.status === "published"
                    ? "bg-green-600"
                    : p.status === "scheduled"
                    ? "bg-yellow-500 text-black"
                    : "bg-gray-500"
                }`}
              >
                {p.status.toUpperCase()}
              </span>
              <Link
                to={`/programs/${p.id}`}
                className="text-indigo-400 hover:text-indigo-300 text-sm font-semibold"
              >
                View Lessons →
              </Link>
            </div>

            {(role === "admin" || role === "editor") && (
              <div className="flex gap-2">
                {p.status !== "published" && (
                  <button
                    onClick={() => handlePublish(p.id)}
                    className="bg-green-600 hover:bg-green-700 px-3 py-1 rounded text-sm"
                  >
                    Publish
                  </button>
                )}
                <button
                  onClick={() => handleDelete(p.id)}
                  className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm"
                >
                  Delete
                </button>
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
