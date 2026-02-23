from flask import Flask, session
from dotenv import load_dotenv
import stripe
import os

load_dotenv()  # en premier avant tout

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_COOKIE_SECURE"] = False
app.secret_key = 'ma cle secrete unique'

stripe.api_key = os.getenv('STRIPE_SECRET_KEY')  #  lit depuis .env

from app.controllers import *

@app.context_processor
def inject_panier_count():
    try:
        from app.services.PanierService import PanierService
        ps = PanierService()
        p = ps.getAllPanier()
        return {'panier_count': p.count}
    except:
        return {'panier_count': 0}
