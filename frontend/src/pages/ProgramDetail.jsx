import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";

export default function ProgramDetail() {
  const { id } = useParams();
  const [program, setProgram] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [newLesson, setNewLesson] = useState("");
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  async function fetchProgram() {
    try {
      const res = await api.get(`/cms/programs/${id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setProgram(res.data.program);
      setLessons(res.data.lessons || []);
    } catch (err) {
      console.error("Error fetching program details:", err);
      alert("Failed to load program details.");
    }
  }

  useEffect(() => {
    fetchProgram();
  }, [id]);

  async function addLesson() {
    if (!newLesson.trim()) return alert("Lesson title required");
    try {
      await api.post(
        `/cms/programs/${id}/lessons`,
        { title: newLesson },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setNewLesson("");
      fetchProgram();
    } catch (err) {
      console.error(err);
      alert("Failed to add lesson");
    }
  }

  async function deleteLesson(lessonId) {
    if (!window.confirm("Delete this lesson?")) return;
    try {
      await api.delete(`/cms/lessons/${lessonId}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchProgram();
    } catch (err) {
      console.error(err);
      alert("Failed to delete lesson");
    }
  }

  if (!program) return <p className="text-gray-400 p-8">Loading...</p>;

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold text-indigo-400 mb-4">
        {program.title}
      </h1>
      <p className="text-gray-400 mb-4">{program.description}</p>

      {(role === "admin" || role === "editor") && (
        <div className="flex gap-3 mb-6">
          <input
            type="text"
            placeholder="New lesson title"
            value={newLesson}
            onChange={(e) => setNewLesson(e.target.value)}
            className="p-2 bg-gray-700 rounded border border-gray-600 w-64"
          />
          <button
            onClick={addLesson}
            className="bg-indigo-500 hover:bg-indigo-600 px-4 rounded"
          >
            + Add Lesson
          </button>
        </div>
      )}

      {lessons.length === 0 ? (
        <p className="text-gray-400">No lessons found for this program.</p>
      ) : (
        <ul className="space-y-3">
          {lessons.map((l, i) => (
            <li
              key={l.id}
              className="bg-gray-800 p-3 rounded flex justify-between items-center border border-gray-700"
            >
              <div>
                <span className="font-semibold text-indigo-400">
                  Lesson {i + 1}:
                </span>{" "}
                {l.title}
              </div>

              {(role === "admin" || role === "editor") && (
                <button
                  onClick={() => deleteLesson(l.id)}
                  className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded text-sm"
                >
                  Delete
                </button>
              )}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
