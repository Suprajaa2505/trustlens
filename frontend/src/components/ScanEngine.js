import "./ScanEngine.css";

function ScanEngine({ data }) {
  const {
    tracker_count, high_risk_trackers, third_party_domains,
    cookie_analysis, geo_risk, geo_results,
    new_trackers, baseline_created
  } = data;

  const geoClass =
    geo_risk === "HIGH" ? "badge-red" :
    geo_risk === "MEDIUM" ? "badge-yellow" : "badge-green";

  return (
    <div className="card animate-fade">
      <div className="pillar-header">
        <span className="pillar-number">1</span>
        <div>
          <h2 className="pillar-title">Scan Engine</h2>
          <p className="pillar-desc">Who is watching you on this site?</p>
        </div>
      </div>

      {/* Plain English Summary */}
      <div className="summary-box">
        <p className="summary-text">
          {tracker_count === 0
            ? "No third-party trackers were found. This site appears clean."
            : `When you visit this site, ${tracker_count} companies load in the background. `+
              `${high_risk_trackers > 0 ? `${high_risk_trackers} of them are advertisers or profilers tracking your behaviour.` : "Most appear to be analytics tools."}`
          }
        </p>
      </div>

      {/* Change detector badge */}
      {!baseline_created && new_trackers?.length > 0 && (
        <div className="new-trackers-alert">
          🆕 {new_trackers.length} new tracker(s) detected since your last scan:&nbsp;
          <strong>{new_trackers.join(", ")}</strong>
        </div>
      )}

      {/* Stats Row */}
      <div className="stats-row">
        <div className="stat-item">
          <span className="stat-value-lg">{tracker_count}</span>
          <span className="stat-label">Total Trackers</span>
        </div>
        <div className="stat-item">
          <span className="stat-value-lg danger">{high_risk_trackers}</span>
          <span className="stat-label">High Risk</span>
        </div>
        <div className="stat-item">
          <span className="stat-value-lg">{cookie_analysis?.long_term_cookies ?? 0}</span>
          <span className="stat-label">Long-term Cookies</span>
        </div>
        <div className="stat-item">
          <span className={`badge ${geoClass}`}>
            {geo_risk} GEO RISK
          </span>
          <span className="stat-label">Data Flow Risk</span>
        </div>
      </div>

      {/* Cookie Insight */}
      {cookie_analysis && (
        <div className="insight-box">
          <span className="insight-icon">🍪</span>
          <p>
            This site stores <strong>{cookie_analysis.long_term_cookies} long-term cookie(s)</strong> on
            your device — the longest lasting <strong>{cookie_analysis.longest_lifetime_days} days</strong>.
            It also uses <strong>{cookie_analysis.session_cookies} session cookie(s)</strong> that disappear when you close the browser.
          </p>
        </div>
      )}

      {/* Geo Insight */}
      {geo_results?.length > 0 && (
        <div className="insight-box">
          <span className="insight-icon">🌍</span>
          <p>
            Your data flows to servers in{" "}
            <strong>{[...new Set(geo_results.map(g => g.country).filter(c => c !== "Unknown"))].join(", ") || "unknown locations"}</strong>.
            {geo_risk === "HIGH" && " Some of these countries have weak privacy laws."}
            {geo_risk === "LOW" && " These countries have strong privacy protections."}
          </p>
        </div>
      )}

      {/* Tracker List */}
      {third_party_domains?.length > 0 && (
        <div className="tracker-list-box">
          <p className="tracker-list-title">Companies detected:</p>
          <div className="tracker-tags">
            {third_party_domains.slice(0, 12).map((d, i) => (
              <span key={i} className="tracker-tag">{d}</span>
            ))}
            {third_party_domains.length > 12 && (
              <span className="tracker-tag muted">+{third_party_domains.length - 12} more</span>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default ScanEngine;