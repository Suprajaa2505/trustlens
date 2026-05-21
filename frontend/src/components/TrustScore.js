import "./TrustScore.css";

function TrustScore({ data }) {
  const { trust_score, trust_level, verdict, advice, reasons } = data;

  const colorClass =
    trust_level === "HIGH" ? "score-green" :
    trust_level === "MEDIUM" ? "score-yellow" : "score-red";

  const adviceClass =
    trust_level === "HIGH" ? "badge-green" :
    trust_level === "MEDIUM" ? "badge-yellow" : "badge-red";

  const emoji =
    trust_level === "HIGH" ? "✅" :
    trust_level === "MEDIUM" ? "⚠️" : "🚨";

  return (
    <div className="card animate-fade">
      <div className="pillar-header">
        <span className="pillar-number">3</span>
        <div>
          <h2 className="pillar-title">Trust Score</h2>
          <p className="pillar-desc">Our overall verdict on this site's privacy</p>
        </div>
      </div>

      <div className="score-center">
        <div className={`score-circle ${colorClass}`}>
          <span className="score-number">{trust_score}</span>
          <span className="score-out">/ 100</span>
        </div>
        <span className={`badge ${adviceClass} advice-badge`}>{emoji} {advice}</span>
        <p className="verdict-text">{verdict}</p>
      </div>

      {reasons.length > 0 && (
        <div className="reasons-box">
          <p className="reasons-title">Why this score?</p>
          <ul className="reasons-list">
            {reasons.map((r, i) => (
              <li key={i} className="reason-item">
                <span className="reason-dot">•</span>
                <span>{r}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default TrustScore;