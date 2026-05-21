import json, os

BASELINE_PATH = "storage/baseline.json"

def load_baseline():
    if not os.path.exists(BASELINE_PATH): return {}
    with open(BASELINE_PATH) as f: return json.load(f)

def save_baseline(data):
    os.makedirs("storage", exist_ok=True)
    with open(BASELINE_PATH, "w") as f: json.dump(data, f, indent=2)

def detect_changes(domain, new_data):
    baseline = load_baseline()
    current_cookies = [c["name"] for c in new_data["cookies"]]
    current_third = list(new_data["third_party_domains"])

    if domain not in baseline:
        baseline[domain] = {"cookies": current_cookies, "third_party_domains": current_third}
        save_baseline(baseline)
        return {"baseline_created": True, "new_cookies": [], "new_third_parties": []}

    old = baseline[domain]
    new_cookies = list(set(current_cookies) - set(old["cookies"]))
    new_third = list(set(current_third) - set(old["third_party_domains"]))

    return {"baseline_created": False, "new_cookies": new_cookies, "new_third_parties": new_third}