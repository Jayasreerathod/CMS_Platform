import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import api from "../api";

export default function Lessons() {
  const { programId } = useParams();
  const [lessons, setLessons] = useState([]);
  const [title, setTitle] = useState("");
  const [lessonNumber, setLessonNumber] = useState(1);
  const [status, setStatus] = useState("");
  const [publishAt, setPublishAt] = useState("");
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  async function fetchLessons() {
    try {
      const res = await api.get(`/cms/programs/${programId}/lessons`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      setLessons(res.data);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    fetchLessons();
  }, []);

  async function handleCreate() {
    try {
      await api.post(
        "/cms/lessons",
        {
          title,
          lesson_number: lessonNumber,
          term_id: "term_id_here", // Replace with dynamic selection later
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setTitle("");
      fetchLessons();
    } catch (err) {
      console.error(err);
      alert("Failed to create lesson");
    }
  }

  async function updateStatus(id, newStatus) {
    try {
      const data =
        newStatus === "scheduled"
          ? { status: newStatus, publish_at: publishAt }
          : { status: newStatus };
      await api.put(`/cms/lessons/${id}/status`, data, {
        headers: { Authorization: `Bearer ${token}` },
      });
      fetchLessons();
    } catch (err) {
      alert("Failed to update lesson status");
    }
  }

  return (
    <div className="p-8 text-white">
      <h1 className="text-2xl font-bold text-indigo-400 mb-6">Lessons</h1>

      {role !== "viewer" && (
        <div className="flex gap-2 mb-6">
          <input
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            placeholder="Lesson title"
            className="p-2 bg-gray-700 border border-gray-600 rounded"
          />
          <input
            type="number"
            value={lessonNumber}
            onChange={(e) => setLessonNumber(e.target.value)}
            className="p-2 bg-gray-700 border border-gray-600 rounded w-20"
          />
          <button
            onClick={handleCreate}
            className="bg-indigo-500 hover:bg-indigo-600 px-3 py-1 rounded"
          >
            + Add Lesson
          </button>
        </div>
      )}

      {lessons.length === 0 ? (
        <p className="text-gray-400">No lessons found.</p>
      ) : (
        <table className="w-full border-collapse text-left">
          <thead>
            <tr className="border-b border-gray-600">
              <th className="p-2">Lesson #</th>
              <th className="p-2">Title</th>
              <th className="p-2">Status</th>
              <th className="p-2">Actions</th>
            </tr>
          </thead>
          <tbody>
            {lessons.map((l) => (
              <tr key={l.id} className="border-b border-gray-700">
                <td className="p-2">{l.lesson_number}</td>
                <td className="p-2">{l.title}</td>
                <td className="p-2">{l.status}</td>
                <td className="p-2">
                  {role !== "viewer" && (
                    <div className="flex gap-2">
                      <button
                        onClick={() => updateStatus(l.id, "published")}
                        className="bg-green-600 hover:bg-green-700 px-2 rounded text-sm"
                      >
                        Publish
                      </button>
                      <button
                        onClick={() => updateStatus(l.id, "scheduled")}
                        className="bg-yellow-500 hover:bg-yellow-600 px-2 rounded text-sm text-black"
                      >
                        Schedule
                      </button>
                      <button
                        onClick={() => updateStatus(l.id, "archived")}
                        className="bg-gray-500 hover:bg-gray-600 px-2 rounded text-sm"
                      >
                        Archive
                      </button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
}
