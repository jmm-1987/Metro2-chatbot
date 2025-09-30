/**
 * Widget de Chatbot Metro Cuadrado Mérida
 * Versión embebible para sitios web externos
 */

(function() {
    'use strict';
    
    // Configuración del widget
    const config = {
        buttonColor: '#d4af37',
        buttonPosition: 'bottom-right', // 'bottom-right' o 'bottom-left'
        buttonText: '💬',
        chatbotUrl: window.location.origin, // URL del chatbot
        zIndex: 9999
    };

    // Estilos del widget
    const styles = `
        #m2-chatbot-widget {
            position: fixed;
            ${config.buttonPosition.includes('right') ? 'right: 20px;' : 'left: 20px;'}
            bottom: 20px;
            z-index: ${config.zIndex};
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
        }

        #m2-chatbot-button {
            width: 60px;
            height: 60px;
            border-radius: 50%;
            background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%);
            border: none;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
        }

        #m2-chatbot-button:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6);
        }

        #m2-chatbot-button::before {
            content: '';
            position: absolute;
            top: 50%;
            left: 50%;
            width: 0;
            height: 0;
            border-radius: 50%;
            background: rgba(255, 255, 255, 0.3);
            transform: translate(-50%, -50%);
            transition: width 0.6s, height 0.6s;
        }

        #m2-chatbot-button:hover::before {
            width: 100%;
            height: 100%;
        }

        #m2-chatbot-button.pulse {
            animation: pulse-animation 2s infinite;
        }

        @keyframes pulse-animation {
            0% {
                box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
            }
            50% {
                box-shadow: 0 4px 20px rgba(212, 175, 55, 0.8);
            }
            100% {
                box-shadow: 0 4px 12px rgba(212, 175, 55, 0.4);
            }
        }

        #m2-chatbot-container {
            display: none;
            position: fixed;
            ${config.buttonPosition.includes('right') ? 'right: 20px;' : 'left: 20px;'}
            bottom: 90px;
            width: 400px;
            height: 600px;
            max-width: calc(100vw - 40px);
            max-height: calc(100vh - 120px);
            background: white;
            border-radius: 16px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            overflow: hidden;
            z-index: ${config.zIndex};
            animation: slideUp 0.3s ease-out;
        }

        #m2-chatbot-container.show {
            display: block;
        }

        @keyframes slideUp {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }

        #m2-chatbot-header {
            background: #2b2a28;
            color: #d4af37;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            border-bottom: 2px solid #d4af37;
        }

        #m2-chatbot-header h3 {
            margin: 0;
            font-size: 16px;
            font-weight: 600;
        }

        #m2-chatbot-close {
            background: transparent;
            border: none;
            color: #d4af37;
            font-size: 24px;
            cursor: pointer;
            width: 30px;
            height: 30px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 4px;
            transition: background 0.2s;
        }

        #m2-chatbot-close:hover {
            background: rgba(212, 175, 55, 0.2);
        }

        #m2-chatbot-iframe {
            width: 100%;
            height: calc(100% - 57px);
            border: none;
        }

        /* Responsive */
        @media (max-width: 768px) {
            #m2-chatbot-container {
                width: calc(100vw - 40px);
                height: calc(100vh - 120px);
            }
        }

        @media (max-width: 480px) {
            #m2-chatbot-button {
                width: 55px;
                height: 55px;
                font-size: 24px;
            }

            #m2-chatbot-container {
                bottom: 80px;
                width: calc(100vw - 20px);
                height: calc(100vh - 100px);
                right: 10px;
                left: 10px;
            }
        }
    `;

    // Inyectar estilos
    function injectStyles() {
        const styleElement = document.createElement('style');
        styleElement.textContent = styles;
        document.head.appendChild(styleElement);
    }

    // Crear el HTML del widget
    function createWidget() {
        const widgetHTML = `
            <div id="m2-chatbot-widget">
                <button id="m2-chatbot-button" class="pulse" aria-label="Abrir chat">
                    ${config.buttonText}
                </button>
                <div id="m2-chatbot-container">
                    <div id="m2-chatbot-header">
                        <h3>Metro Cuadrado Mérida</h3>
                        <button id="m2-chatbot-close" aria-label="Cerrar chat">×</button>
                    </div>
                    <iframe 
                        id="m2-chatbot-iframe" 
                        src="${config.chatbotUrl}"
                        title="Chatbot Metro Cuadrado Mérida"
                        allow="clipboard-write"
                        loading="lazy">
                    </iframe>
                </div>
            </div>
        `;

        document.body.insertAdjacentHTML('beforeend', widgetHTML);
    }

    // Configurar eventos
    function setupEvents() {
        const button = document.getElementById('m2-chatbot-button');
        const container = document.getElementById('m2-chatbot-container');
        const closeButton = document.getElementById('m2-chatbot-close');

        // Abrir/cerrar al hacer clic en el botón
        button.addEventListener('click', function() {
            const isOpen = container.classList.contains('show');
            if (isOpen) {
                closeChat();
            } else {
                openChat();
            }
        });

        // Cerrar al hacer clic en el botón X
        closeButton.addEventListener('click', function() {
            closeChat();
        });

        // Remover la animación de pulso después del primer clic
        button.addEventListener('click', function() {
            button.classList.remove('pulse');
        }, { once: true });
    }

    // Abrir el chat
    function openChat() {
        const container = document.getElementById('m2-chatbot-container');
        const button = document.getElementById('m2-chatbot-button');
        
        container.classList.add('show');
        button.textContent = '✕';
        button.style.transform = 'rotate(90deg)';
    }

    // Cerrar el chat
    function closeChat() {
        const container = document.getElementById('m2-chatbot-container');
        const button = document.getElementById('m2-chatbot-button');
        
        container.classList.remove('show');
        button.textContent = config.buttonText;
        button.style.transform = 'rotate(0deg)';
    }

    // Inicializar el widget cuando el DOM esté listo
    function init() {
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', function() {
                injectStyles();
                createWidget();
                setupEvents();
            });
        } else {
            injectStyles();
            createWidget();
            setupEvents();
        }
    }

    // Ejecutar inicialización
    init();

    // Exponer funciones públicas (opcional)
    window.M2ChatbotWidget = {
        open: openChat,
        close: closeChat,
        toggle: function() {
            const container = document.getElementById('m2-chatbot-container');
            if (container.classList.contains('show')) {
                closeChat();
            } else {
                openChat();
            }
        }
    };
})();

