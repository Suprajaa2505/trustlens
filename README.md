# 🔍 TrustLens — Website Privacy Analyzer

> Scan any website and understand what's happening to your data — in plain English.

TrustLens is a full-stack privacy analysis tool that uses headless browser automation to scan live websites and reveal hidden tracking, cookie manipulation, and privacy policy contradictions.

Built for **non-technical users** who want to know if a website is safe — without reading a privacy policy.

---

## 🚀 What It Does

Paste any URL → TrustLens scans it and gives you:

- **Who is tracking you** — every third-party company loading in the background
- **Where your data goes** — countries your data flows to and their privacy law strength
- **Is the cookie popup manipulating you** — dark pattern detection on consent banners
- **Does their privacy policy match reality** — cross-checks policy claims vs actual trackers
- **A Trust Score (0–100)** — one clear number with plain English verdict

---

## 📸 Screenshots

### Trust Score
![Trust Score](screenshots/reddit-trustscore.png)

### Scan Engine — Tracker Detection
![Scan Engine](screenshots/reddit-scanengine.png)

### Manipulation Detector
![Manipulation Detector](screenshots/reddit-manipulation.png)

---

## 🏗️ How It Works — 3 Pillars

### Pillar 1 — Scan Engine
- Headless Playwright browser opens the URL just like a real user
- Captures all network requests and identifies third-party tracker domains
- Maps each tracker to a country and evaluates privacy law strength
- Detects new trackers compared to previous scan (change detection)

### Pillar 2 — Manipulation Detector
- Analyzes cookie consent banner buttons for visual and language manipulation
- Reads the site's privacy policy and extracts key claims
- Cross-checks policy claims against actual trackers detected
- Flags contradictions in plain English

### Pillar 3 — Trust Score
- Aggregates 5 signals: tracker count, geo risk, dark patterns, policy truth, high-risk trackers
- Produces a weighted score from 0–100
- Gives a plain English verdict: Safe / Use with Caution / Avoid

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Browser Automation | Playwright |
| Backend | Python, Flask, REST API |
| Frontend | React.js |
| Database | SQLite |
| Geo Intelligence | ip-api.com |
| NLP | Regex-based policy analysis |

---

## ⚙️ Setup & Run

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
playwright install chromium
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm start
```

App runs at `http://localhost:3000`

---

## 📁 Project Structure
trustlens/
├── backend/
│   ├── app.py
│   ├── database.py
│   ├── routes/
│   │   ├── scan_routes.py
│   │   └── trust_score_routes.py
│   └── utils/
│       ├── scanner.py
│       ├── darkpattern_detector.py
│       ├── policy_analyzer.py
│       ├── geo_locator.py
│       └── trust_engine.py
└── frontend/
└── src/
├── pages/
│   ├── Home.js
│   └── Results.js
└── components/
├── TrustScore.js
├── ScanEngine.js
└── ManipulationDetector.js

---

## 👤 Author

Built as an academic project to demonstrate real-world privacy analysis for non-technical users.