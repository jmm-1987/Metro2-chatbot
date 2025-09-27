# Configuración de Email para Metro Cuadrado Mérida - PRODUCCIÓN
# IMPORTANTE: Configurar estas variables en Render Dashboard

import os

EMAIL_CONFIG = {
    'emailjs_service_id': os.getenv('EMAILJS_SERVICE_ID', 'service_a1xi29i'),
    'emailjs_template_id': os.getenv('EMAILJS_TEMPLATE_ID', 'template_8dl1y4o'),
    'emailjs_user_id': os.getenv('EMAILJS_USER_ID', 'topNg38j9LTlBzeSQ'),
    'emailjs_private_key': os.getenv('EMAILJS_PRIVATE_KEY', '7v6YJD9QTFfRhOewB16JL'),
    'sender_email': 'avisos@jm2-tech.es',
    'recipient_email': 'jomma.tech@gmail.com'
}

# Para configurar EmailJS en Render:
# 1. Ve a tu servicio en Render Dashboard
# 2. Ve a la sección "Environment"
# 3. Agrega estas variables:
#    - EMAILJS_SERVICE_ID: service_a1xi29i
#    - EMAILJS_TEMPLATE_ID: template_8dl1y4o
#    - EMAILJS_USER_ID: topNg38j9LTlBzeSQ
#    - EMAILJS_PRIVATE_KEY: tu_private_key_de_emailjs

# Para obtener los IDs de EmailJS:
# 1. Ve a https://www.emailjs.com/
# 2. En "Email Services", usa el Service ID: service_a1xi29i
# 3. En "Email Templates", crea una plantilla y obtén el Template ID
# 4. En "Account" → "API Keys", obtén tu Public Key (User ID)

# Para IONOS:
# 1. Usa tu email completo de IONOS
# 2. Usa tu contraseña normal de IONOS (no necesitas app password)
# 3. El servidor SMTP es smtp.ionos.es con puerto 465 (SSL)
