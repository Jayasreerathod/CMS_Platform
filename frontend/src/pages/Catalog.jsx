import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import api from "../api";

export default function Catalog() {
  const [programs, setPrograms] = useState([]);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    async function fetchPrograms() {
      try {
        const res = await api.get("/catalog/programs");
        setPrograms(res.data);
      } catch (err) {
        console.error("Failed to load catalog:", err);
      }
    }
    fetchPrograms();
  }, []);

  async function openProgram(id) {
    setLoading(true);
    try {
      const res = await api.get(`/catalog/programs/${id}`);
      setSelectedProgram(res.data);
    } catch (err) {
      console.error("Failed to load program details:", err);
    } finally {
      setLoading(false);
    }
  }

  if (loading)
    return (
      <div className="p-8 text-gray-300 text-center">
        Loading program details...
      </div>
    );

  if (selectedProgram) {
    return (
      <div className="p-8 text-white">
        <button
          onClick={() => setSelectedProgram(null)}
          className="bg-gray-600 hover:bg-gray-700 px-3 py-1 rounded mb-4"
        >
          ← Back to Catalog
        </button>
        <h1 className="text-3xl font-bold text-indigo-400 mb-2">
          {selectedProgram.title}
        </h1>
        <p className="text-gray-400 mb-6">
          {selectedProgram.description || "No description"}
        </p>

        <h2 className="text-2xl text-indigo-300 mb-3">Published Lessons</h2>
        {selectedProgram.lessons?.length ? (
          <ul className="space-y-3">
            {selectedProgram.lessons.map((lesson) => (
              <li
                key={lesson.id}
                className="bg-gray-800 p-4 rounded border border-gray-700 flex justify-between items-center"
              >
                <span>
                  #{lesson.lesson_number} — {lesson.title}
                </span>
                {lesson.is_paid && (
                  <span className="text-sm bg-yellow-600 px-2 py-1 rounded">
                    Paid
                  </span>
                )}
              </li>
            ))}
          </ul>
        ) : (
          <p className="text-gray-400">No published lessons available.</p>
        )}
      </div>
    );
  }

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold text-indigo-400 mb-6">
        Published Programs
      </h1>
      {programs.length === 0 ? (
        <p className="text-gray-400">No published programs found.</p>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {programs.map((p) => (
            <div
              key={p.id}
              className="bg-gray-800 p-4 rounded border border-gray-700 hover:border-indigo-400 transition"
            >
              <h2 className="text-xl font-semibold text-indigo-400">
                {p.title}
              </h2>
              <p className="text-gray-400 text-sm mb-3">{p.description}</p>
              <button
                onClick={() => openProgram(p.id)}
                className="bg-indigo-500 hover:bg-indigo-600 px-3 py-1 rounded text-sm"
              >
                View Lessons
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
