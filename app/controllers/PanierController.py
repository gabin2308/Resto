# from flask import render_template, request, redirect, url_for
# from app import app
# from app.services.PanierService import PanierService
# from app.controllers.UserController import login_required
# class PanierController:

    
#     @app.route('/panier', methods=['GET'])
#     @login_required
#     def panier():
#         ps = PanierService()
#         p = ps.getAllPanier()
#         metadata = {'title': 'Mon Panier'}
#         return render_template('panier.html',
#                                panier=p.items,
#                                panier_total=p.total,
#                                panier_count=p.count,
#                                metadata=metadata)

    
#     @app.route('/panier/ajouter', methods=['POST'])
#     @login_required
#     def ajouterPanier():
#         ps = PanierService()
#         id       = int(request.form.get('id'))
#         nom      = request.form.get('nom')
#         prix     = float(request.form.get('prix'))
#         quantite = int(request.form.get('quantite', 1))
#         ps.ajouterRepas(id, nom, prix, quantite)
#         return redirect(url_for('categorie'))

    
#     @app.route('/panier/supprimer/<int:id>', methods=['POST'])
#     @login_required
#     def supprimerPanier(id):
#         ps = PanierService()
#         ps.supprimerRepas(id)
#         return redirect(url_for('panier'))

    
#     @app.route('/panier/vider', methods=['POST'])
#     @login_required
#     def viderPanier():
#         ps = PanierService()
#         ps.viderPanier()
#         return redirect(url_for('panier'))

    
#     @app.route('/panier/commander', methods=['GET'])
#     @login_required
#     def passerCommande():
#         ps = PanierService()
#         p = ps.getAllPanier()
#         metadata = {'title': 'Commander'}
#         return render_template('commander.html',
#                                panier=p.items,
#                                panier_total=p.total,
#                                metadata=metadata)

from flask import request, jsonify
from flask import Blueprint
from app.services.PanierService import PanierService
from app.controllers.UserController import login_required

class PanierController:
    def __init__(self):
        self.blueprint = Blueprint("panier", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/",                  view_func=login_required(self.getPanier),       methods=["GET"])
        self.blueprint.add_url_rule("/ajouter",           view_func=login_required(self.ajouterPanier),   methods=["POST"])
        self.blueprint.add_url_rule("/supprimer/<int:id>", view_func=login_required(self.supprimerPanier), methods=["DELETE"])
        self.blueprint.add_url_rule("/vider",             view_func=login_required(self.viderPanier),     methods=["DELETE"])
        self.blueprint.add_url_rule("/commander",         view_func=login_required(self.passerCommande),  methods=["GET"])
    
    def getPanier(self):
        ps = PanierService()
        p  = ps.getAllPanier()
        return jsonify({
            "items": p.items,
            "total": p.total,
            "count": p.count
        })
    
    def ajouterPanier(self):
        ps       = PanierService()
        data     = request.json or {}
        id       = int(data.get('id'))
        nom      = data.get('nom')
        prix     = float(data.get('prix'))
        quantite = int(data.get('quantite', 1))

        if not id or not nom or not prix:
            return jsonify({"error": "Champs manquants"}), 400

        ps.ajouterRepas(id, nom, prix, quantite)
        return jsonify({"success": True, "message": f"{nom} ajouté au panier"})
   
    def supprimerPanier(self, id):
        ps = PanierService()
        ps.supprimerRepas(id)
        return jsonify({"success": True, "message": f"Repas #{id} supprimé"})

   
    def viderPanier(self):
        ps = PanierService()
        ps.viderPanier()
        return jsonify({"success": True, "message": "Panier vidé"})

    
    def passerCommande(self):
        ps = PanierService()
        p  = ps.getAllPanier()
        return jsonify({
            "items": p.items,
            "total": p.total
        })

ctrl = PanierController()