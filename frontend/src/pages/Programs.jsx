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
        const res = await api.get("/cms/programs", {
          headers: token ? { Authorization: `Bearer ${token}` } : {},
        });
        setPrograms(res.data);
      } catch (err) {
        console.error("Error fetching programs:", err);
      }
    }
    fetchPrograms();
  }, [token]);

  // Add new program (admin/editor only)
  async function handleAddProgram() {
    if (!title.trim()) return alert("Please enter a program title");
    try {
      await api.post(
        "/cms/programs",
        { title, description },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Program created!");
      window.location.reload();
    } catch (err) {
      console.error(err);
      alert("Failed to create program");
    }
  }

  // Publish a program
  async function handlePublish(id) {
    try {
      await api.post(
        `/cms/programs/${id}/publish`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Program published!");
      window.location.reload();
    } catch (err) {
      console.error(err);
      alert("Failed to publish program");
    }
  }

  // Delete program
  async function handleDelete(id) {
    if (!window.confirm("Are you sure you want to delete this program?")) return;
    try {
      await api.delete(`/cms/programs/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Program deleted.");
      setPrograms((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      console.error(err);
      alert("Failed to delete program");
    }
  }

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold text-indigo-400 mb-6">Programs</h1>

      {/* Show Add Form only for Admin/Editor */}
      {(role === "admin" || role === "editor") && (
        <div className="flex flex-wrap gap-3 mb-6">
          <input
            type="text"
            placeholder="Program title"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="p-2 bg-gray-700 rounded border border-gray-600"
          />
          <input
            type="text"
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="p-2 bg-gray-700 rounded border border-gray-600"
          />
          <button
            onClick={handleAddProgram}
            className="bg-indigo-500 hover:bg-indigo-600 text-white px-4 rounded"
          >
            + New Program
          </button>
        </div>
      )}

      {programs.length === 0 ? (
        <p className="text-gray-400">No programs found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {programs.map((p) => (
            <div
              key={p.id}
              className="bg-gray-800 p-4 rounded-lg border border-gray-700 hover:border-indigo-400 transition"
            >
              <h2 className="text-xl font-semibold text-indigo-400">
                {p.title}
              </h2>
              <p className="text-gray-400 text-sm mb-3">{p.description}</p>

              <p className="text-sm mb-3">
                <span
                  className={`px-2 py-1 rounded ${
                    p.status === "published"
                      ? "bg-green-600"
                      : p.status === "scheduled"
                      ? "bg-yellow-500 text-black"
                      : "bg-gray-500"
                  }`}
                >
                  {p.status}
                </span>
              </p>

              <Link
                to={`/programs/${p.id}`}
                className="inline-block bg-indigo-500 hover:bg-indigo-600 px-3 py-1 rounded text-sm mr-2"
              >
                Manage Lessons
              </Link>

              {(role === "admin" || role === "editor") && (
                <>
                  {p.status !== "published" && (
                    <button
                      onClick={() => handlePublish(p.id)}
                      className="bg-green-600 hover:bg-green-700 px-3 py-1 rounded text-sm mr-2"
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
                </>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
