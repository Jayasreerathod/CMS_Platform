import { useState } from "react";
import axios from "axios";

export default function ProgramForm({ onCreated }) {
  const [isOpen, setIsOpen] = useState(false);
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [language, setLanguage] = useState("English");
  const [status, setStatus] = useState("draft");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const token = localStorage.getItem("token");
    try {
      await axios.post(
        "http://127.0.0.1:8000/cms/programs",
        {
          title,
          description,
          language_primary: language,
          status,
        },
        { headers: { Authorization: `Bearer ${token}` } }
      );

      setIsOpen(false);
      setTitle("");
      setDescription("");
      setLanguage("English");
      setStatus("draft");
      onCreated(); // refresh program list
    } catch (err) {
      console.error(err);
      setError("Failed to create program. Check your credentials or data.");
    }
  };

  const role = localStorage.getItem("role");

  if (role !== "editor" && role !== "admin") return null;

  return (
    <>
      {/* Button to open modal */}
      <div className="text-right mb-4">
        <button
          onClick={() => setIsOpen(true)}
          className="bg-indigo-600 hover:bg-indigo-700 text-white px-4 py-2 rounded shadow"
        >
          ➕ New Program
        </button>
      </div>

      {/* Modal */}
      {isOpen && (
        <div className="fixed inset-0 flex items-center justify-center bg-black bg-opacity-60 z-50">
          <div className="bg-gray-900 text-white p-6 rounded-lg shadow-lg w-96">
            <h2 className="text-xl font-semibold mb-4 text-indigo-400">
              Create New Program
            </h2>
            {error && <p className="text-red-400 text-sm mb-2">{error}</p>}

            <form onSubmit={handleSubmit}>
              <label className="block mb-2 text-sm text-gray-300">Title</label>
              <input
                type="text"
                className="w-full mb-4 p-2 rounded bg-gray-800 border border-gray-700"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                required
              />

              <label className="block mb-2 text-sm text-gray-300">Description</label>
              <textarea
                className="w-full mb-4 p-2 rounded bg-gray-800 border border-gray-700"
                rows="3"
                value={description}
                onChange={(e) => setDescription(e.target.value)}
                required
              />

              <label className="block mb-2 text-sm text-gray-300">Language</label>
              <select
                className="w-full mb-4 p-2 rounded bg-gray-800 border border-gray-700"
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
              >
                <option>English</option>
                <option>Hindi</option>
                <option>Spanish</option>
                <option>French</option>
              </select>

              <label className="block mb-2 text-sm text-gray-300">Status</label>
              <select
                className="w-full mb-4 p-2 rounded bg-gray-800 border border-gray-700"
                value={status}
                onChange={(e) => setStatus(e.target.value)}
              >
                <option value="draft">Draft</option>
                <option value="published">Published</option>
              </select>

              <div className="flex justify-end space-x-2">
                <button
                  type="button"
                  onClick={() => setIsOpen(false)}
                  className="bg-gray-700 hover:bg-gray-600 text-white px-3 py-2 rounded"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  className="bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-2 rounded"
                >
                  Save
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </>
  );
}
