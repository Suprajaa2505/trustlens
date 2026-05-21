import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useScan } from "../context/ScanContext";
import ScanEngine from "../components/ScanEngine";
import ManipulationDetector from "../components/ManipulationDetector";
import TrustScore from "../components/TrustScore";
import "./Results.css";

function Results() {
  const { scanData, trustData, scannedUrl } = useScan();
  const navigate = useNavigate();

  useEffect(() => {
    if (!scanData || !trustData) navigate("/");
  }, [scanData, trustData, navigate]);

  if (!scanData || !trustData) return null;

  return (
    <div className="results-page">
      <div className="results-header">
        <p className="results-scanning-label">Results for</p>
        <h2 className="results-url">{scannedUrl}</h2>
        <button className="btn-primary" onClick={() => navigate("/")}>
          Scan Another Site
        </button>
      </div>

      <div className="results-container">
        <TrustScore data={trustData} />
        <ScanEngine data={scanData} />
        <ManipulationDetector data={scanData} />
      </div>
    </div>
  );
}

export default Results;