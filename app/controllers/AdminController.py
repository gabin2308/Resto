from flask import render_template, request, redirect, url_for, session, flash
from app import app
from werkzeug.utils import secure_filename
import os
import json
from flask import current_app
#from datetime import datetime
from app.services.CommandesService import CommandesService
from app.services.UserService import UserService
from app.services.RepasService import RepasService
from app.services.PaiementService import PaiementService
from app.controllers.UserController import login_required, reqrole


class AdminController:
    #Gestion des commandes

    @app.route('/admin', methods=['GET']) #Pour rendre accessible les données utiles pour afficher les utilisateurs , repas et commandes 
    @reqrole('admin')
    def admin():
        cs = CommandesService()
        us = UserService()
        rs= RepasService()

        statut = request.args.get('statut', '')


        if statut and statut != 'tous':
            commandes = cs.getByStatut(statut)
        else:
            commandes = cs.getAllCommande()

        repas = rs.getRepasAll()
        users = us.getUsers()
        
        return render_template(
            'admin.html', 
            commandes=commandes,
            repas = repas,users = users,
            metadata={"title": "Admin"}
        )
    
    #Gestion des utilisateurs

    @app.route('/admin/users', methods = ['GET'])
    @reqrole('admin')
    def user():

        us = UserService()
        rs = RepasService()
        cs = CommandesService()
        repas = rs.getRepasAll()
        commandes = cs.getAllCommande()
        users = us.getUsers()
        return render_template('admin.html', users = users, panel= users, metadata={"title":"User"},repas=repas, commandes=commandes)
    
    @app.route('/admin/users', methods=['GET'])
    @reqrole('admin')
    def adminUser():
        us = UserService()
        rs = RepasService()
        user = request.args.get('role_filter', '')

        if user and user != 'tous':
            users = us.findByRole(user)
        else:
            users = us.getUsers()

        repas = rs.getRepasAll()

        return redirect(url_for('user',panel = 'users', metadata={'title': "Admin"}))
    

    
    @app.route('/admin/delete/<int:user_id>', methods=['POST'])
    @reqrole('admin')
    def adminDelete(user_id):
        us = UserService()
        us.deleteUser(user_id)
        return redirect(url_for('user', panel='users'))
    


    @app.route('/admin/update-role/<int:id>/<role>', methods=['POST'])
    @reqrole('admin')
    def updateRole(id, role):
        us= UserService()
        nouveau_role = request.form.get('role')
        roles_autorises = ['admin', 'gestionnaire', 'lecteur']
        if nouveau_role not in roles_autorises:
            flash('Statut invalide.', 'error')
            return redirect(url_for('admin', panel='users'))
        us.updateByRole(id, nouveau_role)
        flash(f'L\" utilisateur # {id} est mit à jour : {nouveau_role}', 'success')
        return redirect(url_for('user', panel="users"))
    
    #Gestion des repas pareil que l'admin
    
    @app.route('/admin/admin', methods=['GET'])
    @reqrole('admin')
    def repas():
        rs = RepasService()
        us = UserService()
        cs = CommandesService()
        commandes = cs.getAllCommande()
        repas = rs.getRepasAll()
        users = us.getUsers()
        return render_template('admin.html', panel = 'repas' ,metadata={"title":"Repas"},repas = repas, users=users, commandes=commandes)

    @app.route('/admin/ajouter-repas', methods=['GET','POST'])
    @reqrole('admin')
    def ajouterRepas():
        rs = RepasService()
        nom = request.form.get('nom')
        categorie = request.form.get('categorie')
        prix = request.form.get('prix')
        quantite = request.form.get('quantite')
        statut = request.form.get('statut')
        description = request.form.get('description')

        # Gestion photo
        filename = None  # ✅ valeur par défaut
        photo = request.files.get('photo')
        if photo and photo.filename:
            filename = secure_filename(photo.filename).lower()
            photo.save(os.path.join(current_app.static_folder, 'img', filename))  # ✅ chemin dynamique

        # Validations
        if statut not in ["disponible", "indisponible"]:
            flash('Statut invalide.', 'error')
            return redirect(url_for('repas', panel='repas'))  # ✅ corrigé

        if categorie not in ["Entrées", "Plats principaux", "Desserts"]:
            flash('Categorie invalide.', 'error')
            return redirect(url_for('repas', panel='repas'))  # ✅ corrigé

        rs.ajouterRepas(nom, description, categorie, prix, statut, quantite, filename)  # ✅ filename passé
        return redirect(url_for('repas', panel='repas'))  # ✅ corrigé
        
    @app.route('/admin/supprimer-repas/<int:id>', methods=['POST'])
    @reqrole('admin')
    def deleteRepas(id):

        rs = RepasService()
        rs.deleteRepas(id)
        return redirect(url_for('repas', panel='repas'))
    
        
    @app.route('/admin/modifier-repas/<int:id>', methods=['POST'])  
    @reqrole('admin')                                               
    def modifierRepas(id):                                         
        rs = RepasService()
        n = request.form.get('nom')
        c = request.form.get('categorie')
        p = request.form.get('prix')
        q = request.form.get('quantite')
        s = request.form.get('statut')
        d = request.form.get('description')

        statuts_autorises = ['disponible', 'indisponible']
        categories_autorisees = ['Entrées', 'Plats principaux', 'Desserts']

        if s not in statuts_autorises:
            flash('Statut invalide.', 'error')
            return redirect(url_for('admin', panel='repas'))

        if c not in categories_autorisees:
            flash('Catégorie invalide.', 'error')
            return redirect(url_for('admin', panel='repas'))

        rs.updateRepas(id, n, d, c, p, s, q)
        flash(f'✔ Repas modifié avec succès.', 'success')
        return redirect(url_for('admin', panel='repas'))  
    
    @app.route('/admin/<int:user_id>/statut/<int:id>', methods=['POST'])
    @reqrole('admin')
    def changerStatutAdmin(user_id,id):
        cs = CommandesService()
        nouveau_statut = request.form.get('statut','')
        statuts_autorises = ['en attente', 'en cours', 'livrée', 'annulée']
        if nouveau_statut not in statuts_autorises:
            flash('Statut invalide.', 'error')
            return redirect(url_for('admin'))
        cs.getUpdateByStatut(user_id, nouveau_statut,id)
        flash(f'La commande # {id} de l\'utilisateur #{user_id} mises à jour : {nouveau_statut}', 'success')
        return redirect(url_for('admin'))
        
    

