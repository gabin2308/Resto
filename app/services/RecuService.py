from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import cm
import io

class RecuService:
    def generer(self, commande):
        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        width, height = A4

        # En-tête
        c.setFont("Helvetica-Bold", 20)
        c.setFillColorRGB(1, 0.42, 0.13)  # orange
        c.drawString(2*cm, height - 2*cm, "🍔 Resto — Reçu de paiement")

        # Ligne séparatrice
        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.line(2*cm, height - 2.5*cm, width - 2*cm, height - 2.5*cm)

        # Infos commande
        c.setFont("Helvetica", 12)
        c.setFillColorRGB(0, 0, 0)
        y = height - 3.5*cm

        c.drawString(2*cm, y, f"Commande #{commande.id}")
        y -= 0.7*cm
        c.drawString(2*cm, y, f"Date : {commande.date}")
        y -= 0.7*cm
        c.drawString(2*cm, y, f"Statut : {commande.statut}")
        y -= 1*cm

        # Items
        c.setFont("Helvetica-Bold", 12)
        c.drawString(2*cm, y, "Articles :")
        y -= 0.7*cm

        c.setFont("Helvetica", 11)
        for item in commande.items:
            ligne = f"  - {item['nom']}  x{item['quantite']}  →  {item['prix'] * item['quantite']:.2f} €"
            c.drawString(2*cm, y, ligne)
            y -= 0.6*cm

        # Total
        y -= 0.5*cm
        c.line(2*cm, y, width - 2*cm, y)
        y -= 0.7*cm
        c.setFont("Helvetica-Bold", 13)
        c.setFillColorRGB(1, 0.42, 0.13)
        c.drawString(2*cm, y, f"Total payé : {commande.total} €")

        # Pied de page
        c.setFont("Helvetica", 9)
        c.setFillColorRGB(0.5, 0.5, 0.5)
        c.drawString(2*cm, 1.5*cm, "Merci pour votre commande — Resto")

        c.showPage()
        c.save()
        buffer.seek(0)
        return buffer