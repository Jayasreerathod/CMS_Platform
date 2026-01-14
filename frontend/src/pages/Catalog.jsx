import { useEffect, useState } from "react";
import api from "../api";

export default function Catalog() {
  const [programs, setPrograms] = useState([]);
  const [selectedProgram, setSelectedProgram] = useState(null);
  const [selectedLesson, setSelectedLesson] = useState(null);
  const [selectedLanguage, setSelectedLanguage] = useState("en");
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

  function openLesson(lesson) {
    setSelectedLesson(lesson);
    setSelectedLanguage(lesson.content_language_primary || "en");
  }

  function closeLesson() {
    setSelectedLesson(null);
  }

  function nextLesson() {
    if (!selectedProgram || !selectedLesson) return;
    const idx = selectedProgram.lessons.findIndex((l) => l.id === selectedLesson.id);
    if (idx < selectedProgram.lessons.length - 1) {
      openLesson(selectedProgram.lessons[idx + 1]);
    }
  }

  function prevLesson() {
    if (!selectedProgram || !selectedLesson) return;
    const idx = selectedProgram.lessons.findIndex((l) => l.id === selectedLesson.id);
    if (idx > 0) {
      openLesson(selectedProgram.lessons[idx - 1]);
    }
  }

  if (loading)
    return (
      <div className="p-8 text-gray-300 text-center">
        Loading program details...
      </div>
    );

  // ------------------------------------------------------------
  // PROGRAM DETAIL VIEW
  // ------------------------------------------------------------
  if (selectedProgram) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-slate-900 to-slate-950 text-white p-8">
        <button
          onClick={() => setSelectedProgram(null)}
          className="bg-slate-700 hover:bg-slate-600 text-white px-4 py-2 rounded mb-6 transition"
        >
          ← Back to Catalog
        </button>

        {/* Program Header */}
        <div className="flex flex-col md:flex-row gap-8 mb-10 animate-fadeIn">
          {selectedProgram.poster_assets_by_language?.en?.landscape && (
            <img
              src={selectedProgram.poster_assets_by_language.en.landscape}
              alt={selectedProgram.title}
              className="w-full md:w-1/3 rounded-lg shadow-2xl border border-slate-700 object-cover"
            />
          )}
          <div>
            <h1 className="text-4xl font-bold text-indigo-400 mb-2 drop-shadow-[0_2px_8px_rgba(99,102,241,0.4)]">
              {selectedProgram.title}
            </h1>
            <p className="text-gray-400 text-lg mb-4">
              {selectedProgram.description || "No description available."}
            </p>
            <div className="flex flex-wrap gap-3">
              <span className="bg-indigo-800 text-sm px-3 py-1 rounded">
                Primary Lang:{" "}
                {selectedProgram.language_primary?.toUpperCase() || "EN"}
              </span>
              <span className="bg-slate-700 text-sm px-3 py-1 rounded">
                {selectedProgram.status?.toUpperCase()}
              </span>
            </div>
          </div>
        </div>

        {/* Published Lessons */}
        <h2 className="text-2xl font-semibold text-indigo-300 mb-4">
          Published Lessons
        </h2>

        {selectedProgram.lessons?.length ? (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {selectedProgram.lessons.map((lesson) => (
              <div
                key={lesson.id}
                onClick={() => openLesson(lesson)}
                className="group relative bg-gradient-to-b from-slate-800 to-slate-900 border border-slate-700/60 rounded-xl overflow-hidden shadow-lg hover:shadow-indigo-600/40 transform hover:-translate-y-2 transition-all duration-300 cursor-pointer hover:border-indigo-600/60 hover-glow"
              >
                <div className="relative">
                  <img
                    src={
                      lesson.thumbnail_assets_by_language?.en?.landscape ||
                      lesson.thumbnail_assets_by_language?.en?.portrait ||
                      "https://via.placeholder.com/400x225?text=No+Thumbnail"
                    }
                    alt={lesson.title}
                    className="w-full h-44 object-cover group-hover:brightness-110 transition duration-300"
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 flex items-center justify-center transition duration-300">
                    <button className="bg-indigo-600 hover:bg-indigo-500 px-4 py-2 rounded-lg text-white font-semibold text-sm shadow-lg flex items-center gap-1">
                      ▶ <span>View</span>
                    </button>
                  </div>
                </div>

                <div className="p-4 flex flex-col justify-between">
                  <h3 className="text-lg font-semibold text-indigo-300 mb-1 group-hover:text-indigo-400 transition">
                    #{lesson.lesson_number} — {lesson.title}
                  </h3>
                  <div className="flex justify-between items-center text-gray-400 text-sm">
                    <p className="capitalize">
                      {lesson.content_type || "video"} •{" "}
                      {lesson.content_language_primary?.toUpperCase() || "EN"}
                    </p>
                    {lesson.duration_ms && (
                      <p className="text-xs text-gray-500">
                        ⏱ {(lesson.duration_ms / 60000).toFixed(1)} min
                      </p>
                    )}
                  </div>
                </div>

                <div className="absolute inset-0 rounded-xl border-2 border-transparent group-hover:border-indigo-500/40 transition-all duration-300 pointer-events-none" />
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500 italic">
            No published lessons available.
          </p>
        )}

        {/* Lesson Modal */}
        {selectedLesson && (
          <div className="fixed inset-0 bg-black/90 backdrop-blur-sm flex items-center justify-center z-50 p-6 animate-fadeIn">
            <div className="bg-slate-900/95 rounded-2xl shadow-2xl p-6 w-full max-w-5xl relative border border-indigo-700/40 overflow-y-auto max-h-[90vh]">
              <button
                onClick={closeLesson}
                className="absolute top-4 right-5 text-gray-400 hover:text-white text-2xl"
              >
                ✕
              </button>

              <h3 className="text-2xl font-bold text-indigo-300 mb-3 border-b border-slate-700 pb-2">
                {selectedLesson.title}
              </h3>

              {selectedLesson.content_languages_available?.length > 1 && (
                <div className="mb-4 flex gap-3">
                  {selectedLesson.content_languages_available.map((lang) => (
                    <button
                      key={lang}
                      onClick={() => setSelectedLanguage(lang)}
                      className={`px-3 py-1 rounded-lg text-sm font-semibold transition ${
                        lang === selectedLanguage
                          ? "bg-indigo-600 text-white"
                          : "bg-slate-700 hover:bg-slate-600 text-gray-300"
                      }`}
                    >
                      {lang.toUpperCase()}
                    </button>
                  ))}
                </div>
              )}

              {selectedLesson.content_type === "article" ? (
                <iframe
                  src={
                    selectedLesson.content_urls_by_language?.[selectedLanguage] ||
                    selectedLesson.content_urls_by_language?.[
                      selectedLesson.content_language_primary
                    ]
                  }
                  title="Lesson Article"
                  className="w-full h-[70vh] rounded-lg border border-slate-700"
                ></iframe>
              ) : (
                <video
                  key={selectedLanguage}
                  src={
                    selectedLesson.content_urls_by_language?.[selectedLanguage] ||
                    selectedLesson.content_urls_by_language?.[
                      selectedLesson.content_language_primary
                    ]
                  }
                  controls
                  className="w-full rounded-lg max-h-[75vh] object-contain border border-slate-700 shadow-md"
                />
              )}

              {/* Navigation */}
              <div className="flex justify-between mt-4">
                <button
                  onClick={prevLesson}
                  className="bg-slate-700 hover:bg-indigo-700 text-white px-3 py-1 rounded shadow-md"
                >
                  ← Prev
                </button>
                <button
                  onClick={nextLesson}
                  className="bg-slate-700 hover:bg-indigo-700 text-white px-3 py-1 rounded shadow-md"
                >
                  Next →
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    );
  }

  // ------------------------------------------------------------
  // CATALOG LIST VIEW (All programs)
  // ------------------------------------------------------------
  return (
    <div className="min-h-screen bg-slate-900 text-white p-8">
      <h1 className="text-3xl font-bold text-indigo-400 mb-6">
        Published Programs
      </h1>

      {programs.length === 0 ? (
        <p className="text-gray-400">No published programs found.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {programs.map((p) => (
            <div
              key={p.id}
              onClick={() => openProgram(p.id)}
              className="group bg-gradient-to-b from-slate-800 to-slate-900 border border-slate-700/60 rounded-xl overflow-hidden shadow-lg hover:shadow-indigo-600/40 transform hover:-translate-y-2 transition-all duration-300 cursor-pointer hover:border-indigo-600/60 hover-glow"
            >
              <img
                src={
                  p.poster_assets_by_language?.en?.portrait ||
                  p.poster_assets_by_language?.en?.landscape ||
                  "https://via.placeholder.com/300x400?text=No+Poster"
                }
                alt={p.title}
                className="w-full h-52 object-cover group-hover:brightness-110 transition duration-300"
              />
              <div className="p-4">
                <h2 className="text-xl font-semibold text-indigo-400 group-hover:text-indigo-300 transition">
                  {p.title}
                </h2>
                <p className="text-gray-400 text-sm mb-3 line-clamp-2">
                  {p.description || "No description"}
                </p>
                <button className="bg-indigo-500 hover:bg-indigo-600 px-3 py-1 rounded text-sm shadow-md">
                  View Lessons
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
