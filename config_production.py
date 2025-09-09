# Configuración de Email para Metro Cuadrado Mérida - PRODUCCIÓN
# IMPORTANTE: Configurar estas variables en Render Dashboard

import os

EMAIL_CONFIG = {
    'smtp_server': 'smtp.ionos.es',
    'smtp_port': 465,  # Puerto SSL para IONOS
    'sender_email': os.getenv('EMAIL_USER', 'tu_email@ionos.com'),
    'sender_password': os.getenv('EMAIL_PASSWORD', 'tu_password'),
    'recipient_email': 'jomma.tech@gmail.com'
}

# Para configurar en Render:
# 1. Ve a tu servicio en Render Dashboard
# 2. Ve a la sección "Environment"
# 3. Agrega estas variables:
#    - EMAIL_USER: tu_email@ionos.com
#    - EMAIL_PASSWORD: tu_contraseña_de_ionos

# Para IONOS:
# 1. Usa tu email completo de IONOS
# 2. Usa tu contraseña normal de IONOS (no necesitas app password)
# 3. El servidor SMTP es smtp.ionos.es con puerto 465 (SSL)
