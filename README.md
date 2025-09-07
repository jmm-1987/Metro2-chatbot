# Chatbot Inmobiliaria

Un chatbot moderno y responsivo para inmobiliaria desarrollado con Flask y Python.

## Características

- 🏠 **Diseño moderno**: Interfaz limpia y atractiva
- 📱 **Responsivo**: Funciona perfectamente en móviles y escritorio
- 💬 **Chat interactivo**: Conversación fluida con opciones predefinidas
- 🎯 **Opciones principales**:
  - Vender mi propiedad
  - Comprar propiedad
  - Alquilar propiedad
  - Alquilar mi propiedad
- ❓ **Preguntas frecuentes**: Sección dedicada con respuestas comunes
- 🎨 **Animaciones suaves**: Transiciones y efectos visuales modernos

## Instalación

1. Clona el repositorio:
```bash
git clone <url-del-repositorio>
cd Raul-chatbot
```

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

3. Ejecuta la aplicación:
```bash
python app.py
```

4. Abre tu navegador en `http://localhost:5000`

## Estructura del Proyecto

```
Raul-chatbot/
├── app.py                 # Aplicación principal Flask
├── requirements.txt       # Dependencias de Python
├── README.md             # Este archivo
├── templates/
│   └── index.html        # Plantilla HTML principal
└── static/
    ├── css/
    │   └── style.css     # Estilos CSS
    └── js/
        └── script.js     # JavaScript del frontend
```

## Funcionalidades

### Mensaje de Bienvenida
Al abrir el chatbot, se muestra un mensaje de bienvenida con 4 opciones principales.

### Flujo de Conversación
1. **Selección de opción**: El usuario elige una de las 4 opciones principales
2. **Tipo de propiedad**: Selecciona el tipo (Casa, Departamento, Terreno, etc.)
3. **Zona**: Elige la zona de interés
4. **Información de contacto**: Se proporcionan los datos de contacto

### Preguntas Frecuentes
- Acceso directo desde el chat
- Modal dedicado con todas las preguntas
- Respuestas detalladas sobre procesos inmobiliarios

## Personalización

### Agregar Nuevas Opciones
Edita el archivo `app.py` y modifica el diccionario `opciones_principales`.

### Modificar Preguntas Frecuentes
Actualiza la lista `preguntas_frecuentes` en `app.py`.

### Cambiar Estilos
Modifica el archivo `static/css/style.css` para personalizar la apariencia.

## Tecnologías Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Iconos**: Font Awesome
- **Fuentes**: Google Fonts (Inter)
- **Diseño**: CSS Grid, Flexbox, Gradientes

## Características Técnicas

- **Responsive Design**: Adaptable a todos los dispositivos
- **Animaciones CSS**: Transiciones suaves y efectos visuales
- **API REST**: Endpoints para comunicación frontend-backend
- **Manejo de Estados**: Control de contexto de conversación
- **Validación**: Sanitización de entrada de usuario

## Próximas Mejoras

- [ ] Integración con base de datos
- [ ] Sistema de notificaciones
- [ ] Chat en tiempo real con WebSockets
- [ ] Panel de administración
- [ ] Integración con APIs de mapas
- [ ] Sistema de citas automáticas

## Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.
