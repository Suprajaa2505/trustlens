import re

ACCEPT_WORDS = ["accept", "agree", "allow", "yes"]
REJECT_WORDS = ["reject", "decline", "deny", "refuse"]
EMOTIONAL_WORDS = ["best experience", "improve your experience", "support us", "we value you"]
MAX_RAW_SCORE = 140

def brightness_from_rgb(rgb):
    nums = re.findall(r'\d+', rgb)
    if len(nums) >= 3:
        r, g, b = int(nums[0]), int(nums[1]), int(nums[2])
        return (r*299 + g*587 + b*114) / 1000
    return 0

def analyze_dark_patterns(banner):
    findings, score = [], 0
    buttons = banner.get("buttons", [])
    text = banner.get("text", "").lower()

    accept_btn = next((b for b in buttons if any(w in b["text"].lower() for w in ACCEPT_WORDS)), None)
    reject_btn = next((b for b in buttons if any(w in b["text"].lower() for w in REJECT_WORDS)), None)

    if not reject_btn:
        findings.append("Reject option missing or hidden.")
        score += 50

    if accept_btn and reject_btn:
        if brightness_from_rgb(accept_btn.get("bg_color","")) - brightness_from_rgb(reject_btn.get("bg_color","")) > 50:
            findings.append("Accept button is brighter and more visible than reject.")
            score += 20
        accept_area = accept_btn["width"] * accept_btn["height"]
        reject_area = reject_btn["width"] * reject_btn["height"]
        if reject_area > 0 and accept_area / reject_area > 1.4:
            findings.append("Accept button is much larger than reject.")
            score += 20

    if any(w in text for w in EMOTIONAL_WORDS):
        findings.append("Emotional language used to push you toward accepting.")
        score += 30

    if banner.get("is_modal"):
        findings.append("Popup blocks the page until you respond.")
        score += 20

    if score >= 70: classification = "Aggressive Dark Pattern"
    elif score >= 30: classification = "Moderate Manipulation"
    elif score > 0: classification = "Mild UX Bias"
    else: classification = "No Manipulation Detected"

    if not banner.get("banner_detected"):
        score = 0
    normalized = round((score / MAX_RAW_SCORE) * 100)

    if not banner.get("banner_detected"):
        summary = "No cookie popup was found on this page. We couldn't check for manipulation tactics."
    elif classification == "Aggressive Dark Pattern":
        summary = f"This site is designed to trick you into accepting all cookies. {len(findings)} manipulation tactic(s) detected. Your privacy is being compromised by design."
    elif classification == "Moderate Manipulation":
        summary = f"This site's cookie popup subtly pushes you toward accepting. {len(findings)} tactic(s) detected."
    elif classification == "Mild UX Bias":
        summary = "Minor bias in the cookie popup. Most users can still make an informed choice."
    else:
        summary = "No tricks detected in the cookie popup. Accept and reject options appear fairly presented."

    return {
        "findings": findings,
        "manipulation_score": normalized,
        "classification": classification,
        "human_summary": summary
    }