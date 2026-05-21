import sqlite3
from datetime import datetime

DB_PATH = "storage/trustlens.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            domain TEXT,
            trust_score INTEGER,
            trust_level TEXT,
            tracker_count INTEGER,
            high_risk_trackers INTEGER,
            geo_risk TEXT,
            dark_pattern_score INTEGER,
            dark_pattern_level TEXT,
            policy_verdict TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_scan(data):
    conn = get_connection()
    conn.execute("""
        INSERT INTO scans (
            url, domain, trust_score, trust_level,
            tracker_count, high_risk_trackers, geo_risk,
            dark_pattern_score, dark_pattern_level,
            policy_verdict, timestamp
        ) VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """, (
        data.get("url"), data.get("domain"),
        data.get("trust_score"), data.get("trust_level"),
        data.get("tracker_count"), data.get("high_risk_trackers"),
        data.get("geo_risk"), data.get("dark_pattern_score"),
        data.get("dark_pattern_level"), data.get("policy_verdict"),
        datetime.utcnow().isoformat()
    ))
    conn.commit()
    conn.close()

def get_last_scan(domain):
    conn = get_connection()
    row = conn.execute("""
        SELECT * FROM scans WHERE domain = ?
        ORDER BY timestamp DESC LIMIT 1
    """, (domain,)).fetchone()
    conn.close()
    return dict(row) if row else None