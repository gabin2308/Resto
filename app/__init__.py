from flask import Flask, session
from dotenv import load_dotenv
from flask_cors import CORS
import stripe
import os
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask import jsonify

load_dotenv()

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_COOKIE_SECURE"] = False
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"  # ← ajoute ça
app.secret_key = 'ma cle secrete unique'

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')

# CORS avec credentials
CORS(app,
     origins=["http://localhost:5175", "http://localhost:5173"],
     supports_credentials=True  # ← obligatoire pour les cookies
)

limiter = Limiter(get_remote_address, app=app, default_limits=["200 per day", "50 per hour"])

@app.errorhandler(429)
def trop_de_requetes(e):
    return jsonify({"error": "Trop de requêtes, veuillez réessayer plus tard."}), 429

from app.controllers import register_all
register_all(app)