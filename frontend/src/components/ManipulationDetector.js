import "./ManipulationDetector.css";

function ManipulationDetector({ data }) {
  const {
    dark_pattern_score, dark_pattern_level,
    dark_pattern_summary, policy_verdict,
    policy_summary
  } = data;

  const dpClass =
    dark_pattern_level === "Aggressive Dark Pattern" ? "badge-red" :
    dark_pattern_level === "Moderate Manipulation" ? "badge-yellow" :
    dark_pattern_level === "Mild UX Bias" ? "badge-yellow" : "badge-green";

  const policyClass =
    policy_verdict === "Misleading" ? "badge-red" :
    policy_verdict === "Partially Transparent" ? "badge-yellow" : "badge-green";

  const barColor =
    dark_pattern_score >= 70 ? "#ef4444" :
    dark_pattern_score >= 30 ? "#f59e0b" : "#22c55e";

  return (
    <div className="card animate-fade">
      <div className="pillar-header">
        <span className="pillar-number">2</span>
        <div>
          <h2 className="pillar-title">Manipulation Detector</h2>
          <p className="pillar-desc">Is this site being honest with you?</p>
        </div>
      </div>

      {/* Dark Patterns */}
      <div className="detect-section">
        <div className="detect-header">
          <span className="detect-icon">🎭</span>
          <div>
            <p className="detect-title">Cookie Popup Analysis</p>
            <span className={`badge ${dpClass}`}>
          {dark_pattern_score === 0 ? "No Popup Detected" : dark_pattern_level}
        </span>
          </div>
        </div>

        <div className="score-bar-wrap">
          <div className="score-bar-track">
            <div
              className="score-bar-fill"
              style={{ width: `${dark_pattern_score}%`, background: barColor }}
            />
          </div>
          <span className="score-bar-label">{dark_pattern_score}/100 manipulation score</span>
        </div>

        <p className="detect-summary">{dark_pattern_summary}</p>
      </div>

      <div className="detect-divider" />

      {/* Policy Truth */}
      <div className="detect-section">
        <div className="detect-header">
          <span className="detect-icon">📄</span>
          <div>
            <p className="detect-title">Privacy Policy vs Reality</p>
            <span className={`badge ${policyClass}`}>{policy_verdict}</span>
          </div>
        </div>
        <p className="detect-summary">{policy_summary}</p>
        {data.policy_verdict !== "Consistent" && data.policy_findings?.length > 0 && (
          <div className="findings-list">
            <p className="findings-title">Specific contradictions found:</p>
            {data.policy_findings.map((f, i) => (
              <div key={i} className="finding-item">
                <span>⚠️</span>
                <span>{f}</span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ManipulationDetector;