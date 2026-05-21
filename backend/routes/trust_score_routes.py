from flask import Blueprint, request, jsonify
import tldextract
from database import save_scan, get_last_scan

trust_bp = Blueprint("trust", __name__)

def calculate_trust_score(data):
    score = 100
    reasons = []

    # Trackers
    tc = data.get("tracker_count", 0)
    hr = data.get("high_risk_trackers", 0)
    deduct = min(30, tc * 0.5 + hr * 5)
    score -= deduct
    if tc > 20: reasons.append(f"{tc} companies are tracking you on this site.")
    elif tc > 10: reasons.append(f"{tc} trackers found — more than average.")
    if hr > 0: reasons.append(f"{hr} of them are high-risk advertisers or profilers.")

    # Geo
    geo = data.get("geo_risk", "LOW")
    geo_deduct = {"HIGH": 20, "MEDIUM": 10, "LOW": 0}[geo]
    score -= geo_deduct
    if geo == "HIGH": reasons.append("Your data flows to countries with weak privacy laws.")
    elif geo == "MEDIUM": reasons.append("Some data goes to countries with partial privacy protection.")

    # Dark patterns
    dp = data.get("dark_pattern_score", 0)
    score -= min(20, dp * 0.2)
    level = data.get("dark_pattern_level", "")
    dp_score = data.get("dark_pattern_score", 0)
    if level == "Aggressive Dark Pattern" and dp_score > 0: reasons.append("This site tricks you into accepting all cookies.")
    elif level == "Moderate Manipulation" and dp_score > 0: reasons.append("The cookie popup subtly pushes you to accept.")

    # Policy
    pv = data.get("policy_verdict", "Consistent")
    policy_deduct = {"Misleading": 20, "Partially Transparent": 10, "Consistent": 0}[pv]
    score -= policy_deduct
    if pv == "Misleading": reasons.append("Their privacy policy contradicts what we actually detected.")
    elif pv == "Partially Transparent": reasons.append("Their policy is missing key information.")

    score = max(0, min(100, round(score)))

    if score >= 70:
        level = "HIGH"
        verdict = "This site is relatively safe to use."
        advice = "Safe to Use"
    elif score >= 40:
        level = "MEDIUM"
        verdict = "This site has some privacy concerns worth knowing about."
        advice = "Use with Caution"
    else:
        level = "LOW"
        verdict = "This site has serious privacy issues. Be careful."
        advice = "Avoid if Possible"

    return {
        "trust_score": score,
        "trust_level": level,
        "verdict": verdict,
        "advice": advice,
        "reasons": reasons
    }

@trust_bp.route("/trust-score", methods=["POST"])
def trust_score():
    body = request.get_json()
    data = body.get("scan_data")
    url = body.get("url")
    if not data or not url:
        return jsonify({"error": "url and scan_data required"}), 400

    result = calculate_trust_score(data)
    domain = tldextract.extract(url).registered_domain

    save_scan({
        "url": url,
        "domain": domain,
        **result,
        **data
    })

    return jsonify(result)