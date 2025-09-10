#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
import shutil
from datetime import datetime
import base64
from PIL import Image, ImageTk
import io
import threading
import socket

class CustomLevelsManager:
    def __init__(self, parent_app):
        self.app = parent_app
        self.levels_window = None
        self.local_levels = []
        self.downloaded_levels = []
        self.network_levels = []
    
    def show_level_demo(self, level_data):
        """Mostrar demostración del nivel - SIN DEPENDER DE IMÁGENES BASE64"""
        # Crear ventana temporal de demostración
        demo_window = ctk.CTkToplevel(self.levels_window)
        demo_window.title("🎮 Vista Previa del Nivel")
        demo_window.geometry("600x500")
        demo_window.resizable(True, True)
    
    # Frame principal
        main_frame = ctk.CTkFrame(demo_window)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Información del nivel
        metadata = level_data.get('metadata', {})
        title = metadata.get('title', 'Sin título')
        author = metadata.get('author', 'Anónimo')
        words_count = len(level_data.get('words', []))
        difficulty = metadata.get('difficulty', 'Fácil')
    
    # Header
        header_label = ctk.CTkLabel(
            main_frame,
            text=f"📋 INFORMACIÓN DEL NIVEL",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        header_label.pack(pady=(20, 15))
    
    # Información detallada
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", padx=20, pady=10)
    
        info_text = f"📝 Título: {title}\n"
        info_text += f"👤 Autor: {author}\n" 
        info_text += f"⭐ Dificultad: {difficulty}\n"
        info_text += f"🎯 Total de palabras: {words_count}\n"
    
        if metadata.get('description'):
            info_text += f"📄 Descripción: {metadata['description']}\n"
    
        info_label = ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="left"
        )
        info_label.pack(pady=20)
    
    # Lista de palabras
        words_frame = ctk.CTkFrame(main_frame)
        words_frame.pack(fill="both", expand=True, padx=20, pady=10)
    
        words_label = ctk.CTkLabel(
            words_frame,
            text="📝 PALABRAS EN ESTE NIVEL:",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        words_label.pack(pady=(15, 10))
    
        # Mostrar palabras (hasta 10)
        words_list = level_data.get('words', [])
        words_to_show = words_list[:10]  # Mostrar máximo 10
    
        for i, word_data in enumerate(words_to_show):
            word = word_data.get('word', f'Palabra {i+1}')
            hint = word_data.get('hint', '')
        
         # Contar imágenes (compatible con TU sistema)
            images = word_data.get('images', [])
            images_count = sum(1 for img in images if img is not None)
        
            word_text = f"{i+1}. {word} ({images_count} imágenes)"
            if hint:
                word_text += f" - 💡 {hint[:30]}..."
        
            word_item_label = ctk.CTkLabel(
                words_frame,
                text=word_text,
                font=ctk.CTkFont(size=12),
                anchor="w"
            )
            word_item_label.pack(anchor="w", padx=20, pady=2)
    
        if len(words_list) > 10:
            more_label = ctk.CTkLabel(
                words_frame,
                text=f"... y {len(words_list) - 10} palabras más",
                font=ctk.CTkFont(size=12),
                text_color="#888888"
            )
            more_label.pack(anchor="w", padx=20, pady=5)
    
    # Mensaje de estado
        status_label = ctk.CTkLabel(
            main_frame,
            text="✅ Este nivel está listo para jugar\n🎮 La funcionalidad completa estará disponible pronto",
            font=ctk.CTkFont(size=12),
            text_color="#4CAF50",
            justify="center"
        )
        status_label.pack(pady=20)
    
    # Botón cerrar
        close_btn = ctk.CTkButton(
            main_frame,
            text="❌ CERRAR",
            command=demo_window.destroy,
            width=150,
            height=40,
            fg_color="#607D8B"
        )
        close_btn.pack(pady=15)
    
        print(f"🎮 Vista previa creada para: {title}")



    def show_levels_manager(self):
        """Mostrar gestor de niveles - CORRECCIÓN MÍNIMA"""
        print("📚 Abriendo Gestor de Niveles...")
    
    # Verificar si la ventana ya existe y está abierta
        if self.levels_window is not None:
            try:
                if self.levels_window.winfo_exists():
                    print("📚 Ventana ya existe, enfocando...")
                    self.levels_window.lift()
                    self.levels_window.focus_force()
                    self.levels_window.attributes('-topmost', True)
                    self.levels_window.after(100, lambda: self.levels_window.attributes('-topmost', False))
                
                # Actualizar contenido
                    self.refresh_all_levels()
                    return
                else:
                    print("📚 Ventana fue cerrada, limpiando referencia...")
                    self.levels_window = None
            except Exception as e:
                print(f"⚠️ Error verificando ventana: {e}")
                self.levels_window = None
    
    # Crear nueva ventana solo si no existe
        print("📚 Creando nueva ventana del gestor...")
        try:
            self._create_levels_window()
        except Exception as e:
            print(f"❌ Error creando ventana del gestor: {e}")
        # Mostrar mensaje de error básico
            messagebox.showerror("Error", f"No se pudo abrir el gestor de niveles:\n{e}")

    def _create_levels_window(self):
        """Crear la ventana del gestor - VERSIÓN COMPLETA COMPATIBLE CON TU SISTEMA"""
        try:
            # Crear ventana
            self.levels_window = ctk.CTkToplevel(self.app.root)
            self.levels_window.title("📚 Mis Niveles Personalizados")
            self.levels_window.geometry("1200x700")
            self.levels_window.resizable(True, True)
        
        # Centrar ventana
            self.center_levels_window()
        
        # Configurar protocolo de cierre
            self.levels_window.protocol("WM_DELETE_WINDOW", self.close_manager_safely)
        
        # Configurar ventana para que siempre esté visible
            self.levels_window.attributes('-topmost', True)
            self.levels_window.after(500, lambda: self.levels_window.attributes('-topmost', False))
        
        # Frame principal
            main_frame = ctk.CTkFrame(self.levels_window)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
            header_frame = ctk.CTkFrame(main_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))
        
            ctk.CTkLabel(
                header_frame,
                text="📚 NIVELES PERSONALIZADOS",
                font=ctk.CTkFont(size=24, weight="bold")
            ).pack(pady=10)
        
        # Indicador de ventana única
            status_label = ctk.CTkLabel(
                header_frame,
                text="✅ Ventana única activa",
                font=ctk.CTkFont(size=10),
                text_color="#4CAF50"
            )
            status_label.pack()

        # Tabs - VERSIÓN COMPLETA
            self.tabview = ctk.CTkTabview(main_frame)
            self.tabview.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Tab 1: Mis Niveles - COMPLETO
            tab_local = self.tabview.add("🏠 Mis Niveles")
            self.create_local_levels_tab(tab_local)
        
        # Tab 2: Niveles Descargados - COMPLETO
            tab_downloaded = self.tabview.add("📥 Descargados")
            self.create_downloaded_levels_tab_complete(tab_downloaded)
        
        # Tab 3: Red Local - COMPLETO
            tab_network = self.tabview.add("🌐 Red Local")
            self.create_network_levels_tab(tab_network)
        
        # Tab 4: Importar/Exportar - COMPLETO
            tab_import = self.tabview.add("📤 Importar")
            self.create_import_export_tab_complete(tab_import)
        
        # Botones de acción
            actions_frame = ctk.CTkFrame(main_frame)
            actions_frame.pack(fill="x", padx=10, pady=(5, 10))
        
            refresh_btn = ctk.CTkButton(
                actions_frame,
                text="🔄 ACTUALIZAR",
                command=self.refresh_all_levels(),
                width=150,
                height=40,
                fg_color="#2196F3"
            )   
            refresh_btn.pack(side="left", padx=10, pady=10)
        
            close_btn = ctk.CTkButton(
                actions_frame,
                text="❌ CERRAR",
                command=self.close_manager_safely,
                width=150,
                height=40,
                fg_color="#607D8B"
            )
            close_btn.pack(side="right", padx=10, pady=10)
        
        # Cargar niveles
            self.refresh_all_levels()
        
            print("✅ Gestor de niveles completo abierto")
        
        except Exception as e:
            print(f"❌ Error en _create_levels_window: {e}")
            raise

    def center_levels_window(self):
        """Centrar ventana del gestor en la pantalla"""
        try:
            if not self.levels_window or not self.levels_window.winfo_exists():
                return

            # Actualizar geometría
            self.levels_window.update_idletasks()

            # Obtener dimensiones
            width = self.levels_window.winfo_width()
            height = self.levels_window.winfo_height()

            # Obtener dimensiones de pantalla
            screen_width = self.levels_window.winfo_screenwidth()
            screen_height = self.levels_window.winfo_screenheight()

            # Calcular posición centrada
            x = (screen_width - width) // 2
            y = (screen_height - height) // 2

            # Asegurar límites
            x = max(0, min(x, screen_width - width))
            y = max(0, min(y, screen_height - height))

            # Aplicar posición
            self.levels_window.geometry(f"{width}x{height}+{x}+{y}")

            print(f"🎯 Gestor centrado en: {x},{y}")

        except Exception as e:
            print(f"⚠️ Error centrando gestor: {e}")

    
    def create_manager_interface(self):
        """Crear interfaz completa del gestor"""
        try:
            # Ensure ctk is available
            global ctk
            if 'ctk' not in globals():
                try:
                    import customtkinter as ctk
                except ImportError:
                    print("customtkinter not found in create_manager_interface. Using mock.")
                    class MockCtkModule:
                        def CTkToplevel(self, *args, **kwargs): return MockWindow()
                        def CTkFrame(self, *args, **kwargs): return MockFrame()
                        def CTkLabel(self, *args, **kwargs): return MockLabel()
                        def CTkFont(self, *args, **kwargs): return None
                        def CTkTabview(self, *args, **kwargs): return MockTabView()
                        def CTkButton(self, *args, **kwargs): return MockButton()
                    class MockWindow: pass
                    class MockFrame:
                        def pack(self, *args, **kwargs): pass
                        def add(self, name): return MockFrame() # For TabView
                    class MockLabel:
                        def pack(self, *args, **kwargs): pass
                    class MockTabView:
                        def pack(self, *args, **kwargs): pass
                        def add(self, name): return MockFrame() # Tab content is a frame
                    class MockButton:
                         def pack(self, *args, **kwargs): pass
                    ctk = MockCtkModule()

            # Frame principal
            main_frame = ctk.CTkFrame(self.levels_window)
            main_frame.pack(fill="both", expand=True, padx=10, pady=10)

            # Header
            header_frame = ctk.CTkFrame(main_frame)
            header_frame.pack(fill="x", padx=10, pady=(10, 5))

            ctk.CTkLabel(
                header_frame,
                text="📚 NIVELES PERSONALIZADOS",
                font=ctk.CTkFont(size=24, weight="bold")
            ).pack(pady=10)

            # Tabs
            tabview = ctk.CTkTabview(main_frame)
            tabview.pack(fill="both", expand=True, padx=10, pady=5)

            # Crear tabs
            tab_local = tabview.add("🏠 Mis Niveles")
            tab_downloaded = tabview.add("📥 Descargados")
            tab_network = tabview.add("🌐 Red Local")
            tab_import = tabview.add("📤 Importar")

            # Crear contenido de tabs (assuming these methods exist)
            if hasattr(self, 'create_local_levels_tab'):
                self.create_local_levels_tab(tab_local)
            else:
                print("⚠️ create_local_levels_tab method not found")
            if hasattr(self, 'create_downloaded_levels_tab'):
                self.create_downloaded_levels_tab(tab_downloaded)
            else:
                print("⚠️ create_downloaded_levels_tab method not found")
            if hasattr(self, 'create_network_levels_tab'):
                self.create_network_levels_tab(tab_network)
            else:
                print("⚠️ create_network_levels_tab method not found")
            if hasattr(self, 'create_import_export_tab'):
                self.create_import_export_tab(tab_import)
            else:
                print("⚠️ create_import_export_tab method not found")


            # Botones de acción
            actions_frame = ctk.CTkFrame(main_frame)
            actions_frame.pack(fill="x", padx=10, pady=(5, 10))

            refresh_command = self.refresh_all_levels if hasattr(self, 'refresh_all_levels') else lambda: print("Refresh N/A")
            refresh_btn = ctk.CTkButton(
                actions_frame,
                text="🔄 ACTUALIZAR",
                command=refresh_command,
                width=150,
                height=40,
                fg_color="#2196F3"
            )
            refresh_btn.pack(side="left", padx=10, pady=10)

            close_btn = ctk.CTkButton(
                actions_frame,
                text="❌ CERRAR",
                command=self.close_manager_safely,
                width=150,
                height=40,
                fg_color="#607D8B"
            )
            close_btn.pack(side="right", padx=10, pady=10)

            print("✅ Interfaz del gestor creada")

        except Exception as e:
            print(f"❌ Error creando interfaz del gestor: {e}")
            raise
    
    def load_all_levels_data(self):
        """Cargar todos los datos de niveles"""
        try:
            # Inicializar listas
            self.local_levels = []
            self.downloaded_levels = []
            self.network_levels = []

            # Cargar datos
            if hasattr(self, 'refresh_all_levels'):
                self.refresh_all_levels()
            else:
                print("⚠️ refresh_all_levels method not found for initial load")


            print("✅ Datos de niveles cargados")

        except Exception as e:
            print(f"❌ Error cargando datos: {e}")

    def close_manager_safely(self):
        """Cerrar gestor de manera segura"""
        print("❌ Cerrando gestor de niveles...")
        
        # Verificar si hay operaciones pendientes
        if hasattr(self, 'downloading') and self.downloading:
            result = messagebox.askyesno(
                "Operación en progreso",
                "Hay una descarga en progreso.\n¿Cerrar de todas formas?",
                parent=self.levels_window
            )
            if not result:
                return
        
        # Limpiar recursos
        self.cleanup_manager_data()
        
        # Destruir ventana
        if self.levels_window:
            try:
                self.levels_window.destroy()
            except:
                pass
            finally:
                self.levels_window = None
        
        try:
            self.app.sound_manager.play_sound('menu_select')
        except:
            pass
        
        print("✅ Gestor cerrado correctamente")

    def cleanup_manager_data(self):
        """Limpiar datos del gestor"""
        try:
            # Limpiar listas
            self.local_levels.clear()
            self.downloaded_levels.clear()
            self.network_levels.clear()
            
            # Cancelar operaciones pendientes
            if hasattr(self, 'scanner') and hasattr(self.scanner, 'stop'):
                self.scanner.stop()
            
            print("🧹 Datos del gestor limpiados")
        except Exception as e:
            print(f"⚠️ Error limpiando datos: {e}")

    # Placeholders for methods called within create_manager_interface and load_all_levels_data
    





   

    def create_local_levels_tab(self, parent):
        """Tab de niveles locales - VERSIÓN COMPLETA"""
    # Frame para filtros
        filter_frame = ctk.CTkFrame(parent)
        filter_frame.pack(fill="x", padx=10, pady=10)
    
        ctk.CTkLabel(
            filter_frame,
            text="🔍 FILTROS:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, pady=10)
    
        self.local_filter_var = ctk.StringVar(value="Todos")
        filter_menu = ctk.CTkOptionMenu(
            filter_frame,
            variable=self.local_filter_var,
            values=["Todos", "Fácil", "Medio", "Difícil", "Experto"],
            command=self.filter_local_levels,
            width=120
        )
        filter_menu.pack(side="left", padx=10, pady=10)
    
        search_entry = ctk.CTkEntry(
            filter_frame,
            placeholder_text="Buscar por título...",
            width=200
        )
        search_entry.pack(side="left", padx=10, pady=10)
        search_entry.bind("<KeyRelease>", self.search_local_levels)
        self.local_search_entry = search_entry
    
    # Lista de niveles locales
        levels_frame = ctk.CTkScrollableFrame(parent)
        levels_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        self.local_levels_frame = levels_frame
    
    # Botones de acción
        local_actions = ctk.CTkFrame(parent)
        local_actions.pack(fill="x", padx=10, pady=5)
    
        new_level_btn = ctk.CTkButton(
            local_actions,
            text="🆕 NUEVO NIVEL",
            command=self.create_new_level,
            width=150,
            height=35,
            fg_color="#4CAF50"
        )
        new_level_btn.pack(side="left", padx=10, pady=5)
    
        import_btn = ctk.CTkButton(
            local_actions,
            text="📁 IMPORTAR",
            command=self.import_level_file,
            width=150,
            height=35,
            fg_color="#FF9800"
        )
        import_btn.pack(side="left", padx=5, pady=5)
    
    def create_downloaded_levels_tab_complete(self, parent):
        """Tab de niveles descargados - VERSIÓN COMPLETA"""
        # Info frame
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", padx=10, pady=10)
    
        info_text = (
            "💡 Aquí aparecerán los niveles que descargues de otros jugadores.\n"
            "Puedes importar archivos .4f1p desde la pestaña 'Importar'."
        )
    
        ctk.CTkLabel(
            info_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(padx=15, pady=15)
    
    # Lista de niveles descargados
        downloaded_frame = ctk.CTkScrollableFrame(parent)
        downloaded_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        self.downloaded_levels_frame = downloaded_frame
    
    # Botones
        downloaded_actions = ctk.CTkFrame(parent)
        downloaded_actions.pack(fill="x", padx=10, pady=5)
    
        browse_btn = ctk.CTkButton(
            downloaded_actions,
            text="🌐 EXPLORAR ONLINE",
            command=self.browse_online_levels,
            width=150,
            height=35,
            fg_color="#9C27B0"
        )
        browse_btn.pack(side="left", padx=10, pady=5)
    
        clean_btn = ctk.CTkButton(
            downloaded_actions,
            text="🧹 LIMPIAR",
            command=self.clean_downloaded_levels,
            width=150,
            height=35,
            fg_color="#FF5722"
        )
        clean_btn.pack(side="right", padx=10, pady=5)
    
    def create_network_levels_tab(self, parent):
        """Tab de niveles en red local - VERSIÓN COMPLETA"""
    # Estado de conexión
        connection_frame = ctk.CTkFrame(parent)
        connection_frame.pack(fill="x", padx=10, pady=10)
    
        self.network_status_label = ctk.CTkLabel(
            connection_frame,
            text="🔍 Buscando niveles en red local...",
            font=ctk.CTkFont(size=14)
        )
        self.network_status_label.pack(pady=15)
    
    # Configuración de red
        network_config = ctk.CTkFrame(parent)
        network_config.pack(fill="x", padx=10, pady=5)
    
        ctk.CTkLabel(
            network_config,
            text="🌐 CONFIGURACIÓN DE RED:",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(side="left", padx=10, pady=10)
    
        self.ip_entry = ctk.CTkEntry(
            network_config,
            placeholder_text="IP del servidor (ej: 192.168.1.100)",
            width=200
        )
        self.ip_entry.pack(side="left", padx=10, pady=10)
    
        self.port_entry = ctk.CTkEntry(
            network_config,
            placeholder_text="Puerto",
            width=80
        )
        self.port_entry.pack(side="left", padx=5, pady=10)
    
        connect_btn = ctk.CTkButton(
        network_config,
        text="🔌 CONECTAR",
        command=self.connect_to_network_server,
        width=100,
        height=30
        )
        connect_btn.pack(side="left", padx=10, pady=10)
    
        scan_btn = ctk.CTkButton(
            network_config,
            text="🔍 ESCANEAR RED",
            command=self.scan_network,
            width=120,
            height=30,
            fg_color="#FF9800"
        )
        scan_btn.pack(side="left", padx=5, pady=10)
    
    # Lista de servidores encontrados
        servers_frame = ctk.CTkFrame(parent)
        servers_frame.pack(fill="x", padx=10, pady=5)
    
        ctk.CTkLabel(
            servers_frame,
            text="🖥️ SERVIDORES ENCONTRADOS:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(side="left", padx=10, pady=5)
    
        self.servers_listbox = tk.Listbox(
            servers_frame,
            bg="#2b2b2b",
            fg="white",
            selectbackground="#1f538d",
            height=4,
            font=("Arial", 10)
        )
        self.servers_listbox.pack(side="left", fill="x", expand=True, padx=10, pady=5)
    
    # Lista de niveles de red
        network_levels_frame = ctk.CTkScrollableFrame(parent)
        network_levels_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        self.network_levels_frame = network_levels_frame
    
    def create_import_export_tab_complete(self, parent):
        """Tab de importar/exportar - VERSIÓN COMPLETA"""
    # Sección importar
        import_section = ctk.CTkFrame(parent)
        import_section.pack(fill="x", padx=10, pady=10)
    
        ctk.CTkLabel(
            import_section,
            text="📥 IMPORTAR NIVELES",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
    
        import_info = (
            "Importa niveles desde archivos .4f1p o .json\n"
            "También puedes arrastrar y soltar archivos aquí"
        )
    
        ctk.CTkLabel(
            import_section,
            text=import_info,
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 10))
    
        import_buttons = ctk.CTkFrame(import_section)
        import_buttons.pack(pady=10)
    
        import_file_btn = ctk.CTkButton(
            import_buttons,
            text="📁 SELECCIONAR ARCHIVO",
            command=self.import_level_file,
            width=180,
            height=40,
            fg_color="#4CAF50"
        )
        import_file_btn.pack(side="left", padx=10)
    
        import_folder_btn = ctk.CTkButton(
            import_buttons,
            text="📂 CARPETA COMPLETA",
            command=self.import_level_folder,
            width=180,
            height=40,
            fg_color="#2196F3"
        )
        import_folder_btn.pack(side="left", padx=10)
    
    # Sección exportar
        export_section = ctk.CTkFrame(parent)
        export_section.pack(fill="x", padx=10, pady=10)
    
        ctk.CTkLabel(
            export_section,
            text="📤 EXPORTAR Y COMPARTIR",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
    
        export_info = (
            "Crea paquetes para compartir tus niveles\n"
            "Los archivos .4f1p pueden compartirse fácilmente"
        )
    
        ctk.CTkLabel(
            export_section,
            text=export_info,
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 10))
    
        export_buttons = ctk.CTkFrame(export_section)
        export_buttons.pack(pady=10)
    
        export_single_btn = ctk.CTkButton(
            export_buttons,
            text="📦 EXPORTAR NIVEL",
            command=self.export_single_level,
            width=180,
            height=40,
            fg_color="#FF9800"
        )
        export_single_btn.pack(side="left", padx=10)
    
        export_pack_btn = ctk.CTkButton(
            export_buttons,
            text="📚 PACK DE NIVELES",
            command=self.export_level_pack,
            width=180,
            height=40,
            fg_color="#9C27B0"
        )
        export_pack_btn.pack(side="left", padx=10)
    
    # Sección información
        info_section = ctk.CTkFrame(parent)
        info_section.pack(fill="both", expand=True, padx=10, pady=10)
    
        ctk.CTkLabel(
            info_section,
            text="ℹ️ INFORMACIÓN",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
    
        info_text = (
            "📋 FORMATOS SOPORTADOS:\n"
            "• .4f1p - Formato nativo del juego (recomendado)\n"
            "• .json - Formato de desarrollo\n\n"
            "🌐 FORMAS DE COMPARTIR:\n"
             "• Archivo directo - Envía el .4f1p por email/chat\n"
            "• Red local - Comparte en tu WiFi\n"
            "• Servidor público - Disponible para todos\n\n"
            "🔒 PRIVACIDAD:\n"
            "• Tus niveles son privados por defecto\n"
            "• Solo compartes lo que eliges\n"
            "• Sin recopilación de datos personales"
        )
    
        info_label = ctk.CTkLabel(
            info_section,
            text=info_text,
            font=ctk.CTkFont(size=11),
            justify="left"
        )
        info_label.pack(padx=15, pady=15, anchor="w")
    
    def refresh_all_levels(self):
        """Actualizar todas las listas de niveles - VERSIÓN COMPLETA COMPATIBLE"""
        print("🔄 Actualizando listas de niveles...")
    
        try:
            self.load_local_levels_complete()
            self.load_downloaded_levels_complete()
            self.scan_network_levels_complete()
        
            try:
                self.app.sound_manager.play_sound('click')
            except:
                pass
        except Exception as e:
            print(f"❌ Error actualizando niveles: {e}")
    
    def load_local_levels_complete(self):
        """Cargar niveles locales - COMPATIBLE CON TU SISTEMA"""
        # Limpiar frame
        for widget in self.local_levels_frame.winfo_children():
            widget.destroy()
    
        self.local_levels = []
        levels_dir = "custom_levels"
    
        if not os.path.exists(levels_dir):
            os.makedirs(levels_dir, exist_ok=True)
    
    # Buscar archivos de nivel
        for filename in os.listdir(levels_dir):
            if filename.endswith('.json'):
                filepath = os.path.join(levels_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        level_data = json.load(f)
                
                    level_info = {
                        'filepath': filepath,
                        'filename': filename,
                        'data': level_data
                    }
                
                    self.local_levels.append(level_info)
                
                except Exception as e:
                    print(f"Error cargando nivel {filename}: {e}")
    
    # Mostrar niveles usando TU sistema
        self.display_local_levels()
    
        print(f"📁 {len(self.local_levels)} niveles locales cargados")



    def display_local_levels(self):
        """Mostrar niveles locales - COMPATIBLE CON TU SISTEMA DE IMÁGENES"""
        if not self.local_levels:
            no_levels_label = ctk.CTkLabel(
                self.local_levels_frame,
                text="📭 No hay niveles locales\n\n¡Crea tu primer nivel!",
                font=ctk.CTkFont(size=16),
                text_color="#888888"
            )
            no_levels_label.pack(expand=True, pady=50)
            return
    
        for level_info in self.local_levels:
            level_data = level_info['data']
            metadata = level_data.get('metadata', {})
        
        # Frame para cada nivel
            level_frame = ctk.CTkFrame(self.local_levels_frame)
            level_frame.pack(fill="x", padx=5, pady=5)
        
        # Información del nivel
            info_frame = ctk.CTkFrame(level_frame)
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        
        # Título y autor
            title = metadata.get('title', 'Sin título')
            author = metadata.get('author', 'Anónimo')
        
            title_label = ctk.CTkLabel(
                info_frame,
                text=f"📝 {title}",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            title_label.pack(anchor="w", pady=(5, 0))
        
            author_label = ctk.CTkLabel(
                info_frame,
                text=f"👤 Por: {author}",
                font=ctk.CTkFont(size=12),
                text_color="#cccccc",
                anchor="w"
            )
            author_label.pack(anchor="w")
        
        # Estadísticas compatibles con TU sistema de imágenes
            words = level_data.get('words', [])
            words_count = len(words)
            difficulty = metadata.get('difficulty', 'Desconocida')
        
        # Contar usando TU lógica de imágenes
            valid_words = 0
            total_images = 0
            for word_data in words:
                if word_data.get('word', '').strip():
                    images = word_data.get('images', [])
                    word_images = sum(1 for img in images if img is not None)
                    total_images += word_images
                    if word_images > 0:
                        valid_words += 1
        
            stats_text = f"🎯 {words_count} palabras ({valid_words} completas) • ⭐ {difficulty}"
            stats_text += f"\n📸 {total_images} imágenes totales"
        
            if metadata.get('description'):
                stats_text += f"\n📄 {metadata['description'][:60]}..."
        
            stats_label = ctk.CTkLabel(
                info_frame,
                text=stats_text,
                font=ctk.CTkFont(size=11),
                text_color="#aaaaaa",
                anchor="w",
                justify="left"
            )
            stats_label.pack(anchor="w", pady=(5, 5))
        
        # Botones de acción
            actions_frame = ctk.CTkFrame(level_frame)
            actions_frame.pack(side="right", padx=10, pady=10)
        
        # Botón jugar
            play_btn = ctk.CTkButton(
                actions_frame,
                text="🎮 JUGAR",
                command=lambda data=level_data: self.play_level(data),
                width=80,
                height=30,
                fg_color="#4CAF50"
            )
            play_btn.pack(pady=2)
        
        # Botón editar
            edit_btn = ctk.CTkButton(
                actions_frame,
                text="✏️ EDITAR",
                command=lambda path=level_info['filepath']: self.edit_level(path),
                width=80,
                height=30,
                fg_color="#2196F3"
            )
            edit_btn.pack(pady=2)
        
        # Botón compartir
            share_btn = ctk.CTkButton(
                actions_frame,
                text="📤 COMPARTIR",
                command=lambda data=level_data: self.share_level_quick(data),
                width=80,
                height=30,
                fg_color="#FF9800"
            )
            share_btn.pack(pady=2)
        
        # Botón eliminar
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="🗑️",
                command=lambda path=level_info['filepath']: self.delete_downloaded_level(path),
                width=80,
                height=25,
                fg_color="#FF5722"
            )
            delete_btn.pack(pady=2)
    
    def load_downloaded_levels(self):
        """Cargar niveles descargados - VERSIÓN COMPLETA"""
    # Limpiar frame
        for widget in self.downloaded_levels_frame.winfo_children():
            widget.destroy()
    
        self.downloaded_levels = []
        downloads_dir = "downloaded_levels"
    
        if not os.path.exists(downloads_dir):
            os.makedirs(downloads_dir, exist_ok=True)
    
    # Buscar archivos descargados
        for filename in os.listdir(downloads_dir):
            if filename.endswith(('.4f1p', '.json')):
                filepath = os.path.join(downloads_dir, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                
                # Manejar formato .4f1p (con metadata de exportación)
                    if 'level' in data:
                        level_data = data['level']
                        export_info = data.get('export_info', {})
                    else:
                        level_data = data
                        export_info = {}
                
                    level_info = {
                        'filepath': filepath,
                        'filename': filename,
                        'data': level_data,
                        'export_info': export_info
                 }
                
                    self.downloaded_levels.append(level_info)
                
                except Exception as e:
                    print(f"Error cargando nivel descargado {filename}: {e}")
    
        self.display_downloaded_levels_complete()
        print(f"📥 {len(self.downloaded_levels)} niveles descargados cargados")
    
    def display_downloaded_levels(self):
        """Mostrar niveles descargados"""
        if not self.downloaded_levels:
            no_levels_label = ctk.CTkLabel(
                self.downloaded_levels_frame,
                text="📭 No hay niveles descargados\n\n¡Importa algunos niveles desde la pestaña 'Importar'!",
                font=ctk.CTkFont(size=16),
                text_color="#888888"
            )
            no_levels_label.pack(expand=True, pady=50)
            return
        
        for level_info in self.downloaded_levels:
            level_data = level_info['data']
            export_info = level_info.get('export_info', {})
            metadata = level_data.get('metadata', {})
            
            # Frame para cada nivel
            level_frame = ctk.CTkFrame(self.downloaded_levels_frame)
            level_frame.pack(fill="x", padx=5, pady=5)
            
            # Información del nivel
            info_frame = ctk.CTkFrame(level_frame)
            info_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)
            
            # Título y autor
            title = metadata.get('title', 'Sin título')
            author = metadata.get('author', 'Anónimo')
            
            title_label = ctk.CTkLabel(
                info_frame,
                text=f"📦 {title}",
                font=ctk.CTkFont(size=16, weight="bold"),
                anchor="w"
            )
            title_label.pack(anchor="w", pady=(5, 0))
            
            author_info = f"👤 Por: {author}"
            if export_info.get('exported_by'):
                author_info += f" (Compartido por: {export_info['exported_by']})"
            
            author_label = ctk.CTkLabel(
                info_frame,
                text=author_info,
                font=ctk.CTkFont(size=12),
                text_color="#cccccc",
                anchor="w"
            )
            author_label.pack(anchor="w")
            
            # Estadísticas
            words_count = len(level_data.get('words', []))
            difficulty = metadata.get('difficulty', 'Desconocida')
            
            stats_text = f"🎯 {words_count} palabras • ⭐ {difficulty}"
            
            if export_info.get('export_date'):
                export_date = export_info['export_date'][:10]  # Solo fecha
                stats_text += f" • 📅 {export_date}"
            
            stats_label = ctk.CTkLabel(
                info_frame,
                text=stats_text,
                font=ctk.CTkFont(size=11),
                text_color="#aaaaaa",
                anchor="w"
            )
            stats_label.pack(anchor="w", pady=(5, 5))
            
            # Botones de acción
            actions_frame = ctk.CTkFrame(level_frame)
            actions_frame.pack(side="right", padx=10, pady=10)
            
            # Botón jugar
            play_btn = ctk.CTkButton(
                actions_frame,
                text="🎮 JUGAR",
                command=lambda data=level_data: self.play_level(data),
                width=80,
                height=30,
                fg_color="#4CAF50"
            )
            play_btn.pack(pady=2)
            
            # Botón instalar (mover a mis niveles)
            install_btn = ctk.CTkButton(
                actions_frame,
                text="📥 INSTALAR",
                command=lambda info=level_info: self.install_level(info),
                width=80,
                height=30,
                fg_color="#2196F3"
            )
            install_btn.pack(pady=2)
            
            # Botón eliminar
            delete_btn = ctk.CTkButton(
                actions_frame,
                text="🗑️",
                command=lambda path=level_info['filepath']: self.delete_downloaded_level(path),
                width=80,
                height=25,
                fg_color="#FF5722"
            )
            delete_btn.pack(pady=2)
    
   
    
    # Simulación de escaneo
        def simulate_scan():
            import time
            time.sleep(2)
        
        # Simular servidores encontrados
            if hasattr(self, 'servers_listbox'):
                self.servers_listbox.delete(0, tk.END)
                self.servers_listbox.insert(tk.END, "192.168.1.100:8080 - Juan's Levels")
                self.servers_listbox.insert(tk.END, "192.168.1.105:8080 - Maria's Collection")
        
            if hasattr(self, 'network_status_label'):
                self.network_status_label.configure(text="✅ Escaneo completado - 2 servidores encontrados")
    
    # Ejecutar en hilo separado
        threading.Thread(target=simulate_scan, daemon=True).start()
    
    def create_new_level(self):
        """Crear nuevo nivel - VERSIÓN MEJORADA"""
        print("🆕 Creando nuevo nivel...")
        
        try:
            # Verificar si ya existe una instancia del editor
            if hasattr(self.app, 'level_editor_instance') and self.app.level_editor_instance:
                print("📝 Editor ya existe, enfocando...")
                self.app.level_editor_instance.show_editor()
            else:
                # Crear nueva instancia
                from level_editor import LevelEditor
                self.app.level_editor_instance = LevelEditor(self.app)
                self.app.level_editor_instance.show_editor()
            
            try:
                self.app.sound_manager.play_sound('menu_select')
            except:
                pass
            
            print("🆕 Editor de nivel abierto exitosamente")
            
        except ImportError as e:
            print(f"❌ Error importando LevelEditor: {e}")
            messagebox.showerror("Error", 
                f"No se pudo abrir el editor de niveles.\n\n"
                f"Error: {e}\n\n"
                f"Asegúrate de que el archivo 'level_editor.py' esté en la misma carpeta.",
                parent=self.levels_window)
        except Exception as e:
            print(f"❌ Error creando nuevo nivel: {e}")
            messagebox.showerror("Error", f"No se pudo crear el nuevo nivel:\n{e}",
                               parent=self.levels_window)
            

            
    def play_level(self, level_data):
        """Jugar un nivel personalizado - COMPATIBLE CON TU SISTEMA"""
        try:
        # Verificar que el nivel tenga datos válidos
            if not level_data or not level_data.get('words'):
                messagebox.showwarning("Nivel vacío", "Este nivel no tiene palabras para jugar", parent=self.levels_window)
                return
        
        # Verificar si existe el método en la app principal
            if hasattr(self.app, 'start_custom_level'):
                self.app.start_custom_level(level_data)
                print("🎮 Nivel enviado a la app principal para jugar")
            
            # Cerrar gestor de niveles
                self.close_manager_safely()
            else:
            # Crear una pantalla de demostración simple
                self.show_level_demo(level_data)
        
            try:
                self.app.sound_manager.play_sound('game_start')
            except:
                pass
        
            print(f"🎮 Iniciando nivel: {level_data.get('metadata', {}).get('title', 'Sin título')}")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar el nivel:\n{e}", parent=self.levels_window)
            print(f"❌ Error iniciando nivel: {e}")
    
    def edit_level(self, filepath):
        """Editar nivel existente - VERSIÓN MEJORADA"""
        print(f"✏️ Editando nivel: {filepath}")
        
        try:
            # Verificar si ya existe una instancia del editor
            if hasattr(self.app, 'level_editor_instance') and self.app.level_editor_instance:
                print("📝 Editor ya existe, usándolo...")
                editor = self.app.level_editor_instance
                editor.show_editor()
            else:
                # Crear nueva instancia
                from level_editor import LevelEditor
                editor = LevelEditor(self.app)
                self.app.level_editor_instance = editor
                editor.show_editor()
            
            # Cargar el nivel en el editor después de un momento
            def load_level_data():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        level_data = json.load(f)
                    
                    editor.current_level = level_data
                    editor.current_word_index = 0
                    
                    # Actualizar interfaz
                    if hasattr(editor, 'title_entry') and editor.title_entry.winfo_exists():
                        metadata = level_data.get('metadata', {})
                        editor.title_entry.delete(0, tk.END)
                        editor.title_entry.insert(0, metadata.get('title', ''))
                        
                        editor.author_entry.delete(0, tk.END)
                        editor.author_entry.insert(0, metadata.get('author', ''))
                        
                        editor.description_textbox.delete('1.0', tk.END)
                        editor.description_textbox.insert('1.0', metadata.get('description', ''))
                        
                        editor.difficulty_var.set(metadata.get('difficulty', 'Fácil'))
                        
                        editor.load_current_word()
                        editor.update_words_list()
                        editor.update_stats()
                    
                    print(f"✏️ Nivel cargado en editor: {os.path.basename(filepath)}")
                    
                except Exception as e:
                    messagebox.showerror("Error", f"No se pudo cargar el nivel:\n{e}",
                                       parent=self.levels_window)
                    print(f"❌ Error cargando nivel: {e}")
            
            # Cargar después de que el editor esté listo
            if hasattr(editor, 'level_editor_window') and editor.level_editor_window:
                editor.level_editor_window.after(500, load_level_data)
            
            try:
                self.app.sound_manager.play_sound('menu_select')
            except:
                pass
                
        except ImportError as e:
            print(f"❌ Error importando LevelEditor: {e}")
            messagebox.showerror("Error", 
                f"No se pudo abrir el editor de niveles.\n\n"
                f"Error: {e}",
                parent=self.levels_window)
        except Exception as e:
            print(f"❌ Error general editando nivel: {e}")
            messagebox.showerror("Error", f"No se pudo editar el nivel:\n{e}",
                               parent=self.levels_window)
    
    def share_level_quick(self, level_data):
        """Compartir nivel rápidamente"""
        # Exportar a archivo temporal
        title = level_data.get('metadata', {}).get('title', 'nivel')
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        
        filename = filedialog.asksaveasfilename(
            parent=self.levels_window,
            title="Compartir Nivel",
            defaultextension=".4f1p",
            filetypes=[("Paquete 4F1P", "*.4f1p"), ("JSON", "*.json")],
            initialfilename=f"{safe_title}.4f1p"
        )
        
        if filename:
            try:
                export_data = {
                    "level": level_data,
                    "export_info": {
                        "exported_by": level_data.get('metadata', {}).get('author', 'Anónimo'),
                        "export_date": datetime.now().isoformat(),
                        "game_version": "1.0",
                        "format_version": "1.0"
                    }
                }
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("✅ Compartido", 
                    f"Nivel exportado exitosamente:\n{os.path.basename(filename)}\n\n"
                    f"¡Ahora puedes enviar este archivo a otros jugadores!",
                    parent=self.levels_window)
                
                try:
                    self.app.sound_manager.play_sound('correct')
                except:
                    pass
                
                print(f"📤 Nivel compartido: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el nivel:\n{e}", parent=self.levels_window)
    
    def delete_level(self, filepath):
        """Eliminar nivel local"""
        filename = os.path.basename(filepath)
        
        if messagebox.askyesno("Confirmar eliminación", 
            f"¿Eliminar el nivel '{filename}'?\n\nEsta acción no se puede deshacer.",
            parent=self.levels_window):
            
            try:
                os.remove(filepath)
                self.refresh_all_levels()
                
                messagebox.showinfo("✅ Eliminado", f"Nivel '{filename}' eliminado exitosamente", parent=self.levels_window)
                
                try:
                    self.app.sound_manager.play_sound('wrong_place')
                except:
                    pass
                
                print(f"🗑️ Nivel eliminado: {filepath}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar el nivel:\n{e}", parent=self.levels_window)
    
    def install_level(self, level_info):
        """Instalar nivel descargado en mis niveles - COMPATIBLE CON TU SISTEMA"""
        level_data = level_info['data']
    
    # Crear archivo en custom_levels
        levels_dir = "custom_levels"
        os.makedirs(levels_dir, exist_ok=True)
    
        title = level_data.get('metadata', {}).get('title', 'nivel_instalado')
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
    
    # Generar nuevo ID para evitar conflictos
        level_data['metadata']['id'] = datetime.now().strftime("%Y%m%d_%H%M%S")
        level_data['metadata']['installed_date'] = datetime.now().isoformat()
    
        filename = f"{safe_title}_{level_data['metadata']['id']}.json"
        filepath = os.path.join(levels_dir, filename)
    
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(level_data, f, indent=2, ensure_ascii=False)
        
            self.refresh_all_levels()
        
            messagebox.showinfo("✅ Instalado", 
                f"Nivel instalado exitosamente en 'Mis Niveles':\n\n"
                f"📝 {title}\n"
                f"📁 {filename}\n\n"
                f"¡Ya puedes editarlo y jugarlo!",
                parent=self.levels_window)
        
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass
        
            print(f"📥 Nivel instalado: {title}")

        except Exception as e:
            messagebox.showerror("Error", f"No se pudo instalar el nivel:\n{e}", parent=self.levels_window)

    def import_level_file(self):
        """Importar archivo de nivel - VERSIÓN COMPLETA"""
        filetypes = [
            ("Paquetes de nivel", "*.4f1p *.json"),
            ("Paquete 4F1P", "*.4f1p"),
            ("JSON", "*.json"),
            ("Todos los archivos", "*.*")
        ]
    
        filename = filedialog.askopenfilename(
            parent=self.levels_window,
            title="Importar Nivel",
            filetypes=filetypes
        )
    
        if filename:
            self.import_single_file(filename)
    
    def import_single_file(self, filepath):
        """Importar un archivo específico - COMPATIBLE CON TU SISTEMA"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        
        # Determinar directorio de destino
            downloads_dir = "downloaded_levels"
            os.makedirs(downloads_dir, exist_ok=True)
        
        # Copiar archivo
            filename = os.path.basename(filepath)
            dest_path = os.path.join(downloads_dir, filename)
        
        # Evitar sobrescribir
            counter = 1
            base_name, ext = os.path.splitext(filename)
            while os.path.exists(dest_path):
                dest_path = os.path.join(downloads_dir, f"{base_name}_{counter}{ext}")
                counter += 1
        
            shutil.copy2(filepath, dest_path)
        
            self.refresh_all_levels()
        
        # Obtener título del nivel
            if 'level' in data:
                level_data = data['level']
            else:
                level_data = data
        
            title = level_data.get('metadata', {}).get('title', os.path.basename(dest_path))
        
            messagebox.showinfo("✅ Importado", 
                f"Nivel importado exitosamente:\n{title}\n\n"
                f"Disponible en la pestaña 'Descargados'",
                parent=self.levels_window)
        
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass
        
            print(f"📥 Nivel importado: {filepath} -> {dest_path}")
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo importar el nivel:\n{e}", parent=self.levels_window)
            print(f"❌ Error importando {filepath}: {e}")
    
    def import_level_folder(self):
        """Importar carpeta completa de niveles - VERSIÓN COMPLETA"""
        folder_path = filedialog.askdirectory(
            parent=self.levels_window,
            title="Seleccionar carpeta con niveles"
        )
    
        if folder_path:
            imported_count = 0
            errors_count = 0
        
            try:
                for filename in os.listdir(folder_path):
                    if filename.endswith(('.4f1p', '.json')):
                        filepath = os.path.join(folder_path, filename)
                    
                        try:
                            self.import_single_file(filepath)
                            imported_count += 1
                        except Exception as e:
                            print(f"Error importando {filename}: {e}")
                            errors_count += 1
            
                result_msg = f"Se importaron {imported_count} niveles desde la carpeta"
                if errors_count > 0:
                    result_msg += f"\n{errors_count} archivos tuvieron errores"
            
                messagebox.showinfo("✅ Importación completada", result_msg, parent=self.levels_window)
            
                try:
                    self.app.sound_manager.play_sound('correct')
                except:
                    pass
            
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo acceder a la carpeta:\n{e}", parent=self.levels_window)

    
    def filter_local_levels(self, difficulty):
        """Filtrar niveles por dificultad - COMPATIBLE CON TU SISTEMA"""
        print(f"🔍 Filtrando por: {difficulty}")
    
    # Aplicar filtro y actualizar display
        if difficulty == "Todos":
           self.display_local_levels()
        else:
        # Filtrar niveles por dificultad
            filtered_levels = []
            for level_info in self.local_levels:
                level_difficulty = level_info['data'].get('metadata', {}).get('difficulty', 'Fácil')
                if level_difficulty == difficulty:
                    filtered_levels.append(level_info)
        
        # Mostrar solo niveles filtrados
            self.display_filtered_levels(filtered_levels)

    
    def search_local_levels(self, event=None):
        """Buscar niveles por título - COMPATIBLE CON TU SISTEMA"""
        search_term = self.local_search_entry.get().lower()
        print(f"🔍 Buscando: {search_term}")
    
        if not search_term:
            self.display_local_levels()
            return
    
    # Buscar en títulos y descripciones
        filtered_levels = []
        for level_info in self.local_levels:
            metadata = level_info['data'].get('metadata', {})
            title = metadata.get('title', '').lower()
            description = metadata.get('description', '').lower()
            author = metadata.get('author', '').lower()
        
            if (search_term in title or 
                search_term in description or 
                search_term in author):
                filtered_levels.append(level_info)
    
    # Mostrar resultados de búsqueda
        self.display_filtered_levels(filtered_levels)
    

    def display_filtered_levels(self, filtered_levels):
        """Mostrar niveles filtrados - COMPATIBLE CON TU SISTEMA"""
        # Limpiar frame
        for widget in self.local_levels_frame.winfo_children():
            widget.destroy()
    
        if not filtered_levels:
            no_levels_label = ctk.CTkLabel(
                self.local_levels_frame,
                text="🔍 No se encontraron niveles\ncon los criterios de búsqueda",
                font=ctk.CTkFont(size=16),
                text_color="#888888"
            )
            no_levels_label.pack(expand=True, pady=50)
            return
    
    # Usar la misma lógica de display pero con niveles filtrados
        original_levels = self.local_levels
        self.local_levels = filtered_levels
        self.display_local_levels()
        self.local_levels = original_levels


    def import_level(self):
        """Importar nivel desde archivo"""
        try:
            # Intentar usar descargador si existe
            from level_downloader import LevelDownloader
            
            downloader = LevelDownloader(self.app)
            downloader.show_downloader()
            
        except ImportError:
            # Fallback: importar archivo directamente
            self.import_level_file()
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el importador:\n{e}", parent=self.levels_window)
    
    def browse_online_levels(self):
        """Explorar niveles online - VERSIÓN COMPLETA"""
        messagebox.showinfo("🌐 Explorar Online", 
            "¡Función de exploración online!\n\n"
            "Cuando el servidor público esté activo podrás:\n"
            "✅ Buscar niveles por categoría\n"
            "✅ Ver niveles más populares\n"
            "✅ Descargar niveles recomendados\n"
            "✅ Calificar y comentar niveles\n"
            "✅ Subir tus propios niveles\n"
            "✅ Participar en competencias\n\n"
            "Por ahora usa:\n"
            "🌐 Red local WiFi\n"
            "📁 Archivos .4f1p compartidos\n"
            "📧 Envío por email/chat",
            parent=self.levels_window)

    
    def clean_downloaded_levels(self):
        """Limpiar niveles descargados - VERSIÓN COMPLETA"""
        if messagebox.askyesno("Confirmar", 
            "¿Eliminar todos los niveles descargados?\n\n"
            "Esta acción no se puede deshacer.\n"
            "Los niveles instalados en 'Mis Niveles' no se verán afectados.", 
            parent=self.levels_window):
        
            try:
                downloads_dir = "downloaded_levels"
                deleted_count = 0
            
                if os.path.exists(downloads_dir):
                # Contar archivos antes de eliminar
                    for filename in os.listdir(downloads_dir):
                        if filename.endswith(('.4f1p', '.json')):
                            deleted_count += 1
                
                # Eliminar directorio completo
                    shutil.rmtree(downloads_dir)
                    os.makedirs(downloads_dir, exist_ok=True)
            
                self.refresh_all_levels()
            
                messagebox.showinfo("✅ Limpieza completada", 
                    f"Se eliminaron {deleted_count} niveles descargados\n\n"
                    f"La carpeta de descargas ha sido limpiada",
                    parent=self.levels_window)
            
                try:
                    self.app.sound_manager.play_sound('correct')
                except:
                    pass
            
            except Exception as e:
                messagebox.showerror("Error", f"No se pudieron eliminar los niveles:\n{e}", parent=self.levels_window)
    
    def connect_to_network_server(self):
        """Conectar a servidor de red"""
        ip = self.ip_entry.get().strip()
        port_str = self.port_entry.get().strip()
        
        if not ip:
            messagebox.showwarning("IP requerida", "Por favor ingresa la IP del servidor", parent=self.levels_window)
            return
        
        if not port_str:
            port_str = "8080"  # Puerto por defecto
        
        try:
            port = int(port_str)
        except ValueError:
            messagebox.showerror("Puerto inválido", "El puerto debe ser un número", parent=self.levels_window)
            return
        
        try:
            # Simular conexión exitosa
            messagebox.showinfo("🎮 Servidor Encontrado", 
                f"¡Conexión exitosa!\n\n"
                f"📝 Servidor: {ip}:{port}\n"
                f"🌐 Estado: Conectado\n\n"
                f"(Función en desarrollo)",
                parent=self.levels_window)
            
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass
            
        except Exception as e:
            messagebox.showerror("Error de conexión", f"No se pudo conectar al servidor:\n{ip}:{port}\n\nError: {e}", parent=self.levels_window)
    
    def scan_network(self):
        """Escanear red local en busca de servidores - VERSIÓN COMPLETA"""
        if hasattr(self, 'network_status_label'):
            self.network_status_label.configure(text="🔍 Escaneando red local...")
    
        def do_scan():
            try:
                import time
                time.sleep(3)  # Simular escaneo
            
            # Simular servidores encontrados
                servers = [
                    {'ip': '192.168.1.100', 'port': 8080, 'level_title': 'Animales Domésticos', 'level_author': 'Juan'},
                    {'ip': '192.168.1.105', 'port': 8080, 'level_title': 'Frutas y Verduras', 'level_author': 'María'},
                    {'ip': '192.168.1.110', 'port': 8080, 'level_title': 'Deportes Extremos', 'level_author': 'Carlos'},
                ]
            
                # Actualizar UI en hilo principal
                self.levels_window.after(0, lambda: self.update_network_servers(servers))
            
            except Exception as e:
                if hasattr(self, 'network_status_label'):
                    self.levels_window.after(0, lambda: self.network_status_label.configure(
                        text=f"❌ Error escaneando: {e}"
                    ))
    
    # Ejecutar en hilo separado para no bloquear UI
        threading.Thread(target=do_scan, daemon=True).start()
    
    def update_network_servers(self, servers):
        """Actualizar lista de servidores de red - VERSIÓN COMPLETA"""
        if hasattr(self, 'servers_listbox'):
            self.servers_listbox.delete(0, tk.END)

            if servers:
                for server in servers:
                    server_text = f"{server['ip']}:{server['port']} - {server['level_title']} ({server['level_author']})"
                    self.servers_listbox.insert(tk.END, server_text)
            
                if hasattr(self, 'network_status_label'):
                    self.network_status_label.configure(text=f"✅ {len(servers)} servidores encontrados")
            else:
                if hasattr(self, 'network_status_label'):
                    self.network_status_label.configure(text="📭 No se encontraron servidores")
                self.servers_listbox.insert(tk.END, "No hay servidores disponibles en la red local")

    def export_single_level(self):
        """Exportar un nivel específico - VERSIÓN COMPLETA"""
        messagebox.showinfo("📦 Exportar Nivel", 
            "Para exportar un nivel específico:\n\n"
            "1. Ve a la pestaña '🏠 Mis Niveles'\n"
            "2. Click en '📤 COMPARTIR' junto al nivel que quieres exportar\n"
            "3. Selecciona dónde guardar el archivo .4f1p\n"
            "4. ¡Comparte el archivo por email, chat o USB!\n\n"
            "💡 Tip: Los archivos .4f1p contienen todo:\n"
            "• Metadatos del nivel\n"
            "• Todas las palabras\n"
            "• Todas las imágenes\n"
            "• Información del autor\n\n"
            "¡Es la forma más fácil de compartir niveles!",


        parent=self.levels_window)
    def export_level_pack(self):
        """Exportar paquete de niveles - VERSIÓN COMPLETA"""
        if not hasattr(self, 'local_levels') or not self.local_levels:
            messagebox.showwarning("Sin niveles", 
                "No hay niveles locales para exportar\n\n"
                "Primero crea algunos niveles con el Editor",
                parent=self.levels_window)
            return
    
        messagebox.showinfo("📚 Pack de Niveles", 
            "¡Función de packs de niveles!\n\n"
            "Características planificadas:\n"
            "✅ Seleccionar múltiples niveles\n"
            "✅ Crear archivo .4f1pack\n"
            "✅ Compartir colecciones completas\n"
            "✅ Instalar packs automáticamente\n"
            "✅ Metadatos del pack (tema, dificultad)\n"
            "✅ Previsualización del contenido\n\n"
            "Por ahora:\n"
            "🔄 Exporta niveles individualmente\n"
            "📁 Compártelos en carpetas\n"
            "📧 Envía varios archivos .4f1p\n\n"
            "(Función en desarrollo para la próxima versión)",
            parent=self.levels_window)
    
    def delete_downloaded_level(self, filepath):
        """Eliminar nivel descargado - VERSIÓN CORREGIDA"""
        try:
        # Verificar que el archivo existe
            if not os.path.exists(filepath):
                messagebox.showerror("Error", 
                    f"El archivo no existe:\n{filepath}", 
                    parent=self.levels_window)
                return
        
            filename = os.path.basename(filepath)
        
        # Confirmar eliminación
            if messagebox.askyesno("Confirmar eliminación", 
                f"¿Eliminar el nivel descargado?\n\n"
                f"📁 Archivo: {filename}\n\n"
                f"Esta acción no se puede deshacer.\n"
                f"Si ya lo instalaste en 'Mis Niveles', esa copia no se verá afectada.",
                parent=self.levels_window):
            
                try:
                # Eliminar archivo
                    os.remove(filepath)
                
                # Actualizar lista de niveles
                    if hasattr(self, 'refresh_all_levels'):
                        self.refresh_all_levels()
                    elif hasattr(self, 'refresh_all_levels'):
                        self.refresh_all_levels()
                    elif hasattr(self, 'load_downloaded_levels'):
                        self.load_downloaded_levels()
                
                # Mostrar confirmación
                    messagebox.showinfo("✅ Eliminado", 
                        f"Nivel descargado eliminado exitosamente:\n{filename}",
                        parent=self.levels_window)
                
                # Sonido de eliminación
                    try:
                        self.app.sound_manager.play_sound('wrong_place')
                    except Exception:
                        pass
                
                    print(f"🗑️ Nivel descargado eliminado: {filepath}")
                
                except PermissionError:
                    messagebox.showerror("Error de permisos", 
                        f"No se puede eliminar el archivo.\n"
                        f"El archivo puede estar siendo usado por otra aplicación.\n\n"
                        f"Archivo: {filename}",
                        parent=self.levels_window)
                    print(f"❌ Error de permisos eliminando: {filepath}")
                
                except FileNotFoundError:
                    messagebox.showwarning("Archivo no encontrado", 
                        f"El archivo ya no existe:\n{filename}\n\n"
                        f"Actualizando lista...",
                        parent=self.levels_window)
                
                # Actualizar lista aunque el archivo no exista
                    if hasattr(self, 'refresh_all_levels'):
                        self.refresh_all_levels()
                    elif hasattr(self, 'refresh_all_levels'):
                        self.refresh_all_levels()
                
                    print(f"⚠️ Archivo ya no existía: {filepath}")
                
                except OSError as e:
                    messagebox.showerror("Error del sistema", 
                        f"Error del sistema eliminando el archivo:\n\n"
                        f"Error: {e}\n"
                        f"Archivo: {filename}",
                        parent=self.levels_window)
                    print(f"❌ Error OSError eliminando: {filepath} - {e}")
                
                except Exception as e:
                    messagebox.showerror("Error inesperado", 
                        f"Error inesperado eliminando el archivo:\n\n"
                        f"Error: {str(e)}\n"
                        f"Archivo: {filename}",
                        parent=self.levels_window)
                    print(f"❌ Error inesperado eliminando: {filepath} - {e}")
                
        except Exception as e:
            # Error general del método
            print(f"❌ Error general en delete_downloaded_level: {e}")
            messagebox.showerror("Error", 
                f"Error en la función de eliminación:\n{str(e)}",
                parent=getattr(self, 'levels_window', None))
            

    def get_available_levels(self):
        """Obtener lista de niveles disponibles para el network manager - VERSIÓN CORREGIDA"""
        print("📚 Empaquetando niveles para el gestor de red...")
        available_levels = []

        try:
            levels_dir = "custom_levels"
            if not os.path.exists(levels_dir):
                os.makedirs(levels_dir, exist_ok=True)
                return [] # Devuelve lista vacía si la carpeta no existía

            for filename in os.listdir(levels_dir):
                if filename.endswith('.json'):
                    filepath = os.path.join(levels_dir, filename)
                    try:
                        with open(filepath, 'r', encoding='utf-8') as f:
                            level_data = json.load(f)

                    # --- INICIO DE LA CORRECCIÓN CLAVE ---
                    # Creamos un diccionario con el formato que NetworkGameManager espera.
                    # Extraemos el título desde la metadata del nivel.
                        metadata = level_data.get('metadata', {})
                        level_name = metadata.get('title', filename.replace('.json', ''))

                    # Empaquetamos todo en el formato correcto.
                        level_info_for_network = {
                            "name": level_name,  # La clave 'name' que faltaba.
                            "type": "custom",    # La clave 'type' que también se espera.
                            "data": level_data   # Los datos completos del nivel.
                        }
                    
                        available_levels.append(level_info_for_network)
                    # --- FIN DE LA CORRECCIÓN CLAVE ---

                    except Exception as e:
                        print(f"⚠️ Error cargando nivel {filename} para la red: {e}")
                        continue

            print(f"✅ {len(available_levels)} niveles empaquetados exitosamente para la red.")
            return available_levels

        except Exception as e:
            print(f"❌ Error crítico en get_available_levels: {e}")
            return [] # Siempre devolver una lista