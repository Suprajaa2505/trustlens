import { useNavigate } from "react-router-dom";
import "./Navbar.css";

function Navbar() {
  const navigate = useNavigate();
  return (
    <nav className="navbar">
      <div className="nav-inner">
        <div className="nav-brand" onClick={() => navigate("/")}>
          <span className="nav-logo">🔍</span>
          <span className="nav-title">TrustLens</span>
          <span className="nav-tagline">Privacy Scanner</span>
        </div>
        <div className="nav-links">
          <button className="nav-btn" onClick={() => navigate("/")}>Home</button>
          <button className="nav-btn nav-btn-primary" onClick={() => navigate("/")}>Scan a Site</button>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;