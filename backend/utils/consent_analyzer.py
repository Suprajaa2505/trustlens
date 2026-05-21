from datetime import datetime

AD_KEYWORDS = ["ad", "ads", "doubleclick", "marketing", "facebook", "criteo"]
ANALYTICS_KEYWORDS = ["analytics", "ga", "google", "stats", "segment"]
PROFILE_KEYWORDS = ["track", "profile", "pixel", "retarget", "behavior"]

def classify_tracker(domain):
    d = domain.lower()
    if any(k in d for k in AD_KEYWORDS): return "advertising"
    if any(k in d for k in ANALYTICS_KEYWORDS): return "analytics"
    if any(k in d for k in PROFILE_KEYWORDS): return "profiling"
    return "unknown"

def analyze_cookie_lifetime(cookies):
    session, long_term, longest_days = 0, 0, 0
    now = datetime.utcnow().timestamp()
    for c in cookies:
        if "expires" not in c or c["expires"] == -1:
            session += 1
        else:
            long_term += 1
            days = int((c["expires"] - now) / 86400)
            if days > longest_days:
                longest_days = days
    return {
        "session_cookies": session,
        "long_term_cookies": long_term,
        "longest_lifetime_days": max(longest_days, 0)
    }