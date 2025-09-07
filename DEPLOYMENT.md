# 🚀 Guía de Despliegue en Render

## 📋 Pasos para Desplegar el Chatbot de Metro Cuadrado Mérida

### 1. **Preparar el Repositorio**

1. Sube todos los archivos a GitHub
2. Asegúrate de que estos archivos estén incluidos:
   - `app.py`
   - `requirements.txt`
   - `render.yaml`
   - `Procfile`
   - `runtime.txt`
   - `config_production.py`
   - `templates/` (carpeta completa)
   - `static/` (carpeta completa)

### 2. **Crear Servicio en Render**

1. Ve a [render.com](https://render.com)
2. Conecta tu cuenta de GitHub
3. Haz clic en "New +" → "Web Service"
4. Conecta tu repositorio
5. Configura el servicio:
   - **Name**: `metro-cuadrado-chatbot`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python app.py`
   - **Plan**: Free (para empezar)

### 3. **Configurar Variables de Entorno**

En el dashboard de Render, ve a tu servicio → "Environment" y agrega:

```
EMAIL_USER=tu_email@gmail.com
EMAIL_PASSWORD=tu_app_password_de_gmail
FLASK_ENV=production
PORT=10000
```

### 4. **Configurar Gmail para Envío de Emails**

1. **Habilitar verificación en 2 pasos:**
   - Ve a tu cuenta de Google
   - Seguridad → Verificación en 2 pasos
   - Actívala si no está activada

2. **Generar contraseña de aplicación:**
   - Ve a Seguridad → Contraseñas de aplicaciones
   - Selecciona "Correo" y "Otro (nombre personalizado)"
   - Escribe "Metro Cuadrado Chatbot"
   - Copia la contraseña generada (16 caracteres)

3. **Usar la contraseña en Render:**
   - En las variables de entorno de Render
   - `EMAIL_USER`: tu email de Gmail
   - `EMAIL_PASSWORD`: la contraseña de aplicación generada

### 5. **Desplegar**

1. Haz clic en "Create Web Service"
2. Render comenzará a construir y desplegar tu aplicación
3. El proceso tomará unos minutos
4. Una vez completado, tendrás una URL como: `https://metro-cuadrado-chatbot.onrender.com`

### 6. **Verificar el Despliegue**

1. Abre la URL de tu aplicación
2. Prueba el chatbot:
   - Selecciona una opción
   - Completa el formulario
   - Verifica que se envíe el email

### 7. **Configurar Dominio Personalizado (Opcional)**

Si tienes un dominio personalizado:
1. Ve a tu servicio en Render
2. Settings → Custom Domains
3. Agrega tu dominio
4. Configura los DNS según las instrucciones

## 🔧 Archivos de Configuración

### `render.yaml`
```yaml
services:
  - type: web
    name: metro-cuadrado-chatbot
    env: python
    plan: free
    buildCommand: pip install -r requirements.txt
    startCommand: python app.py
    envVars:
      - key: FLASK_ENV
        value: production
      - key: PORT
        value: 10000
```

### `requirements.txt`
```
Flask==2.3.3
Werkzeug==2.3.7
Jinja2==3.1.2
MarkupSafe==2.1.3
itsdangerous==2.1.2
click==8.1.7
blinker==1.6.3
email-validator==2.1.0
```

## 🚨 Solución de Problemas

### Error de Email
- Verifica que las variables de entorno estén configuradas
- Asegúrate de usar la contraseña de aplicación, no tu contraseña normal
- Verifica que la verificación en 2 pasos esté activada

### Error de Build
- Verifica que `requirements.txt` esté en la raíz del proyecto
- Asegúrate de que todos los archivos estén subidos a GitHub

### Error de Puerto
- Render asigna automáticamente el puerto
- El código ya está configurado para usar `os.environ.get('PORT')`

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Render Dashboard
2. Verifica las variables de entorno
3. Asegúrate de que todos los archivos estén en el repositorio

¡Tu chatbot estará listo para usar en producción! 🎉
