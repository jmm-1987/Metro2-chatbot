# 🚀 Guía de Integración del Chatbot Metro Cuadrado Mérida

## 📱 Dos Formas de Uso

### 1️⃣ **Código QR (Para puerta del negocio)**

Los clientes escanean el QR y acceden directamente a la aplicación completa en su móvil.

**URL para el QR:**
```
https://tu-dominio-render.com
```

**Ventajas:**
- ✅ Versión fullscreen optimizada para móviles
- ✅ Totalmente responsive
- ✅ Experiencia completa sin distracciones
- ✅ Ya está funcionando, no requiere cambios

**Cómo generar el QR:**
1. Ve a https://www.qr-code-generator.com/
2. Pega la URL de tu aplicación en Render
3. Descarga el QR en alta resolución
4. Imprímelo y colócalo en la puerta del negocio

---

### 2️⃣ **Widget Flotante (Para web de la inmobiliaria)**

Integra el chatbot en la web existente mediante un botón flotante que abre una ventana con iframe.

## 🔧 Integración en la Web Existente

### **Opción A: Integración Rápida (Recomendada)**

Añade una sola línea de código antes de `</body>` en tu web:

```html
<!-- Chatbot Metro Cuadrado Mérida -->
<script src="https://tu-dominio-render.com/static/js/widget.js"></script>
<!-- Fin Chatbot -->
```

**¡Eso es todo!** El botón flotante aparecerá automáticamente en la esquina inferior derecha.

---

### **Opción B: Configuración Personalizada**

Si quieres personalizar el widget, descarga el archivo `widget.js` y modifica estas opciones:

```javascript
const config = {
    buttonColor: '#d4af37',           // Color del botón
    buttonPosition: 'bottom-right',   // Posición: 'bottom-right' o 'bottom-left'
    buttonText: '💬',                 // Emoji o texto del botón
    chatbotUrl: 'URL_DEL_CHATBOT',   // URL de tu chatbot
    zIndex: 9999                      // Z-index del widget
};
```

---

## 🎨 Características del Widget

- ✅ **Botón flotante elegante** con animación de pulso
- ✅ **Totalmente responsive** - se adapta a móviles, tablets y desktop
- ✅ **Ligero y rápido** - menos de 10KB, no afecta la velocidad de carga
- ✅ **Animaciones suaves** - experiencia de usuario profesional
- ✅ **Colores corporativos** de Metro Cuadrado Mérida
- ✅ **Fácil de cerrar** - click en X o en el botón flotante
- ✅ **Compatible con todos los navegadores** modernos

---

## 📋 Cómo se Ve

### En Desktop:
```
┌─────────────────────────────┐
│                             │
│   TU PÁGINA WEB ACTUAL      │
│                             │
│                             │
│                         ┌───┤
│                         │ 💬 │ ← Botón flotante
│                         └───┤
└─────────────────────────────┘
```

Al hacer clic:
```
┌─────────────────────────────┐
│                             │
│   TU PÁGINA WEB ACTUAL      │
│                    ┌────────┤
│                    │CHATBOT │
│                    │        │
│                    │ [Chat] │
│                    │        │
│                    │   ✕    │
│                    └────────┤
│                         ┌───┤
│                         │ ✕ │ ← Click para cerrar
│                         └───┤
└─────────────────────────────┘
```

### En Móvil:
El chatbot ocupa casi toda la pantalla con un diseño optimizado.

---

## 🧪 Probar el Widget

Visita la página de ejemplo incluida en el proyecto:

```
https://tu-dominio-render.com/ejemplo-integracion
```

Esta página muestra:
- ✅ Cómo se ve el widget en acción
- ✅ El código exacto para copiar y pegar
- ✅ Instrucciones paso a paso
- ✅ Opciones avanzadas

---

## 🔌 Control Programático (Opcional)

Si necesitas controlar el widget desde JavaScript de tu web:

```javascript
// Abrir el chat programáticamente
M2ChatbotWidget.open();

// Cerrar el chat
M2ChatbotWidget.close();

// Alternar (abrir si está cerrado, cerrar si está abierto)
M2ChatbotWidget.toggle();
```

**Ejemplo de uso:**
```html
<!-- Botón personalizado en tu web -->
<button onclick="M2ChatbotWidget.open()">
    ¿Necesitas ayuda? Habla con nuestro asistente
</button>
```

---

## 🛠️ Solución de Problemas

### El botón no aparece
1. Verifica que el script esté antes de `</body>`
2. Revisa la consola del navegador (F12) para ver errores
3. Asegúrate de que la URL del chatbot sea correcta

### El chatbot no carga en el iframe
1. Verifica que tu servidor de Render esté activo
2. Revisa que no haya restricciones de CORS
3. Comprueba que la URL en `widget.js` sea correcta

### El botón se ve cortado o fuera de lugar
1. Verifica que no haya conflictos de CSS con tu web
2. Ajusta el `zIndex` en la configuración del widget
3. Cambia la posición del botón si interfiere con otros elementos

---

## 📞 Soporte

Si tienes problemas con la integración:
- 📧 Email: info@m2merida.com
- 📱 Teléfono: 622 304 050

---

## 🔐 Seguridad y CORS

### Configuración CORS
El chatbot está configurado con **CORS habilitado** para permitir su integración en cualquier sitio web.

**¿Qué significa esto?**
- ✅ El widget puede cargarse desde cualquier dominio
- ✅ Los archivos estáticos (widget.js) son accesibles externamente
- ✅ Las peticiones API funcionan desde otros sitios web
- ✅ El iframe puede cargarse sin restricciones

### Seguridad
- ✅ El widget solo carga contenido de tu propio dominio
- ✅ No recopila datos del sitio web donde se integra
- ✅ Funciona de forma aislada en un iframe
- ✅ No interfiere con el funcionamiento de la web existente
- ✅ Si quieres restringir a dominios específicos, puedes modificar la configuración CORS en `app.py`

### Restringir a dominios específicos (Opcional)
Si quieres que el widget **solo funcione en tu web**, edita `app.py`:

```python
CORS(app, resources={
    r"/*": {
        "origins": ["https://tudominio.com", "https://www.tudominio.com"],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type"],
    }
})
```

---

## 📊 Resumen de URLs

| Uso | URL | Descripción |
|-----|-----|-------------|
| **QR Code** | `https://tu-dominio-render.com` | Versión completa para móviles |
| **Script Widget** | `https://tu-dominio-render.com/static/js/widget.js` | Script para integrar en web |
| **Demo** | `https://tu-dominio-render.com/ejemplo-integracion` | Página de ejemplo y prueba |

---

## ✅ Checklist de Implementación

**Para el Código QR:**
- [ ] Generar el QR con la URL de producción
- [ ] Imprimir en buena calidad
- [ ] Colocar en la puerta del negocio
- [ ] Probar escaneando con móvil

**Para la Web:**
- [ ] Añadir el script en la página web
- [ ] Probar en diferentes navegadores
- [ ] Verificar en móvil, tablet y desktop
- [ ] Confirmar que no interfiere con otros elementos
- [ ] Probar el flujo completo del chatbot

---

🎉 **¡Listo!** Tu chatbot está integrado y funcionando.

