from flask import render_template, request, redirect, url_for
from app import app
import json
from datetime import datetime
from app.services.CommandesService import CommandesService
from app.services.PanierService import PanierService
class CommandeCOntroller:
    
    @app.route('/panier/commander', methods=['POST'])
    def confirmerCommande():
       
       
        cs = CommandesService()
        ps = PanierService()
        p = ps.getAllPanier()
        commandes = cs.getAllCommande()
        cs.ajouter(
            date   = datetime.now().strftime('%Y-%m-%d %H:%M'),
            items  = p.items,
            total  = p.total,
            statut = 'en attente'
        )
        ps.vider()
        metadata={"title":"confirmation"}
        return render_template('confirmation.html', panier=p.items , commandes=commandes, metadata=metadata)
    
   
    @app.route('/commandes', methods=['GET'])
    def mesCommandes():
        from app.services.CommandesService import CommandesService
        cs = CommandesService()
        commandes = cs.getAllCommande()
        metadata = {'title': 'Mes Commandes'}
        return render_template('commandes.html',
                            commandes=commandes,
                            metadata=metadata)