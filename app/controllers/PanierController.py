from flask import render_template, request, redirect, url_for
from app import app
from app.services.PanierService import PanierService

class PanierController:

    
    @app.route('/panier', methods=['GET'])
    def panier():
        ps = PanierService()
        p = ps.getAllPanier()
        metadata = {'title': 'Mon Panier'}
        return render_template('panier.html',
                               panier=p.items,
                               panier_total=p.total,
                               panier_count=p.count,
                               metadata=metadata)

    
    @app.route('/panier/ajouter', methods=['POST'])
    def ajouterPanier():
        ps = PanierService()
        id       = int(request.form.get('id'))
        nom      = request.form.get('nom')
        prix     = float(request.form.get('prix'))
        quantite = int(request.form.get('quantite', 1))
        ps.ajouterRepas(id, nom, prix, quantite)
        return redirect(url_for('categorie'))

    
    @app.route('/panier/supprimer/<int:id>', methods=['POST'])
    def supprimerPanier(id):
        ps = PanierService()
        ps.supprimerRepas(id)
        return redirect(url_for('panier'))

    
    @app.route('/panier/vider', methods=['POST'])
    def viderPanier():
        ps = PanierService()
        ps.viderPanier()
        return redirect(url_for('panier'))

    
    @app.route('/panier/commander', methods=['GET'])
    def passerCommande():
        ps = PanierService()
        p = ps.getAllPanier()
        metadata = {'title': 'Commander'}
        return render_template('commander.html',
                               panier=p.items,
                               panier_total=p.total,
                               metadata=metadata)