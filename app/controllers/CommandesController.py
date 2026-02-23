from flask import render_template, request, redirect, url_for, session
from app import app
import json
from datetime import datetime
from app.services.CommandesService import CommandesService
from app.services.PanierService import PanierService
from app.controllers.UserController import login_required

class CommandesController:

    
    #@app.route('/panier/commander', methods=['POST'])
    #@login_required
    #def confirmerCommande():

        #user_id = session.get('user_id')
        #if not user_id:
            #return redirect(url_for('login'))

        #cs      = CommandesService()
        #ps      = PanierService()
        #p       = ps.getAllPanier()

        #cs.ajouter(
            #date    = datetime.now().strftime('%Y-%m-%d %H:%M'),
            #items   = p.items,
            #total   = p.total,
            #statut  = 'en attente',
            #user_id = user_id  
        #)
        #ps.viderPanier()

        #commandes = cs.getByUserId(user_id)  #  uniquement ses commandes
        #metadata  = {'title': 'Confirmation'}
        #return render_template('confirmation.html',
                               #panier=p.items,
                               #commandes=commandes,
                               #metadata=metadata)


    @app.route('/commandes', methods=['GET'])
    @login_required
    def mesCommandes():
        cs      = CommandesService()

        user_id = session.get('user_id')  
        
        print(f"DEBUG user_id = {user_id}")  #  vérifie dans le terminal

        statut  = request.args.get('statut', 'tous')

        if statut and statut != 'tous':
            commandes = cs.getByUserIdAndStatut(user_id, statut)  
        else:
            commandes = cs.getByUserId(session['user_id'])  

        metadata = {'title': 'Mes Commandes'}
        return render_template('commandes.html',
                               commandes=commandes,
                               metadata=metadata)