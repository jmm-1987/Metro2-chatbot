# 🛡️ Configuración CORS - Chatbot Metro Cuadrado Mérida

## ¿Qué es CORS?

**CORS** (Cross-Origin Resource Sharing) es un mecanismo de seguridad de los navegadores que controla qué sitios web pueden acceder a recursos de tu servidor.

### Problema sin CORS:
```
Navegador: "¿Puedo cargar widget.js desde chatbot.render.com?"
Servidor: "No tengo configuración CORS, ¡bloqueado!"
❌ Error: CORS policy blocked
```

### Con CORS habilitado:
```
Navegador: "¿Puedo cargar widget.js desde chatbot.render.com?"
Servidor: "¡Sí! Header Access-Control-Allow-Origin: *"
✅ Widget funciona perfectamente
```

---

## 🔧 Configuración Actual

Tu aplicación está configurada con **CORS permisivo** para máxima compatibilidad:

```python
CORS(app, resources={
    r"/*": {
        "origins": "*",  # ✅ Permite TODOS los dominios
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
        "expose_headers": ["Content-Type"],
        "supports_credentials": False
    }
})
```

### ¿Qué significa esto?

| Parámetro | Valor | Significado |
|-----------|-------|-------------|
| `origins: "*"` | Todos | Cualquier web puede cargar el widget |
| `methods` | GET, POST, OPTIONS | Métodos HTTP permitidos |
| `allow_headers` | Content-Type | Headers que el cliente puede enviar |
| `supports_credentials` | False | No se envían cookies entre dominios |

---

## 🎯 Casos de Uso

### 1️⃣ **Configuración Actual (Recomendada para empezar)**
```python
"origins": "*"  # ✅ Funciona en cualquier sitio
```

**Ventajas:**
- ✅ Funciona inmediatamente en cualquier web
- ✅ No necesitas actualizar configuración cada vez
- ✅ Perfecto para demos y pruebas
- ✅ Ideal si trabajas con múltiples clientes

**Desventajas:**
- ⚠️ Cualquier sitio web puede embeber tu chatbot
- ⚠️ Posible uso no autorizado

---

### 2️⃣ **Solo tu dominio (Más seguro)**
```python
"origins": ["https://www.m2merida.com"]
```

**Cuándo usar:**
- Si solo quieres el widget en TU web oficial
- Máxima seguridad
- Evitar uso no autorizado

**Cómo aplicar:**
Edita `app.py` línea 17-25:
```python
CORS(app, resources={
    r"/*": {
        "origins": ["https://www.m2merida.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
    }
})
```

---

### 3️⃣ **Múltiples dominios específicos**
```python
"origins": [
    "https://www.m2merida.com",
    "https://m2merida.com",
    "https://inmobiliaria-ejemplo.com"
]
```

**Cuándo usar:**
- Si tienes varios sitios web
- Si trabajas con partners específicos
- Balance entre seguridad y flexibilidad

---

## 🔍 Verificar que CORS funciona

### Método 1: Consola del navegador
1. Abre tu web (donde está el widget)
2. Presiona F12 → Consola
3. Si NO hay errores CORS = ✅ Funciona
4. Si ves `CORS policy blocked` = ❌ Necesitas ajustar

### Método 2: Herramientas online
```bash
curl -H "Origin: https://ejemplo.com" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS --verbose \
     https://tu-chatbot.onrender.com/static/js/widget.js
```

Busca en la respuesta:
```
Access-Control-Allow-Origin: *
```

---

## 🚨 Solución de Problemas

### Error: "CORS policy: No 'Access-Control-Allow-Origin' header"

**Causa:** CORS no está configurado o mal configurado

**Solución:**
1. Verifica que `Flask-CORS==4.0.0` esté en `requirements.txt`
2. Verifica que `from flask_cors import CORS` esté en `app.py`
3. Verifica que `CORS(app, ...)` esté DESPUÉS de `app = Flask(__name__)`
4. Haz commit y push a Render
5. Espera que se redespliegue (2-3 minutos)

---

### Error: "CORS policy: The 'Access-Control-Allow-Origin' header contains multiple values"

**Causa:** CORS configurado en múltiples lugares

**Solución:**
- Asegúrate de tener UNA sola configuración CORS en `app.py`
- No configures CORS en nginx u otros proxies si usas Flask-CORS

---

### El widget funciona en localhost pero no en producción

**Causa:** Configuración diferente entre local y producción

**Solución:**
1. Verifica que los cambios estén en GitHub
2. Verifica que Render haya desplegado la última versión
3. Limpia caché del navegador (Ctrl + Shift + R)
4. Revisa logs de Render para errores

---

## 📋 Checklist de Despliegue

Antes de desplegar con CORS:

- [ ] `Flask-CORS==4.0.0` agregado a `requirements.txt`
- [ ] `from flask_cors import CORS` en `app.py`
- [ ] `CORS(app, ...)` configurado después de crear la app
- [ ] Decisión tomada: ¿Permitir todos los orígenes o solo específicos?
- [ ] Commit y push a GitHub
- [ ] Esperado despliegue en Render
- [ ] Probado en navegador (F12 → sin errores CORS)
- [ ] Widget funciona correctamente desde otro dominio

---

## 🔒 Recomendaciones de Seguridad

### Para Producción:
1. **Empieza permisivo** (`origins: "*"`) para verificar que todo funciona
2. **Monitorea el uso** durante unos días
3. **Restringe después** a dominios específicos si es necesario

### Si usas `origins: "*"`:
- ✅ No hay datos sensibles en las respuestas del chatbot
- ✅ El chatbot es público de todas formas
- ✅ No hay información privada en los mensajes
- ✅ Los datos de contacto ya son públicos

### Restricciones adicionales (opcional):
```python
# Limitar tasa de peticiones (rate limiting)
# Validar origen en el backend
# Registrar qué dominios usan el widget
```

---

## 📚 Referencias

- [Documentación Flask-CORS](https://flask-cors.readthedocs.io/)
- [MDN Web Docs - CORS](https://developer.mozilla.org/es/docs/Web/HTTP/CORS)
- [Render - CORS Configuration](https://render.com/docs/cors)

---

## ✅ Estado Actual

**Configuración:** CORS Habilitado - Permisivo (`origins: "*"`)

**Funciona desde:**
- ✅ Cualquier sitio web
- ✅ Localhost durante desarrollo
- ✅ Dominios en HTTP y HTTPS
- ✅ Subdominios

**Archivos modificados:**
- ✅ `requirements.txt` - Flask-CORS agregado
- ✅ `app.py` - CORS configurado
- ✅ Listo para desplegar en Render

---

🎉 **¡Tu chatbot ahora funciona desde cualquier sitio web!**
