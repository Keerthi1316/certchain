import { Routes, Route, Navigate, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import Nav from './components/Nav.jsx';
import Stars from './components/Stars.jsx';
import WalletModal from './components/WalletModal.jsx';
import { Toasts } from './components/ui.jsx';
import { ErrorBoundary } from './components/ErrorBoundary.jsx';
import Landing from './pages/Landing.jsx';
import Verify from './pages/Verify.jsx';
import Login from './pages/Login.jsx';
import AdminLayout from './pages/AdminLayout.jsx';
import Dashboard from './pages/Dashboard.jsx';
import Issue from './pages/Issue.jsx';
import Certificates from './pages/Certificates.jsx';

export default function App() {
  const { pathname } = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return (
    <ErrorBoundary>
      <div className="bg" /><Stars /><Nav />
      <Routes>
        <Route path="/" element={<Landing />} />
        <Route path="/verify" element={<Verify />} />
        <Route path="/verify/:id" element={<Verify />} />
        <Route path="/login" element={<Login />} />
        <Route element={<AdminLayout />}>
          <Route path="/admin" element={<Dashboard />} />
          <Route path="/admin/issue" element={<Issue />} />
          <Route path="/certificates" element={<Certificates />} />
        </Route>
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
      <WalletModal /><Toasts />
    </ErrorBoundary>
  );
}
