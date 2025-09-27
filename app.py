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
        "mensaje": "Perfecto, estaremos encantados de ayudarte con el proceso de venta. ¿Necesitas información acerca de documentación y trámites necesarios?",
        "opciones": ["Sí, quiero información", "Continuar con el proceso"]
    },
    "comprar": {
        "titulo": "Comprar propiedad",
        "descripcion": "Encuentra la propiedad perfecta para ti",
        "mensaje": "Muy bien, puedes consultar los inmuebles disponibles en nuestra web. Si lo prefieres puedes elegir una de estas dos opciones:",
        "opciones": ["Continuar con atención personalizada", "Contactar directamente"]
    },
    "alquilar": {
        "titulo": "Alquilar propiedad",
        "descripcion": "Encuentra el lugar perfecto para alquilar",
        "mensaje": "¡Genial! Te ayudaremos a encontrar el lugar perfecto para alquilar. ¿Qué tipo de propiedad necesitas?",
        "opciones": ["Vivienda", "Terreno", "Nave industrial", "Local comercial"]
    },
    "alquilar_mi_propiedad": {
        "titulo": "Alquilar mi propiedad",
        "descripcion": "Renta tu propiedad de forma segura",
        "mensaje": "¡Excelente! Te ayudaremos a alquilar tu propiedad. ¿Qué tipo de propiedad quieres alquilar?",
        "opciones": ["Vivienda", "Terreno", "Nave industrial", "Local comercial"]
    }
}

# Preguntas frecuentes generales
preguntas_frecuentes = [
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

# Preguntas frecuentes específicas para vender propiedades
preguntas_frecuentes_vender = [
    {
        "pregunta": "¿Cuáles son los requisitos para vender una propiedad?",
        "respuesta": "Para vender una propiedad necesitas: escritura pública, certificado de libertad de gravamen, pago de impuestos al día, y documentación personal (DNI, recibo de servicios). En Metro Cuadrado Mérida te asesoramos en todo el proceso."
    },
    {
        "pregunta": "¿Qué documentos necesito para vender mi casa?",
        "respuesta": "Los documentos principales son: escritura de propiedad, certificado de libertad de gravamen, recibo de IBI al día, certificado energético, y documentación personal. Te ayudamos a obtener todo lo necesario."
    },
    {
        "pregunta": "¿Cuánto tiempo tarda en venderse una propiedad?",
        "respuesta": "El tiempo de venta depende del mercado y precio. En Metro Cuadrado Mérida trabajamos activamente para encontrar compradores cualificados. El proceso legal una vez encontrado comprador es de 30-45 días."
    },
    {
        "pregunta": "¿Cómo fijan el precio de mi propiedad?",
        "respuesta": "Realizamos una tasación profesional gratuita considerando ubicación, características, estado de conservación y valores del mercado en Mérida. Nuestros expertos conocen perfectamente la zona."
    },
    {
        "pregunta": "¿Qué gastos tengo al vender mi propiedad?",
        "respuesta": "Los gastos principales son: comisión inmobiliaria (3%), plusvalía municipal, gastos notariales y registrales. Te explicamos todos los costes de forma transparente antes de empezar."
    },
    {
        "pregunta": "¿Puedo vender mi casa si aún debo dinero al banco?",
        "respuesta": "Sí, es posible vender una propiedad con hipoteca. El dinero de la venta se usa para cancelar la deuda pendiente. Te asesoramos en todo el proceso de cancelación hipotecaria."
    }
]

# Función para enviar email
def enviar_email(datos_usuario, tipo_consulta):
    try:
        print(f"=== INICIO ENVÍO EMAIL ===")
        print(f"Intentando enviar email con configuración:")
        print(f"SMTP Server: {EMAIL_CONFIG['smtp_server']}")
        print(f"SMTP Port: {EMAIL_CONFIG['smtp_port']}")
        print(f"From: {EMAIL_CONFIG['sender_email']}")
        print(f"To: {EMAIL_CONFIG['recipient_email']}")
        print(f"Datos usuario: {datos_usuario}")
        print(f"Tipo consulta: {tipo_consulta}")
        
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
        - Email: {datos_usuario.get('email', 'No proporcionado') if datos_usuario.get('email') else 'No proporcionado'}
        - Tipo de propiedad: {datos_usuario.get('tipo_propiedad', 'No especificado')}
        - Zona: {datos_usuario.get('zona', 'No especificada')}
        - Presupuesto: {datos_usuario.get('presupuesto', 'No especificado') if datos_usuario.get('presupuesto') else 'No especificado'}
        - Comentarios adicionales: {datos_usuario.get('comentarios', 'Ninguno')}
        
        Por favor, contactar al cliente lo antes posible.
        
        Saludos,
        Sistema de Chatbot Metro Cuadrado Mérida
        """
        
        msg.attach(MIMEText(cuerpo, 'plain'))
        
        # Intentar solo puerto 587 con timeout reducido
        try:
            print("Intentando puerto 587 (STARTTLS)...")
            server = smtplib.SMTP(EMAIL_CONFIG['smtp_server'], 587, timeout=10)
            server.starttls()
            server.login(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['sender_password'])
            text = msg.as_string()
            server.sendmail(EMAIL_CONFIG['sender_email'], EMAIL_CONFIG['recipient_email'], text)
            server.quit()
            print("Email enviado exitosamente con puerto 587")
            return True
        except Exception as e:
            print(f"ERROR enviando email: {e}")
            print(f"Tipo de error: {type(e).__name__}")
            import traceback
            print(f"Traceback completo: {traceback.format_exc()}")
            return False
        
    except Exception as e:
        print(f"ERROR GENERAL enviando email: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        print(f"Traceback completo: {traceback.format_exc()}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje_usuario = data.get('mensaje', '').lower()
    
    # Debug: imprimir el mensaje recibido
    print(f"Mensaje recibido: '{data.get('mensaje', '')}' -> Convertido a: '{mensaje_usuario}'")
    
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
    
    # Manejo específico para opciones de vender
    mensaje_original = data.get('mensaje', '')
    print(f"Comparando mensaje original: '{mensaje_original}'")
    
    if mensaje_original == 'Sí, quiero información':
        print("Detectado: Sí, quiero información")
        return jsonify({
            'tipo': 'preguntas_frecuentes_vender',
            'mensaje': 'Aquí tienes información importante sobre el proceso de venta:',
            'preguntas': preguntas_frecuentes_vender
        })
    
    if mensaje_original == 'Continuar con el proceso':
        print("Detectado: Continuar con el proceso")
        return jsonify({
            'tipo': 'opcion_seleccionada',
            'mensaje': '¡Excelente! Para vender tu propiedad necesitamos algunos datos básicos. ¿Qué tipo de propiedad quieres vender?',
            'opciones': [{'id': tipo, 'texto': tipo} for tipo in ['Vivienda', 'Terreno', 'Nave industrial', 'Local comercial']],
            'contexto': 'vender_proceso'
        })
    
    # Manejo de tipos de propiedad para venta
    tipos_propiedad = ['Vivienda', 'Terreno', 'Nave industrial', 'Local comercial']
    if mensaje_original in tipos_propiedad:
        print(f"Detectado tipo de propiedad: {mensaje_original}")
        return jsonify({
            'tipo': 'opcion_seleccionada',
            'mensaje': f'Perfecto, has seleccionado {mensaje_original}. Para continuar con la venta, necesitamos más información. ¿En qué zona se encuentra tu propiedad?',
            'opciones': [{'id': zona, 'texto': zona} for zona in ['Centro', 'Norte', 'Bodegones-Sur', 'Nueva Ciudad', 'Sindicales']],
            'contexto': 'vender_zona'
        })
    
    # Manejo de zonas para venta
    zonas = ['Centro', 'Norte', 'Bodegones-Sur', 'Nueva Ciudad', 'Sindicales']
    if mensaje_original in zonas:
        print(f"Detectada zona: {mensaje_original}")
        return jsonify({
            'tipo': 'solicitar_datos',
            'mensaje': f'Excelente, zona {mensaje_original}. Queremos darte el mejor servicio. Necesitaremos algunos datos adicionales para que un asesor inmobiliario te pueda contactar sin ningún compromiso. ¿Cuál es tu nombre completo?'
        })
    
    # Manejo de datos del usuario (nombre, teléfono, comentarios)
    # Esto debería manejarse en el frontend, pero por seguridad agregamos validación básica
    if len(mensaje_original.strip()) > 0 and mensaje_original not in ['preguntas frecuentes', 'faq']:
        # Si es un mensaje de texto simple (probablemente datos del usuario), 
        # devolvemos una respuesta genérica para que el frontend lo procese
        return jsonify({
            'tipo': 'texto',
            'mensaje': 'Datos recibidos. Continuando con el proceso...'
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

@app.route('/api/faq-vender')
def get_faq_vender():
    return jsonify(preguntas_frecuentes_vender)

@app.route('/api/enviar-datos', methods=['POST'])
def enviar_datos():
    try:
        print("=== INICIO ENVIAR DATOS ===")
        data = request.get_json()
        print(f"Datos recibidos: {data}")
        
        # Validar datos requeridos
        if not data.get('nombre') or not data.get('telefono'):
            print("ERROR: Faltan datos requeridos (nombre o teléfono)")
            return jsonify({
                'success': False,
                'message': 'Nombre y teléfono son requeridos'
            }), 400
        
        print("Datos válidos, procediendo a enviar email...")
        # Enviar email
        email_enviado = enviar_email(data, data.get('tipo_consulta', 'Consulta general'))
        print(f"Resultado del envío de email: {email_enviado}")
        
        if email_enviado:
            print("Email enviado exitosamente")
            return jsonify({
                'success': True,
                'message': 'Datos enviados correctamente. Un asesor se pondrá en contacto contigo pronto.'
            })
        else:
            print("Error al enviar email")
            return jsonify({
                'success': False,
                'message': 'Error al enviar los datos. Por favor, intenta de nuevo.'
            }), 500
            
    except Exception as e:
        print(f"ERROR en enviar_datos: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({
            'success': False,
            'message': 'Error interno del servidor'
        }), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

# Para gunicorn en producción - Render necesita esta variable
application = app
