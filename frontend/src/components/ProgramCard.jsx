import axios from "axios";
import { useNavigate } from "react-router-dom";

export default function ProgramCard({ program, onUpdated }) {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  const role = localStorage.getItem("role");

  const handleDelete = async () => {
    if (!window.confirm("Are you sure you want to delete this program?")) return;
    try {
      await axios.delete(`http://127.0.0.1:8000/cms/programs/${program.id}`, {
        headers: { Authorization: `Bearer ${token}` },
      });
      onUpdated();
    } catch (err) {
      console.error(err);
      alert("Failed to delete program.");
    }
  };

  const handlePublish = async () => {
    try {
      await axios.post(
        `http://127.0.0.1:8000/cms/programs/${program.id}/publish`,
        {},
        { headers: { Authorization: `Bearer ${token}` } }
      );
      alert("Program published!");
      onUpdated();
    } catch (err) {
      console.error(err);
      alert("Publish failed.");
    }
  };

  return (
    <div className="bg-gray-900 p-5 rounded-lg border border-gray-700 shadow-md hover:border-indigo-500 transition flex flex-col justify-between">
      <div>
        <h3 className="text-xl font-semibold text-indigo-400 mb-2">
          {program.title}
        </h3>
        <p className="text-gray-400 text-sm mb-4">
          {program.description || "No description available"}
        </p>
      </div>

      <div className="flex justify-between items-center mt-auto">
        {/* Only logged-in users can manage lessons */}
        {token ? (
          <button
            onClick={() => navigate(`/programs/${program.id}`)}
            className="text-sm bg-indigo-600 hover:bg-indigo-700 text-white px-3 py-1 rounded"
          >
            Manage Lessons
          </button>
        ) : (
          <span className="text-gray-600 text-sm">Login to manage</span>
        )}

        {/* Only admins can publish/delete */}
        {token && role === "admin" && (
          <div className="flex gap-2">
            <button
              onClick={handlePublish}
              className="text-sm bg-green-600 hover:bg-green-700 text-white px-3 py-1 rounded"
            >
              Publish
            </button>
            <button
              onClick={handleDelete}
              className="text-sm bg-red-600 hover:bg-red-700 text-white px-3 py-1 rounded"
            >
              Delete
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
