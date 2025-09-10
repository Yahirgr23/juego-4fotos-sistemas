Documentación del Proyecto: 4 Fotos 1 Palabra - Duelo 1 vs 1 
1. Introducción al Proyecto 
Este proyecto implementa una versión del popular juego "4 Fotos 1 Palabra" con un 
enfoque en la interacción local y multijugador. Desarrollado en Python utilizando 
customtkinter para la interfaz gráfica y pygame para la gestión de audio, el juego 
permite a los usuarios adivinar una palabra común a cuatro imágenes, crear sus propios 
niveles y compartirlos en una red local. 
2. Estructura de Archivos 
El proyecto está organizado en varios módulos Python, cada uno con responsabilidades 
específicas: 
• main.py: Punto de entrada principal de la aplicación, gestiona la inicialización, 
la navegación entre pantallas y la integración de los demás módulos. 
• animated_credits_screen.py: Maneja la pantalla de créditos animada al inicio del 
juego, incluyendo la generación de sonidos sintéticos. 
• level_editor.py: Proporciona una interfaz gráfica para que los usuarios creen y 
editen sus propios niveles de juego. 
• custom_levels_manager.py: Administra los niveles personalizados creados o 
descargados por el usuario, permitiendo jugarlos, editarlos, compartirlos e 
instalarlos. 
• level_downloader.py: Facilita la descarga de niveles desde diversas fuentes, 
incluyendo la red local, URLs directas y, en el futuro, un servidor público. 
• level_server.py: Implementa un servidor TCP/IP básico para que un jugador 
pueda compartir un nivel con otros en la misma red local. 
• network_game_manager.py: Gestiona la lógica de conexión y comunicación 
entre jugadores en partidas multijugador a través de la red local. 
• game_config.json: Archivo de configuración del juego que almacena ajustes 
como el tema, el estado del sonido y las rutas de los niveles. 
• README.md: Archivo de descripción general del proyecto. 
• requirements.txt: Lista de dependencias Python necesarias para ejecutar el 
proyecto. 
3. Dependencias del Sistema 
Para ejecutar este juego, se requiere Python 3 y las siguientes librerías: 
• customtkinter: Para la interfaz gráfica de usuario. 
• pygame: Para la reproducción y gestión de audio. 
• numpy: Utilizado en la generación de sonidos sintéticos. 
• Pillow (PIL): Para el procesamiento de imágenes (redimensionamiento, manejo 
de formatos). 
• requests: Para realizar peticiones HTTP (descarga de niveles desde URLs). 
• Flask, Flask-SQLAlchemy, Flask-CORS, Flask-SocketIO, Werkzeug, PyJWT, 
python-socketio, eventlet, psycopg2-binary: Componentes relacionados con un 
posible servidor backend (no directamente usados en la lógica de cliente/servidor 
P2P actual, pero listados en requirements.txt). 
4. Funcionalidades Principales 
4.1. main.py - El Corazón de la Aplicación 
El archivo main.py es el coordinador central del juego. 
Funcionalidades Clave: 
• Inicialización: Configura la ventana principal de customtkinter, inicializa 
pygame.mixer para el audio y carga los managers principales. 
• Gestión de Pantallas: Controla la transición entre la pantalla de créditos, el 
menú principal y las pantallas de juego (demo o personalizadas). 
• Managers Globales: Instancia y proporciona acceso a: 
o SoundManager: Para la gestión de efectos de sonido y música de fondo. 
o AnimationManager: Para transiciones visuales suaves. 
o SocketClient: (Aunque un placeholder en la versión proporcionada, se 
sugiere para una futura conexión a un servidor central). 
o LevelEditor: Para crear niveles. 
o CustomLevelsManager: Para gestionar niveles. 
o NetworkGameManager: Para el juego en red. 
• Conexión a Servidor: Incluye lógica para intentar conectar a un servidor 
(posiblemente público) al inicio y un fallback a modo demo si la conexión falla. 
• Manejo de Eventos: Gestiona el cierre seguro de la aplicación, asegurando que 
todos los recursos (sonidos, ventanas, conexiones) se liberen correctamente. 
Diagrama de flujo de funcionamiento: 
4.2. animated_credits_screen.py - Créditos Animados 
Esta clase se encarga de mostrar una atractiva pantalla de créditos con animaciones y 
sonidos al inicio del juego. 
Funcionalidades Clave: 
• Creación de Ventana: Genera una ventana CTkToplevel independiente para los 
créditos. 
• Sonidos Sintéticos: Utiliza pygame y numpy para crear sonidos únicos 
(aparición, brillo, whoosh, fanfarria, ambiente) directamente en el código, sin 
necesidad de archivos de audio externos. 
o  
▪ Secuencia de Animación: Controla la aparición secuencial de 
elementos de texto (título, subtítulo, nombres de desarrolladores, 
mensaje final) con efectos de fade-in, pulse y bounce. 
• Cierre Automático/Manual: Los créditos se cierran automáticamente después 
de un tiempo o pueden ser saltados por el usuario. Al cerrarse, transfiere el 
control al menú principal. 
4.3. level_editor.py - Editor de Niveles 
Permite a los usuarios diseñar y guardar sus propios niveles personalizados del juego. 
Funcionalidades Clave: 
• Interfaz Completa: Ofrece campos para el título del nivel, autor, descripción y 
dificultad. 
o  
▪ Gestión de Palabras/Rondas: Los niveles se componen de 
múltiples "rondas", cada una con una palabra a adivinar y hasta 
cuatro imágenes. 
o Edición por Ronda: Permite al usuario editar la palabra y la pista de la 
ronda actual. 
o Gestión de Imágenes: 
▪ Carga de Imágenes: Los usuarios pueden seleccionar imágenes 
desde su sistema de archivos o pegarlas directamente desde el 
portapapeles. 
▪ Arrastrar y Soltar (Drag & Drop): Soporte para arrastrar 
archivos de imagen directamente a los slots correspondientes. 
▪ Almacenamiento de Imágenes: Las imágenes se convierten a 
formato Base64 y se incrustan directamente en el archivo JSON 
del nivel, lo que facilita la portabilidad y el intercambio. 
▪     * **Eliminación de Imágenes:** Opción para quitar 
imágenes de los slots. 
▪  
o Navegación: Permite avanzar o retroceder entre las palabras (rondas) del 
nivel. 
o Validación: Verifica que el nivel cumpla con los requisitos mínimos (ej. 
palabra, al menos 1 imagen) y proporciona advertencias. 
• Guardado y Carga: 
o Guardar Ronda: Persiste los cambios de la ronda actual en la estructura 
de datos del nivel. 
o Guardar Nivel Completo: Guarda todo el nivel como un archivo .json o 
un paquete .4f1p en la carpeta custom_levels. 
o Cargar Nivel: Permite abrir niveles existentes para su edición. 
• Prueba de Nivel: Integra una función para probar el nivel que se está creando 
directamente en el juego, sin necesidad de salir del editor. 
• Exportar Nivel: Permite exportar el nivel como un archivo .4f1p (un formato 
de paquete personalizado basado en JSON que incluye metadatos y todas las 
imágenes Base64) para compartirlo fácilmente. 
4.4. custom_levels_manager.py - Gestor de Niveles Personalizados 
Este módulo proporciona una interfaz para que los usuarios administren todos los 
niveles que han creado o descargado. 
Funcionalidades Clave: 
• Pestañas de Organización: Organiza los niveles en categorías: 
o Mis Niveles (        
en el editor. 
Mis Niveles): Muestra los niveles creados por el usuario 
▪ * **Descargados (`     
Descargados`):** Muestra los niveles 
obtenidos de otras fuentes (importados, de red local, etc.). 
o Red Local (  
Red Local): Busca y muestra niveles compartidos por 
otros usuarios en la misma red WiFi. 
o Importar (     Importar): Herramientas para importar niveles desde 
archivos o carpetas. 
• Acciones por Nivel: Para cada nivel listado, ofrece opciones como: 
o Jugar (            Jugar): Inicia una partida con ese nivel. 
o Editar (      
Editar): Abre el nivel en el LevelEditor. 
o Compartir (     Compartir): Exporta el nivel para compartirlo. 
o Eliminar (   ): Borra el archivo del nivel. 
o Instalar (     
Niveles". 
Instalar): Mueve un nivel de "Descargados" a "Mis 
• Filtrado y Búsqueda: Permite filtrar niveles por dificultad o buscar por 
título/autor. 
• Gestión de Directorios: Organiza los niveles en carpetas custom_levels y 
downloaded_levels. 
• Integración con Red: Se conecta con NetworkGameManager para obtener 
niveles disponibles en la red y con LevelDownloader para importar. 
4.5. level_downloader.py - Descargador de Niveles 
Un módulo para obtener niveles de diferentes fuentes. 
Funcionalidades Clave: 
• Pestañas de Descarga: 
o Red Local (  
Red Local): Permite escanear la red para encontrar 
servidores de niveles activos y conectarse manualmente a ellos. 
▪ * **Online (`   
Online`):** (Función futura) Diseñado para 
interactuar con un servidor público central, con opciones de filtro 
y 
búsqueda. Actualmente, es un placeholder que muestra 
información sobre funcionalidades planificadas. 
▪  
o URL Directa (   URL Directa): Permite pegar una URL para descargar 
un archivo de nivel directamente. 
• Búsqueda por Código de Sala: Permite a los usuarios buscar una sala específica 
usando un código generado por el host. 
• Selección de Archivo Local: Facilita la importación de archivos de nivel desde 
el sistema de archivos del usuario. 
4.6. level_server.py - Servidor de Nivel Local 
Este script permite a un jugador actuar como host y compartir uno de sus niveles con 
otros jugadores en la misma red local. 
Funcionalidades Clave: 
• Servidor TCP/IP: Crea un socket de servidor que escucha conexiones entrantes. 
• Descubrimiento de IP y Puerto: Detecta automáticamente la IP local de la 
máquina y encuentra un puerto libre para el servidor. 
• Código de Sala: Genera un código alfanumérico único de 6 dígitos para que 
otros jugadores puedan identificar y unirse a la sala. 
• Manejo de Clientes: Acepta conexiones de múltiples clientes en hilos separados 
para no bloquear el servidor. 
• Servicio de Nivel: Cuando un cliente se conecta, el servidor puede enviar la 
información del nivel al cliente en formato JSON, incluyendo los metadatos y 
los datos de las imágenes incrustadas. 
• Interfaz Web Simple: Genera una página HTML básica (/) con información del 
servidor y un botón para descargar el nivel, accesible a través del navegador web 
desde la red local. También sirve el archivo JSON del nivel (/level). 
o  
▪ Heartbeat: Mantiene la conexión activa con los clientes enviando 
pequeños paquetes de datos periódicamente. 
4.7. network_game_manager.py - Gestor de Juego en Red 
Este módulo maneja toda la lógica de conexión, creación de salas y uniones para 
partidas multijugador en la red local. 
Funcionalidades Clave: 
• Host (Crear Sala): 
o Inicia un servidor TCP/IP local. 
o Espera a que los clientes se conecten. 
o Una vez conectado un cliente, el host puede seleccionar un nivel de su 
colección (utilizando CustomLevelsManager). 
o Envía los datos del nivel seleccionado al cliente. 
o Sincroniza el inicio del juego. 
• Cliente (Unirse a Sala): 
o Se conecta a la IP y puerto del host. 
o Recibe los datos del nivel del host. 
o Sincroniza el inicio del juego. 
• Comunicación en Tiempo Real: 
o Envío/Recepción de Mensajes: Implementa un protocolo de 
comunicación basado en JSON sobre sockets TCP, incluyendo un 
encabezado de longitud para asegurar la integridad de los mensajes. 
o Mensajes de Juego: Permite el intercambio de eventos de juego como 
palabras adivinadas, intentos fallidos y mensajes de chat rápido (emojis). 
o Callbacks: Se integra con la clase principal del juego (JuegoApp) para 
que los eventos de red actualicen la interfaz de usuario en tiempo real. 
• Validación de Conexión: Incluye funciones para probar la conectividad a una 
IP antes de intentar una unión completa, proporcionando mensajes de error útiles. 
• Manejo de Desconexiones: Detecta y gestiona la desconexión de clientes o del 
host. 
• Heartbeat: Mantiene la conexión activa enviando pequeños paquetes de datos 
periódicamente, detectando si el otro extremo se ha desconectado 
inesperadamente. 
5. game_config.json - Configuración del Juego 
Este archivo JSON almacena configuraciones persistentes para la aplicación, 
permitiendo personalizar el comportamiento del juego sin modificar el código. 
Estructura del Archivo: 
{ 
"version": "1.0", 
"last_update": "2025-05-29T17:05:50.395696", 
"settings": { 
"theme": "dark", 
"sound_enabled": true, 
"auto_save": true, 
"default_difficulty": "Medio" 
}, 
"paths": { 
"custom_levels": "custom_levels", 
"downloaded_levels": "downloaded_levels", 
"assets": "assets" 
} 
} 
Parámetros Importantes: 
• version: Versión actual del archivo de configuración. 
• last_update: Marca de tiempo de la última modificación. 
• settings: Objeto que contiene ajustes del juego: 
o theme: Tema de la interfaz ("dark", "light"). 
o sound_enabled: Si el sonido está activado (booleano). 
o auto_save: Si el auto-guardado está activado. 
o default_difficulty: Dificultad por defecto para nuevos niveles. 
• paths: Rutas a directorios importantes: 
o custom_levels: Carpeta para niveles creados por el usuario. 
o downloaded_levels: Carpeta para niveles descargados. 
o assets: Carpeta de recursos (sonidos, etc.). 
6. Diagramas de Interacción entre Módulos 
6.1. Diagrama General de Módulos 
graph TD 
A[main.py: App Principal] --> B(animated_credits_screen.py: Créditos); 
A --> C(clientescreens/menu_principal.py: Menú); 
C --> D(level_editor.py: Editor de Niveles); 
C --> E(custom_levels_manager.py: Gestor de Niveles); 
C --> F(network_game_manager.py: Gestor Red Local); 
E -- solicita niveles --> G(level_downloader.py: Descargador); 
F -- usa --> E; 
G -- puede usar --> F; 
F --> H(level_server.py: Servidor de Nivel); 
A --> I(clienteutils/sound_manager.py: Sonido); 
A --> J(clienteutils/animation_manager.py: Animación); 
A -- (futuro) --> K(clientenetwork/socket_client.py: Cliente API); 
D -- guarda/carga --> L(Archivos .json/.4f1p); 
E -- lee/escribe --> L; 
G -- lee/escribe --> L; 
H -- lee --> L; 
F -- lee --> L; 
A -- lee/escribe --> M(game_config.json: Configuración); 
6.2. Flujo de Creación y Compartición de Niveles 
graph LR 
A[Usuario en Menú Principal] --> B(Abre Editor de Niveles); 
B -- Crea Palabra/Ronda --> C(Agrega 4 Imágenes); 
C -- Guarda Ronda --> D{Nivel Data Structure}; 
D -- Guarda Nivel Completo --> E(Archivo .json/.4f1p en custom_levels/); 
E -- (Desde Menú Principal) --> F(Abre Gestor de Niveles); 
F -- Muestra Niveles Locales --> E; 
E -- Exporta Nivel --> G(Archivo .4f1p para compartir); 
G -- Comparte con otro usuario --> H[Otro Usuario]; 
H -- Importa Nivel --> I(Archivo .4f1p en downloaded_levels/); 
I -- Instala Nivel --> E; 
6.3. Flujo de Juego en Red Local 
graph TD 
A[Jugador A (Host)] --> B(Crea Sala en NetworkGameManager); 
B -- Obtiene IP y Código --> C(Muestra IP/Código al Jugador B); 
C --> D[Jugador B (Cliente)]; 
D -- Ingresa IP del Host --> E(Se Une a Sala en NetworkGameManager); 
B -- Espera Conexión --> D; 
B -- Confirma Conexión --> D; 
B -- Host selecciona Nivel --> F(Muestra Selector de Niveles); 
F -- Envía Nivel Seleccionado --> D; 
B -- Inicia Juego --> G(Pantalla de Juego Multijugador); 
D -- Recibe Nivel y Inicia Juego --> G; 
G -- Envía Respuestas/Emojis --> B; 
G -- Recibe Respuestas/Emojis --> D; 
G -- Sincroniza Puntuación --> G; 
7. Notas de Desarrollo y Consideraciones Futuras 
• Modularidad: El proyecto está diseñado con una fuerte modularidad, lo que 
facilita la adición de nuevas funcionalidades y el mantenimiento. 
• Persistencia de Datos: Los niveles se guardan en formato JSON, permitiendo 
una fácil inspección y edición externa. Las imágenes se incrustan en Base64 para 
simplificar el intercambio de archivos. 
• Manejo de Errores: Se incluye un manejo básico de errores con try-except y 
mensajes informativos para el usuario, especialmente en operaciones de archivo 
y red. 
• Experiencia de Usuario: Se han implementado animaciones y sonidos para 
mejorar la inmersión y la retroalimentación del usuario. 
• Funcionalidades Futuras: El código incluye estructuras y placeholders para 
funcionalidades futuras como un servidor público de niveles, más opciones de 
juego online, y una galería de niveles de la comunidad. 
• Seguridad: Para el entorno de red local, se asume un entorno de confianza. Para 
un servidor público, se requerirían capas de seguridad y autenticación más 
robusta
