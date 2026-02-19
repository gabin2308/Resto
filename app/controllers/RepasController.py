from flask import render_template, redirect, url_for, request
from app import app
import json 
from app.services.RepasService import RepasService


class RepasController:
    @app.route('/repas', methods=['POST'])
    def repasByName():
        cs = RepasService()
        repas_name = request.form.get("repas_name", "")

        repas = cs.getRepasByName(repas_name)

        metadata = {}

        if len(repas) != 1:
            metadata["title"] = "resluts"
        else:
            metadata["title"] = repas[0].nom
        return render_template("repas.html", repas=repas, metadata=metadata)