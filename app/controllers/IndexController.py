# from flask import redirect, render_template, url_for
# from app import app
# import json
# from app.services.RepasService import RepasService
# from app.controllers.UserController import login_required
# class IndexController:
#     @app.route('/', methods=['GET'])
#     @login_required
#     def index():
#         rs = RepasService()
#         repas  = rs.getRepasAll()
#         categorie = rs.getAllCategorie()

#         data = {
#             "categorie": list(categorie)
#         }

#         metadata = {
#             "title" : "🍔Food", "pagename":"index"
#         }

#         return render_template("index.html", data=data, metadata=metadata,repas=repas)

from flask import jsonify
from app import app

class IndexController:

    @app.route('/api', methods=['GET'])
    def index():
        return jsonify({
            "message": "API Resto en ligne",
            "version": "1.0",
            "routes": [
                "/api/auth",
                "/api/repas",
                "/api/panier",
                "/api/commandes",
                "/api/paiement",
                "/api/admin",
                "/api/gestionnaire"
            ]
        })