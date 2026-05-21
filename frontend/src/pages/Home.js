import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useScan } from "../context/ScanContext";
import "./Home.css";

function Home() {
  const [url, setUrl] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const { setScanData, setTrustData, setScannedUrl } = useScan();
  const navigate = useNavigate();

  const handleScan = async () => {
    if (!url.trim()) { setError("Please enter a website URL."); return; }
    if (!url.startsWith("http")) { setError("URL must start with http:// or https://"); return; }

    setError("");
    setLoading(true);

    try {
      // Step 1 — Scan
      const scanRes = await fetch("http://localhost:5000/scan", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url })
      });
      const scanResult = await scanRes.json();
      if (scanResult.error) throw new Error(scanResult.error);

      // Step 2 — Trust Score
      const trustRes = await fetch("http://localhost:5000/trust-score", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url, scan_data: scanResult })
      });
      const trustResult = await trustRes.json();
      if (trustResult.error) throw new Error(trustResult.error);

      setScanData(scanResult);
      setTrustData(trustResult);
      setScannedUrl(url);
      navigate("/results");

    } catch (err) {
      setError("Scan failed: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <div className="home-hero">
        <span className="hero-badge badge badge-blue">Free Privacy Scanner</span>
        <h1 className="hero-title">Is this website <span className="hero-highlight">safe for your data?</span></h1>
        <p className="hero-subtitle">
          Paste any website URL below. We'll scan it in seconds and tell you exactly
          what's happening to your personal data — in plain English.
        </p>

        <div className="scan-box">
          <input
            className="scan-input"
            type="text"
            placeholder="https://example.com"
            value={url}
            onChange={e => setUrl(e.target.value)}
            onKeyDown={e => e.key === "Enter" && handleScan()}
            disabled={loading}
          />
          <button className="btn-primary" onClick={handleScan} disabled={loading}>
            {loading ? "Scanning..." : "Scan Now"}
          </button>
        </div>

        {loading && (
          <div className="loading-box">
            <div className="spinner" />
            <p className="loading-text">Scanning the website — this takes 20-40 seconds...</p>
            <p className="loading-sub">We're checking trackers, cookie popups, and the privacy policy.</p>
          </div>
        )}

        {error && <div className="error-box">{error}</div>}
      </div>

      <div className="how-it-works">
        <h2 className="section-title">How it works</h2>
        <div className="steps-grid">
          <div className="step-card">
            <span className="step-icon">🔍</span>
            <h3>1. We Scan</h3>
            <p>Our tool opens the website just like you would and watches what happens in the background.</p>
          </div>
          <div className="step-card">
            <span className="step-icon">🕵️</span>
            <h3>2. We Detect</h3>
            <p>We find all the companies tracking you, check if the cookie popup is manipulative, and read their privacy policy.</p>
          </div>
          <div className="step-card">
            <span className="step-icon">📊</span>
            <h3>3. We Explain</h3>
            <p>You get a simple Trust Score and plain English explanations — no technical jargon.</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Home;