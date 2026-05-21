from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from database import init_db
from routes.scan_routes import scan_bp
from routes.trust_score_routes import trust_bp

load_dotenv()

app = Flask(__name__)
CORS(app)
init_db()

app.register_blueprint(scan_bp)
app.register_blueprint(trust_bp)

@app.route("/health")
def health():
    return jsonify({"status": "TrustLens running", "version": "2.0"})

if __name__ == "__main__":
    app.run(debug=True)