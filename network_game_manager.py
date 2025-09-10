#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import json
import time
from datetime import datetime
import customtkinter as ctk
from tkinter import messagebox
import tkinter.messagebox as msgbox  # ← ESTE FALTABA
import os  
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class NetworkGameManager:
    def __init__(self, parent_app):
        self.app = parent_app
        self.server_socket = None
        self.client_socket = None
        self.is_host = False
        self.is_server = False  # ← AGREGAR ESTA LÍNEA
        self.is_connected = False
        self.opponent_name = ""
        self.game_room_code = ""
        self.network_window = None
        self.available_levels = []
        self.current_game_level = None
        self.custom_levels_manager = None
        self.client_sockets = []  # ← AGREGAR ESTA LÍNEA TAMBIÉN


    def set_custom_levels_manager(self, custom_levels_manager):
        """Establecer manager de niveles personalizados"""
        self.custom_levels_manager = custom_levels_manager
        self.load_available_levels()
        print("🔗 Custom levels manager conectado")




    def start_heartbeat(self):
        """Iniciar heartbeat para mantener la conexión activa"""
        def send_heartbeat():
            while self.is_connected:
                try:
                    heartbeat_msg = {
                        "type": "heartbeat",
                        "timestamp": time.time()
                    }
                
                    if self.is_host:
                        # Host envía a todos los clientes
                        for client in self.client_sockets[:]:  # Copia para evitar modificación durante iteración
                            try:
                                if not self.send_message_to_socket(client, heartbeat_msg):
                                    self.cleanup_client(client)
                            except:
                                self.cleanup_client(client)
                    else:
                        # Cliente envía al host
                        if self.client_socket:
                            try:
                                self.send_message_to_socket(self.client_socket, heartbeat_msg)
                            except:
                                print("❌ Conexión con el host perdida")
                                self.is_connected = False
                                break
                
                # Esperar 5 segundos antes del siguiente heartbeat
                    time.sleep(5)
                
                except Exception as e:
                    print(f"❌ Error en heartbeat: {e}")
                    break
    
    # Iniciar en hilo separado
        heartbeat_thread = threading.Thread(target=send_heartbeat, daemon=True)
        heartbeat_thread.start()
        print("💓 Heartbeat iniciado")

    # En network_game_manager.py, reemplaza la función entera con esta versión:

    def load_available_levels(self):
        """Cargar todos los niveles disponibles - VERSIÓN CORREGIDA FINAL"""
        self.available_levels = []
        print("🔄 Cargando lista de niveles disponibles para la red...")

        try:
            # --- INICIO DE LA CORRECCIÓN ---
            # 1. Cargar niveles personalizados
            if self.custom_levels_manager:
                print("   -> Pidiendo niveles al CustomLevelsManager...")
                # La función get_available_levels() ya nos da la lista en el formato correcto.
                # Simplemente la tomamos y la añadimos directamente.
                custom_levels_list = self.custom_levels_manager.get_available_levels()
                self.available_levels.extend(custom_levels_list)
                print(f"   -> {len(custom_levels_list)} niveles personalizados añadidos.")
            else:
                print("   -> Advertencia: CustomLevelsManager no está conectado.")
        # --- FIN DE LA CORRECCIÓN ---
    
            # 2. Cargar niveles descargados (esta parte ya estaba bien)
            downloaded_path = "downloaded_levels"
            if os.path.exists(downloaded_path):
                downloaded_count = 0
                for filename in os.listdir(downloaded_path):
                    if filename.endswith('.json'):
                        try:
                            filepath = os.path.join(downloaded_path, filename)
                            with open(filepath, 'r', encoding='utf-8') as f:
                                level_data = json.load(f)
                            
                                # Empaquetamos los descargados en el formato correcto
                                metadata = level_data.get('metadata', {})
                                level_name = metadata.get('title', filename.replace('.json', ''))
                            
                                self.available_levels.append({
                                    "type": "downloaded", 
                                    "name": level_name,
                                    "data": level_data,
                                    "id": f"downloaded_{filename}"
                                })
                                downloaded_count += 1
                        except Exception as e:
                            print(f"⚠️ Error cargando nivel descargado {filename}: {e}")
                print(f"   -> {downloaded_count} niveles descargados añadidos.")
    
            print(f"📚 Total de niveles disponibles para la red: {len(self.available_levels)}")
        
            if not self.available_levels:
                print("⚠️ No se encontró ningún nivel disponible.")
        
        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ Error crítico cargando niveles: {e}")
        

    def show_level_selection(self):
        """Mostrar ventana de selección de nivel (SOLO PARA HOST)"""
        if not self.is_host:  # ← CAMBIAR de is_server a is_host
            self.show_error("Error", "Solo el host puede seleccionar niveles")
            return
    
        if not self.available_levels:
            self.show_error("Sin niveles", "No hay niveles disponibles.\n\nCrea niveles en el editor primero.")
            return
    
    # Crear ventana de selección
        level_window = ctk.CTkToplevel()
        level_window.title("🎯 Seleccionar Nivel para Jugar")
        level_window.geometry("600x700")
        level_window.resizable(False, False)
    
    # Centrar ventana
        level_window.update_idletasks()
        x = (level_window.winfo_screenwidth() // 2) - (300)
        y = (level_window.winfo_screenheight() // 2) - (350)
        level_window.geometry(f"600x700+{x}+{y}")
    
    # Hacer ventana modal
        level_window.transient()
        level_window.grab_set()
    
    # Marco principal
        main_frame = ctk.CTkFrame(level_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
        title_label = ctk.CTkLabel(
            main_frame,
            text="🎯 Selecciona el Nivel",
            font=ctk.CTkFont(size=28, weight="bold")
        )
        title_label.pack(pady=20)
    
    # Subtítulo
        subtitle_label = ctk.CTkLabel(
            main_frame,
            text="Ambos jugadores jugarán este mismo nivel",
            font=ctk.CTkFont(size=16),
            text_color="gray"
        )
        subtitle_label.pack(pady=5)
    
    # Información
        info_label = ctk.CTkLabel(
            main_frame,
            text=f"📚 {len(self.available_levels)} niveles disponibles",
            font=ctk.CTkFont(size=14)
        )
        info_label.pack(pady=10)
    
    # Frame scrollable para lista de niveles
        levels_frame = ctk.CTkScrollableFrame(main_frame, width=550, height=450)
        levels_frame.pack(pady=20, fill="both", expand=True)
    
    # Agregar niveles a la lista
        for i, level in enumerate(self.available_levels):
        # Frame para cada nivel
            level_frame = ctk.CTkFrame(levels_frame)
            level_frame.pack(fill="x", padx=10, pady=8)
        
        # Frame para información del nivel
            info_frame = ctk.CTkFrame(level_frame)
            info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=15)
        
        # Número del nivel
            number_label = ctk.CTkLabel(
                info_frame,
                text=f"#{i+1}",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="gray",
                anchor="w"
            )
            number_label.pack(anchor="w")
        
        # Nombre del nivel
            name_label = ctk.CTkLabel(
                info_frame,
                text=level["name"],
                font=ctk.CTkFont(size=18, weight="bold"),
                anchor="w"
            )
            name_label.pack(anchor="w", pady=(5, 0))
        
        # Tipo de nivel con color
            if level["type"] == "custom":
                type_text = "📝 Nivel Personalizado"
                type_color = "#4CAF50"
            else:
                type_text = "📥 Nivel Descargado"
                type_color = "#2196F3"
        
            type_label = ctk.CTkLabel(
                info_frame,
                text=type_text,
                font=ctk.CTkFont(size=14),
                text_color=type_color,
                anchor="w"
            )
            type_label.pack(anchor="w", pady=(2, 0))
        
        # Información adicional del nivel
            level_data = level["data"]
            if "word" in level_data:
                word_label = ctk.CTkLabel(
                    info_frame,
                    text=f"🎯 Palabra: {level_data['word'].upper()}",
                    font=ctk.CTkFont(size=12),
                    text_color="orange",
                    anchor="w"
                )
                word_label.pack(anchor="w", pady=(2, 0))
        
        # Botón para seleccionar este nivel
            select_button = ctk.CTkButton(
                level_frame,
                text="▶️ JUGAR\nESTE NIVEL",
                command=lambda lvl=level: self.start_game_with_level(lvl, level_window),
                width=120,
                height=80,
                font=ctk.CTkFont(size=14, weight="bold"),
                fg_color="#4CAF50",
                hover_color="#45A049"
            )
            select_button.pack(side="right", padx=15, pady=15)
    
    # Frame para botones inferiores
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", pady=10)
    
    # Botón para recargar niveles
        reload_button = ctk.CTkButton(
            buttons_frame,
            text="🔄 Recargar Niveles",
            command=lambda: self.reload_levels_and_refresh(level_window),
            width=180,
            height=40,
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        reload_button.pack(side="left", padx=10, pady=10)
    
    # Botón cancelar
        cancel_button = ctk.CTkButton(
            buttons_frame,
            text="❌ Cancelar",
            command=level_window.destroy,
            width=180,
            height=40,
            fg_color="#f44336",
            hover_color="#d32f2f"
        )
        cancel_button.pack(side="right", padx=10, pady=10)


    def reload_levels_and_refresh(self, level_window):
        """Recargar niveles y refrescar ventana"""
        level_window.destroy()
        self.load_available_levels()
        self.show_level_selection()


    def start_game_with_level(self, selected_level, level_window):
        """Iniciar juego con el nivel seleccionado - VERSIÓN CORREGIDA"""
        try:
            print(f"🎮 [HOST] Iniciando juego con nivel: {selected_level['name']}")
        
        # Cerrar ventana de selección
            level_window.destroy()
        
        # Guardar nivel actual
            self.current_game_level = selected_level
        
        # Configurar estado multijugador para el host
            self.app.is_multiplayer = True
            self.app.opponent_name = self.opponent_name
        
        # Preparar mensaje con el nivel
            level_message = {
                "type": "game_level",
                "level_data": selected_level["data"],
                "level_name": selected_level["name"],
                "level_type": selected_level["type"]
            }
        
            # Enviar nivel a todos los clientes conectados
            print(f"📤 [HOST] Enviando nivel a {len(self.client_sockets)} clientes...")
            self.broadcast_to_clients(level_message)
        
        # Dar tiempo para que el mensaje llegue
            time.sleep(0.5)
        
        # Iniciar juego en el host
            print("🎮 [HOST] Iniciando juego local...")
            self.start_local_game(selected_level["data"])
        
        except Exception as e:
            print(f"❌ Error iniciando juego: {e}")
            import traceback
            traceback.print_exc()
            self.show_error("Error", f"No se pudo iniciar el juego:\n{str(e)}")


    def start_local_game(self, level_data):
        """Realiza la transición de la UI del lobby a la pantalla de juego."""
        try:
            level_name = level_data.get('metadata', {}).get('title', 'Sin Nombre')
            print(f"🎮 Iniciando transición a juego local para el nivel: '{level_name}'")

        # 1. Cierra la ventana del lobby de red.
            self.cleanup_lobby_ui()

        # 2. Configurar correctamente el estado multijugador
            self.app.is_multiplayer = True
            if self.is_host:
                self.app.player_name = self.app.player_name
                self.app.opponent_name = self.opponent_name
            else:
                self.app.player_name = self.app.player_name
                self.app.opponent_name = self.opponent_name
        
        # 3. Asignar el network_manager a la app para que el juego pueda acceder
            self.app.network_manager = self
        
        # 4. Iniciar la pantalla del juego
            if hasattr(self.app, 'start_custom_level'):
                print(f"🎮 Llamando a start_custom_level con nivel: {level_name}")
                self.app.root.after(50, lambda: self.app.start_custom_level(level_data))
            else:
                print("⚠️ El método 'start_custom_level' no existe en la app principal.")

        except Exception as e:
            import traceback
            traceback.print_exc()
            print(f"❌ Error iniciando juego local: {e}")


    def set_game_callbacks(self, game_instance):
        """Establecer callbacks del juego"""
        self.game_instance = game_instance

    def send_word_guessed(self, data):
        """Enviar cuando se adivina una palabra"""
        message = {
            "type": "word_guessed",
            "data": data
        }
        self.broadcast_game_message(message)

    def send_wrong_attempt(self, data):
        """Enviar intento fallido"""
        message = {
            "type": "wrong_attempt",
            "data": data
        }
        self.broadcast_game_message(message)

    def send_chat_message(self, data):
        """Enviar mensaje de chat - VERSIÓN CORREGIDA"""
        message = {
            "type": "chat_message",
            "data": data
        }
    
        if self.is_host:
            # El host envía a todos los clientes
            self.broadcast_to_clients(message)
        else:
        # El cliente envía al host
            if hasattr(self, 'client_socket') and self.client_socket:
                try:
                    self.send_message_to_socket(self.client_socket, message)
                except Exception as e:
                    print(f"❌ Error enviando chat al host: {e}")

                    
    def broadcast_game_message(self, message):  
        """Enviar mensaje de juego"""
        if self.is_host:
            self.broadcast_to_clients(message)
        else:
            self.send_message_to_socket(self.client_socket, message)

    def handle_game_message(self, message, source_socket=None):
        """Manejar mensajes durante el juego"""
        msg_type = message.get("type")
        data = message.get("data", {})
    
        if msg_type == "word_guessed":
            # Reenviar a todos si es host
            if self.is_host and source_socket:
                for client in self.client_sockets:
                    if client != source_socket:
                        self.send_message_to_socket(client, message)
        
        # Notificar al juego
            if hasattr(self, 'game_instance'):
                self.app.root.after(0, lambda: self.game_instance.on_opponent_guessed_word(data))
    
        elif msg_type == "wrong_attempt":
        # Similar al anterior
            if self.is_host and source_socket:
                for client in self.client_sockets:
                    if client != source_socket:
                        self.send_message_to_socket(client, message)
        
            if hasattr(self, 'game_instance'):
                self.app.root.after(0, lambda: self.game_instance.on_opponent_wrong_attempt(data))
    
        elif msg_type == "chat_message":
        # Reenviar chat
            if self.is_host and source_socket:
                for client in self.client_sockets:
                    if client != source_socket:
                        self.send_message_to_socket(client, message)
        
        # Mostrar en chat local
            if hasattr(self, 'game_instance'):
                emoji = data.get('emoji', '')
                player = data.get('player', 'Jugador')
                self.app.root.after(0, lambda: self.game_instance.add_to_chat(player, emoji, is_self=False))

    def handle_client_message(self, message, client_socket):
        """Manejar mensajes de clientes - VERSIÓN COMPLETA"""
        try:
        # Si el mensaje es string, parsearlo
            if isinstance(message, str):
                data = json.loads(message)
            else:
                data = message
            
            msg_type = data.get("type")
        
            print(f"📨 Mensaje recibido del cliente: {msg_type}")
        
        # Manejar diferentes tipos de mensajes
            if msg_type == "ready_for_game":
                print("✅ Cliente listo para jugar")
            # Si ya hay un nivel seleccionado, enviarlo inmediatamente
                if self.current_game_level:
                    level_message = {
                        "type": "game_level",
                        "level_data": self.current_game_level["data"],
                        "level_name": self.current_game_level["name"],
                        "level_type": self.current_game_level["type"]
                    }
                    self.send_message_to_socket(client_socket, level_message)
                    print("📤 Nivel actual enviado a cliente que se conectó")
        
            elif msg_type == "request_game_start":
                print("🎮 Cliente solicita inicio de juego")
            # El host debe seleccionar un nivel
                if hasattr(self, 'network_window') and self.network_window:
                    self.network_window.after(0, self.show_level_selection)
        
            elif msg_type == "player_answer":
            # Manejar respuesta del jugador
                answer = data.get("answer", "")
                player_name = data.get("player_name", "Jugador")
                print(f"📝 Respuesta de {player_name}: {answer}")
                self.handle_player_answer(answer, client_socket, player_name)
        
            elif msg_type == "player_name":
                # Guardar nombre del jugador
                player_name = data.get("name", "Jugador")
                print(f"👤 Jugador conectado: {player_name}")
            
            elif msg_type == "chat_message":
            # Mensaje de chat recibido
                print(f"💬 Chat de {data.get('player', 'Jugador')}: {data.get('data', {})}")
                # Reenviar a todos los demás clientes
                self.handle_game_message(data, client_socket)
            
            elif msg_type == "word_guessed":
                # Jugador adivinó una palabra
                print(f"✅ {data.get('data', {}).get('player', 'Jugador')} adivinó una palabra")
                self.handle_game_message(data, client_socket)
            
            elif msg_type == "wrong_attempt":
                # Intento fallido
                print(f"❌ Intento fallido de {data.get('data', {}).get('player', 'Jugador')}")
                self.handle_game_message(data, client_socket)
            
            elif msg_type == "game_over":
                # Juego terminado
                print(f"🏁 Juego terminado por {data.get('player', 'Jugador')}")
            # Reenviar a todos
                for client in self.client_sockets:
                    if client != client_socket:
                        self.send_message_to_socket(client, data)
                    
            elif msg_type == "disconnect":
            # Cliente se desconecta
                print(f"👋 {data.get('player', 'Jugador')} se desconectó")
                self.cleanup_client(client_socket)
                # Notificar a otros clientes
                disconnect_msg = {
                    "type": "player_disconnected",
                    "player": data.get('player', 'Jugador')
                }
                for client in self.client_sockets:
                    if client != client_socket:
                        self.send_message_to_socket(client, disconnect_msg)
        
            else:
                print(f"⚠️ Tipo de mensaje no reconocido: {msg_type}")
            # Reenviar mensajes desconocidos a otros clientes por si acaso
                for client in self.client_sockets:
                    if client != client_socket:
                        self.send_message_to_socket(client, data)
            
        except json.JSONDecodeError as e:
            print(f"❌ Error decodificando JSON: {e}")
            print(f"   Mensaje raw: {message}")
        except Exception as e:
            print(f"❌ Error procesando mensaje del cliente: {e}")
            import traceback
            traceback.print_exc()


    def handle_server_message(self, message):
        """Manejar mensajes del servidor (PARA CLIENTES) - VERSIÓN CORREGIDA"""
        try:
            print(f"🔵 [CLIENTE] Procesando mensaje: {message.get('type')}")
        
            msg_type = message.get("type")
        
            if msg_type == "game_level":
                print("🎮 [CLIENTE] Nivel de juego recibido!")
                level_data = message.get("level_data")
            
                if level_data:
                # Configurar el estado multijugador
                    self.app.is_multiplayer = True
                    self.app.opponent_name = self.opponent_name
                
                # IMPORTANTE: Asegurar que la UI se actualice en el hilo principal
                    if hasattr(self.app, 'root') and self.app.root:
                        print("🚀 [CLIENTE] Iniciando juego en hilo principal...")
                        self.app.root.after(100, lambda: self.start_local_game(level_data))
                    else:
                        print("❌ [CLIENTE] No se encontró ventana principal")
                else:
                    print("❌ [CLIENTE] Datos de nivel vacíos")
                
            elif msg_type == "word_guessed":
            # Palabra adivinada por el oponente
                if hasattr(self, 'game_instance') and self.game_instance:
                    data = message.get("data", {})
                    self.app.root.after(0, lambda: self.game_instance.on_opponent_guessed_word(data))
                
            elif msg_type == "wrong_attempt":
                # Intento fallido del oponente
                if hasattr(self, 'game_instance') and self.game_instance:
                    data = message.get("data", {})
                    self.app.root.after(0, lambda: self.game_instance.on_opponent_wrong_attempt(data))
                
            elif msg_type == "chat_message":
            # Mensaje de chat
                if hasattr(self, 'game_instance') and self.game_instance:
                    data = message.get("data", {})
                    emoji = data.get('emoji', '')
                    player = data.get('player', 'Oponente')
                    self.app.root.after(0, lambda: self.game_instance.add_to_chat(player, emoji, is_self=False))
                
        except Exception as e:
            print(f"❌ [CLIENTE] Error procesando mensaje: {e}")
            import traceback
            traceback.print_exc()



    def handle_player_answer(self, answer, client_socket, player_name):
        """Manejar respuesta de un jugador"""
        try:
            print(f"🎯 Procesando respuesta de {player_name}: {answer}")
        
        # Aquí debes implementar la lógica de verificación de respuesta
        # según tu juego actual
        
            if self.current_game_level:
                correct_word = self.current_game_level["data"].get("word", "").upper()
                player_answer = answer.upper().strip()
            
                if player_answer == correct_word:
                    print(f"✅ {player_name} acertó!")
                
                # Enviar mensaje de victoria
                    win_message = {
                        "type": "player_won",
                        "winner": player_name,
                        "correct_word": correct_word
                    }
                    self.broadcast_to_clients(win_message)
                
                else:
                    print(f"❌ {player_name} falló: {player_answer} != {correct_word}")
        
        except Exception as e:
            print(f"❌ Error procesando respuesta: {e}")



    def broadcast_to_clients(self, message):
    
        """Enviar mensaje a todos los clientes conectados - VERSIÓN MEJORADA"""
        if not self.is_host:
            print("⚠️ Solo el host puede hacer broadcast")
            return
    
        try:
            disconnected_clients = []
        
        # Verificar que hay clientes conectados
            if hasattr(self, 'client_sockets') and self.client_sockets:
            # Filtrar clientes válidos
                valid_clients = []
                for client_socket in self.client_sockets:
                    try:
                    # Verificar que el socket sigue siendo válido
                        if client_socket and client_socket.fileno() != -1:
                            valid_clients.append(client_socket)
                        else:
                            disconnected_clients.append(client_socket)
                    except:
                        disconnected_clients.append(client_socket)
            
            # Actualizar lista de clientes
                self.client_sockets = valid_clients
            
                if valid_clients:
                    print(f"📡 Broadcasting a {len(valid_clients)} clientes válidos...")
                
                    for client_socket in valid_clients:
                        try:
                            success = self.send_message_to_socket(client_socket, message)
                            if success:
                                print(f"✅ Mensaje enviado exitosamente a cliente")
                            else:
                                print(f"❌ Fallo al enviar a cliente")
                                disconnected_clients.append(client_socket)
                        except Exception as e:
                            print(f"⚠️ Cliente desconectado: {e}")
                            disconnected_clients.append(client_socket)
                else:
                    print("⚠️ No hay clientes válidos conectados para broadcast")
                
            # Remover clientes desconectados
                for client in disconnected_clients:
                    if client in self.client_sockets:
                        self.client_sockets.remove(client)
                        try:
                            client.close()
                        except:
                            pass
                        print("🔌 Cliente removido de la lista")
            else:
                print("⚠️ No hay clientes conectados para broadcast")
            
        except Exception as e:
            print(f"❌ Error en broadcast: {e}")
            import traceback
            traceback.print_exc()




    


    def get_local_ip(self):
        """Obtener la IP local real - NUEVO MÉTODO"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            print(f"📍 IP local detectada: {local_ip}")
            return local_ip
        except Exception as e:
            print(f"❌ Error obteniendo IP: {e}")
            return "127.0.0.1"
    
    def test_connection_before_join(self, ip, port=8888):
        """Probar conexión antes de intentar unirse - NUEVO MÉTODO"""
        print(f"🔗 Probando conexión a {ip}:{port}...")
        
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)  # 3 segundos timeout
            
            start_time = time.time()
            result = sock.connect_ex((ip, port))
            end_time = time.time()
            
            sock.close()
            
            if result == 0:
                print(f"✅ Conexión exitosa en {(end_time - start_time)*1000:.0f}ms")
                return True, "Conexión exitosa"
            else:
                error_msg = self.get_connection_error_message(result)
                print(f"❌ Conexión falló: {error_msg}")
                return False, error_msg
                
        except Exception as e:
            error_msg = f"Error de conexión: {str(e)}"
            print(f"❌ {error_msg}")
            return False, error_msg
    
    def get_connection_error_message(self, error_code):
        """Obtener mensaje de error amigable - NUEVO MÉTODO"""
        error_messages = {
            10060: "Timeout - El dispositivo no responde. Verifica que esté en la misma red WiFi.",
            10061: "Conexión rechazada - No hay servidor ejecutándose. El host debe crear sala primero.",
            11001: "Host no encontrado - IP incorrecta o dispositivo apagado.",
            10065: "Red no alcanzable - Verifica tu conexión WiFi."
        }
        
        return error_messages.get(error_code, f"Error desconocido: {error_code}")
    
    def scan_local_network(self):
        """Escanear red local para encontrar servidores del juego - NUEVO MÉTODO"""
        print("🔍 Escaneando red local...")
        
        local_ip = self.get_local_ip()
        if local_ip == "127.0.0.1":
            return []
        
        # Obtener rango de red
        ip_parts = local_ip.split('.')
        network_base = '.'.join(ip_parts[:3])
        
        found_servers = []
        
        def check_ip(ip):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((ip, 8888))
                sock.close()
                
                if result == 0:
                    found_servers.append(ip)
                    print(f"🎮 Servidor encontrado en: {ip}")
            except:
                pass
        
        # Escanear IPs comunes primero (más rápido)
        common_ips = [f"{network_base}.{i}" for i in [1, 2, 100, 101, 102, 254]]
        
        threads = []
        for ip in common_ips:
            if ip != local_ip:
                t = threading.Thread(target=check_ip, args=(ip,))
                t.start()
                threads.append(t)
        
        # Esperar resultados
        for t in threads:
            t.join(timeout=2)
        
        return found_servers
    
    # 🔧 MODIFICAR EL MÉTODO EXISTENTE DE CONEXIÓN
    def connect_to_server(self, ip):
        """Conectar al servidor - MÉTODO MODIFICADO"""
        
        # 🔧 AGREGAR VALIDACIÓN ANTES DE CONECTAR
        print(f"🌐 Intentando conectar a {ip}...")
        
        # Validar formato IP
        try:
            socket.inet_aton(ip)
        except socket.error:
            self.show_connection_error("IP inválida", f"'{ip}' no es una IP válida.\nEjemplo: 192.168.1.100")
            return False
        
        # Probar conexión primero
        can_connect, error_msg = self.test_connection_before_join(ip)
        
        if not can_connect:
            self.show_connection_error("Error de conexión", error_msg)
            return False
        
        # Si llegamos aquí, la conexión es posible
        # ... tu código existente de conexión ...
        
        try:
            # Tu código actual de socket aquí
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((ip, 8888))
            
            # ... resto de tu código existente ...
            
            return True
            
        except Exception as e:
            self.show_connection_error("Error conectando", f"No se pudo conectar: {str(e)}")
            return False
    
    def show_connection_error(self, title, message):
        """Mostrar error de conexión con consejos - NUEVO MÉTODO"""
        import tkinter.messagebox as msgbox
        
        # Agregar consejos útiles al mensaje
        full_message = f"{message}\n\n💡 Consejos:\n"
        full_message += "• Verifica que ambos estén en la misma WiFi\n"
        full_message += "• El host debe crear sala PRIMERO\n"
        full_message += "• Usa la IP exacta que te dé el host\n"
        full_message += "• Desactiva firewall temporalmente para probar"
        
        msgbox.showerror(title, full_message)
        
    def show_network_options(self):
        """Mostrar opciones de red local"""
        print("🌐 Abriendo opciones de red local...")
        
        if self.network_window:
            self.network_window.destroy()
        
        # Crear ventana
        self.network_window = ctk.CTkToplevel(self.app.root)
        self.network_window.title("🌐 Juego en Red Local")
        self.network_window.geometry("900x700")
        self.network_window.resizable(False, False)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.network_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        ctk.CTkLabel(
            main_frame,
            text="🌐 JUEGO EN RED LOCAL",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=(15, 20))
        
        # Información
        info_text = (
            "🏠 Juega con otros en tu misma red WiFi\n"
            "📱 Ambos deben estar conectados al mismo router\n"
            "🎮 Un jugador crea sala, otro se une"
        )
        
        ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="center"
        ).pack(pady=(0, 20))
        
        # Opción 1: Crear sala
        host_frame = ctk.CTkFrame(main_frame)
        host_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            host_frame,
            text="🏠 CREAR SALA",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            host_frame,
            text="Crea una sala para que otros se conecten",
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 10))
        
        create_btn = ctk.CTkButton(
            host_frame,
            text="🏠 CREAR SALA DE JUEGO",
            command=self.create_game_room,
            width=200,
            height=40,
            fg_color="#4CAF50"
        )
        create_btn.pack(pady=(0, 15))
        
        self.start_game_btn = ctk.CTkButton(
            host_frame,
            text="🚀 INICIAR JUEGO",
            command=self.start_network_game, # Llama a la función que abre los niveles
            width=200,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#FF9800",
            hover_color="#F57C00",
            state="disabled"  # Empieza deshabilitado
        )
        self.start_game_btn.pack(pady=(5, 15))

        # Opción 2: Unirse a sala
        join_frame = ctk.CTkFrame(main_frame)
        join_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            join_frame,
            text="🚪 UNIRSE A SALA",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            join_frame,
            text="Conéctate a la sala de otro jugador",
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 10))
        
        # Campo IP
        ip_frame = ctk.CTkFrame(join_frame, fg_color="transparent")
        ip_frame.pack(pady=5)
        
        ctk.CTkLabel(
            ip_frame,
            text="IP del host:",
            font=ctk.CTkFont(size=12)
        ).pack(side="left", padx=(0, 10))
        
        self.ip_entry = ctk.CTkEntry(
            ip_frame,
            placeholder_text="192.168.1.100",
            width=150
        )
        self.ip_entry.pack(side="left")
        
        join_btn = ctk.CTkButton(
            join_frame,
            text="🚪 UNIRSE A SALA",
            command=self.join_game_room,
            width=200,
            height=40,
            fg_color="#2196F3"
        )
        join_btn.pack(pady=(10, 15))
        
        # Estado de conexión
        self.network_status_label = ctk.CTkLabel(
            main_frame,
            text="💤 Listo para conectar",
            font=ctk.CTkFont(size=12)
        )
        self.network_status_label.pack(pady=15)
        
        # Botones inferiores
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(side="bottom", pady=15)
        
        scan_btn = ctk.CTkButton(
            buttons_frame,
            text="🔍 BUSCAR SALAS",
            command=self.scan_for_rooms,
            width=150,
            height=35,
            fg_color="#FF9800"
        )
        scan_btn.pack(side="left", padx=10)
        
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ CERRAR",
            command=self.close_network_window,
            width=150,
            height=35,
            fg_color="#607D8B"
        )
        close_btn.pack(side="left", padx=10)
        
        print("✅ Opciones de red local abiertas")
    
    def create_game_room(self):
        """Crear sala de juego - VERSIÓN CORREGIDA"""
        if not self.app.player_name:
            messagebox.showwarning("Nombre requerido", "Ingresa tu nombre en el menú principal primero")
            return
    
        try:
            print("🏠 === INICIANDO CREACIÓN DE SALA ===")
        
            # Obtener IP local y puerto
            local_ip = self.get_local_ip()
            port = 8888  # Puerto fijo para simplificar
        
            print(f"📍 IP: {local_ip}, Puerto: {port}")
        
            # Crear servidor
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            
            # IMPORTANTE: Configurar timeout para accept()
            self.server_socket.settimeout(1.0)  # Timeout de 1 segundo para poder cancelar
        
            print("🔌 Socket creado, intentando bind...")
            self.server_socket.bind(('0.0.0.0', port))  # Escuchar en todas las interfaces
        
            print("📡 Bind exitoso, iniciando listen...")
            self.server_socket.listen(5)
        
            # Configurar estado
            self.is_connected = True
            self.is_host = True
            self.is_server = True
            self.client_sockets = []
        
            # Generar código de sala
            import random
            import string
            self.game_room_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        
            print(f"✅ SERVIDOR ACTIVO: {local_ip}:{port} - Código: {self.game_room_code}")
        
            # Actualizar UI
            self.network_status_label.configure(
                text=f"🏠 Sala creada: {local_ip}:{port}\n🎮 Código: {self.game_room_code}\n⏳ Esperando jugador..."
            )
        
            # Iniciar hilo del servidor
            self.server_thread = threading.Thread(target=self.accept_connections, daemon=True)
            self.server_thread.start()
            print("✅ Servidor esperando conexiones")
        
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass
        
            messagebox.showinfo("🏠 Sala Creada", 
                f"Sala creada exitosamente!\n\n"
                f"📍 IP: {local_ip}:{port}\n"
                f"🎮 Código: {self.game_room_code}\n\n"
                f"Dile a tu amigo que se conecte a esta IP")
        
            print("🏠 === SALA CREADA EXITOSAMENTE ===")
        
        except Exception as e:
            error_msg = str(e)
            print(f"❌ ERROR CREANDO SALA: {error_msg}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo crear la sala:\n{error_msg}")
            
    def accept_connections(self):
        """Aceptar conexiones entrantes - MÉTODO CORREGIDO"""
        print("🔍 === SERVIDOR ESPERANDO CONEXIONES ===")
        
        while self.is_server:
            try:
                # Intentar aceptar conexión con timeout
                client_socket, address = self.server_socket.accept()
                print(f"🎉 ¡CONEXIÓN RECIBIDA! Cliente: {address[0]}:{address[1]}")
                
                # Configurar socket del cliente
                client_socket.settimeout(30.0)
                
                # Agregar a lista de clientes
                self.client_sockets.append(client_socket)
                
                # Manejar cliente en hilo separado
                client_thread = threading.Thread(
                    target=self.handle_client_connection,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                
            except socket.timeout:
                # Timeout normal, continuar esperando
                continue
            except Exception as e:
                if self.is_server:
                    print(f"❌ Error aceptando conexión: {e}")
                break
        
        print("🔍 === SERVIDOR DETENIDO ===")

    def handle_server_connection(self):
        """Manejar conexión con el servidor - CON HEARTBEAT"""
        try:
            print("📡 === CLIENTE ESPERANDO MENSAJES ===")
        
        # Esperar mensaje de bienvenida
            welcome_msg = self.receive_message_from_socket(self.client_socket)

            if welcome_msg and welcome_msg.get("type") == "welcome":
                print(f"🎉 Bienvenida recibida del host: {welcome_msg.get('host_name')}")
            
                self.opponent_name = welcome_msg.get("host_name", "Host")
                self.game_room_code = welcome_msg.get("room_code", "UNKNOWN")
            
            # Enviar solicitud de unión
                join_request = {
                    "type": "join_request",
                    "player_name": self.app.player_name
                }
            
                self.send_message_to_socket(self.client_socket, join_request)
                print("📤 Solicitud de unión enviada")
            
                # Esperar confirmación
                confirmation = self.receive_message_from_socket(self.client_socket)
            
                if confirmation and confirmation.get("type") == "connection_confirmed":
                    print("✅ CONEXIÓN CONFIRMADA")
                
                # Actualizar UI
                    if hasattr(self, 'network_window') and self.network_window:
                        self.network_window.after(0, lambda: self.on_connection_established())
                
                # AÑADIR HEARTBEAT AQUÍ PARA EL CLIENTE:
                    if not hasattr(self, 'heartbeat_started'):
                        self.heartbeat_started = True
                        self.start_heartbeat()
                
                # IMPORTANTE: Ahora el cliente entra en modo escucha
                    print("🎧 Cliente entrando en modo escucha de mensajes del servidor...")
                    self.listen_to_server_messages()
                
                else:
                    raise Exception("Confirmación inválida del servidor")
            else:
                raise Exception("No se recibió mensaje de bienvenida")
            
        except Exception as e:
            print(f"❌ Error en conexión cliente: {e}")
            if hasattr(self, 'network_window') and self.network_window:
                self.network_window.after(0, lambda: messagebox.showerror(
                    "Error", f"Conexión perdida: {e}"
                ))
            self.cleanup_connection()


    def listen_to_server_messages(self):
        """Cliente escucha mensajes del servidor continuamente"""
        while self.is_connected:
            try:
                message = self.receive_message_from_socket(self.client_socket)
                if message:
                    print(f"📨 [CLIENTE] Mensaje recibido: {message.get('type')}")
                # Procesar en el hilo principal de UI
                    if hasattr(self, 'app') and hasattr(self.app, 'root'):
                        self.app.root.after(0, lambda m=message: self.handle_server_message(m))
                else:
                # Servidor desconectado
                    print("💔 Servidor cerró la conexión")
                    break
            except socket.timeout:
                continue
            except Exception as e:
                print(f"❌ Error recibiendo mensaje del servidor: {e}")
                break
    
        print("🔌 Cliente: bucle de mensajes terminado")

    
    

    def handle_game_messages(self, socket_connection):
        """Manejar mensajes durante el juego"""
        while self.is_connected:
            try:
                message = self.receive_message_from_socket(socket_connection)
                if message:
                    self.process_game_message(message, socket_connection)
                else:
                    # Conexión cerrada
                    break
            except socket.timeout:
                continue
            except Exception as e:
                print(f"❌ Error recibiendo mensaje: {e}")
                break
        
        print("🔌 Bucle de mensajes terminado")

    def process_game_message(self, message, socket_connection):
        """Procesar mensajes del juego"""
        msg_type = message.get("type")
        print(f"📨 Mensaje recibido: {msg_type}")
        
        if msg_type == "game_level":
            # Nivel recibido
            if hasattr(self, 'network_window') and self.network_window:
                self.network_window.after(0, lambda: self.handle_game_level(message))
        elif msg_type == "game_move":
            # Movimiento del oponente
            pass
        elif msg_type == "chat":
            # Mensaje de chat
            pass

    def receive_message_from_socket(self, socket_conn):
        """Recibir mensaje de un socket específico - VERSIÓN MEJORADA CON HEARTBEAT"""
        try:
            buffer = ""
            socket_conn.settimeout(10.0)  # Timeout más largo para heartbeats
            
            while True:
                # Recibir datos
                data = socket_conn.recv(1024).decode('utf-8')
                if not data:
                    return None
                
                buffer += data
                
                # Buscar mensajes completos (terminados en \n)
                while '\n' in buffer:
                    line, buffer = buffer.split('\n', 1)
                    if line:
                        try:
                            message = json.loads(line)
                            
                            # Filtrar heartbeats silenciosamente
                            if message.get("type") == "heartbeat":
                                continue  # Ignorar y continuar recibiendo
                            
                            return message
                        except json.JSONDecodeError as e:
                            print(f"⚠️ Error decodificando JSON: {e}")
                            print(f"   Línea problemática: {line}")
                            continue
                        
        except socket.timeout:
            return None
        except ConnectionResetError:
            print("⚠️ Conexión reiniciada por el otro extremo")
            return None
        except ConnectionAbortedError:
            print("⚠️ Conexión abortada")
            return None
        except Exception as e:
            print(f"❌ Error recibiendo mensaje: {e}")
            return None
        
    def on_connection_established(self):
        """Cuando la conexión se establece exitosamente"""
        self.network_status_label.configure(
            text=f"✅ Conectado a {self.opponent_name}\n🎮 Sala: {self.game_room_code}"
        )
        
        try:
            self.app.sound_manager.play_sound('correct')
        except:
            pass
        
        messagebox.showinfo("✅ Conectado", 
            f"¡Conectado exitosamente!\n\n"
            f"🎮 Oponente: {self.opponent_name}\n"
            f"🏠 Sala: {self.game_room_code}")

    def send_message_to_socket(self, socket_conn, message):
        """Enviar mensaje a un socket específico - VERSIÓN MEJORADA"""
        try:
            if not socket_conn:
                print("⚠️ Socket no válido para enviar mensaje")
                return False
                
            # Verificar que el socket sigue abierto
            try:
                # Intentar obtener información del socket
                socket_conn.getpeername()
            except:
                print("⚠️ Socket cerrado o desconectado")
                return False
            
            message_json = json.dumps(message) + '\n'
            socket_conn.sendall(message_json.encode('utf-8'))
            return True
            
        except BrokenPipeError:
            print("⚠️ Pipe roto - el cliente se desconectó")
            return False
        except ConnectionResetError:
            print("⚠️ Conexión reiniciada por el cliente")
            return False
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")
            return False


   # En network_game_manager.py

    # En network_game_manager.py

    def handle_client_connection(self, client_socket, address):
        """Manejar conexión de cliente individual - CON HEARTBEAT"""
        try:
            print(f"✅ [HOST-THREAD] Hilo iniciado para el cliente {address}")
        
        # Handshake inicial
            time.sleep(0.5)
            welcome_msg = { 
                "type": "welcome", 
                "host_name": self.app.player_name, 
                "room_code": self.game_room_code 
            }
            self.send_message_to_socket(client_socket, welcome_msg)
        
            response = self.receive_message_from_socket(client_socket)
        
            if response and response.get("type") == "join_request":
                self.opponent_name = response.get("player_name", "Jugador")
                print(f"✅ [HOST-THREAD] {self.opponent_name} se ha unido.")
                confirm_msg = { 
                    "type": "connection_confirmed", 
                    "opponent_name": self.app.player_name 
                }
                self.send_message_to_socket(client_socket, confirm_msg)
            
                if hasattr(self, 'network_window') and self.network_window:
                    self.network_window.after(0, self.on_player_joined)
            
            # AÑADIR HEARTBEAT AQUÍ:
                if not hasattr(self, 'heartbeat_started'):
                    self.heartbeat_started = True
                    self.start_heartbeat()
            
                print(f"🎧 [HOST-THREAD] Handshake completo. Entrando en bucle de escucha para {self.opponent_name}...")
                self.listen_to_client_messages(client_socket)
            
            else:
                print(f"❌ [HOST-THREAD] Handshake fallido con {address}. Respuesta: {response}")

        except Exception as e:
            print(f"💥 [HOST-THREAD] ERROR INESPERADO en handle_client_connection: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print(f"🧹 [HOST-THREAD] El hilo para {address} está terminando. Limpiando cliente...")
            self.cleanup_client(client_socket)

    

    # En network_game_manager.py

    def listen_to_client_messages(self, client_socket):
        """Escuchar mensajes del cliente continuamente - VERSIÓN CON MÁS DIAGNÓSTICO"""
        while self.is_connected and client_socket in self.client_sockets:
            try:
                print("..... [HOST-LOOP] Esperando mensaje del cliente...")
                message = self.receive_message_from_socket(client_socket)
            
                if message:
                    print(f"👍 [HOST-LOOP] Mensaje recibido: {message.get('type')}")
                    self.handle_client_message(message, client_socket)
                else:
                    print("👋 [HOST-LOOP] El cliente cerró la conexión (receive_message_from_socket devolvió None). Saliendo del bucle.")
                    break
                
            except socket.timeout:
                print("..... [HOST-LOOP] Timeout de socket. No hay mensajes. Volviendo a escuchar.")
                continue # Esto es normal, simplemente significa que no hubo mensajes.
            
            except Exception as e:
                print(f"💥 [HOST-LOOP] Error en el bucle de escucha: {e}. Saliendo del bucle.")
                break
            
        print("🛑 [HOST-THREAD] Saliendo de la función listen_to_client_messages.")


    def wait_for_player(self):
        """Esperar a que se conecte un jugador - VERSIÓN ULTRA SIMPLIFICADA"""
        try:
            print("⏳ Esperando jugador...")
        
        # Aceptar conexión
            client_socket, address = self.server_socket.accept()
            print(f"🎮 ¡JUGADOR CONECTADO! IP: {address[0]}:{address[1]}")
        
        # Configurar socket para evitar timeouts
            client_socket.settimeout(30)
        
        # Agregar a lista de clientes
            if not hasattr(self, 'client_sockets'):
                self.client_sockets = []
            self.client_sockets.append(client_socket)
        
            print("📝 Cliente agregado a la lista")
        
        # PAUSA CRÍTICA - Dejar que la conexión se estabilice
            print("⏱️ Estabilizando conexión...")
            time.sleep(2)
        
        # Preparar mensaje de bienvenida MUY SIMPLE
            welcome_msg = {
                "type": "welcome",
                "host_name": self.app.player_name,
                "room_code": self.game_room_code
            }
        
            print(f"📤 Preparando mensaje: {welcome_msg}")
        
        # ENVÍO SIMPLIFICADO - Sin protocolo de longitud
            try:
                message_json = json.dumps(welcome_msg)
                message_bytes = message_json.encode('utf-8')
            
                print(f"📤 Enviando {len(message_bytes)} bytes...")
            
            # Enviar todo de una vez
                client_socket.sendall(message_bytes)
                client_socket.sendall(b'\n')  # Terminador
            
                print("✅ Mensaje de bienvenida enviado exitosamente")
            
            except Exception as send_error:
                print(f"❌ ERROR ENVIANDO BIENVENIDA: {send_error}")
                self.cleanup_client(client_socket)
                return
        
        # Esperar respuesta del cliente
            print("⏳ Esperando respuesta del cliente...")
        
            try:
            # Recibir respuesta simple
                response_data = b''
                while b'\n' not in response_data:
                    chunk = client_socket.recv(1024)
                    if not chunk:
                        print("❌ Cliente cerró conexión")
                        self.cleanup_client(client_socket)
                        return
                    response_data += chunk
                    print(f"📨 Recibidos {len(chunk)} bytes...")
            
            # Procesar respuesta
                response_json = response_data.decode('utf-8').strip()
                response = json.loads(response_json)
            
                print(f"✅ Respuesta recibida: {response}")
            
            except Exception as receive_error:
                print(f"❌ ERROR RECIBIENDO RESPUESTA: {receive_error}")
                self.cleanup_client(client_socket)
                return
        
        # Verificar respuesta
            if response.get("type") == "join_request":
                self.opponent_name = response.get("player_name", "Jugador Desconocido")
                print(f"🎉 ¡{self.opponent_name} se quiere unir!")
            
            # Enviar confirmación
                confirm_msg = {
                    "type": "connection_confirmed",
                    "opponent_name": self.app.player_name,
                    "status": "ready"
                }
            
                try:
                    confirm_json = json.dumps(confirm_msg)
                    client_socket.sendall(confirm_json.encode('utf-8'))
                    client_socket.sendall(b'\n')
                    print("✅ Confirmación enviada")
                
                # Actualizar UI
                    self.network_window.after(0, self.on_player_joined)
                
                # Iniciar juego después de un momento
                    self.network_window.after(3000, self.start_network_game)
                
                except Exception as confirm_error:
                    print(f"❌ ERROR ENVIANDO CONFIRMACIÓN: {confirm_error}")
                    self.cleanup_client(client_socket)
                    return
            else:
                print(f"❌ Respuesta inesperada: {response}")
                self.cleanup_client(client_socket)
    
        except Exception as e:
            print(f"❌ ERROR GENERAL en wait_for_player: {e}")
            import traceback
            traceback.print_exc()

    
    def wait_for_player_debug(self):
        """Esperar jugador con DEBUG EXTREMO"""
        try:
            print("🔍 === WAIT_FOR_PLAYER DEBUG INICIADO ===")
            print(f"🔌 Socket servidor: {self.server_socket}")
            print(f"📍 Estado is_host: {self.is_host}")
            print(f"📍 Estado is_server: {self.is_server}")
        
            print("⏳ Llamando server_socket.accept()...")
        
        # ACCEPT CON TIMEOUT PARA DEBUG
            self.server_socket.settimeout(60)  # 60 segundos timeout
        
            try:
                client_socket, address = self.server_socket.accept()
                print(f"🎉 ¡¡¡CONEXIÓN ACEPTADA!!! Cliente: {address[0]}:{address[1]}")
            except socket.timeout:
                print("⏰ TIMEOUT en accept() - No llegó ningún cliente en 60 segundos")
                return
            except Exception as accept_error:
                print(f"❌ ERROR EN ACCEPT: {accept_error}")
                return
        
        # Configurar cliente
            print("⚙️ Configurando socket del cliente...")
            client_socket.settimeout(30)
        
        # Agregar a lista
            if not hasattr(self, 'client_sockets'):
                self.client_sockets = []
            self.client_sockets.append(client_socket)
            print(f"📝 Cliente agregado. Total clientes: {len(self.client_sockets)}")
        
        # PAUSA CRÍTICA
            print("⏱️ Pausa de estabilización (3 segundos)...")
            time.sleep(3)
        
        # Preparar mensaje de bienvenida
            welcome_msg = {
                "type": "welcome",
                 "host_name": self.app.player_name,
                "room_code": self.game_room_code,
                "timestamp": time.time()
            }
        
            print(f"📋 Mensaje preparado: {welcome_msg}")
        
        # INTENTAR ENVÍO MÚLTIPLES VECES
            for attempt in range(3):
                try:
                    print(f"📤 Intento {attempt + 1} de envío...")
                
                # Método 1: JSON simple
                    message_json = json.dumps(welcome_msg)
                    message_bytes = message_json.encode('utf-8')
                
                    print(f"📏 Tamaño mensaje: {len(message_bytes)} bytes")
                    print(f"📄 Contenido: {message_json}")
                
                # Enviar con terminador
                    client_socket.sendall(message_bytes)
                    client_socket.sendall(b'\n')
                
                    print(f"✅ ENVÍO {attempt + 1} COMPLETADO")
                    break
                
                except Exception as send_error:
                    print(f"❌ ERROR EN ENVÍO {attempt + 1}: {send_error}")
                    if attempt == 2:  # Último intento
                        print("💥 TODOS LOS INTENTOS DE ENVÍO FALLARON")
                        self.cleanup_client(client_socket)
                        return
                    time.sleep(1)
        
        # Esperar respuesta del cliente
            print("⏳ Esperando respuesta del cliente...")
        
            try:
                response_data = b''
                max_wait = 30  # 30 segundos
                start_time = time.time()
            
                while b'\n' not in response_data:
                    if time.time() - start_time > max_wait:
                        print(f"⏰ TIMEOUT esperando respuesta ({max_wait}s)")
                        self.cleanup_client(client_socket)
                        return
                
                    try:
                        chunk = client_socket.recv(1024)
                        if not chunk:
                            print("💔 Cliente cerró conexión durante respuesta")
                            self.cleanup_client(client_socket)
                            return
                    
                        response_data += chunk
                        print(f"📨 Chunk recibido: {len(chunk)} bytes. Total: {len(response_data)}")
                    
                    except socket.timeout:
                        print("⏱️ Timeout parcial en recv, continuando...")
                        continue
            
            # Procesar respuesta
                response_json = response_data.decode('utf-8').strip()
                print(f"📋 Respuesta JSON: {response_json}")
            
                response = json.loads(response_json)
                print(f"✅ Respuesta parseada: {response}")
            
            except Exception as receive_error:
                print(f"❌ ERROR RECIBIENDO RESPUESTA: {receive_error}")
                import traceback
                traceback.print_exc()
                self.cleanup_client(client_socket)
                return
        
        # Verificar tipo de respuesta
            if response.get("type") == "join_request":
                self.opponent_name = response.get("player_name", "Jugador Desconocido")
                print(f"🎉 ¡{self.opponent_name} quiere unirse!")
            
                # Enviar confirmación
                confirm_msg = {
                    "type": "connection_confirmed",
                    "opponent_name": self.app.player_name,
                    "status": "ready",
                    "timestamp": time.time()
                }
            
                try:
                    confirm_json = json.dumps(confirm_msg)
                    client_socket.sendall(confirm_json.encode('utf-8'))
                    client_socket.sendall(b'\n')
                    print("✅ Confirmación enviada")
                
                # Actualizar UI en hilo principal
                    if hasattr(self, 'network_window') and self.network_window:
                        self.network_window.after(0, self.on_player_joined)
                
                    print("🎮 ¡CONEXIÓN ESTABLECIDA EXITOSAMENTE!")
                
                # Iniciar juego después de un momento
                    if hasattr(self, 'network_window') and self.network_window:
                        self.network_window.after(3000, self.start_network_game)
                
                except Exception as confirm_error:
                    print(f"❌ ERROR ENVIANDO CONFIRMACIÓN: {confirm_error}")
                    self.cleanup_client(client_socket)
                    return
            else:
                print(f"❌ Respuesta inesperada: {response}")
                self.cleanup_client(client_socket)
                return
        
            print("🏆 === WAIT_FOR_PLAYER COMPLETADO EXITOSAMENTE ===")
    
        except Exception as e:
            print(f"💥 ERROR CRÍTICO EN WAIT_FOR_PLAYER: {e}")
            import traceback
            traceback.print_exc()
        
        # Actualizar UI con error
            if hasattr(self, 'network_window') and self.network_window:
                self.network_window.after(0, lambda: self.network_status_label.configure(
                    text="❌ Error esperando jugador"
                ))
                traceback.print_exc()

    def join_game_room_debug(self):
        """Unirse a sala - VERSIÓN CON DEBUG EXTREMO"""
        if not self.app.player_name:
            messagebox.showwarning("Nombre requerido", "Ingresa tu nombre en el menú principal primero")
            return
    
        host_ip = self.ip_entry.get().strip()
        if not host_ip:
            messagebox.showwarning("IP requerida", "Ingresa la IP del host")
            return
    
        try:
            print("🚪 === INICIANDO CONEXIÓN COMO CLIENTE ===")
            print(f"🎯 IP objetivo: {host_ip}")
            print(f"👤 Mi nombre: {self.app.player_name}")
        
            self.network_status_label.configure(text=f"🔌 Conectando a {host_ip}...")
        
        # Buscar puerto del host
            print("🔍 Buscando puerto del servidor...")
            port = self.find_host_port(host_ip)
            if not port:
                error_msg = f"No se encontró servidor en {host_ip}\n\n¿El host ya creó la sala?"
                print(f"❌ {error_msg}")
                messagebox.showerror("Host no encontrado", error_msg)
                return
        
            print(f"✅ Puerto encontrado: {port}")
        
            # Crear socket cliente
            print("🔌 Creando socket cliente...")
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(30)
        
        # Conectar
            print(f"🚀 Conectando a {host_ip}:{port}...")
            self.client_socket.connect((host_ip, port))
            print(f"✅ CONECTADO EXITOSAMENTE a {host_ip}:{port}")
        
            self.is_connected = True
            self.is_host = False
            self.is_server = False
        
            # PAUSA CRÍTICA MÁS LARGA
            print("⏱️ Pausa de estabilización cliente (5 segundos)...")
            time.sleep(5)
        
        # Recibir mensaje de bienvenida
            print("⏳ Iniciando recepción de mensaje de bienvenida...")
        
            welcome_data = b''
            max_wait = 30
            start_time = time.time()
            received_chunks = 0
        
            print(f"🕐 Tiempo límite: {max_wait} segundos")
        
            while b'\n' not in welcome_data:
                elapsed = time.time() - start_time
                remaining = max_wait - elapsed
            
                if elapsed > max_wait:
                    error_msg = f"Timeout esperando mensaje de bienvenida ({max_wait}s)"
                    print(f"⏰ {error_msg}")
                    print(f"📊 Datos recibidos hasta ahora: {len(welcome_data)} bytes")
                    if welcome_data:
                        print(f"📄 Contenido parcial: {welcome_data}")
                    raise Exception(error_msg)
            
                try:
                    print(f"📡 Intentando recv... (quedan {remaining:.1f}s)")
                    chunk = self.client_socket.recv(1024)
                
                    if not chunk:
                        error_msg = "Servidor cerró conexión sin enviar datos"
                        print(f"💔 {error_msg}")
                        raise Exception(error_msg)
                
                    welcome_data += chunk
                    received_chunks += 1
                    print(f"📨 Chunk #{received_chunks}: {len(chunk)} bytes. Total: {len(welcome_data)}")
                
                # Mostrar contenido si es texto
                    try:
                        partial_text = chunk.decode('utf-8', errors='ignore')
                        print(f"📄 Contenido chunk: {repr(partial_text)}")
                    except:
                        print(f"📄 Contenido chunk: {chunk}")
                
                except socket.timeout:
                    print(f"⏱️ Timeout parcial en recv (chunk #{received_chunks + 1})")
                    continue
                except Exception as recv_error:
                    print(f"❌ Error en recv: {recv_error}")
                    raise Exception(f"Error recibiendo datos: {recv_error}")
        
            # Procesar mensaje completo
            print(f"✅ Mensaje completo recibido: {len(welcome_data)} bytes")
        
            try:
                welcome_json = welcome_data.decode('utf-8').strip()
                print(f"📋 JSON recibido: {welcome_json}")
            
                welcome_msg = json.loads(welcome_json)
                print(f"✅ Mensaje parseado: {welcome_msg}")
            
            except Exception as parse_error:
                print(f"❌ Error parseando mensaje: {parse_error}")
                print(f"📄 Datos raw: {welcome_data}")
                raise Exception(f"Mensaje inválido del servidor: {parse_error}")
        
            if welcome_msg.get("type") != "welcome":
                error_msg = f"Tipo de mensaje inválido: {welcome_msg.get('type')}"
                print(f"❌ {error_msg}")
                raise Exception(error_msg)
        
            self.opponent_name = welcome_msg.get("host_name", "Host Desconocido")
            self.game_room_code = welcome_msg.get("room_code", "UNKNOWN")
        
            print(f"🎮 Host: {self.opponent_name}, Sala: {self.game_room_code}")
        
        # Enviar solicitud de unión
            join_request = {
                "type": "join_request",
                "player_name": self.app.player_name,
                "timestamp": time.time()
            }
        
            print(f"📤 Enviando solicitud: {join_request}")
        
            try:
                request_json = json.dumps(join_request)
                self.client_socket.sendall(request_json.encode('utf-8'))
                self.client_socket.sendall(b'\n')
                print("✅ Solicitud enviada")
            
            except Exception as request_error:
                print(f"❌ Error enviando solicitud: {request_error}")
                raise Exception(f"No se pudo enviar solicitud: {request_error}")
        
        #    Esperar confirmación
            print("⏳ Esperando confirmación...")
        
            confirm_data = b''
            start_time = time.time()
        
            while b'\n' not in confirm_data:
                if time.time() - start_time > 15:
                    raise Exception("Timeout esperando confirmación")
            
                chunk = self.client_socket.recv(1024)
                if not chunk:
                    raise Exception("Servidor cerró conexión durante confirmación")
            
                confirm_data += chunk
                print(f"📨 Confirmación chunk: {len(chunk)} bytes...")
        
            confirm_json = confirm_data.decode('utf-8').strip()
            confirmation = json.loads(confirm_json)
        
            print(f"✅ CONFIRMACIÓN RECIBIDA: {confirmation}")
        
            if confirmation.get("type") != "connection_confirmed":
                raise Exception(f"Confirmación inválida: {confirmation}")
        
            # ¡ÉXITO TOTAL!
            print("🏆 === CONEXIÓN COMPLETADA EXITOSAMENTE ===")
        
            # Actualizar UI
            self.network_status_label.configure(
                text=f"✅ Conectado a {self.opponent_name}\n🎮 Sala: {self.game_room_code}"
            )
        
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass
        
            messagebox.showinfo("✅ Conectado", 
                f"¡Conectado exitosamente!\n\n"
                f"🎮 Oponente: {self.opponent_name}\n"
                f"🏠 Sala: {self.game_room_code}")
        
        except Exception as e:
            error_msg = str(e)
            print(f"💥 ERROR CRÍTICO CONECTANDO: {error_msg}")
            import traceback
            traceback.print_exc()
        
            # Limpiar conexión fallida
            if hasattr(self, 'client_socket') and self.client_socket:
                try:
                    self.client_socket.close()
                except:
                    pass
                self.client_socket = None
        
            self.is_connected = False
            self.network_status_label.configure(text="❌ Error de conexión")
        
            messagebox.showerror("Error de conexión", f"No se pudo conectar:\n{error_msg}")
    
    def join_game_room(self):
        """Unirse a sala - VERSIÓN CORREGIDA"""
        if not self.app.player_name:
            messagebox.showwarning("Nombre requerido", "Ingresa tu nombre en el menú principal primero")
            return
    
        host_ip = self.ip_entry.get().strip()
        if not host_ip:
            messagebox.showwarning("IP requerida", "Ingresa la IP del host")
            return
    
        try:
            print("🚪 === INICIANDO CONEXIÓN COMO CLIENTE ===")
            print(f"🎯 IP objetivo: {host_ip}")
            
            self.network_status_label.configure(text=f"🔌 Conectando a {host_ip}...")
            
            # Crear socket cliente
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.settimeout(10.0)  # Timeout más corto
            
            # Conectar
            port = 8888
            print(f"🚀 Conectando a {host_ip}:{port}...")
            self.client_socket.connect((host_ip, port))
            print("✅ CONECTADO AL SERVIDOR")
            
            self.is_connected = True
            self.is_host = False
            self.is_server = False
            
            # Iniciar hilo para manejar mensajes
            self.client_thread = threading.Thread(
                target=self.handle_server_connection,
                daemon=True
            )
            self.client_thread.start()
            
            # Actualizar UI temporalmente
            self.network_status_label.configure(text="⏳ Esperando respuesta del servidor...")
            
        except socket.timeout:
            error_msg = "Tiempo de espera agotado. Verifica que el host haya creado la sala."
            print(f"⏰ {error_msg}")
            messagebox.showerror("Timeout", error_msg)
            self.cleanup_connection()
        except Exception as e:
            error_msg = str(e)
            print(f"💥 ERROR CONECTANDO: {error_msg}")
            messagebox.showerror("Error de conexión", f"No se pudo conectar:\n{error_msg}")
            self.cleanup_connection()

            


    
    def find_host_port(self, host_ip):
        """Encontrar puerto del host - MEJORADO"""
        common_ports = [8080, 8081, 8082, 8083, 8084, 8085]
    
        print(f"🔍 Buscando servidor en {host_ip}...")
    
        for port in common_ports:
            try:
                test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                test_socket.settimeout(2)
                result = test_socket.connect_ex((host_ip, port))
                test_socket.close()
            
                if result == 0:
                    print(f"✅ Servidor encontrado en puerto {port}")
                    return port
                else:
                    print(f"❌ Puerto {port}: {result}")
            except Exception as e:
                print(f"❌ Error probando puerto {port}: {e}")
    
        print(f"❌ No se encontró servidor en {host_ip}")
        return None

    
    def on_player_joined(self):
        """Cuando un jugador se une a la sala"""
        self.network_status_label.configure(
            text=f"✅ {self.opponent_name} se unió a la sala\n🎮 ¡Listo para jugar!"
        )
        
        try:
            self.app.sound_manager.play_sound('correct')
        except:
            pass
        
        messagebox.showinfo("🎮 Jugador Conectado", 
            f"¡{self.opponent_name} se unió a la sala!\n\n"
            f"🏠 Sala: {self.game_room_code}\n"
            f"✅ ¡Listos para jugar!")
        if hasattr(self, 'start_game_btn'):
            self.start_game_btn.configure(state="normal") # Habilita el botón

        # --- CÓDIGO DE DEPURACIÓN AQUÍ ---
        if hasattr(self, 'start_game_btn'):
            print("🟢 [DEBUG] Botón 'start_game_btn' encontrado. Habilitando...")
            self.start_game_btn.configure(state="normal")
        else:
            print("🔴 [DEBUG] ERROR: Atributo 'start_game_btn' NO fue encontrado.")
            print("🔴 [DEBUG] Esto significa que la ventana de red o el botón no existen en esta instancia.")


    
    def start_network_game(self):
        """Iniciar juego en red - PUNTO DE ENTRADA PRINCIPAL"""
        self.load_available_levels()
        try:
            if self.is_host:  # ← CAMBIAR de is_server a is_host
                print("🎯 Host: Seleccionando nivel para jugar...")
                self.show_level_selection()
            else:
                print("⏳ Cliente: Solicitando inicio de juego al host...")
                self.request_game_start()
        except Exception as e:
            print(f"❌ Error iniciando juego en red: {e}")
            self.show_error("Error", f"No se pudo iniciar el juego:\n{str(e)}")



    def request_game_start(self):
        """Cliente solicita inicio de juego"""
        if not self.is_server and hasattr(self, 'client_socket') and self.client_socket:
            try:
                message = {
                    "type": "request_game_start",
                    "player_name": getattr(self, 'player_name', 'Jugador')
                }
                self.client_socket.send(json.dumps(message).encode())
                print("📤 Solicitando al host que seleccione un nivel...")
            
            # Mostrar mensaje al cliente
                self.show_info("Esperando host", "Esperando que el host seleccione un nivel...\n\nPor favor espera un momento.")
            
            except Exception as e:
                print(f"❌ Error solicitando inicio: {e}")
                self.show_error("Error", "No se pudo solicitar inicio de juego")


    def show_error(self, title, message):
        """Mostrar mensaje de error"""
        try:
            msgbox.showerror(title, message)
        except Exception as e:
            print(f"❌ Error mostrando mensaje: {e}")



    def show_info(self, title, message):
        """Mostrar mensaje informativo"""
        try:
            msgbox.showinfo(title, message)
        except Exception as e:
            print(f"ℹ️ Info: {message}")

    def is_connected(self):
        """Verificar si hay conexión activa"""
        if self.is_server:
            return hasattr(self, 'client_sockets') and len(self.client_sockets) > 0
        else:
            return hasattr(self, 'client_socket') and self.client_socket is not None



    def scan_for_rooms(self):
        """Buscar salas disponibles en la red"""
        self.network_status_label.configure(text="🔍 Buscando salas en la red...")
        
        def do_scan():
            try:
                # Obtener red local
                local_network = self.get_local_network()
                found_rooms = []
                
                # Escanear IPs comunes
                for i in range(100, 200):  # Rango común de IPs
                    ip = f"{local_network}.{i}"
                    
                    try:
                        # Intentar conectar
                        test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        test_socket.settimeout(0.5)
                        result = test_socket.connect_ex((ip, 8080))
                        
                        if result == 0:
                            # Puerto abierto, puede ser una sala
                            found_rooms.append(ip)
                            print(f"🔍 Sala posible encontrada: {ip}")
                        
                        test_socket.close()
                        
                    except:
                        pass
                
                # Actualizar UI
                self.network_window.after(0, lambda: self.show_scan_results(found_rooms))
                
            except Exception as e:
                self.network_window.after(0, lambda: self.network_status_label.configure(
                    text=f"❌ Error escaneando: {e}"
                ))
        
        # Ejecutar escaneo en hilo separado
        threading.Thread(target=do_scan, daemon=True).start()
    
    def show_scan_results(self, found_rooms):
        """Mostrar resultados del escaneo"""
        if found_rooms:
            rooms_text = "\n".join([f"🏠 {ip}" for ip in found_rooms])
            self.network_status_label.configure(
                text=f"✅ {len(found_rooms)} salas encontradas:\n{rooms_text}"
            )
            
            # Auto-llenar la primera IP encontrada
            if self.ip_entry:
                self.ip_entry.delete(0, 'end')
                self.ip_entry.insert(0, found_rooms[0])
        else:
            self.network_status_label.configure(text="📭 No se encontraron salas activas")
    
    def send_message(self, message):
        """Enviar mensaje por red - VERSIÓN CORREGIDA"""
        try:
            # Determinar qué socket usar
            target_socket = None
        
            if self.is_host and hasattr(self, 'client_sockets') and self.client_sockets:
                # Host enviando a cliente
                target_socket = self.client_sockets[0]  # Primer cliente conectado
            elif not self.is_host and hasattr(self, 'client_socket') and self.client_socket:
                # Cliente enviando a host
                target_socket = self.client_socket
        
            if not target_socket:
                print("❌ No hay socket disponible para enviar mensaje")
                return False
        
        # Preparar mensaje
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')
        
        # Enviar con longitud primero (protocolo más estable)
            message_length = len(message_bytes)
            length_header = message_length.to_bytes(4, byteorder='big')
        
        # Enviar header de longitud + mensaje
            target_socket.sendall(length_header)
            target_socket.sendall(message_bytes)
        
            print(f"✅ Mensaje enviado: {message.get('type', 'unknown')} ({message_length} bytes)")
            return True
        
        except Exception as e:
            print(f"❌ Error enviando mensaje: {e}")
            return False
    
    def receive_message(self):
        """Recibir mensaje por red - VERSIÓN CORREGIDA"""
        try:
            # Determinar qué socket usar
            source_socket = None

            if self.is_host and hasattr(self, 'client_sockets') and self.client_sockets:
                # Host recibiendo de cliente
                source_socket = self.client_sockets[0]
            elif not self.is_host and hasattr(self, 'client_socket') and self.client_socket:
            # Cliente recibiendo de host
                source_socket = self.client_socket
        
            if not source_socket:
                print("❌ No hay socket disponible para recibir mensaje")
                return None
        
        # Recibir header de longitud (4 bytes)
            length_header = b''
            while len(length_header) < 4:
                chunk = source_socket.recv(4 - len(length_header))
                if not chunk:
                    print("❌ Conexión cerrada por el otro extremo")
                    return None
                length_header += chunk
        
        # Decodificar longitud
            message_length = int.from_bytes(length_header, byteorder='big')
        
            if message_length > 10000:  # Límite de seguridad
                print(f"❌ Mensaje demasiado largo: {message_length} bytes")
                return None
        
        # Recibir mensaje completo
            message_bytes = b''
            while len(message_bytes) < message_length:
                chunk = source_socket.recv(message_length - len(message_bytes))
                if not chunk:
                    print("❌ Conexión interrumpida durante recepción")
                    return None
                message_bytes += chunk
        
        # Decodificar JSON
            message_json = message_bytes.decode('utf-8')
            message = json.loads(message_json)
        
            print(f"✅ Mensaje recibido: {message.get('type', 'unknown')} ({message_length} bytes)")
            return message
        
        except json.JSONDecodeError as e:
            print(f"❌ Error decodificando JSON: {e}")
            return None
        except Exception as e:
            print(f"❌ Error recibiendo mensaje: {e}")
            return None
        

    def send_message_to_client(self, message, client_socket):
        """Enviar mensaje a cliente específico"""
        try:
            message_json = json.dumps(message)
            message_bytes = message_json.encode('utf-8')
        
        # Enviar longitud primero
            length_header = len(message_bytes).to_bytes(4, byteorder='big')
            client_socket.sendall(length_header)
            client_socket.sendall(message_bytes)
        
            return True
        except Exception as e:
            print(f"❌ Error enviando a cliente: {e}")
            return False
        


    def receive_message_from_client(self, client_socket):
        """Recibir mensaje de cliente específico"""
        try:
            client_socket.settimeout(10)  # 10 segundos timeout
        
        # Recibir longitud
            length_header = b''
            while len(length_header) < 4:
                chunk = client_socket.recv(4 - len(length_header))
                if not chunk:
                    return None
                length_header += chunk
        
            message_length = int.from_bytes(length_header, byteorder='big')
        
        # Recibir mensaje
            message_bytes = b''
            while len(message_bytes) < message_length:
                chunk = client_socket.recv(message_length - len(message_bytes))
                if not chunk:
                    return None
                message_bytes += chunk
        
            message = json.loads(message_bytes.decode('utf-8'))
            return message
        
        except Exception as e:
            print(f"❌ Error recibiendo de cliente: {e}")
            return None
        
    def cleanup_connection(self):
        """Limpiar conexión fallida"""
        self.is_connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except:
                pass
            self.client_socket = None
        
        if hasattr(self, 'network_status_label'):
            self.network_status_label.configure(text="❌ Desconectado")

    def cleanup_client(self, client_socket):
        """Limpiar cliente desconectado - VERSIÓN MEJORADA"""
        try:
            # Remover de la lista de clientes
            if hasattr(self, 'client_sockets') and client_socket in self.client_sockets:
                self.client_sockets.remove(client_socket)
                print(f"🔌 Cliente removido de la lista. Quedan {len(self.client_sockets)} clientes")
        
        # Cerrar socket
            try:
                client_socket.close()
            except:
                pass
        
        # Notificar al juego si hay una instancia activa
            if hasattr(self, 'game_instance') and self.game_instance:
            # Notificar desconexión del oponente
                self.app.root.after(0, lambda: self.notify_opponent_disconnected())
            
        except Exception as e:
            print(f"⚠️ Error limpiando cliente: {e}")


    def get_local_ip(self):
        """Obtener la IP local real"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            local_ip = s.getsockname()[0]
            s.close()
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def get_local_network(self):
        """Obtener red local base"""
        local_ip = self.get_local_ip()
        parts = local_ip.split('.')
        return '.'.join(parts[:3])
    
    def find_free_port(self, start_port=8080):
        """Encontrar puerto libre"""
        for port in range(start_port, start_port + 100):
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind(('', port))
                    return port
            except OSError:
                continue
        return None
    

    def notify_opponent_disconnected(self):
        """Notificar que el oponente se desconectó"""
        if hasattr(self.app, 'current_screen') and self.app.current_screen:
        # Buscar si hay una instancia del juego activa
            if hasattr(self.app, 'custom_game_state'):
            # Añadir notificación si existe el método
                try:
                # Buscar el label de notificaciones en la pantalla actual
                    for widget in self.app.current_screen.winfo_children():
                        if isinstance(widget, ctk.CTkFrame):
                            for subwidget in widget.winfo_children():
                                if hasattr(subwidget, 'cget') and isinstance(subwidget, ctk.CTkTextbox):
                                # Encontramos el textbox de notificaciones
                                    subwidget.configure(state="normal")
                                    timestamp = datetime.now().strftime("%H:%M:%S")
                                    subwidget.insert("end", f"[{timestamp}] ⚠️ {self.opponent_name} se ha desconectado\n")
                                    subwidget.see("end")
                                    subwidget.configure(state="disabled")
                                    break
                except Exception as e:
                    print(f"⚠️ Error añadiendo notificación: {e}")
            
            # Mostrar mensaje
                messagebox.showwarning(
                    "Oponente desconectado",
                    f"{self.opponent_name} se ha desconectado del juego.\n\nEl juego continuará en modo local.",
                    parent=self.app.current_screen
                )

    def close_network_window(self):
        """Cierra la ventana de red, manteniendo la conexión activa."""
        self.cleanup_lobby_ui()
    # Hemos quitado cualquier llamada a self.disconnect() o self.client_socket.close() de aquí.
    # El sonido también lo quitamos para evitar cualquier conflicto.
    
    # En network_game_manager.py, añade esta nueva función
    def cleanup_lobby_ui(self):
        """Limpia y destruye SOLO la ventana del lobby de red, sin tocar los sockets."""
        if hasattr(self, 'network_window') and self.network_window and self.network_window.winfo_exists():
            print("🧹 Limpiando y destruyendo la ventana del lobby de red...")
            self.network_window.destroy()
            self.network_window = None
        else:
            print("🧹 La ventana del lobby de red ya estaba cerrada o no existía.")


    def shutdown_network_connection(self):
        """Desconectar de la red"""
        try:
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
            
            if self.client_socket:
                self.client_socket.close()
                self.client_socket = None
            
            self.is_connected = False
            self.is_host = False
            self.opponent_name = ""
            self.game_room_code = ""
            
            print("🔌 Desconectado de la red")
            
        except Exception as e:
            print(f"⚠️ Error desconectando: {e}")
    
    def send_game_move(self, move_data):
        """Enviar movimiento de juego"""
        if self.is_connected:
            game_message = {
                "type": "game_move",
                "player": self.app.player_name,
                "move": move_data,
                "timestamp": datetime.now().isoformat()
            }
            return self.send_message(game_message)
        return False
    
    def receive_game_move(self):
        """Recibir movimiento del oponente"""
        if self.is_connected:
            message = self.receive_message()
            if message and message.get("type") == "game_move":
                return message.get("move")
        return None