from flask import redirect, render_template, url_for
from app import app
import json
from app.services.RepasService import RepasService
from app.controllers.UserController import login_required
class IndexController:
    @app.route('/', methods=['GET'])
    @login_required
    def index():
        rs = RepasService()
        repas  = rs.getRepasAll()
        categorie = rs.getAllCategorie()

        data = {
            "categorie": list(categorie)
        }

        metadata = {
            "title" : "🍔Food", "pagename":"index"
        }

        return render_template("index.html", data=data, metadata=metadata,repas=repas)