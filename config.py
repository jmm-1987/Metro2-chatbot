# Configuración de Email para Metro Cuadrado Mérida
# IMPORTANTE: Cambiar estas credenciales por las reales antes de usar en producción

EMAIL_CONFIG = {
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'sender_email': 'tu_email@gmail.com',  # Cambiar por el email real
    'sender_password': 'tu_password',  # Cambiar por la contraseña real o app password
    'recipient_email': 'jomma.tech@gmail.com'
}

# Para Gmail, necesitarás:
# 1. Habilitar la verificación en 2 pasos
# 2. Generar una "Contraseña de aplicación" específica
# 3. Usar esa contraseña en lugar de tu contraseña normal

# Alternativamente, puedes usar variables de entorno:
# import os
# EMAIL_CONFIG = {
#     'smtp_server': 'smtp.gmail.com',
#     'smtp_port': 587,
#     'sender_email': os.getenv('EMAIL_USER'),
#     'sender_password': os.getenv('EMAIL_PASSWORD'),
#     'recipient_email': 'jomma.tech@gmail.com'
# }
