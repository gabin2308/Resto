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
    
from app.services.CommandesService import CommandesService

@app.context_processor
def inject_commandes_count():
    from flask import session
    count = 0
    if "logged" in session and session.get("user_id"):
        cs = CommandesService()
        commandes = cs.getByUserIdAndStatut(session["user_id"], "en attente")
        count = len(commandes) if commandes else 0
    return dict(commandes_count=count)
