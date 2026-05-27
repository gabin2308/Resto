# from flask import render_template, redirect, url_for, request
# from flask import Blueprint, render_template, session
# from app import app
# import json 
# from app.services.RepasService import RepasService
# from app.controllers.UserController import login_required

# class RepasController:
#     ##@app.route('/repas', methods=['GET'])
#     ##@login_required
#     ##def repas():
#         ##rs = RepasService()
#         ##repas_name = request.form.get("repas_name", "")

#         ##repas = rs.getRepasByNom(repas_name)

#         ##metadata = {}

#         ##if len(repas) != 1:
#             #metadata["title"] = "results"
#         ##else:
#             #metadata["title"] = repas[0].nom
#         ##return render_template("repas.html", repas=repas, metadata=metadata)
    
        
#     @app.route('/categorie', methods=['GET'])
#     @login_required
#     def categorie():

#         rs = RepasService()

#         cat = request.args.get('cat') #cat = request.args.get('cat','tous')

#         if  not cat or cat.lower() == 'tous':
#             repas = rs.getRepasAll()

#         else:
#             repas = rs.getRepasByCategorie(cat)

#         return render_template('repas.html',repas=repas, metadata={'title': 'Nos Repas'})
    
#     @app.route('/prix', methods=['GET'])
#     @login_required
#     def prix():
#         rs = RepasService()
#         prix = request.args.get('prix_max', '')
#         if prix :
#             repas = rs.getRepasByPrix(prix)
#         else:
#             repas = rs.getRepasAll()

#         return render_template('repas.html', repas=repas, metadata={"title": 'Nos Repas'})
        

#     @app.route('/recherche/repas', methods=['GET'])
#     @login_required
#     def recherche():

#         rs = RepasService()
#         search = request.args.get('search', '')
#         if search:
#             repas = rs.getRepasByNom(search)
#         else:
#             repas = rs.getRepasAll()
        
#         return render_template('repas.html', repas = repas , metadata = {"title": 'Nos Repas'})

#     #@app.route('/repas/ajouter', methods=['POST'])
#     #def ajouter():

#         #rs = RepasService()
#         #id       = int(request.form.get('id'))
#         #nom      = request.form.get('nom')
#         #description    = request.form.get('description')
#         #categorie = request.form.get('categorie', 1)
#         #prix = float(request.form.get('prix', 0.0))
#         #statut = request.form.get('statut', 'disponible')
#         #quantite = int(request.form.get('quantite', 0))

#         #rs.ajouterRepas(id, nom,description,categorie,prix,statut,quantite)

#         #return None
from flask import request, jsonify
from flask import Blueprint
from app.services.RepasService import RepasService
from app.controllers.UserController import login_required

class RepasController:
    def __init__(self):
        self.blueprint = Blueprint("repas", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/",          view_func=self.getRepas,      methods=["GET"])
        self.blueprint.add_url_rule("/categories", view_func=self.getCategories, methods=["GET"])
        self.blueprint.add_url_rule("/prix",       view_func=self.getRepasByPrix, methods=["GET"])
        self.blueprint.add_url_rule("/recherche",  view_func=self.recherche,     methods=["GET"])

    def getRepas(self):
        rs  = RepasService()
        cat = request.args.get('cat')

        if not cat or cat.lower() == 'tous':
            repas = rs.getRepasAll()
        else:
            repas = rs.getRepasByCategorie(cat)

        return jsonify([r.to_dict() for r in repas])

    def getCategories(self):
        rs = RepasService()
        return jsonify(list(rs.getAllCategorie()))

    def getRepasByPrix(self):
        rs   = RepasService()
        prix = request.args.get('prix_max')

        if prix:
            repas = rs.getRepasByPrix(prix)
        else:
            repas = rs.getRepasAll()

        return jsonify([r.to_dict() for r in repas])

    def recherche(self):
        rs     = RepasService()
        search = request.args.get('search', '')

        if search:
            repas = rs.getRepasByNom(search)
        else:
            repas = rs.getRepasAll()

        return jsonify([r.to_dict() for r in repas])

ctrl = RepasController()