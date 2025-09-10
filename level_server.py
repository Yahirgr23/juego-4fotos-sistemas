#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import json
import os
from datetime import datetime
import random
import string

class LevelServer:
    def __init__(self, level_data):
        self.level_data = level_data
        self.server_socket = None
        self.clients = []
        self.running = False
        self.host = self.get_local_ip()
        self.port = self.find_free_port()
        self.room_code = self.generate_room_code()
        
    def get_local_ip(self):
        """Obtener IP local de la máquina"""
        try:
            # Conectar a un servidor externo para obtener la IP local
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                s.connect(("8.8.8.8", 80))
                local_ip = s.getsockname()[0]
            return local_ip
        except Exception:
            return "127.0.0.1"
    
    def find_free_port(self, start_port=8080):
        """Encontrar un puerto libre"""
        port = start_port
        while port < start_port + 100:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.bind((self.host, port))
                    return port
            except OSError:
                port += 1
        return None
    
    def generate_room_code(self):
        """Generar código de sala único"""
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    
    def start(self):
        """Iniciar servidor"""
        if not self.port:
            print("❌ No se pudo encontrar un puerto libre")
            return None
        
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            
            self.running = True
            
            # Iniciar hilo del servidor
            server_thread = threading.Thread(target=self.server_loop, daemon=True)
            server_thread.start()
            
            server_info = {
                'ip': self.host,
                'port': self.port,
                'room_code': self.room_code,
                'level_title': self.level_data.get('metadata', {}).get('title', 'Nivel sin título'),
                'level_author': self.level_data.get('metadata', {}).get('author', 'Anónimo')
            }
            
            print(f"🌐 Servidor iniciado en {self.host}:{self.port}")
            print(f"🎮 Código de sala: {self.room_code}")
            
            return server_info
            
        except Exception as e:
            print(f"❌ Error iniciando servidor: {e}")
            return None
    
    def server_loop(self):
        """Bucle principal del servidor"""
        print(f"🔄 Servidor escuchando en {self.host}:{self.port}")
        
        while self.running:
            try:
                client_socket, address = self.server_socket.accept()
                print(f"🔌 Cliente conectado desde {address}")
                
                # Crear hilo para manejar cliente
                client_thread = threading.Thread(
                    target=self.handle_client,
                    args=(client_socket, address),
                    daemon=True
                )
                client_thread.start()
                
            except Exception as e:
                if self.running:
                    print(f"❌ Error aceptando conexión: {e}")
    
    def handle_client(self, client_socket, address):
        """Manejar cliente conectado"""
        try:
            # Recibir petición del cliente
            data = client_socket.recv(4096).decode('utf-8')
            
            if not data:
                return
            
            try:
                request = json.loads(data)
            except json.JSONDecodeError:
                # Manejar petición HTTP simple
                if data.startswith('GET'):
                    self.handle_http_request(client_socket, data)
                    return
                else:
                    raise
            
            # Procesar petición JSON
            self.process_request(client_socket, request)
            
        except Exception as e:
            print(f"❌ Error manejando cliente {address}: {e}")
        finally:
            client_socket.close()
    
    def handle_http_request(self, client_socket, request):
        """Manejar petición HTTP básica"""
        try:
            # Parsear petición
            lines = request.split('\n')
            first_line = lines[0].split()
            path = first_line[1] if len(first_line) > 1 else '/'
            
            if path == '/':
                response = self.get_server_info_html()
            elif path == '/level':
                response = self.get_level_json()
            elif path == '/api/level':
                response = self.get_level_api_response()
            else:
                response = self.get_404_response()
            
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"❌ Error en petición HTTP: {e}")
    
    def get_server_info_html(self):
        """Generar página de información del servidor"""
        level_title = self.level_data.get('metadata', {}).get('title', 'Nivel sin título')
        level_author = self.level_data.get('metadata', {}).get('author', 'Anónimo')
        level_description = self.level_data.get('metadata', {}).get('description', '')
        level_difficulty = self.level_data.get('metadata', {}).get('difficulty', 'Medio')
        words_count = len(self.level_data.get('words', []))
        
        html = f"""
<!DOCTYPE html>
<html>
<head>
    <title>🎮 Servidor de Nivel - 4 Fotos 1 Palabra</title>
    <meta charset="UTF-8">
    <style>
        body {{
            font-family: Arial, sans-serif;
            background: linear-gradient(135deg, #1a1a1a, #2d2d2d);
            color: white;
            margin: 0;
            padding: 20px;
            text-align: center;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background: rgba(255,255,255,0.1);
            padding: 30px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
        }}
        .title {{
            font-size: 2.5em;
            margin-bottom: 20px;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
        }}
        .level-info {{
            background: rgba(255,255,255,0.1);
            padding: 20px;
            border-radius: 10px;
            margin: 20px 0;
            text-align: left;
        }}
        .stat {{
            margin: 10px 0;
            font-size: 1.1em;
        }}
        .code {{
            font-size: 2em;
            font-weight: bold;
            color: #4CAF50;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.5);
            margin: 20px 0;
        }}
        .instructions {{
            background: rgba(76, 175, 80, 0.2);
            padding: 15px;
            border-radius: 10px;
            margin: 20px 0;
        }}
        .download-btn {{
            background: #4CAF50;
            color: white;
            padding: 15px 30px;
            border: none;
            border-radius: 25px;
            font-size: 1.2em;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 10px;
            transition: background 0.3s;
        }}
        .download-btn:hover {{
            background: #45a049;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="title">🎮 4 Fotos 1 Palabra</div>
        <h2>🌐 Servidor Local de Nivel</h2>
        
        <div class="level-info">
            <h3>📝 Información del Nivel</h3>
            <div class="stat">📋 <strong>Título:</strong> {level_title}</div>
            <div class="stat">