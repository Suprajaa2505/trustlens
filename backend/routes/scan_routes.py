from flask import Blueprint, request, jsonify
import tldextract
from utils.scanner import scan_website
from utils.consent_analyzer import analyze_cookie_lifetime, classify_tracker
from utils.darkpattern_detector import analyze_dark_patterns
from utils.policy_analyzer import extract_policy_claims, compare_claims_with_evidence
from utils.geo_locator import locate_country
from utils.country_risk_engine import evaluate_country
from utils.change_detector import detect_changes

scan_bp = Blueprint("scan", __name__)

@scan_bp.route("/scan", methods=["POST"])
def scan():
    body = request.get_json()
    url = body.get("url")
    if not url:
        return jsonify({"error": "URL required"}), 400

    try:
        # Pillar 1 — Scan Engine
        evidence = scan_website(url, mode="accept", extract_consent=True)
        domain = tldextract.extract(url).registered_domain

        cookies = evidence.get("cookies", [])
        third_parties = list(evidence.get("third_party_domains", []))

        cookie_analysis = analyze_cookie_lifetime(cookies)

        # Geo mapping
        geo_results = [locate_country(d) for d in third_parties[:10]]
        country_risks = [evaluate_country(g["country"]) for g in geo_results]
        high_risk_countries = [c for c in country_risks if c["risk"] == "HIGH"]
        geo_risk = "HIGH" if len(high_risk_countries) > 2 else "MEDIUM" if len(high_risk_countries) > 0 else "LOW"

        # Tracker classification
        classified = [classify_tracker(d) for d in third_parties]
        high_risk_trackers = classified.count("advertising") + classified.count("profiling")

        # Change detection
        changes = detect_changes(domain, {"cookies": cookies, "third_party_domains": third_parties})

        # Pillar 2 — Manipulation Detector
        banner = evidence.get("consent_banner", {})
        dark_result = analyze_dark_patterns(banner)

        policy_result = {"verdict": "Consistent", "findings": [], "human_summary": "Policy not found."}
        policy_url = evidence.get("policy_url")
        if policy_url:
            from utils.scanner import fetch_policy_text
            policy_text = fetch_policy_text(policy_url)
            if policy_text:
                claims = extract_policy_claims(policy_text)
                policy_result = compare_claims_with_evidence(claims, third_parties)

        return jsonify({
            "domain": domain,
            # Pillar 1
            "tracker_count": len(third_parties),
            "high_risk_trackers": high_risk_trackers,
            "third_party_domains": third_parties[:15],
            "cookie_analysis": cookie_analysis,
            "geo_risk": geo_risk,
            "geo_results": geo_results[:10],
            "new_trackers": changes.get("new_third_parties", []),
            "baseline_created": changes.get("baseline_created", False),
            # Pillar 2
            "dark_pattern_score": dark_result["manipulation_score"],
            "dark_pattern_level": dark_result["classification"],
            "dark_pattern_summary": dark_result["human_summary"],
            "policy_verdict": policy_result["verdict"],
            "policy_summary": policy_result["human_summary"],
            "policy_findings": policy_result.get("findings", []),
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500