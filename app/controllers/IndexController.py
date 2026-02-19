from flask import redirect, render_template, url_for
from app import app
import json
from app.services.RepasService import RepasService

class IndexController:
    @app.route('/', methods=['GET'])
    def index():
        rs = RepasService()
        repas  = rs.getRepasdAll()
        repas_pays = rs.getAllPays()

        data = {
            "pays": list(repas_pays)
        }

        metadata = {
            "title" : "🍔Food", "pagename":"index"
        }

        return render_template("index.html", data=data, metadata=metadata,repas=repas)