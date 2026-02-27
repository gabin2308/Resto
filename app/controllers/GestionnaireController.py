from flask import render_template, request, redirect, url_for, session, flash
from app import app
import json
#from datetime import datetime
from app.services.CommandesService import CommandesService
from app.services.UserService import UserService
from app.controllers.UserController import login_required, reqrole


class GestionnaireController:

    @app.route('/gestionnaire', methods=['GET'])
    @reqrole('gestionnaire','admin')
    def gestionnaire():
        cs = CommandesService()
        us = UserService()

        res = request.args.get('search', '')
        statut = request.args.get('statut', '')

        if res:
            user = us.getUserById(res)
        else:
            user = us.getUsers()

        if statut and statut != 'tous':
            commandes = cs.getByStatut(statut)
        else:
            commandes = cs.getAllCommande()

        return render_template(
            'gestionnaire.html',
            commandes=commandes,
            user=user,
            metadata={"title": "Gestionnaire"}
        )

    @app.route('/gestionnaire/utilisateur/<int:user_id>/statut/<int:id>', methods=['POST'])
    @reqrole('gestionnaire','admin')
    def changerStatut(user_id,id):
        cs = CommandesService()
        nouveau_statut = request.form.get('statut','')
        statuts_autorises = ['en attente', 'en cours', 'livrée', 'annulée']
        if nouveau_statut not in statuts_autorises:
            flash('Statut invalide.', 'error')
            return redirect(url_for('gestionnaire'))
        cs.getUpdateByStatut(user_id, nouveau_statut,id)
        flash(f'La commande # {id} de l\'utilisateur #{user_id} mises à jour : {nouveau_statut}', 'success')
        return redirect(url_for('gestionnaire'))