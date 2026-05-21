import json, os

DB_PATH = os.path.join("data", "country_privacy_db.json")

def load_country_db():
    with open(DB_PATH) as f:
        return json.load(f)

def evaluate_country(country_name):
    db = load_country_db()
    if country_name in db:
        return db[country_name]
    return {"privacy_level": "UNKNOWN", "laws": ["No clear framework"], "risk": "HIGH"}