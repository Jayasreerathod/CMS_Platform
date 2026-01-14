import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Navbar from "./components/Navbar";
import Programs from "./pages/Programs";
import ProgramDetail from "./pages/ProgramDetail";
import LessonEditor from "./pages/LessonEditor";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";
import Catalog from "./pages/Catalog";
import Lessons from "./pages/Lessons";


function PrivateRoute({ children }) {
  const token = localStorage.getItem("token");
  if (!token) return <Navigate to="/login" replace />;
  return children;
}

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        {/* Public Catalog */}
        <Route path="/" element={<Navigate to="/catalog" />} />
        <Route path="/catalog" element={<Catalog />} />

        {/* CMS (requires login) */}
        <Route
          path="/programs"
          element={
            <PrivateRoute>
              <Programs />
            </PrivateRoute>
          }
        />
        <Route
          path="/programs/:programId"
          element={
            <PrivateRoute>
              <ProgramDetail />
            </PrivateRoute>
          }
        />
        <Route
          path="/lessons/:id"
          element={
            <PrivateRoute>
              <LessonEditor />
            </PrivateRoute>
          }
        />
        <Route path="/catalog" element={<Catalog />} />
        <Route path="/programs/:programId" element={<ProgramDetail />} />
        <Route path="/login" element={<Login />} />
        <Route path="*" element={<NotFound />} />
      </Routes>
    </BrowserRouter>
  );
}
