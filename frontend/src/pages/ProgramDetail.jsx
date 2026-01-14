import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import api from "../api";

export default function ProgramDetail() {
  const { programId } = useParams();
  console.log("Program ID:", programId);
  const [program, setProgram] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [showModal, setShowModal] = useState(false);
  const [newLessonTitle, setNewLessonTitle] = useState("");
  const [publishMinutes, setPublishMinutes] = useState(2);
  const token = localStorage.getItem("token");

  async function fetchProgram() {
    try {
      const res = await api.get(`/cms/programs/${programId}`);
      setProgram(res.data.program);
      setLessons(res.data.lessons);
    } catch (err) {
      console.error(err);
    }
  }

  useEffect(() => {
    fetchProgram();
  }, [programId]);

  async function handlePublish(id) {
    try {
      await api.post(`/cms/lessons/${id}/publish`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Lesson published successfully");
      fetchProgram();
    } catch {
      alert("Failed to publish lesson.");
    }
  }

  async function handleSchedule(id) {
    const minutes = prompt("Publish after (minutes):", "2");
    if (!minutes) return;
    try {
      await api.post(
        `/cms/lessons/${id}/schedule`,
        { publish_in_minutes: parseInt(minutes) },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Lesson scheduled successfully");
      fetchProgram();
    } catch {
      alert("Failed to schedule publish.");
    }
  }

  async function handleArchive(id) {
    if (!window.confirm("Are you sure to archive this lesson?")) return;
    try {
      await api.post(`/cms/lessons/${id}/archive`, {}, {
        headers: { Authorization: `Bearer ${token}` },
      });
      alert("Lesson archived successfully");
      fetchProgram();
    } catch {
      alert("Failed to archive lesson.");
    }
  }

  async function addLesson() {
    try {
      await api.post(
        `/cms/programs/${programId}/lessons`,
        { title: newLessonTitle || "New Lesson" },
        { headers: { Authorization: `Bearer ${token}` } }
      );
      setNewLessonTitle("");
      setShowModal(false);
      fetchProgram();
    } catch {
      alert("Failed to add lesson.");
    }
  }

  if (!program) return <p className="text-white p-8">Loading...</p>;

  return (
    <div className="p-8 text-white">
      <h1 className="text-3xl font-bold text-indigo-400 mb-4">
        ✏️ {program.title}
      </h1>
      <p className="mb-6 text-gray-300">{program.description}</p>

      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-indigo-300">Lessons</h2>
        <button
          onClick={() => setShowModal(true)}
          className="bg-indigo-600 hover:bg-indigo-700 px-3 py-1 rounded text-white"
        >
          + Add Lesson
        </button>
      </div>

      {lessons.length === 0 ? (
        <p className="text-gray-400">No lessons yet.</p>
      ) : (
        <div className="space-y-4">
          {lessons.map((lesson) => (
            <div
              key={lesson.id}
              className="border border-indigo-800 rounded-lg p-4 bg-gray-900/50 shadow-md"
            >
              <h3 className="text-lg font-semibold text-indigo-300">
                {lesson.title}
              </h3>
              <p className="text-sm text-gray-400">
                Type: {lesson.content_type || "video"} | Lang:{" "}
                {lesson.content_language_primary}
              </p>
              <div className="mt-3 flex gap-2 items-center">
                <span
                  className={`px-2 py-1 rounded text-xs ${
                    lesson.status === "published"
                      ? "bg-green-600"
                      : lesson.status === "scheduled"
                      ? "bg-yellow-600"
                      : lesson.status === "archived"
                      ? "bg-gray-600"
                      : "bg-indigo-700"
                  }`}
                >
                  {lesson.status.toUpperCase()}
                </span>

                {lesson.status !== "published" && (
                  <>
                    <button
                      onClick={() => handlePublish(lesson.id)}
                      className="bg-green-600 hover:bg-green-700 text-sm px-2 py-1 rounded"
                    >
                      Publish
                    </button>
                    <button
                      onClick={() => handleSchedule(lesson.id)}
                      className="bg-yellow-500 hover:bg-yellow-600 text-sm px-2 py-1 rounded text-black"
                    >
                      Schedule
                    </button>
                  </>
                )}

                {lesson.status !== "archived" && (
                  <button
                    onClick={() => handleArchive(lesson.id)}
                    className="bg-gray-600 hover:bg-gray-700 text-sm px-2 py-1 rounded"
                  >
                    Archive
                  </button>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* Add Lesson Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/70 flex items-center justify-center z-50">
          <div className="bg-gray-800 p-6 rounded-lg shadow-lg w-96">
            <h3 className="text-xl font-semibold text-indigo-400 mb-4">
              Add New Lesson
            </h3>
            <input
              value={newLessonTitle}
              onChange={(e) => setNewLessonTitle(e.target.value)}
              placeholder="Lesson title"
              className="w-full p-2 mb-4 bg-gray-700 rounded border border-gray-600"
            />
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowModal(false)}
                className="bg-gray-600 hover:bg-gray-700 px-3 py-1 rounded"
              >
                Cancel
              </button>
              <button
                onClick={addLesson}
                className="bg-indigo-600 hover:bg-indigo-700 px-3 py-1 rounded"
              >
                Add
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
