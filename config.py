# Configuración de Email para Metro Cuadrado Mérida
# IMPORTANTE: Cambiar estas credenciales por las reales antes de usar en producción

import os

EMAIL_CONFIG = {
    'emailjs_service_id': 'service_a1xi29i',
    'emailjs_template_id': 'template_8dl1y4o',
    'emailjs_user_id': 'topNg38j9LTlBzeSQ',  # Public Key
    'emailjs_private_key': '7v6YJD9QTFfRhOewB16JL',  # Private Key (necesaria para modo estricto)
    'sender_email': 'avisos@jm2-tech.es',
    'recipient_email': 'jomma.tech@gmail.com'
}

# Para EmailJS:
# 1. Ve a https://www.emailjs.com/
# 2. En "Email Services", usa el Service ID: service_a1xi29i
# 3. En "Email Templates", crea una plantilla y obtén el Template ID
# 4. En "Account" → "API Keys", obtén tu Public Key (User ID)
# 5. Reemplaza los valores 'tu_template_id_de_emailjs' y 'tu_user_id_public_key_de_emailjs'
