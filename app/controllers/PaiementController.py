from flask import request, jsonify, session as flask_session, Blueprint
from datetime import datetime
import stripe
import os

from app.services.PaiementService import PaiementService
from app.services.CommandesService import CommandesService
from app.services.PanierService import PanierService
from app.controllers.UserController import login_required
from app import FRONTEND_URL

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")


class PaiementController:
    def __init__(self):
        self.blueprint = Blueprint("paiement", __name__)
        self._register_routes()

    def _register_routes(self):
        self.blueprint.add_url_rule("/", view_func=self.getPanier, methods=["GET"])
        self.blueprint.add_url_rule("/checkout", view_func=self.checkout, methods=["POST"])
        self.blueprint.add_url_rule("/success", view_func=self.paiementSuccess, methods=["GET"])
        self.blueprint.add_url_rule("/cancel", view_func=self.paiementCancel, methods=["GET"])
        self.blueprint.add_url_rule("/historique", view_func=self.historique, methods=["GET"])
    # =========================
    # PANIER
    # =========================
    @login_required
    def getPanier(self):
        ps = PanierService()
        p = ps.getAllPanier()

        return jsonify({
            "items": p.items,
            "total": p.total
        })

    # =========================
    # CHECKOUT STRIPE
    # =========================
    
    def checkout(self):
        ps = PanierService()
        p = ps.getAllPanier()

        if not p.items:
            return jsonify({"error": "Panier vide"}), 400

        user_id = flask_session.get("user_id")
        if not user_id:
            return jsonify({"error": "Non authentifié"}), 401

        # snapshot panier
        flask_session["pending_order"] = {
            "items": [item.copy() for item in p.items],
            "total": p.total
        }

        line_items = [
            {
                "price_data": {
                    "currency": "eur",
                    "product_data": {"name": item["nom"]},
                    "unit_amount": int(float(item["prix"]) * 100),
                },
                "quantity": item["quantite"],
            }
            for item in p.items
        ]

        stripe_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=line_items,
            mode="payment",

            success_url=f"{FRONTEND_URL}/paiement/success?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{FRONTEND_URL}/paiement/cancel",
        )

        return jsonify({"url": stripe_session.url})

    # =========================
    # SUCCESS STRIPE
    # =========================
    def paiementSuccess(self):
        ps  = PanierService()
        cs  = CommandesService()
        pys = PaiementService()
        user_id = flask_session.get("user_id")
        if not user_id:
            return jsonify({"error": "Non authentifié"}), 401

        session_id = request.args.get("session_id", "")

        # ← vérifie si ce stripe_id a déjà été traité
        existant = pys.getByStripeId(session_id)
        if existant:
            return jsonify({
                "success": True,
                "id_commande": existant.id_commande,
                "message": "Commande déjà confirmée"
            })

        order = flask_session.get("pending_order")
        if not order:
            return jsonify({"error": "Commande introuvable"}), 400

        id_commande = cs.ajouter(
            date    = datetime.now().strftime('%Y-%m-%d %H:%M'),
            items   = order["items"],
            total   = order["total"],
            statut  = "en attente",
            user_id = user_id
        )
        pys.ajouter(
            id_commande = id_commande,
            stripe_id   = session_id,
            montant     = order["total"],
            statut      = "payé",
            date        = datetime.now().strftime('%Y-%m-%d %H:%M')
        )
        ps.viderPanier()
        flask_session.pop("pending_order", None)
        return jsonify({
            "success":     True,
            "id_commande": id_commande,
            "message":     "Commande confirmée"
        })

    # =========================
    # CANCEL
    # =========================
    
    def paiementCancel(self):
        flask_session.pop("pending_order", None)

        return jsonify({
            "success": False,
            "message": "Paiement annulé"
        })
    
    @login_required
    def historique(self):
        pys     = PaiementService()
        user_id = flask_session.get("user_id")
        statut  = request.args.get("statut", "tous")
        if statut and statut != "tous":
            paiements = pys.getByUserIdAndStatut(user_id, statut)
        else:
            paiements = pys.getByUserId(user_id)
        return jsonify([p.to_dict() for p in paiements])


ctrl = PaiementController()