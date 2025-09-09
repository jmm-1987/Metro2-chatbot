// Variables globales
let currentContext = null;
let isTyping = false;
let userData = {
    tipo_consulta: '',
    tipo_propiedad: '',
    zona: '',
    nombre: '',
    telefono: '',
    email: '',
    presupuesto: '',
    comentarios: ''
};
let currentStep = 0;

// Inicialización
document.addEventListener('DOMContentLoaded', function() {
    // Establecer hora de bienvenida
    const welcomeTime = document.getElementById('welcomeTime');
    if (welcomeTime) {
        welcomeTime.textContent = getCurrentTime();
    }
    
    // Ocultar input por defecto
    hideTextInput();
    
    // Event listeners
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    
    messageInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    messageInput.addEventListener('input', function() {
        sendButton.disabled = messageInput.value.trim() === '';
    });
    
    // Cargar FAQ al abrir el modal
    document.getElementById('faqModal').addEventListener('click', function(e) {
        if (e.target === this) {
            closeFAQ();
        }
    });
    
    // Asegurar que los eventos de las opciones principales estén asignados
    setTimeout(() => {
        attachMainOptionsEvents();
    }, 500);
});

// Función para obtener la hora actual
function getCurrentTime() {
    const now = new Date();
    return now.toLocaleTimeString('es-ES', { 
        hour: '2-digit', 
        minute: '2-digit' 
    });
}

// Función para enviar mensaje
async function sendMessage() {
    const messageInput = document.getElementById('messageInput');
    const message = messageInput.value.trim();
    
    if (!message || isTyping) return;
    
    // Agregar mensaje del usuario
    addUserMessage(message);
    messageInput.value = '';
    document.getElementById('sendButton').disabled = true;
    
    // Procesar datos según el paso actual
    if (currentStep === 2) {
        // Estamos en el paso de recolección de datos
        processUserData(message);
        return;
    }
    
    // Mostrar indicador de escritura
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mensaje: message })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        handleBotResponse(data);
        
    } catch (error) {
        hideTypingIndicator();
        addBotMessage('Lo siento, hubo un error. Por favor, intenta de nuevo.');
        console.error('Error:', error);
    }
}

// Función para seleccionar opción
async function selectOption(optionId) {
    console.log(`selectOption llamado con: ${optionId}`);
    
    if (isTyping) {
        console.log('Chat está escribiendo, ignorando click');
        return;
    }
    
    // Buscar el texto de la opción de manera más robusta
    const optionCard = document.querySelector(`[data-option-id="${optionId}"]`);
    let optionText = optionId; // fallback
    
    if (optionCard) {
        const titleElement = optionCard.querySelector('h4');
        if (titleElement) {
            optionText = titleElement.textContent;
        }
    }
    
    console.log(`Agregando mensaje del usuario: ${optionText}`);
    addUserMessage(optionText);
    
    showTypingIndicator();
    
    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ mensaje: optionId })
        });
        
        const data = await response.json();
        hideTypingIndicator();
        handleBotResponse(data);
        
    } catch (error) {
        hideTypingIndicator();
        addBotMessage('Lo siento, hubo un error. Por favor, intenta de nuevo.');
        console.error('Error:', error);
    }
}

// Función para manejar respuesta del bot
function handleBotResponse(data) {
    switch (data.tipo) {
        case 'bienvenida':
            addBotMessage(data.mensaje);
            showMainOptions(data.opciones);
            hideTextInput(); // Ocultar input cuando hay opciones
            break;
            
        case 'opcion_seleccionada':
            addBotMessage(data.mensaje);
            currentContext = data.contexto;
            if (data.opciones) {
                showSubOptions(data.opciones);
                hideTextInput(); // Ocultar input cuando hay opciones
            }
            break;
            
        case 'preguntas_frecuentes':
            addBotMessage(data.mensaje);
            showFAQContent(data.preguntas);
            hideTextInput(); // Ocultar input cuando hay opciones
            break;
            
        case 'solicitar_datos':
            addBotMessage(data.mensaje);
            showTextInput(); // Mostrar input cuando se solicitan datos
            break;
            
        case 'texto':
        default:
            addBotMessage(data.mensaje);
            break;
    }
}

// Función para agregar mensaje del usuario
function addUserMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message user-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-user"></i>
        </div>
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    scrollToBottom();
}

// Función para agregar mensaje del bot
function addBotMessage(message) {
    const chatMessages = document.getElementById('chatMessages');
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message bot-message';
    messageDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-home"></i>
        </div>
        <div class="message-content">
            <p>${escapeHtml(message)}</p>
            <div class="message-time">${getCurrentTime()}</div>
        </div>
    `;
    
    chatMessages.appendChild(messageDiv);
    
    // Scroll al inicio de la nueva respuesta del bot con más tiempo para el renderizado
    setTimeout(() => {
        scrollToMessage(messageDiv);
    }, 200);
}

// Función para mostrar opciones principales
function showMainOptions(opciones) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Remover opciones anteriores
    const existingOptions = document.getElementById('mainOptions');
    if (existingOptions) {
        existingOptions.remove();
    }
    
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options-container slide-up';
    optionsContainer.id = 'mainOptions';
    
    opciones.forEach((option, index) => {
        const optionCard = document.createElement('div');
        optionCard.className = 'option-card';
        optionCard.setAttribute('data-option-id', option.id);
        
        const icon = getOptionIcon(option.id);
        const description = getOptionDescription(option.id);
        
        optionCard.innerHTML = `
            <div class="option-icon">
                <i class="${icon}"></i>
            </div>
            <div class="option-content">
                <h4>${option.texto}</h4>
                <p>${description}</p>
            </div>
        `;
        
        // Agregar animación escalonada
        optionCard.style.animationDelay = `${index * 0.1}s`;
        optionCard.classList.add('slide-up');
        
        optionsContainer.appendChild(optionCard);
    });
    
    chatMessages.appendChild(optionsContainer);
    hideTextInput(); // Ocultar input cuando se muestran opciones
    scrollToBottom();
}

// Función para asignar eventos a las opciones principales
function attachMainOptionsEvents() {
    const mainOptions = document.getElementById('mainOptions');
    if (!mainOptions) {
        console.log('No se encontraron opciones principales para asignar eventos');
        return;
    }
    
    const optionCards = mainOptions.querySelectorAll('.option-card');
    console.log(`Asignando eventos a ${optionCards.length} opciones principales`);
    
    optionCards.forEach((card, index) => {
        const optionId = card.getAttribute('data-option-id');
        if (optionId) {
            // Remover eventos anteriores si existen
            const newCard = card.cloneNode(true);
            card.parentNode.replaceChild(newCard, card);
            
            // Asignar nuevo evento
            newCard.addEventListener('click', (e) => {
                e.preventDefault();
                console.log(`Click en opción: ${optionId}`);
                selectOption(optionId);
            });
            
            console.log(`Evento asignado a opción ${index + 1}: ${optionId}`);
        }
    });
}

// Función para manejar el click en opciones principales
function handleMainOptionClick(event) {
    const optionId = event.currentTarget.getAttribute('data-option-id');
    if (optionId) {
        selectOption(optionId);
    }
}

// Función para mostrar sub-opciones
function showSubOptions(opciones) {
    const chatMessages = document.getElementById('chatMessages');
    
    // Remover opciones anteriores
    const existingOptions = document.querySelector('.options-container:not(#mainOptions)');
    if (existingOptions) {
        existingOptions.remove();
    }
    
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options-container';
    
    opciones.forEach(option => {
        const optionCard = document.createElement('div');
        optionCard.className = 'option-card';
        
        optionCard.innerHTML = `
            <div class="option-icon">
                <i class="fas fa-building"></i>
            </div>
            <div class="option-content">
                <h4>${option.texto}</h4>
                <p>Selecciona para continuar</p>
            </div>
        `;
        
        // Asignar evento click después de crear el elemento
        optionCard.addEventListener('click', () => selectSubOption(option.id));
        
        optionsContainer.appendChild(optionCard);
    });
    
    chatMessages.appendChild(optionsContainer);
    hideTextInput(); // Ocultar input cuando se muestran opciones
    scrollToBottom();
}

// Función para seleccionar sub-opción
function selectSubOption(optionId) {
    if (isTyping) return;
    
    addUserMessage(optionId);
    
    // Guardar tipo de propiedad
    userData.tipo_propiedad = optionId;
    currentStep = 1;
    
    // Mensajes específicos según el contexto
    let responseMessage = '';
    
    switch (currentContext) {
        case 'vender':
            responseMessage = `Perfecto, has seleccionado ${optionId}. Para continuar con la venta, necesitamos más información. ¿En qué zona se encuentra tu propiedad?`;
            break;
        case 'comprar':
            responseMessage = `Excelente elección, ${optionId}. ¿En qué zona te gustaría buscar?`;
            break;
        case 'alquilar':
            responseMessage = `Muy bien, ${optionId}. ¿En qué zona necesitas alquilar?`;
            break;
        case 'alquilar_mi_propiedad':
            responseMessage = `Perfecto, ${optionId}. ¿En qué zona se encuentra tu propiedad para alquilar?`;
            break;
        default:
            responseMessage = `Has seleccionado ${optionId}. ¿En qué más puedo ayudarte?`;
    }
    
    addBotMessage(responseMessage);
    
    // Mostrar opciones de zona
    showZoneOptions();
}

// Función para mostrar opciones de zona
function showZoneOptions() {
    const chatMessages = document.getElementById('chatMessages');
    
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options-container';
    
    const zonas = ['Centro', 'Norte', 'Bodegones-Sur', 'Nueva Ciudad', 'Sindicales'];
    
    zonas.forEach(zona => {
        const optionCard = document.createElement('div');
        optionCard.className = 'option-card';
        
        optionCard.innerHTML = `
            <div class="option-icon">
                <i class="fas fa-map-marker-alt"></i>
            </div>
            <div class="option-content">
                <h4>${zona}</h4>
                <p>Selecciona esta zona</p>
            </div>
        `;
        
        // Asignar evento click después de crear el elemento
        optionCard.addEventListener('click', () => selectZone(zona));
        
        optionsContainer.appendChild(optionCard);
    });
    
    chatMessages.appendChild(optionsContainer);
    hideTextInput(); // Ocultar input cuando se muestran opciones
    scrollToBottom();
}

// Función para seleccionar zona
function selectZone(zona) {
    if (isTyping) return;
    
    addUserMessage(zona);
    
    // Guardar zona
    userData.zona = zona;
    currentStep = 2;
    
    let responseMessage = '';
    
    switch (currentContext) {
        case 'vender':
            responseMessage = `Excelente, zona ${zona}. Queremos darte el mejor servicio. Necesitaremos algunos datos adicionales para que un asesor inmobiliario te pueda contactar sin ningún compromiso.¿Cuál es tu nombre completo?`;
            break;
        case 'comprar':
            responseMessage = `Perfecto, zona ${zona}. Para encontrar las mejores opciones, necesitamos algunos datos. ¿Cuál es tu nombre completo?`;
            break;
        case 'alquilar':
            responseMessage = `Muy bien, zona ${zona}. Para ayudarte a encontrar el lugar perfecto, necesitamos algunos datos. ¿Cuál es tu nombre completo?`;
            break;
        case 'alquilar_mi_propiedad':
            responseMessage = `Excelente, zona ${zona}. Para alquilar tu propiedad, necesitamos algunos datos. ¿Cuál es tu nombre completo?`;
            break;
    }
    
    addBotMessage(responseMessage);
    
    // Mostrar input para solicitar datos específicos
    showTextInput();
}

// Función para mostrar formulario de datos
function showDataForm() {
    const chatMessages = document.getElementById('chatMessages');
    
    const formContainer = document.createElement('div');
    formContainer.className = 'data-form-container';
    formContainer.innerHTML = `
        <div class="form-card">
            <h4>📝 Datos de Contacto</h4>
            <form id="userDataForm">
                <div class="form-group">
                    <label for="nombre">Nombre completo *</label>
                    <input type="text" id="nombre" name="nombre" required>
                </div>
                <div class="form-group">
                    <label for="telefono">Teléfono *</label>
                    <input type="tel" id="telefono" name="telefono" required>
                </div>
                <div class="form-group">
                    <label for="email">Email (opcional)</label>
                    <input type="email" id="email" name="email" placeholder="ejemplo@correo.com">
                </div>
                ${getPresupuestoField()}
                <div class="form-group">
                    <label for="comentarios">Comentarios adicionales</label>
                    <textarea id="comentarios" name="comentarios" rows="3" placeholder="Cuéntanos más detalles..."></textarea>
                </div>
                <button type="submit" class="submit-btn">
                    <i class="fas fa-paper-plane"></i>
                    Enviar Consulta
                </button>
            </form>
        </div>
    `;
    
    chatMessages.appendChild(formContainer);
    scrollToBottom();
    
    // Agregar event listener al formulario
    document.getElementById('userDataForm').addEventListener('submit', handleFormSubmit);
}

// Función para obtener el campo de presupuesto según el contexto
function getPresupuestoField() {
    switch (currentContext) {
        case 'vender':
            return `
                <div class="form-group">
                    <label for="presupuesto">Precio estimado de venta (opcional)</label>
                    <input type="text" id="presupuesto" name="presupuesto" placeholder="Ej: $2,500,000">
                </div>
            `;
        case 'comprar':
            return `
                <div class="form-group">
                    <label for="presupuesto">Presupuesto para compra (opcional)</label>
                    <input type="text" id="presupuesto" name="presupuesto" placeholder="Ej: $1,500,000 - $2,000,000">
                </div>
            `;
        case 'alquilar':
            return `
                <div class="form-group">
                    <label for="presupuesto">Presupuesto mensual (opcional)</label>
                    <input type="text" id="presupuesto" name="presupuesto" placeholder="Ej: $8,000 - $12,000">
                </div>
            `;
        case 'alquilar_mi_propiedad':
            return `
                <div class="form-group">
                    <label for="presupuesto">Renta mensual esperada (opcional)</label>
                    <input type="text" id="presupuesto" name="presupuesto" placeholder="Ej: $10,000 - $15,000">
                </div>
            `;
        default:
            return '';
    }
}

// Función para manejar el envío del formulario
async function handleFormSubmit(event) {
    event.preventDefault();
    
    if (isTyping) return;
    
    // Recopilar datos del formulario
    const formData = new FormData(event.target);
    userData.nombre = formData.get('nombre');
    userData.telefono = formData.get('telefono');
    userData.email = formData.get('email') || '';
    userData.presupuesto = formData.get('presupuesto') || '';
    userData.comentarios = formData.get('comentarios') || '';
    userData.tipo_consulta = getTipoConsultaTexto();
    
    // Validar datos requeridos
    if (!userData.nombre || !userData.telefono) {
        addBotMessage('Por favor, completa al menos el nombre y teléfono para continuar.');
        return;
    }
    
    // Mostrar mensaje de envío
    addBotMessage('Enviando tu consulta...');
    showTypingIndicator();
    
    try {
        // Enviar datos al servidor
        const response = await fetch('/api/enviar-datos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        hideTypingIndicator();
        
        if (result.success) {
            addBotMessage(result.message);
            
            // Mostrar resumen de la consulta
            setTimeout(() => {
                showConsultaResumen();
            }, 1000);
        } else {
            addBotMessage(result.message);
        }
        
    } catch (error) {
        hideTypingIndicator();
        addBotMessage('Error al enviar la consulta. Por favor, intenta de nuevo.');
        console.error('Error:', error);
    }
}

// Función para obtener el texto del tipo de consulta
function getTipoConsultaTexto() {
    switch (currentContext) {
        case 'vender':
            return 'Vender propiedad';
        case 'comprar':
            return 'Comprar propiedad';
        case 'alquilar':
            return 'Alquilar propiedad';
        case 'alquilar_mi_propiedad':
            return 'Alquilar mi propiedad';
        default:
            return 'Consulta general';
    }
}

// Función para mostrar resumen de la consulta
function showConsultaResumen() {
    const resumen = `
        📋 **Resumen de tu consulta:**
        
        **Tipo:** ${getTipoConsultaTexto()}
        **Propiedad:** ${userData.tipo_propiedad}
        **Zona:** ${userData.zona}
        **Nombre:** ${userData.nombre}
        **Teléfono:** ${userData.telefono}
        ${userData.email ? `**Email:** ${userData.email}` : ''}
        ${userData.presupuesto ? `**Presupuesto:** ${userData.presupuesto}` : ''}
        ${userData.comentarios ? `**Comentarios:** ${userData.comentarios}` : ''}
        
        ✅ **¡Consulta enviada exitosamente!**
        
        Un asesor especializado de Metro Cuadrado Mérida se pondrá en contacto contigo en las próximas 24 horas.
        
        Mientras tanto, puedes:
        • Revisar nuestras preguntas frecuentes
        • Contactarnos directamente
        • Iniciar una nueva consulta
    `;
    
    addBotMessage(resumen);
    
    // Mostrar opciones finales
    setTimeout(() => {
        showFinalOptions();
    }, 2000);
}

// Función para mostrar opciones finales
function showFinalOptions() {
    const chatMessages = document.getElementById('chatMessages');
    
    const optionsContainer = document.createElement('div');
    optionsContainer.className = 'options-container';
    
    const options = [
        {
            icon: 'fas fa-question-circle',
            title: 'Ver Preguntas Frecuentes',
            description: 'Consulta información adicional',
            action: () => showFAQ()
        },
        {
            icon: 'fas fa-phone',
            title: 'Contacto Directo',
            description: 'Ver información de contacto',
            action: () => showContactInfo()
        },
        {
            icon: 'fas fa-redo',
            title: 'Nueva Consulta',
            description: 'Iniciar un nuevo proceso',
            action: () => restartChat()
        }
    ];
    
    options.forEach(option => {
        const optionCard = document.createElement('div');
        optionCard.className = 'option-card';
        
        optionCard.innerHTML = `
            <div class="option-icon">
                <i class="${option.icon}"></i>
            </div>
            <div class="option-content">
                <h4>${option.title}</h4>
                <p>${option.description}</p>
            </div>
        `;
        
        optionCard.addEventListener('click', option.action);
        optionsContainer.appendChild(optionCard);
    });
    
    chatMessages.appendChild(optionsContainer);
    hideTextInput(); // Ocultar input cuando se muestran opciones
    scrollToBottom();
}

// Función para mostrar información de contacto
function showContactInfo() {
    if (isTyping) return;
    
    // Solo agregar mensaje del usuario si no viene del botón inferior
    const isFromButton = event && event.target && event.target.closest('.quick-btn');
    if (!isFromButton) {
        addUserMessage('Información de Contacto');
    }
    
    const contactInfo = `
        📞 Teléfono: +52 (999) 123-4567
        📧 Email: info@metrocua.com
        🏢 Dirección: Av. Paseo de Montejo, Mérida, Yucatán
        ⏰ Horarios: Lunes a Viernes 9:00 - 18:00, Sábados 9:00 - 14:00
        
        ¡Gracias por contactar Metro Cuadrado Mérida! Un asesor especializado se pondrá en contacto contigo pronto.
    `;
    
    addBotMessage(contactInfo);
    
    // Solo mostrar opción de reinicio si no viene del botón inferior
    if (!isFromButton) {
        setTimeout(() => {
            showRestartOption();
        }, 1000);
    }
}

// Función para mostrar opción de reinicio
function showRestartOption() {
    const chatMessages = document.getElementById('chatMessages');
    
    const restartContainer = document.createElement('div');
    restartContainer.className = 'options-container';
    
    const restartCard = document.createElement('div');
    restartCard.className = 'option-card';
    
    restartCard.innerHTML = `
        <div class="option-icon">
            <i class="fas fa-redo"></i>
        </div>
        <div class="option-content">
            <h4>Nueva Consulta</h4>
            <p>Haz clic para empezar una nueva conversación</p>
        </div>
    `;
    
    // Asignar evento click después de crear el elemento
    restartCard.addEventListener('click', () => restartChat());
    
    chatMessages.appendChild(restartContainer);
    hideTextInput(); // Ocultar input cuando se muestran opciones
    scrollToBottom();
}

// Función para mostrar indicador de escritura
function showTypingIndicator() {
    isTyping = true;
    const chatMessages = document.getElementById('chatMessages');
    
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message bot-message typing-indicator';
    typingDiv.id = 'typingIndicator';
    typingDiv.innerHTML = `
        <div class="message-avatar">
            <i class="fas fa-home"></i>
        </div>
        <div class="message-content">
            <div class="loading"></div>
        </div>
    `;
    
    chatMessages.appendChild(typingDiv);
    scrollToBottom();
}

// Función para ocultar indicador de escritura
function hideTypingIndicator() {
    isTyping = false;
    const typingIndicator = document.getElementById('typingIndicator');
    if (typingIndicator) {
        typingIndicator.remove();
    }
}

// Función para mostrar FAQ
async function showFAQ() {
    const modal = document.getElementById('faqModal');
    const faqContent = document.getElementById('faqContent');
    
    try {
        const response = await fetch('/api/faq');
        const faqs = await response.json();
        
        faqContent.innerHTML = '';
        faqs.forEach(faq => {
            const faqItem = document.createElement('div');
            faqItem.className = 'faq-item';
            faqItem.innerHTML = `
                <div class="faq-question">${faq.pregunta}</div>
                <div class="faq-answer">${faq.respuesta}</div>
            `;
            faqContent.appendChild(faqItem);
        });
        
        modal.style.display = 'block';
    } catch (error) {
        console.error('Error loading FAQ:', error);
        faqContent.innerHTML = '<p>Error al cargar las preguntas frecuentes.</p>';
        modal.style.display = 'block';
    }
}

// Función para cerrar FAQ
function closeFAQ() {
    document.getElementById('faqModal').style.display = 'none';
}

// Función para mostrar contenido de FAQ en el chat
function showFAQContent(preguntas) {
    const chatMessages = document.getElementById('chatMessages');
    
    const faqContainer = document.createElement('div');
    faqContainer.className = 'options-container';
    
    preguntas.forEach((faq, index) => {
        const faqCard = document.createElement('div');
        faqCard.className = 'option-card';
        
        faqCard.innerHTML = `
            <div class="option-icon">
                <i class="fas fa-question-circle"></i>
            </div>
            <div class="option-content">
                <h4>${faq.pregunta}</h4>
                <p>Haz clic para ver la respuesta</p>
            </div>
        `;
        
        // Asignar evento click después de crear el elemento
        faqCard.addEventListener('click', () => showFAQAnswer(faq));
        
        faqContainer.appendChild(faqCard);
    });
    
    chatMessages.appendChild(faqContainer);
    hideTextInput(); // Ocultar input cuando se muestran opciones
    scrollToBottom();
}

// Función para mostrar respuesta de FAQ
function showFAQAnswer(faq) {
    if (isTyping) return;
    
    addUserMessage(faq.pregunta);
    addBotMessage(faq.respuesta);
    
    // Mostrar opción para más preguntas
    setTimeout(() => {
        const chatMessages = document.getElementById('chatMessages');
        const moreOptions = document.createElement('div');
        moreOptions.className = 'options-container';
        
        const moreCard = document.createElement('div');
        moreCard.className = 'option-card';
        
        moreCard.innerHTML = `
            <div class="option-icon">
                <i class="fas fa-list"></i>
            </div>
            <div class="option-content">
                <h4>Ver más preguntas</h4>
                <p>Haz clic para ver todas las preguntas frecuentes</p>
            </div>
        `;
        
        // Asignar evento click después de crear el elemento
        moreCard.addEventListener('click', () => showFAQ());
        
        moreOptions.appendChild(moreCard);
        chatMessages.appendChild(moreOptions);
        hideTextInput(); // Ocultar input cuando se muestran opciones
        scrollToBottom();
    }, 500);
}

// Función para reiniciar chat
function restartChat() {
    const chatMessages = document.getElementById('chatMessages');
    
    // Agregar efecto de fade out
    chatMessages.style.opacity = '0.5';
    chatMessages.style.transition = 'opacity 0.3s ease-out';
    
    setTimeout(() => {
        // Limpiar completamente la pantalla
        chatMessages.innerHTML = '';
        
        // Crear y agregar el mensaje de bienvenida inicial
        const welcomeMessage = document.createElement('div');
        welcomeMessage.className = 'message bot-message fade-in';
        welcomeMessage.innerHTML = `
            <div class="message-avatar">
                <i class="fas fa-home"></i>
            </div>
            <div class="message-content">
                <p>¡Hola! Bienvenido a Metro Cuadrado Mérida. ¿En qué podemos ayudarte hoy?</p>
                <div class="message-time">${getCurrentTime()}</div>
            </div>
        `;
        
        chatMessages.appendChild(welcomeMessage);
        
        // Mostrar opciones principales con animación
        setTimeout(() => {
            showMainOptions([
                { id: 'vender', texto: 'Vender mi propiedad' },
                { id: 'comprar', texto: 'Comprar propiedad' },
                { id: 'alquilar', texto: 'Alquilar propiedad' },
                { id: 'alquilar_mi_propiedad', texto: 'Alquilar mi propiedad' }
            ]);
            
            // Asegurar que los eventos se asignen después de que el DOM esté listo
            setTimeout(() => {
                attachMainOptionsEvents();
            }, 100);
        }, 200);
        
        // Restaurar opacidad
        chatMessages.style.opacity = '1';
        
        // Resetear variables
        currentContext = null;
        isTyping = false;
        currentStep = 0;
        userData = {
            tipo_consulta: '',
            tipo_propiedad: '',
            zona: '',
            nombre: '',
            telefono: '',
            email: '',
            presupuesto: '',
            comentarios: ''
        };
        
        // Hacer scroll hacia arriba
        scrollToBottom();
    }, 300);
}

// Función para alternar chat (minimizar/maximizar)
function toggleChat() {
    const chatContainer = document.querySelector('.chat-container');
    const minimizeBtn = document.querySelector('.btn-minimize i');
    
    if (chatContainer.style.height === '60px') {
        chatContainer.style.height = '80vh';
        minimizeBtn.className = 'fas fa-minus';
    } else {
        chatContainer.style.height = '60px';
        minimizeBtn.className = 'fas fa-plus';
    }
}

// Función para hacer scroll hacia abajo
function scrollToBottom() {
    const chatMessages = document.getElementById('chatMessages');
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Función para hacer scroll a un mensaje específico
function scrollToMessage(messageElement) {
    if (messageElement) {
        // Usar scrollIntoView que es más confiable
        setTimeout(() => {
            messageElement.scrollIntoView({
                behavior: 'smooth',
                block: 'start',
                inline: 'nearest'
            });
        }, 200);
    }
}

// Función para hacer scroll al inicio de la última respuesta del bot
function scrollToLastBotMessage() {
    const chatMessages = document.getElementById('chatMessages');
    const botMessages = chatMessages.querySelectorAll('.bot-message');
    
    if (botMessages.length > 0) {
        const lastBotMessage = botMessages[botMessages.length - 1];
        scrollToMessage(lastBotMessage);
    }
}

// Función para mostrar input de texto
function showTextInput() {
    const inputContainer = document.querySelector('.chat-input-container');
    if (inputContainer) {
        inputContainer.style.display = 'block';
        
        // Restaurar el input wrapper
        const inputWrapper = inputContainer.querySelector('.input-wrapper');
        if (inputWrapper) inputWrapper.style.display = 'flex';
        
        // Restaurar las quick-actions
        const quickActions = inputContainer.querySelector('.quick-actions');
        if (quickActions) quickActions.style.display = 'flex';
        
        const messageInput = document.getElementById('messageInput');
        if (messageInput) {
            messageInput.focus();
        }
    }
}

// Función para ocultar input de texto
function hideTextInput() {
    const inputContainer = document.querySelector('.chat-input-container');
    if (inputContainer) {
        // Solo ocultar el input y las quick-actions, pero mantener el botón de reiniciar en el header visible
        const inputWrapper = inputContainer.querySelector('.input-wrapper');
        const quickActions = inputContainer.querySelector('.quick-actions');
        
        if (inputWrapper) inputWrapper.style.display = 'none';
        if (quickActions) quickActions.style.display = 'none';
    }
}

// Función para procesar datos del usuario
function processUserData(message) {
    // Determinar qué dato estamos recolectando
    if (!userData.nombre) {
        userData.nombre = message;
        addBotMessage(`Perfecto, ${message}. Ahora necesitamos tu número de teléfono.`);
        return;
    }
    
    if (!userData.telefono) {
        userData.telefono = message;
        addBotMessage(`Excelente. ¿Hay algo más que quieras agregar en comentarios? Puedes indicar la franja horaria en la que quieres que te llamemos o algún otro detalle que consideres importante.`);
        return;
    }
    
    if (!userData.comentarios && message.toLowerCase() !== 'no' && message.toLowerCase() !== 'nada') {
        userData.comentarios = message;
    }
    
    // Todos los datos recolectados, proceder con el envío
    userData.tipo_consulta = getTipoConsultaTexto();
    hideTextInput();
    showTypingIndicator();
    
    // Simular envío de datos
    setTimeout(() => {
        hideTypingIndicator();
        sendUserData();
    }, 1500);
}

// Función para enviar datos del usuario
async function sendUserData() {
    try {
        const response = await fetch('/api/enviar-datos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData)
        });
        
        const result = await response.json();
        
        if (result.success) {
            addBotMessage(result.message);
            setTimeout(() => {
                showConsultaResumen();
            }, 1000);
        } else {
            addBotMessage(result.message);
        }
        
    } catch (error) {
        addBotMessage('Error al enviar la consulta. Por favor, intenta de nuevo.');
        console.error('Error:', error);
    }
}

// Función para escapar HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Funciones auxiliares para iconos y descripciones
function getOptionIcon(optionId) {
    const icons = {
        'vender': 'fas fa-hand-holding-usd',
        'comprar': 'fas fa-search',
        'alquilar': 'fas fa-key',
        'alquilar_mi_propiedad': 'fas fa-building'
    };
    return icons[optionId] || 'fas fa-question-circle';
}

function getOptionDescription(optionId) {
    const descriptions = {
        'vender': 'Te ayudamos a vender tu propiedad al mejor precio',
        'comprar': 'Encuentra la propiedad perfecta para ti',
        'alquilar': 'Encuentra el lugar perfecto para alquilar',
        'alquilar_mi_propiedad': 'Renta tu propiedad de forma segura'
    };
    return descriptions[optionId] || 'Selecciona esta opción';
}
