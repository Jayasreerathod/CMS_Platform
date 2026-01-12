import { useState } from "react";

export default function AssetUploader({ onUpload }) {
  const [file, setFile] = useState(null);

  const handleUpload = () => {
    if (file) onUpload(file);
  };

  return (
    <div className="bg-gray-800 border border-gray-700 rounded-lg p-6 mt-4">
      <h2 className="text-lg font-semibold text-blue-300 mb-2">Upload Lesson Asset</h2>
      <input
        type="file"
        className="text-gray-300 mb-3"
        onChange={(e) => setFile(e.target.files[0])}
      />
      <button
        onClick={handleUpload}
        className="bg-blue-600 hover:bg-blue-700 px-4 py-2 rounded text-white"
      >
        Upload
      </button>
    </div>
  );
}
