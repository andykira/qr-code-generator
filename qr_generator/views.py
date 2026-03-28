from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse
import qrcode
import io


class GenerateQRCodeView(APIView):
    def post(self, request):
        # 1. On récupère la donnée envoyée par React (le texte, l'URL ou le numéro)
        qr_data = request.data.get('data')

        if not qr_data:
            return Response({"error": "Veuillez fournir une donnée à encoder."}, status=400)

        # 2. On configure l'aspect du QR Code (design épuré)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,  # Haute correction pour qu'il soit bien lisible
            box_size=10,
            border=4,
        )

        qr.add_data(qr_data)
        qr.make(fit=True)

        # On crée l'image en noir et blanc (tu pourras changer les couleurs plus tard pour du premium)
        img = qr.make_image(fill_color="black", back_color="white")

        # 3. La ruse : on sauvegarde l'image dans un "fichier virtuel" en mémoire (BytesIO)
        # Ça évite de saturer ton disque dur avec des milliers d'images !
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)

        # 4. On renvoie directement l'image au front-end
        # Utiliser buffer.getvalue() pour renvoyer les octets réels
        response = HttpResponse(buffer.getvalue(), content_type="image/png")
        response['Content-Disposition'] = 'inline; filename="qrcode.png"'
        return response