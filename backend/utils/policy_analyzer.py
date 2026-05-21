import re

def extract_policy_claims(text):
    t = text.lower()
    def match(patterns): return any(re.search(p, t) for p in patterns)

    return {
        "no_sharing_claim": match([r"we do not share.*personal", r"never share.*with third", r"will not share"]),
        "no_selling_claim": match([r"we do not sell.*personal", r"never sell.*information", r"will not sell"]),
        "mentions_third_party": match([r"third[- ]party (partner|service|vendor)", r"share.*with.*partner"]),
        "mentions_right_to_delete": match([r"right to (request )?delet", r"right to erasure", r"right to be forgotten"]),
        "mentions_data_retention": match([r"retain.*?\d+\s*(day|month|year)", r"retention period", r"we keep your"]),
        "mentions_user_profiling": match([r"build.*profil", r"behavioral.*advertis", r"interest.based advertis"]),
    }

def compare_claims_with_evidence(claims, tracker_evidence):
    findings, score = [], 0
    tc = len(tracker_evidence)

    if claims["no_sharing_claim"] and tc > 0:
        findings.append(f"Policy claims no third-party sharing, but {tc} tracker(s) were detected.")
        score += 50

    if claims["no_selling_claim"] and claims["mentions_user_profiling"]:
        findings.append("Policy claims not to sell data, yet mentions building user profiles for ads.")
        score += 30

    if not claims["mentions_third_party"] and tc > 0:
        findings.append(f"Policy doesn't mention third-party sharing, but {tc} external tracker(s) found.")
        score += 30

    if not claims["mentions_right_to_delete"]:
        findings.append("Policy doesn't mention your right to delete your data.")
        score += 20

    if not claims["mentions_data_retention"]:
        findings.append("Policy doesn't say how long they keep your data.")
        score += 10

    score = min(score, 100)

    if score >= 60: verdict = "Misleading"
    elif score >= 30: verdict = "Partially Transparent"
    else: verdict = "Consistent"

    if verdict == "Misleading":
        summary = f"Their privacy policy doesn't match reality. We found {tc} tracker(s) that contradict what they claim."
    elif verdict == "Partially Transparent":
        summary = f"Their policy is incomplete. Some important information about your data is missing."
    else:
        summary = f"Their privacy policy appears honest. No major contradictions found with {tc} tracker(s) detected."

    return {"verdict": verdict, "findings": findings, "human_summary": summary}