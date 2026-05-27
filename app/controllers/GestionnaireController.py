# from flask import render_template, request, redirect, url_for, session, flash
# from app import app
# import json
# #from datetime import datetime
# from app.services.CommandesService import CommandesService
# from app.services.UserService import UserService
# from app.controllers.UserController import login_required, reqrole


# class GestionnaireController:

#     @app.route('/gestionnaire', methods=['GET'])
#     @reqrole('gestionnaire','admin')
#     def gestionnaire():
#         cs = CommandesService()
#         us = UserService()

#         res = request.args.get('search', '')
#         statut = request.args.get('statut', '')

#         if res:
#             user = us.getUserById(res)
#         else:
#             user = us.getUsers()

#         if statut and statut != 'tous':
#             commandes = cs.getByStatut(statut)
#         else:
#             commandes = cs.getAllCommande()

#         return render_template(
#             'gestionnaire.html',
#             commandes=commandes,
#             user=user,
#             metadata={"title": "Gestionnaire"}
#         )

#     @app.route('/gestionnaire/utilisateur/<int:user_id>/statut/<int:id>', methods=['POST'])
#     @reqrole('gestionnaire','admin')
#     def changerStatut(user_id,id):
#         cs = CommandesService()
#         nouveau_statut = request.form.get('statut','')
#         statuts_autorises = ['en attente', 'en cours', 'livrée', 'annulée']
#         if nouveau_statut not in statuts_autorises:
#             flash('Statut invalide.', 'error')
#             return redirect(url_for('gestionnaire'))
#         cs.getUpdateByStatut(user_id, nouveau_statut,id)
#         flash(f'La commande # {id} de l\'utilisateur #{user_id} mises à jour : {nouveau_statut}', 'success')
#         return redirect(url_for('gestionnaire'))

from flask import request, jsonify
from flask import Blueprint
from app.services.CommandesService import CommandesService
from app.services.UserService import UserService
from app.controllers.UserController import reqrole

class GestionnaireController:
    def __init__(self):
        self.blueprint = Blueprint("gestionnaire", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/",                           view_func=self.gestionnaire,  methods=["GET"])
        self.blueprint.add_url_rule("/commandes/<int:id>/statut",  view_func=self.changerStatut, methods=["PUT"])

    def gestionnaire(self):
        cs     = CommandesService()
        us     = UserService()
        search = request.args.get('search', '')
        statut = request.args.get('statut', '')

        if search:
            users = us.getUserById(search)
        else:
            users = us.getUsers()

        if statut and statut != 'tous':
            commandes = cs.getByStatut(statut)
        else:
            commandes = cs.getAllCommande()

        return jsonify({
            "commandes": [c.to_dict() for c in commandes],
            "users":     [u.to_dict() for u in users] if isinstance(users, list) else [users.to_dict()]
        })

    def changerStatut(self, id):
        cs              = CommandesService()
        data            = request.json or {}
        nouveau_statut  = data.get('statut', '')
        user_id         = data.get('user_id')
        statuts_autorises = ['en attente', 'en cours', 'livrée', 'annulée']

        if nouveau_statut not in statuts_autorises:
            return jsonify({"error": "Statut invalide"}), 400

        cs.getUpdateByStatut(user_id, nouveau_statut, id)
        return jsonify({
            "success": True,
            "message": f"Commande #{id} mise à jour : {nouveau_statut}"
        })

ctrl = GestionnaireController()