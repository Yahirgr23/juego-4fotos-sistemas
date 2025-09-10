#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
import requests
import threading
from datetime import datetime
import socket
from level_server import NetworkScanner

class LevelDownloader:
    def __init__(self, parent_app):
        self.app = parent_app
        self.downloader_window = None
        self.scanner = NetworkScanner()
        self.downloading = False
        
    def show_downloader(self):
        """Mostrar ventana del descargador"""
        print("📥 Abriendo Descargador de Niveles...")
        
        if self.downloader_window:
            self.downloader_window.destroy()
        
        # Crear ventana
        self.downloader_window = ctk.CTkToplevel(self.app.root)
        self.downloader_window.title("📥 Descargar Niveles")
        self.downloader_window.geometry("800x600")
        self.downloader_window.resizable(True, True)
        
        # Frame principal
        main_frame = ctk.CTkFrame(self.downloader_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        header_frame = ctk.CTkFrame(main_frame)
        header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            header_frame,
            text="📥 DESCARGADOR DE NIVELES",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=10)
        
        # Tabs
        tabview = ctk.CTkTabview(main_frame)
        tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tab 1: Red Local
        tab_network = tabview.add("🌐 Red Local")
        self.create_network_tab(tab_network)
        
        # Tab 2: Servidor Público
        tab_online = tabview.add("☁️ Online")
        self.create_online_tab(tab_online)
        
        # Tab 3: URL Directa
        tab_url = tabview.add("🔗 URL Directa")
        self.create_url_tab(tab_url)
        
        # Botones inferiores
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(fill="x", padx=10, pady=(5, 10))
        
        refresh_btn = ctk.CTkButton(
            buttons_frame,
            text="🔄 ACTUALIZAR",
            command=self.refresh_all,
            width=150,
            height=40,
            fg_color="#2196F3"
        )
        refresh_btn.pack(side="left", padx=10, pady=10)
        
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="❌ CERRAR",
            command=self.close_downloader,
            width=150,
            height=40,
            fg_color="#607D8B"
        )
        close_btn.pack(side="right", padx=10, pady=10)
        
        print("✅ Descargador de niveles abierto")
    
    def create_network_tab(self, parent):
        """Tab de red local"""
        # Información
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        info_text = (
            "🌐 Busca niveles en tu red local WiFi.\n"
            "Otros usuarios pueden compartir niveles desde su computadora."
        )
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(padx=15, pady=15)
        
        # Controles de escaneo
        scan_frame = ctk.CTkFrame(parent)
        scan_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            scan_frame,
            text="🔍 ESCANEAR RED:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        self.network_entry = ctk.CTkEntry(
            scan_frame,
            placeholder_text="Red (ej: 192.168.1)",
            width=150
        )
        self.network_entry.pack(side="left", padx=10, pady=10)
        self.network_entry.insert(0, self.scanner.get_local_network())
        
        scan_btn = ctk.CTkButton(
            scan_frame,
            text="🔍 ESCANEAR",
            command=self.scan_network,
            width=120,
            height=35,
            fg_color="#4CAF50"
        )
        scan_btn.pack(side="left", padx=10, pady=10)
        
        # Estado del escaneo
        self.scan_status_label = ctk.CTkLabel(
            scan_frame,
            text="💤 Listo para escanear",
            font=ctk.CTkFont(size=12)
        )
        self.scan_status_label.pack(side="left", padx=10, pady=10)
        
        # Lista de servidores encontrados
        servers_frame = ctk.CTkFrame(parent)
        servers_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            servers_frame,
            text="🖥️ SERVIDORES ENCONTRADOS:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        # Scrollable frame para servidores
        self.servers_scroll_frame = ctk.CTkScrollableFrame(servers_frame)
        self.servers_scroll_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Conexión manual
        manual_frame = ctk.CTkFrame(parent)
        manual_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            manual_frame,
            text="🔌 CONEXIÓN MANUAL:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        self.manual_ip_entry = ctk.CTkEntry(
            manual_frame,
            placeholder_text="IP (ej: 192.168.1.100)",
            width=150
        )
        self.manual_ip_entry.pack(side="left", padx=5, pady=10)
        
        self.manual_port_entry = ctk.CTkEntry(
            manual_frame,
            placeholder_text="Puerto",
            width=80
        )
        self.manual_port_entry.pack(side="left", padx=5, pady=10)
        
        connect_btn = ctk.CTkButton(
            manual_frame,
            text="🔌 CONECTAR",
            command=self.connect_manual,
            width=100,
            height=35,
            fg_color="#FF9800"
        )
        connect_btn.pack(side="left", padx=10, pady=10)
    
    def create_online_tab(self, parent):
        """Tab de servidor público"""
        # Información
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        info_text = (
            "☁️ Explora niveles públicos subidos por la comunidad.\n"
            "Descarga y juega niveles creados por otros jugadores."
        )
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(padx=15, pady=15)
        
        # Filtros
        filter_frame = ctk.CTkFrame(parent)
        filter_frame.pack(fill="x", padx=10, pady=5)
        
        ctk.CTkLabel(
            filter_frame,
            text="🔍 FILTROS:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, pady=10)
        
        self.difficulty_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=["Todos", "Fácil", "Medio", "Difícil", "Experto"],
            width=100
        )
        self.difficulty_filter.pack(side="left", padx=5, pady=10)
        
        self.category_filter = ctk.CTkOptionMenu(
            filter_frame,
            values=["Todas", "Animales", "Objetos", "Comida", "Deportes", "Naturaleza"],
            width=120
        )
        self.category_filter.pack(side="left", padx=5, pady=10)
        
        search_btn = ctk.CTkButton(
            filter_frame,
            text="🔍 BUSCAR",
            command=self.search_online_levels,
            width=100,
            height=35,
            fg_color="#4CAF50"
        )
        search_btn.pack(side="left", padx=10, pady=10)
        
        # Lista de niveles online
        online_frame = ctk.CTkFrame(parent)
        online_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        ctk.CTkLabel(
            online_frame,
            text="📋 NIVELES PÚBLICOS:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        self.online_levels_frame = ctk.CTkScrollableFrame(online_frame)
        self.online_levels_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Botón actualizar
        update_btn = ctk.CTkButton(
            parent,
            text="🔄 ACTUALIZAR LISTA",
            command=self.refresh_online_levels,
            width=200,
            height=40,
            fg_color="#2196F3"
        )
        update_btn.pack(pady=10)
    
    def create_url_tab(self, parent):
        """Tab de URL directa"""
        # Información
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", padx=10, pady=10)
        
        info_text = (
            "🔗 Descarga niveles directamente desde una URL.\n"
            "Pega el enlace de descarga que te hayan compartido."
        )
        
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(padx=15, pady=15)
        
        # Campo URL
        url_frame = ctk.CTkFrame(parent)
        url_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(
            url_frame,
            text="🌐 URL del nivel:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))
        
        self.url_entry = ctk.CTkEntry(
            url_frame,
            placeholder_text="https://ejemplo.com/nivel.4f1p",
            width=500,
            height=40
        )
        self.url_entry.pack(pady=10)
        
        download_url_btn = ctk.CTkButton(
            url_frame,
            text="📥 DESCARGAR DESDE URL",
            command=self.download_from_url,
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50"
        )
        download_url_btn.pack(pady=15)
        
        # Código de sala
        code_frame = ctk.CTkFrame(parent)
        code_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(
            code_frame,
            text="🎮 Código de sala:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))
        
        code_input_frame = ctk.CTkFrame(code_frame)
        code_input_frame.pack(pady=10)
        
        self.room_code_entry = ctk.CTkEntry(
            code_input_frame,
            placeholder_text="Código de 6 dígitos",
            width=200,
            height=40,
            font=ctk.CTkFont(size=16)
        )
        self.room_code_entry.pack(side="left", padx=10)
        
        connect_code_btn = ctk.CTkButton(
            code_input_frame,
            text="🔍 BUSCAR SALA",
            command=self.search_room_code,
            width=150,
            height=40,
            fg_color="#FF9800"
        )
        connect_code_btn.pack(side="left", padx=10)
        
        # Archivo local
        file_frame = ctk.CTkFrame(parent)
        file_frame.pack(fill="x", padx=10, pady=20)
        
        ctk.CTkLabel(
            file_frame,
            text="📁 Archivo local:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(15, 10))
        
        select_file_btn = ctk.CTkButton(
            file_frame,
            text="📂 SELECCIONAR ARCHIVO",
            command=self.select_local_file,
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#9C27B0"
        )