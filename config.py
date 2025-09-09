# Configuración de Email para Metro Cuadrado Mérida
# IMPORTANTE: Cambiar estas credenciales por las reales antes de usar en producción

EMAIL_CONFIG = {
    'smtp_server': 'smtp.ionos.es',
    'smtp_port': 465,  # Puerto SSL para IONOS
    'sender_email': 'tu_email@ionos.com',  # Cambiar por el email real
    'sender_password': 'tu_password',  # Cambiar por la contraseña real
    'recipient_email': 'jomma.tech@gmail.com'
}

# Para IONOS:
# 1. Usa tu email completo de IONOS
# 2. Usa tu contraseña normal de IONOS (no necesitas app password)
# 3. El servidor SMTP es smtp.ionos.es con puerto 465 (SSL)

# Alternativamente, puedes usar variables de entorno:
# import os
# EMAIL_CONFIG = {
#     'smtp_server': 'smtp.ionos.es',
#     'smtp_port': 465,
#     'sender_email': os.getenv('EMAIL_USER'),
#     'sender_password': os.getenv('EMAIL_PASSWORD'),
#     'recipient_email': 'jomma.tech@gmail.com'
# }
