# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import requests
import os
import random
try:
    from config import EMAIL_CONFIG
except ImportError:
    from config_production import EMAIL_CONFIG

app = Flask(__name__)

# Configurar CORS para permitir el widget en otros sitios web
CORS(app, resources={
    r"/*": {
        "origins": "*",  # Permite todos los orígenes (o especifica dominios concretos)
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})

# Variable global para rastrear el contexto actual del usuario
user_contexts = {}

# Mensajes variados para evitar repetición
MENSAJES_VARIADOS = {
    'bienvenida': [
        '¡Hola! Bienvenido a Metro Cuadrado Mérida. ¿En qué podemos ayudarte hoy?',
        '¡Hola! Es un placer recibirte en Metro Cuadrado Mérida. ¿Cómo puedo asistirte?',
        '¡Bienvenido! Gracias por contactar con Metro Cuadrado Mérida. ¿Qué necesitas hoy?'
    ],
    'vender': [
        'Perfecto, estaremos encantados de ayudarte con el proceso de venta. ¿Necesitas información acerca de documentación y trámites necesarios, o prefieres continuar con el proceso?',
        'Excelente decisión. Nos encantaría ayudarte a vender tu propiedad. ¿Quieres que te expliquemos los documentos que necesitas, o prefieres avanzar directamente con el proceso?',
        'Muy bien, te ayudaremos con la venta. ¿Te gustaría conocer los trámites y documentación requerida, o prefieres ir directamente al proceso de venta?'
    ],
    'comprar': [
        'Muy bien, puedes consultar los inmuebles disponibles en nuestra web. Si lo prefieres puedes elegir una de estas dos opciones:',
        'Perfecto, en nuestra web encontrarás todas las propiedades disponibles. También puedes seleccionar una de estas alternativas:',
        'Genial, te invitamos a ver nuestras propiedades en la web. O si lo prefieres, elige una de estas opciones:'
    ],
    'alquilar': [
        'Muy bien, puedes consultar las propiedades disponibles para alquilar en nuestra web. Si lo prefieres puedes elegir una de estas dos opciones:',
        'Perfecto, en nuestra web encontrarás todos los inmuebles en alquiler. También puedes seleccionar una de estas alternativas:',
        'Genial, te invitamos a ver las propiedades en alquiler en nuestra web. O si lo prefieres, elige una de estas opciones:'
    ],
    'alquilar_mi_propiedad': [
        '¡Excelente! Te ayudaremos a alquilar tu propiedad. ¿Qué tipo de propiedad quieres alquilar?',
        '¡Muy bien! Podemos ayudarte a rentar tu inmueble. ¿De qué tipo de propiedad se trata?',
        '¡Perfecto! Te asistiremos para alquilar tu propiedad. ¿Qué tipo de inmueble deseas rentar?'
    ],
    'info_venta': [
        'Aquí tienes información importante sobre el proceso de venta:',
        'Te muestro los datos más relevantes sobre la venta de propiedades:',
        'A continuación encontrarás información clave sobre el proceso de venta:'
    ],
    'continuar_proceso_venta': [
        '¡Excelente! Para vender tu propiedad necesitamos algunos datos básicos. ¿Qué tipo de propiedad quieres vender?',
        '¡Perfecto! Vamos a iniciar el proceso de venta. ¿Qué clase de propiedad deseas vender?',
        '¡Muy bien! Para empezar necesitamos saber qué tipo de inmueble quieres vender. ¿Cuál es?'
    ],
    'atencion_personalizada': [
        'Excelente. Continuemos con el proceso para brindarte asistencia personalizada. ¿Qué tipo de propiedad buscas?',
        'Perfecto. Vamos a ofrecerte atención personalizada. ¿Qué tipo de inmueble te interesa?',
        'Muy bien. Te daremos un servicio personalizado. ¿Qué clase de propiedad estás buscando?'
    ],
    'contacto_directo': [
        'Perfecto, aquí tienes nuestra información de contacto para que puedas hablar directamente con un asesor especializado.',
        'Excelente, te proporciono nuestros datos de contacto para que hables con uno de nuestros asesores expertos.',
        'Muy bien, aquí están nuestros contactos para que puedas comunicarte directamente con un profesional de nuestro equipo.'
    ],
    'tipo_propiedad_comprar': [
        'Excelente elección, {tipo}. ¿En qué zona te gustaría buscar?',
        'Perfecto, {tipo}. ¿En qué zona prefieres buscar tu propiedad?',
        'Muy buena opción, {tipo}. ¿Qué zona te interesa más?'
    ],
    'tipo_propiedad_alquilar': [
        'Excelente elección, {tipo}. ¿En qué zona te gustaría buscar?',
        'Perfecto, {tipo}. ¿En qué zona prefieres buscar el alquiler?',
        'Muy buena opción, {tipo}. ¿Qué zona te interesa para alquilar?'
    ],
    'tipo_propiedad_alquilar_mi': [
        'Perfecto, has seleccionado {tipo}. Para continuar con el alquiler de tu propiedad, necesitamos más información. ¿En qué zona se encuentra?',
        'Excelente, {tipo}. Para avanzar con el proceso de alquiler, necesitamos algunos datos más. ¿En qué zona está ubicada?',
        'Muy bien, {tipo}. Necesitamos más detalles para alquilar tu inmueble. ¿En qué zona se encuentra?'
    ],
    'tipo_propiedad_vender': [
        'Perfecto, has seleccionado {tipo}. Para continuar con la venta, necesitamos más información. ¿En qué zona se encuentra tu propiedad?',
        'Excelente, {tipo}. Para avanzar con el proceso de venta, necesitamos algunos datos más. ¿En qué zona está ubicada?',
        'Muy bien, {tipo}. Necesitamos más detalles para la venta. ¿En qué zona se encuentra tu inmueble?'
    ],
    'zona_comprar': [
        'Perfecto, zona {zona}. Esta información es muy valiosa para nosotros ya que podemos trabajar en tu caso antes de contactarte. Ahora necesitamos algunos datos de contacto. ¿Cuál es tu nombre completo?',
        'Excelente, zona {zona}. Con esta información podremos preparar opciones antes de contactarte. Por favor, dinos ¿cuál es tu nombre completo?',
        'Muy bien, zona {zona}. Esto nos ayudará a buscar las mejores opciones para ti. ¿Podrías indicarnos tu nombre completo?'
    ],
    'zona_alquilar': [
        'Perfecto, zona {zona}. Esta información nos ayudará a preparar opciones de alquiler antes de contactarte. Ahora necesitamos algunos datos de contacto. ¿Cuál es tu nombre completo?',
        'Excelente, zona {zona}. Con esto podremos buscar las mejores opciones de alquiler para ti. Por favor, dinos ¿cuál es tu nombre completo?',
        'Muy bien, zona {zona}. Esto nos ayudará a encontrar el alquiler perfecto. ¿Podrías indicarnos tu nombre completo?'
    ],
    'zona_alquilar_mi': [
        'Excelente, zona {zona}. Queremos darte el mejor servicio para alquilar tu propiedad. Necesitaremos algunos datos adicionales para que un asesor te pueda contactar sin ningún compromiso. ¿Cuál es tu nombre completo?',
        'Perfecto, zona {zona}. Para ofrecerte la mejor atención en el alquiler de tu inmueble, necesitamos algunos datos de contacto. Un asesor se pondrá en contacto contigo. ¿Cuál es tu nombre completo?',
        'Muy bien, zona {zona}. Nos gustaría poder contactarte sin compromiso para ayudarte con el alquiler. Necesitamos algunos datos. ¿Cuál es tu nombre completo?'
    ],
    'zona_vender': [
        'Excelente, zona {zona}. Queremos darte el mejor servicio. Necesitaremos algunos datos adicionales para que un asesor inmobiliario te pueda contactar sin ningún compromiso. ¿Cuál es tu nombre completo?',
        'Perfecto, zona {zona}. Para ofrecerte la mejor atención, necesitamos algunos datos de contacto. Un asesor se pondrá en contacto contigo. ¿Cuál es tu nombre completo?',
        'Muy bien, zona {zona}. Nos gustaría poder contactarte sin compromiso. Necesitamos algunos datos. ¿Cuál es tu nombre completo?'
    ],
    'datos_recibidos': [
        'Datos recibidos. Continuando con el proceso...',
        'Información recibida. Procesando tus datos...',
        'Datos guardados. Avanzando con el proceso...'
    ],
    'preguntas_frecuentes': [
        'Aquí tienes las preguntas más frecuentes:',
        'Te muestro las consultas más comunes:',
        'Estas son las preguntas que más nos hacen:'
    ],
    'no_entiendo': [
        'No entiendo tu consulta. Por favor, selecciona una de las opciones disponibles o escribe "preguntas frecuentes" para más información.',
        'Disculpa, no he comprendido tu mensaje. Por favor, elige una opción del menú o escribe "preguntas frecuentes" para ayudarte.',
        'Perdona, no entiendo lo que me indicas. Selecciona una de las opciones que te muestro o escribe "preguntas frecuentes" para más detalles.'
    ],
    'datos_enviados_exito': [
        'Datos enviados correctamente. Un asesor se pondrá en contacto contigo pronto.',
        'Información recibida con éxito. Pronto recibirás la llamada de uno de nuestros asesores.',
        '¡Perfecto! Tus datos han sido enviados. Un especialista te contactará en breve.'
    ],
    'error_envio': [
        'Error al enviar los datos. Por favor, intenta de nuevo.',
        'Ha ocurrido un problema al enviar tu información. Por favor, inténtalo nuevamente.',
        'No hemos podido enviar tus datos. Por favor, intenta otra vez.'
    ],
    'faltan_datos': [
        'Nombre y teléfono son requeridos',
        'Por favor, proporciona tu nombre y teléfono',
        'Necesitamos tu nombre y número de teléfono para continuar'
    ]
}

def obtener_mensaje(clave, **kwargs):
    """Obtiene un mensaje aleatorio de las alternativas disponibles y reemplaza variables"""
    mensajes = MENSAJES_VARIADOS.get(clave, [''])
    mensaje = random.choice(mensajes)
    if kwargs:
        mensaje = mensaje.format(**kwargs)
    return mensaje

# Datos de ejemplo para las opciones
opciones_principales = {
    "vender": {
        "titulo": "Vender mi propiedad",
        "descripcion": "Te ayudamos a vender tu propiedad al mejor precio",
        "mensaje_clave": "vender",
        "opciones": ["Sí, quiero información", "Continuar con el proceso"]
    },
    "comprar": {
        "titulo": "Comprar propiedad",
        "descripcion": "Encuentra la propiedad perfecta para ti",
        "mensaje_clave": "comprar",
        "opciones": ["Seguir con el proceso", "Contactar directamente"]
    },
    "alquilar": {
        "titulo": "Alquilar propiedad",
        "descripcion": "Encuentra el lugar perfecto para alquilar",
        "mensaje_clave": "alquilar",
        "opciones": ["Seguir con el proceso", "Contactar directamente"]
    },
    "alquilar_mi_propiedad": {
        "titulo": "Alquilar mi propiedad",
        "descripcion": "Renta tu propiedad de forma segura",
        "mensaje_clave": "alquilar_mi_propiedad",
        "opciones": ["Vivienda", "Local comercial","Nave industrial", "Terreno", "Finca Rústica"]
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

# Función para enviar email usando EmailJS API
def enviar_email(datos_usuario, tipo_consulta):
    try:
        print(f"=== INICIO ENVÍO EMAIL (EmailJS) ===")
        print(f"Intentando enviar email con EmailJS API...")
        print(f"Service ID: {EMAIL_CONFIG['emailjs_service_id']}")
        print(f"Template ID: {EMAIL_CONFIG['emailjs_template_id']}")
        print(f"User ID: {EMAIL_CONFIG['emailjs_user_id']}")
        print(f"Private Key: {'*' * 10}...{EMAIL_CONFIG['emailjs_private_key'][-4:] if EMAIL_CONFIG.get('emailjs_private_key') else 'No configurada'}")
        print(f"From: {EMAIL_CONFIG['sender_email']}")
        print(f"To: {EMAIL_CONFIG['recipient_email']}")
        print(f"Datos usuario: {datos_usuario}")
        print(f"Tipo consulta: {tipo_consulta}")

        # Preparar los datos para la plantilla de EmailJS
        template_params = {
            "from_name": datos_usuario.get('nombre', 'Anonimo'),
            "from_email": datos_usuario.get('email', EMAIL_CONFIG['sender_email']),
            "to_email": EMAIL_CONFIG['recipient_email'],
            "subject": f"Nueva consulta de {tipo_consulta} - Metro Cuadrado Merida",
            "message": f"""
Nueva consulta recibida desde el chatbot de Metro Cuadrado Merida

Tipo de consulta: {tipo_consulta}
Fecha: {datetime.now().strftime('%d/%m/%Y %H:%M')}

Datos del cliente:
- Nombre: {datos_usuario.get('nombre', 'No proporcionado')}
- Telefono: {datos_usuario.get('telefono', 'No proporcionado')}
- Email: {datos_usuario.get('email', 'No proporcionado') if datos_usuario.get('email') else 'No proporcionado'}
- Tipo de propiedad: {datos_usuario.get('tipo_propiedad', 'No especificado')}
- Zona: {datos_usuario.get('zona', 'No especificada')}
- Presupuesto: {datos_usuario.get('presupuesto', 'No especificado') if datos_usuario.get('presupuesto') else 'No especificado'}
- Comentarios adicionales: {datos_usuario.get('comentarios', 'Ninguno')}

Por favor, contactar al cliente lo antes posible.

Saludos,
Sistema de Chatbot Metro Cuadrado Merida
            """,
            "tipo_consulta": tipo_consulta,
            "tipo_propiedad": datos_usuario.get('tipo_propiedad', 'No especificado'),
            "zona": datos_usuario.get('zona', 'No especificada'),
            "nombre": datos_usuario.get('nombre', 'No proporcionado'),
            "telefono": datos_usuario.get('telefono', 'No proporcionado'),
            "email_cliente": datos_usuario.get('email', 'No proporcionado'),
            "presupuesto": datos_usuario.get('presupuesto', 'No especificado'),
            "comentarios": datos_usuario.get('comentarios', 'Ninguno')
        }

        # Estructura de la solicitud a la API de EmailJS
        emailjs_data = {
            "service_id": EMAIL_CONFIG['emailjs_service_id'],
            "template_id": EMAIL_CONFIG['emailjs_template_id'],
            "user_id": EMAIL_CONFIG['emailjs_user_id'],
            "accessToken": EMAIL_CONFIG.get('emailjs_private_key', ''),
            "template_params": template_params
        }

        print("Enviando solicitud a EmailJS API...")
        # Realizar la solicitud POST a la API de EmailJS
        response = requests.post("https://api.emailjs.com/api/v1.0/email/send", 
                               json=emailjs_data, 
                               timeout=30,
                               headers={
                                   'Content-Type': 'application/json; charset=utf-8'
                               })

        print(f"Respuesta de EmailJS - Código: {response.status_code}")
        print(f"Respuesta de EmailJS - Texto: {response.text}")

        if response.status_code == 200:
            print("✅ Email enviado exitosamente con EmailJS")
            return True
        else:
            print(f"❌ Error enviando email con EmailJS. Código de estado: {response.status_code}")
            print(f"Respuesta de EmailJS: {response.text}")
            return False

    except requests.exceptions.Timeout:
        print("❌ Error de Timeout al conectar con EmailJS.")
        import traceback
        print(f"Traceback completo: {traceback.format_exc()}")
        return False
    except Exception as e:
        print(f"❌ ERROR GENERAL enviando email con EmailJS: {e}")
        print(f"Tipo de error: {type(e).__name__}")
        import traceback
        print(f"Traceback completo: {traceback.format_exc()}")
        return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ejemplo-integracion')
def ejemplo_integracion():
    return render_template('ejemplo_integracion.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    mensaje_usuario = data.get('mensaje', '').lower()
    mensaje_original = data.get('mensaje', '')
    
    # Obtener IP del cliente para rastrear contexto (simplificado)
    client_ip = request.remote_addr
    
    # Debug: imprimir el mensaje recibido
    print(f"Mensaje recibido: '{mensaje_original}' -> Convertido a: '{mensaje_usuario}'")
    print(f"Contexto actual para IP {client_ip}: {user_contexts.get(client_ip, 'Ninguno')}")
    
    # Mensaje de bienvenida
    if mensaje_usuario in ['hola', 'hi', 'buenos días', 'buenas tardes', 'buenas noches', 'inicio', 'empezar']:
        return jsonify({
            'tipo': 'bienvenida',
            'mensaje': obtener_mensaje('bienvenida'),
            'opciones': [
                {'id': 'vender', 'texto': 'Vender mi propiedad'},
                {'id': 'comprar', 'texto': 'Comprar propiedad'},
                {'id': 'alquilar', 'texto': 'Alquilar propiedad'},
                {'id': 'alquilar_mi_propiedad', 'texto': 'Alquilar mi propiedad'}
            ]
        })
    
    # Manejo de opciones principales (comparación exacta para evitar confusiones)
    for opcion_id, opcion_data in opciones_principales.items():
        if mensaje_usuario == opcion_id or opcion_data['titulo'].lower() == mensaje_usuario:
            # Establecer contexto del usuario
            user_contexts[client_ip] = opcion_id
            print(f"Estableciendo contexto para IP {client_ip}: {opcion_id}")
            
            return jsonify({
                'tipo': 'opcion_seleccionada',
                'mensaje': obtener_mensaje(opcion_data['mensaje_clave']),
                'opciones': [{'id': tipo, 'texto': tipo} for tipo in opcion_data['opciones']],
                'contexto': opcion_id
            })
    
    # Manejo específico para opciones de vender
    print(f"Comparando mensaje original: '{mensaje_original}'")
    
    if mensaje_original == 'Sí, quiero información':
        print("Detectado: Sí, quiero información")
        return jsonify({
            'tipo': 'preguntas_frecuentes_vender',
            'mensaje': obtener_mensaje('info_venta'),
            'preguntas': preguntas_frecuentes_vender
        })
    
    if mensaje_original == 'Continuar con el proceso':
        print("Detectado: Continuar con el proceso")
        return jsonify({
            'tipo': 'opcion_seleccionada',
            'mensaje': obtener_mensaje('continuar_proceso_venta'),
            'opciones': [{'id': tipo, 'texto': tipo} for tipo in ['Vivienda', 'Local comercial', 'Nave industrial', 'Terreno', 'Finca Rústica']],
            'contexto': 'vender_proceso'
        })
    
    # Manejo específico para opciones de comprar y alquilar
    if mensaje_original == 'Seguir con el proceso':
        # Obtener contexto del usuario para saber si es comprar o alquilar
        contexto_usuario = user_contexts.get(client_ip, 'comprar')
        print(f"Detectado: Seguir con el proceso ({contexto_usuario})")
        
        if contexto_usuario == 'alquilar':
            contexto_proceso = 'alquilar_proceso'
        else:  # comprar por defecto
            contexto_proceso = 'comprar_proceso'
        
        return jsonify({
            'tipo': 'opcion_seleccionada',
            'mensaje': obtener_mensaje('atencion_personalizada'),
            'opciones': [{'id': tipo, 'texto': tipo} for tipo in ['Vivienda', 'Local comercial', 'Nave industrial','Terreno', 'Finca Rústica']],
            'contexto': contexto_proceso
        })
    
    if mensaje_original == 'Contactar directamente':
        print("Detectado: Contactar directamente")
        return jsonify({
            'tipo': 'contacto_directo',
            'mensaje': obtener_mensaje('contacto_directo')
        })
    
    # Manejo de tipos de propiedad (para venta, compra y alquiler)
    tipos_propiedad = ['Vivienda', 'Local comercial','Nave industrial', 'Terreno', 'Finca Rústica']
    if mensaje_original in tipos_propiedad:
        print(f"Detectado tipo de propiedad: {mensaje_original}")
        
        # Obtener contexto del usuario
        contexto_usuario = user_contexts.get(client_ip, 'vender')
        print(f"Contexto del usuario: {contexto_usuario}")
        
        # Determinar el contexto y mensaje según la opción principal seleccionada
        if contexto_usuario == 'comprar':
            contexto_actual = 'comprar_zona'
            mensaje = obtener_mensaje('tipo_propiedad_comprar', tipo=mensaje_original)
        elif contexto_usuario == 'alquilar':
            contexto_actual = 'alquilar_zona'
            mensaje = obtener_mensaje('tipo_propiedad_alquilar', tipo=mensaje_original)
        elif contexto_usuario == 'alquilar_mi_propiedad':
            contexto_actual = 'alquilar_mi_zona'
            mensaje = obtener_mensaje('tipo_propiedad_alquilar_mi', tipo=mensaje_original)
        else:  # vender por defecto
            contexto_actual = 'vender_zona'
            mensaje = obtener_mensaje('tipo_propiedad_vender', tipo=mensaje_original)
        
        return jsonify({
            'tipo': 'opcion_seleccionada',
            'mensaje': mensaje,
            'opciones': [{'id': zona, 'texto': zona} for zona in ['Centro', 'Norte', 'Bodegones-Sur', 'Nueva Ciudad', 'Sindicales']],
            'contexto': contexto_actual
        })
    
    # Manejo de zonas (para venta, compra y alquiler)
    zonas = ['Centro', 'Norte', 'Bodegones-Sur', 'Nueva Ciudad', 'Sindicales']
    if mensaje_original in zonas:
        print(f"Detectada zona: {mensaje_original}")
        
        # Obtener contexto del usuario
        contexto_usuario = user_contexts.get(client_ip, 'vender')
        print(f"Contexto del usuario para zona: {contexto_usuario}")
        
        # Mensaje según el contexto
        if contexto_usuario == 'comprar':
            mensaje = obtener_mensaje('zona_comprar', zona=mensaje_original)
        elif contexto_usuario == 'alquilar':
            mensaje = obtener_mensaje('zona_alquilar', zona=mensaje_original)
        elif contexto_usuario == 'alquilar_mi_propiedad':
            mensaje = obtener_mensaje('zona_alquilar_mi', zona=mensaje_original)
        else:  # vender por defecto
            mensaje = obtener_mensaje('zona_vender', zona=mensaje_original)
        
        return jsonify({
            'tipo': 'solicitar_datos',
            'mensaje': mensaje
        })
    
    # Manejo de datos del usuario (nombre, teléfono, comentarios)
    # Esto debería manejarse en el frontend, pero por seguridad agregamos validación básica
    if len(mensaje_original.strip()) > 0 and mensaje_original not in ['preguntas frecuentes', 'faq']:
        # Si es un mensaje de texto simple (probablemente datos del usuario), 
        # devolvemos una respuesta genérica para que el frontend lo procese
        return jsonify({
            'tipo': 'texto',
            'mensaje': obtener_mensaje('datos_recibidos')
        })
    
    # Preguntas frecuentes
    if 'preguntas frecuentes' in mensaje_usuario or 'faq' in mensaje_usuario:
        return jsonify({
            'tipo': 'preguntas_frecuentes',
            'mensaje': obtener_mensaje('preguntas_frecuentes'),
            'preguntas': preguntas_frecuentes
        })
    
    # Respuesta por defecto
    return jsonify({
        'tipo': 'texto',
        'mensaje': obtener_mensaje('no_entiendo')
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
                'message': obtener_mensaje('faltan_datos')
            }), 400
        
        print("Datos válidos, procediendo a enviar email...")
        # Enviar email
        email_enviado = enviar_email(data, data.get('tipo_consulta', 'Consulta general'))
        print(f"Resultado del envío de email: {email_enviado}")
        
        if email_enviado:
            print("Email enviado exitosamente")
            return jsonify({
                'success': True,
                'message': obtener_mensaje('datos_enviados_exito')
            })
        else:
            print("Error al enviar email")
            return jsonify({
                'success': False,
                'message': obtener_mensaje('error_envio')
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
