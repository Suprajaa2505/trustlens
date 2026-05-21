def calculate_risk_profile(company_map):
    risk_score, signals = 0, {"high_risk_companies": 0, "profiling_detected": False, "unknown_entities": 0}

    for c in company_map:
        if c["risk"] == "HIGH": risk_score += 15; signals["high_risk_companies"] += 1
        elif c["risk"] == "MEDIUM": risk_score += 8
        else: risk_score += 3
        if "Profiling" in c.get("purpose", ""): signals["profiling_detected"] = True
        if "Unknown" in c.get("company", ""): signals["unknown_entities"] += 1

    risk_score = min(100, risk_score)
    level = "HIGH" if risk_score > 70 else "MEDIUM" if risk_score > 35 else "LOW"
    return risk_score, level, signals