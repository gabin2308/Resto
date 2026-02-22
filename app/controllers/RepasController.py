from flask import render_template, redirect, url_for, request
from flask import Blueprint, render_template, session
from app import app
import json 
from app.services.RepasService import RepasService


class RepasController:
    @app.route('/repas', methods=['GET'])
    def repas():
        rs = RepasService()
        repas_name = request.form.get("repas_name", "")

        repas = rs.getRepasByNom(repas_name)

        metadata = {}

        if len(repas) != 1:
            metadata["title"] = "results"
        else:
            metadata["title"] = repas[0].nom
        return render_template("repas.html", repas=repas, metadata=metadata)
    
        
    @app.route('/categorie', methods=['GET'])
    def categorie():

        rs = RepasService()

        cat = request.args.get('cat') #cat = request.args.get('cat','tous')

        if  not cat or cat.lower() == 'tous':
            repas = rs.getRepasAll()

        else:
            repas = rs.getRepasByCategorie(cat)

        return render_template('repas.html',repas=repas, metadata={'title': 'Nos Repas'})
    
    @app.route('/prix', methods=['GET'])
    def prix():
        rs = RepasService()
        prix = request.args.get('prix_max', '')
        if prix :
            repas = rs.getRepasByPrix(prix)

        return render_template('repas.html', repas=repas, metadata={"title": 'Nos Repas'})
        

    @app.route('/recherche/repas', methods=['GET'])
    def recherche():

        rs = RepasService()
        search = request.args.get('search', '')
        if search:
            repas = rs.getRepasByNom(search)
        
        return render_template('repas.html', repas = repas , metadata = {"title": 'Nos Repas'})

    #@app.route('/repas/ajouter', methods=['POST'])
    #def ajouter():

        #rs = RepasService()
        #id       = int(request.form.get('id'))
        #nom      = request.form.get('nom')
        #description    = request.form.get('description')
        #categorie = request.form.get('categorie', 1)
        #prix = float(request.form.get('prix', 0.0))
        #statut = request.form.get('statut', 'disponible')
        #quantite = int(request.form.get('quantite', 0))

        #rs.ajouterRepas(id, nom,description,categorie,prix,statut,quantite)

        #return None