# Configuración de Email para Metro Cuadrado Mérida - PRODUCCIÓN
# IMPORTANTE: Configurar estas variables en Render Dashboard

import os

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': os.getenv('EMAIL_USER', 'tu_email@gmail.com'),
    'sender_password': os.getenv('EMAIL_PASSWORD', 'tu_password'),
    'recipient_email': 'jomma.tech@gmail.com'
}

# Para configurar en Render:
# 1. Ve a tu servicio en Render Dashboard
# 2. Ve a la sección "Environment"
# 3. Agrega estas variables:
#    - EMAIL_USER: tu_email@gmail.com
#    - EMAIL_PASSWORD: tu_app_password_de_gmail

# Para Gmail, necesitarás:
# 1. Habilitar la verificación en 2 pasos
# 2. Generar una "Contraseña de aplicación" específica
# 3. Usar esa contraseña en la variable EMAIL_PASSWORD
