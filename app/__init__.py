from flask import Flask,session

app = Flask(__name__, static_url_path='/static')
app.config["SESSION_COOKIE_SECURE"] = False
app.secret_key = 'ma cle secrete unique'

from app.controllers import *
#from app.controllers.PanierController import panier_bp 

#app.register_blueprint(panier_bp) 

@app.context_processor
def inject_panier_count():
    try:
        from app.services.PanierService import PanierService
        ps = PanierService()
        p = ps.getAllPanier()
        return {'panier_count': p.count}  # ✅ lit depuis SQLite
    except:
        return {'panier_count': 0}