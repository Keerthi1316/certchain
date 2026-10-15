import { NavLink, Outlet, Navigate, useNavigate } from 'react-router-dom';
import { useApp } from '../state.jsx';

export default function AdminLayout() {
  const { token, setToken, toast } = useApp();
  const nav = useNavigate();
  if (!token) return <Navigate to="/login" replace />;
  const link = ({ isActive }) => 'sl' + (isActive ? ' on' : '');
  return (
    <div className="shell">
      <aside className="glass side" aria-label="Admin navigation">
        <div className="eyebrow side-t">Admin</div>
        <NavLink end to="/admin" className={link}>▦ <span>Dashboard</span></NavLink>
        <NavLink to="/admin/issue" className={link}>✦ <span>Issue</span></NavLink>
        <NavLink to="/certificates" className={link}>❖ <span>Certificates</span></NavLink>
        <button className="sl" onClick={() => { setToken(null); toast('Signed out'); nav('/'); }}>⏻ <span>Sign out</span></button>
      </aside>
      <div className="amain av"><Outlet /></div>
    </div>
  );
}
