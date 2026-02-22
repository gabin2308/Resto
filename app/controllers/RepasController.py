from flask import render_template, redirect, url_for, request
from flask import Blueprint, render_template, session
from app import app
import json 
from app.services.RepasService import RepasService


class RepasController:
    @app.route('/repas', methods=['GET'])
    def repas():
        cs = RepasService()
        repas_name = request.form.get("repas_name", "")

        repas = cs.getRepasByNom(repas_name)

        metadata = {}

        if len(repas) != 1:
            metadata["title"] = "results"
        else:
            metadata["title"] = repas[0].nom
        return render_template("repas.html", repas=repas, metadata=metadata)
    
        
    @app.route('/categorie', methods=['GET'])
    def categorie():
        cs = RepasService()
        cat = request.args.get('cat') #cat = request.args.get('cat','tous')

        if  not cat or cat.lower() == 'tous':
            repas = cs.getRepasAll()
        else:
            repas = cs.getRepasByCategorie(cat)

        return render_template('repas.html', repas=repas, metadata={'title': 'Nos Repas'})
    

    