import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import { AuthProvider, useAuth } from "../context/AuthContext";
import Sidebar from "../components/Sidebar";

import Dashboard from "./Dashboard";
import Assets from "./Assets";
import Vulnerabilities from "./Vulnerabilities";
import PHIRisks from "./PHIRisks";
import Compliance from "./Compliance";
import Anomalies from "./Anomalies";
import Login from "./Login";

function ProtectedRoute({ children }) {
  const { token, loading } = useAuth();
  
  if (loading) {
    return <div style={{ padding: "20px" }}>Loading...</div>;
  }
  
  if (!token) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
}

function AppLayout({ children }) {
  return (
    <div style={{ display: "flex" }}>
      <Sidebar />
      <div style={{ flex: 1, background: "#f8fafc", minHeight: "100vh" }}>
        {children}
      </div>
    </div>
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />
      <Route
        path="/"
        element={
          <ProtectedRoute>
            <AppLayout>
              <Dashboard />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/assets"
        element={
          <ProtectedRoute>
            <AppLayout>
              <Assets />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/vulnerabilities"
        element={
          <ProtectedRoute>
            <AppLayout>
              <Vulnerabilities />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/phi-risks"
        element={
          <ProtectedRoute>
            <AppLayout>
              <PHIRisks />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/compliance"
        element={
          <ProtectedRoute>
            <AppLayout>
              <Compliance />
            </AppLayout>
          </ProtectedRoute>
        }
      />
      <Route
        path="/anomalies"
        element={
          <ProtectedRoute>
            <AppLayout>
              <Anomalies />
            </AppLayout>
          </ProtectedRoute>
        }
      />
    </Routes>
  );
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <AppRoutes />
      </BrowserRouter>
    </AuthProvider>
  );
}

export default App;
