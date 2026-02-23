from flask import render_template, request, redirect, url_for, session as flask_session
from app import app
from datetime import datetime
import stripe
from app.services.PaiementService import PaiementService
from app.services.CommandesService import CommandesService
from app.services.PanierService import PanierService
from app.controllers.UserController import login_required

class PaiementController:

    
    @app.route('/paiement', methods=['GET'])
    @login_required
    def paiement():
        ps = PanierService()
        p  = ps.getAllPanier()
        metadata = {'title': 'Paiement'}
        return render_template('paiement.html',
                               panier=p.items,
                               panier_total=p.total,
                               metadata=metadata)

    
    @app.route('/paiement/checkout', methods=['POST'])
    @login_required
    def checkout():
        ps = PanierService()
        p  = ps.getAllPanier()
        line_items = []
        for item in p.items:
            line_items.append({
                'price_data': {
                    'currency': 'eur',
                    'product_data': {'name': item['nom']},
                    'unit_amount': int(float(item['prix']) * 100),
                },
                'quantity': item['quantite'],
            })

        #  stripe_session au lieu de session pour ne pas écraser flask session
        stripe_session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('paiementSuccess', _external=True) + '?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=url_for('paiementCancel', _external=True),
        )
        return redirect(stripe_session.url)

    
    @app.route('/paiement/success', methods=['GET'])
    @login_required
    def paiementSuccess():
        ps  = PanierService()
        cs  = CommandesService()
        pys = PaiementService()
        p   = ps.getAllPanier()

        #  virgule ajoutée + user_id depuis flask_session
        id_commande = cs.ajouter(
            date    = datetime.now().strftime('%Y-%m-%d %H:%M'),
            items   = p.items,
            total   = p.total,
            statut  = 'en attente',                      #  virgule
            user_id = flask_session.get('user_id', 0)   #  flask_session
        )

        pys.ajouter(
            id_commande = id_commande,
            stripe_id   = request.args.get('session_id', ''),
            montant     = p.total,
            statut      = 'payé',
            date        = datetime.now().strftime('%Y-%m-%d %H:%M')
        )

        ps.viderPanier()
        return render_template('paiement_success.html',
                               metadata={'title': 'Paiement confirmé'})

    
    @app.route('/paiement/cancel', methods=['GET'])
    @login_required
    def paiementCancel():
        return render_template('paiement_cancel.html',
                               metadata={'title': 'Paiement annulé'})