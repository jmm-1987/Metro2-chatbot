from flask import Flask, render_template, request, jsonify
import json
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
try:
    from config import EMAIL_CONFIG
except ImportError:
    from config_production import EMAIL_CONFIG

app = Flask(__name__)

# Datos de ejemplo para las opciones
opciones_principales = {
    "vender": {
        "titulo": "Vender mi propiedad",
        "descripcion": "Te ayudamos a vender tu propiedad al mejor precio",
        "mensaje": "¡Excelente decisión! Para vender tu propiedad necesitamos algunos datos básicos. ¿Qué tipo de propiedad quieres vender?",
        "opciones": ["Casa", "Departamento", "Terreno", "Local comercial", "Oficina"]
    },
    "comprar": {
        "titulo": "Comprar propiedad",
        "descripcion": "Encuentra la propiedad perfecta para ti",
        "mensaje": "¡Perfecto! Te ayudaremos a encontrar la propiedad ideal. ¿Qué tipo de propiedad buscas?",
        "opciones": ["Casa", "Departamento", "Terreno", "Local comercial", "Oficina"]
    },
    "alquilar": {
        "titulo": "Alquilar propiedad",
        "descripcion": "Encuentra el lugar perfecto para alquilar",
        "mensaje": "¡Genial! Te ayudaremos a encontrar el lugar perfecto para alquilar. ¿Qué tipo de propiedad necesitas?",
        "opciones": ["Casa", "Departamento", "Terreno", "Local comercial", "Oficina"]
    },
    "alquilar_mi_propiedad": {
        "titulo": "Alquilar mi propiedad",
        "descripcion": "Renta tu propiedad de forma segura",
        "mensaje": "¡Excelente! Te ayudaremos a alquilar tu propiedad. ¿Qué tipo de propiedad quieres alquilar?",
        "opciones": ["Casa", "Departamento", "Terreno", "Local comercial", "Oficina"]
    }
}

# Preguntas frecuentes
preguntas_frecuentes = [
    {
        "pregunta": "¿Cuáles son los requisitos para vender una propiedad?",
        "respuesta": "Para vender una propiedad necesitas: escritura pública, certificado de libertad de gravamen, pago de impuestos al día, y documentación personal (DNI, recibo de servicios). En Metro Cuadrado Mérida te asesoramos en todo el proceso."
    },
    {
        "pregunta": "¿Cuánto tiempo toma el proceso de compra?",
        "respuesta": "El proceso de compra puede tomar entre 30 a 60 días hábiles, dependiendo de la documentación y trámites necesarios. Nuestro equipo te acompañará en cada paso."
    },
    {
        "pregunta": "¿Qué comisión cobran por la venta?",
        "respuesta": "Nuestra comisión es del 3% sobre el valor de venta de la propiedad, solo se cobra cuando la operación se concreta exitosamente. Transparencia total en Metro Cuadrado Mérida."
    },
    {
        "pregunta": "¿Ofrecen financiamiento?",
        "respuesta": "Sí, trabajamos con los principales bancos de Mérida para ofrecerte las mejores opciones de financiamiento adaptadas a tu situación."
    },
    {
        "pregunta": "¿Cómo calculan el valor de mi propiedad?",
        "respuesta": "Realizamos una tasación profesional considerando ubicación en Mérida, características, estado de conservación y valores del mercado local. Nuestros expertos conocen perfectamente la zona."
    }
]

# Función para enviar email
def enviar_email(datos_usuario, tipo_consulta):
    try:
        # Crear mensaje
        msg = MIMEMultipart()
        msg['From'] = EMAIL_CONFIG['sender_email']
        msg['To'] = EMAIL_CONFIG['recipient_email']
        msg['Subject'] = f'Nueva consulta de {tipo_consulta} - Metro Cuadrado Mérida'
        
        # Crear cuerpo del email
        cuerpo = f"""
        Nueva consulta recibida desde el chatbot de Metro Cuadrado Mérida
        
        Tipo de consulta: {tipo_consulta}
        Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}
        
        Datos del cliente:
        - Nombre: {datos_usuario.get('nombre', 'No proporcionado')}
        - Teléfono: {datos_usuario.get('telefono', 'No proporcionado')}
        - Email: {datos_usuario.get('email', 'No proporcionado')}
        - Tipo de propiedad: {datos_usuario.get('tipo_propiedad', 'No especificado')}
        - Zona: {datos_usuario.get('zona', 'No especificada')}
        - Presupuesto: {datos_usuario.get('presupuesto', 'No especificado')}
        - Comentarios adicionales: {datos_usuario.get('comentarios', 'Ninguno')}
        
        Por favor, contactar al cliente lo antes posible.
        
        Saludos,
        Sistema de Chatbot Metro Cuadrado Mérida
        """
        
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        # Enviar email
        server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], EMAIL_CONFIG['smtp_port'])
        server.starttls()
        server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
        text = msg.as_string()
        server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['recipient_email'], text)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error enviando email: {e}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje_usuario = data.get('mensaje', '').lower()
    
    # Mensaje de bienvenida
    if mensaje_usuario in ['hola', 'hi', 'buenos días', 'buenas tardes', 'buenas noches', 'inicio', 'empezar']:
        return jsonify({
            'tipo': 'bienvenida',
            'mensaje': '¡Hola! Bienvenido a Metro Cuadrado Mérida. ¿En qué podemos ayudarte hoy?',
            'opciones': [
                {'id': 'vender', 'texto': 'Vender mi propiedad'},
                {'id': 'comprar', 'texto': 'Comprar propiedad'},
                {'id': 'alquilar', 'texto': 'Alquilar propiedad'},
                {'id': 'alquilar_mi_propiedad', 'texto': 'Alquilar mi propiedad'}
            ]
        })
    
    # Manejo de opciones principales
    for opcion_id, opcion_data in opciones_principales.items():
        if opcion_id in mensaje_usuario or opcion_data['titulo'].lower() in mensaje_usuario:
            return jsonify({
                'tipo': 'opcion_seleccionada',
                'mensaje': opcion_data['mensaje'],
                'opciones': [{'id': tipo, 'texto': tipo} for tipo in opcion_data['opciones']],
                'contexto': opcion_id
            })
    
    # Preguntas frecuentes
    if 'preguntas frecuentes' in mensaje_usuario or 'faq' in mensaje_usuario:
        return jsonify({
            'tipo': 'preguntas_frecuentes',
            'mensaje': 'Aquí tienes las preguntas más frecuentes:',
            'preguntas': preguntas_frecuentes
        })
    
    # Respuesta por defecto
    return jsonify({
        'tipo': 'texto',
        'mensaje': 'No entiendo tu consulta. Por favor, selecciona una de las opciones disponibles o escribe "preguntas frecuentes" para más información.'
    })

@app.route('/api/faq')
def get_faq():
    return jsonify(preguntas_frecuentes)

@app.route('/api/enviar-datos', methods=['POST'])
def enviar_datos():
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        if not data.get('nombre') or not data.get('telefono'):
            return jsonify({
                'success': False,
                'message': 'Nombre y teléfono son requeridos'
            }), 400
        
        # Enviar email
        email_enviado = enviar_email(data, data.get('tipo_consulta', 'Consulta general'))
        
        if email_enviado:
            return jsonify({
                'success': True,
                'message': 'Datos enviados correctamente. Un asesor se pondrá en contacto contigo pronto.'
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Error al enviar los datos. Por favor, intenta de nuevo.'
            }), 500
            
    except Exception as e:
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
else:
    # Para gunicorn en producción
    application = app
