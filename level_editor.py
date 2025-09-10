#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import json
import os
from datetime import datetime
import shutil
from PIL import Image, ImageTk
import base64
import io

class LevelEditor:
    def __init__(self, parent_app):
        self.word_ui_dirty = False # Para rastrear cambios en la palabra actual en la UI
        self.app = parent_app
        self.current_level = {
            "metadata": {
                "title": "",
                "author": "",
                "description": "",
                "difficulty": "Fácil",
                "created_date": "",
                "version": "1.0",
                "id": ""
            },
            "words": []
        }
        self.current_word_index = 0
        self.image_paths = [None, None, None, None]
        self.level_editor_window = None
        self.image_references = [None, None, None, None]
        self.image_status_labels = []
        self.image_labels = []
        self.image_buttons = []
        

        
    def show_editor(self):
        """Mostrar ventana del editor - VERSIÓN VENTANA ÚNICA"""
        print("🛠️ Abriendo Editor de Niveles...")
        
        # IMPORTANTE: Verificar si la ventana ya existe y está abierta
        if self.level_editor_window is not None:
            try:
                # Verificar si la ventana aún existe
                if self.level_editor_window.winfo_exists():
                    print("🛠️ Ventana ya existe, enfocando...")
                    # Traer ventana al frente
                    self.level_editor_window.lift()
                    self.level_editor_window.focus_force()
                    self.level_editor_window.attributes('-topmost', True)
                    # Quitar topmost después de un momento
                    self.level_editor_window.after(100, lambda: self.level_editor_window.attributes('-topmost', False))
                    
                    # Mostrar mensaje al usuario
                    self.show_already_open_message()
                    return
                else:
                    # La ventana fue cerrada, limpiar referencia
                    print("🛠️ Ventana fue cerrada, limpiando referencia...")
                    self.level_editor_window = None
            except Exception as e:
                print(f"⚠️ Error verificando ventana: {e}")
                self.level_editor_window = None

        # Crear nueva ventana solo si no existe
        print("🛠️ Creando nueva ventana del editor...")
        self._create_editor_window()
    
    def show_already_open_message(self):
        """Mostrar mensaje de que la ventana ya está abierta"""
        if self.level_editor_window:
            temp_label = ctk.CTkLabel(
                self.level_editor_window,
                text="ℹ️ El editor ya está abierto",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#2196F3",
                fg_color="#1a1a1a"
            )
            temp_label.place(relx=0.5, rely=0.95, anchor="center")
            self.level_editor_window.after(2000, temp_label.destroy)
        
        try:
            self.app.sound_manager.play_sound('menu_select')
        except:
            pass



    def center_window(self):
        """Centrar la ventana en la pantalla"""
        if self.level_editor_window:
            self.level_editor_window.update_idletasks()
            
            # Obtener dimensiones de la ventana
            window_width = self.level_editor_window.winfo_width()
            window_height = self.level_editor_window.winfo_height()
            
            # Obtener dimensiones de la pantalla
            screen_width = self.level_editor_window.winfo_screenwidth()
            screen_height = self.level_editor_window.winfo_screenheight()
            
            # Calcular posición centrada
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            # Aplicar posición
            self.level_editor_window.geometry(f"{window_width}x{window_height}+{x}+{y}")


    def _create_editor_window(self):

        self.level_editor_window = ctk.CTkToplevel(self.app.root)
        self.level_editor_window.title("🛠️ Editor de Niveles 1 vs 1 - 4 Fotos 1 Palabra")
        self.level_editor_window.geometry("1200x950")
        self.level_editor_window.resizable(True, True)
        self.level_editor_window.protocol("WM_DELETE_WINDOW", self.close_editor_safely)
        self.level_editor_window.attributes('-topmost', True)
        self.level_editor_window.after(500, lambda: self.level_editor_window.attributes('-topmost', False))

    # Grid principal
        self.level_editor_window.grid_rowconfigure(0, weight=1)
        self.level_editor_window.grid_columnconfigure(0, weight=1)

        main_frame = ctk.CTkFrame(self.level_editor_window)
        main_frame.grid(row=0, column=0, sticky="nsew")
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=0)
        main_frame.grid_columnconfigure(0, weight=1)

    # Frame de contenido
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=(10, 5))
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=3)
        content_frame.grid_rowconfigure(0, weight=1)

    # Panel izquierdo
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.grid(row=0, column=0, sticky="nsew", padx=(10, 5), pady=10)
        self.create_level_info_panel(left_panel)

        separator = ctk.CTkFrame(left_panel, height=2, fg_color=("#d0d0d0", "#404040"))
        separator.pack(fill="x", padx=20, pady=10)

        self.create_words_list_panel(left_panel)

    # Panel central
        center_panel = ctk.CTkFrame(content_frame)
        center_panel.grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=10)
        self.create_word_editor_panel(center_panel)

    # Frame de botones
        actions_frame = ctk.CTkFrame(main_frame)
        actions_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5, 10))
        self.create_action_buttons(actions_frame)

    # Inicializar
        self.reset_level()

        print("✅ Editor de niveles abierto con layout completo")



    def close_editor_safely(self):
        if self.word_ui_dirty or self.has_unsaved_changes():
            result = messagebox.askyesnocancel(
                "Cambios sin guardar",
                "¿Deseas guardar los cambios antes de cerrar?",
                parent=self.level_editor_window
            )
            
            if result is None:
                return
            elif result:
                self.save_level()
        
        self.cleanup_editor_data()
        
        if self.level_editor_window:
            try:
                self.level_editor_window.destroy()
            except:
                pass
            finally:
                self.level_editor_window = None
        
        try:
            self.app.sound_manager.play_sound('menu_select')
        except:
            pass
        
        print("✅ Editor cerrado correctamente")
    

    def has_unsaved_changes(self):
        if self.current_level["words"]:
            return True
        
        if self.current_level["metadata"].get("title"):
            return True
        
        return False

    
    def cleanup_editor_data(self):
        try:
            for i in range(len(self.image_references)):
                self.image_references[i] = None
                self.image_paths[i] = None
            
            self.image_status_labels.clear()
            self.image_labels.clear()
            self.image_buttons.clear()
            
            self.current_word_index = 0
            self.word_ui_dirty = False
            
            print("🧹 Datos del editor limpiados")
        except Exception as e:
            print(f"⚠️ Error limpiando datos: {e}")



    def initialize_editor_data(self):
        """Inicializar datos del editor"""
        try:
            # Resetear nivel si no existe
            if not hasattr(self, 'current_level') or not self.current_level:
                if hasattr(self, 'reset_level'):
                    self.reset_level()
                else:
                    print("⚠️ reset_level method not found, cannot initialize current_level")
                    self.current_level = {} # Basic initialization

            # Inicializar variables de UI
            self.current_word_index = 0
            self.image_paths = [None, None, None, None]
            self.image_references = [None, None, None, None] # PhotoImage objects for Tkinter
            self.word_ui_dirty = False

            # Cargar datos (assuming these methods exist)
            if hasattr(self, 'load_current_word'):
                self.load_current_word()
            else:
                print("⚠️ load_current_word method not found")
            if hasattr(self, 'update_words_list'):
                self.update_words_list()
            else:
                print("⚠️ update_words_list method not found")
            if hasattr(self, 'update_stats'):
                self.update_stats()
            else:
                print("⚠️ update_stats method not found")
            if hasattr(self, 'update_navigation_buttons'):
                self.update_navigation_buttons()
            else:
                print("⚠️ update_navigation_buttons method not found")


            print("✅ Datos del editor inicializados")

        except Exception as e:
            print(f"❌ Error inicializando datos: {e}")


    def create_level_info_panel(self, parent_frame):
        print(f"Placeholder: create_level_info_panel in {parent_frame}")
        # Example: ctk.CTkLabel(parent_frame, text="Level Info Panel").pack()
        pass

    def create_words_list_panel(self, parent_frame):
        print(f"Placeholder: create_words_list_panel in {parent_frame}")
        pass

    def create_word_editor_panel(self, parent_frame):
        print(f"Placeholder: create_word_editor_panel in {parent_frame}")
        pass

    def update_words_list(self):
        print("Placeholder: update_words_list")
        pass

    def update_stats(self):
        print("Placeholder: update_stats")
        pass

    def update_navigation_buttons(self):
        print("Placeholder: update_navigation_buttons")
        pass

    def create_words_list_panel(self, parent):
        ctk.CTkLabel(
            parent,
            text="📝 PALABRAS/RONDAS",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
    
        list_frame = ctk.CTkFrame(parent)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
        self.words_listbox = tk.Listbox(
            list_frame,
            bg="#2b2b2b",
            fg="white",
            selectbackground="#1f538d",
            font=("Arial", 11),
            height=8,
            width=25
        )
        self.words_listbox.pack(fill="both", expand=True, padx=5, pady=5)
        self.words_listbox.bind("<Double-Button-1>", self.select_word_from_list)
    
        delete_btn = ctk.CTkButton(
            list_frame,
            text="🗑️ ELIMINAR PALABRA",
            command=self.delete_current_word,
            width=180,
            height=30,
            fg_color="#FF5722",
            font=ctk.CTkFont(size=10)
        )
        delete_btn.pack(pady=5)
    
        self.rounds_info_label = ctk.CTkLabel(
            parent,
            text="Total de rondas: 0",
            font=ctk.CTkFont(size=11, weight="bold"),
            text_color=("#4CAF50", "#8BC34A")
        )
        self.rounds_info_label.pack(pady=(5, 10))

    def open_file_browser(self):
        """Abrir explorador de archivos para seleccionar múltiples imágenes"""
        print("📂 Abriendo explorador de archivos...")
        
        try:
            # Hacer la ventana temporal topmost
            if self.level_editor_window:
                self.level_editor_window.attributes('-topmost', True)
                self.level_editor_window.update()
            
            filetypes = [
                ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
                ("PNG", "*.png"),
                ("JPEG", "*.jpg *.jpeg"),
                ("Todos los archivos", "*.*")
            ]
            
            # Abrir diálogo para seleccionar múltiples archivos
            filenames = filedialog.askopenfilenames(
                parent=self.level_editor_window,
                title="Seleccionar imágenes (máximo 4)",
                filetypes=filetypes,
                initialdir=os.path.expanduser("~/Pictures")
            )
            
            # Restaurar ventana
            if self.level_editor_window:
                self.level_editor_window.attributes('-topmost', False)
                self.level_editor_window.lift()
                self.level_editor_window.focus_force()
            
            if not filenames:
                print("❌ No se seleccionaron archivos")
                return
            
            # Cargar hasta 4 imágenes
            for i, filename in enumerate(filenames[:4]):
                # Buscar el primer slot vacío
                empty_slot = -1
                for j in range(4):
                    if self.image_paths[j] is None:
                        empty_slot = j
                        break
                
                if empty_slot != -1:
                    self.load_image_to_slot(filename, empty_slot)
                else:
                    # Si no hay slots vacíos, reemplazar desde el principio
                    self.load_image_to_slot(filename, i)
            
            self.show_status_message(f"📂 {len(filenames[:4])} imágenes cargadas")
            
        except Exception as e:
            print(f"❌ Error abriendo explorador: {e}")
            messagebox.showerror("Error", f"Error abriendo explorador:\n{str(e)}", parent=self.level_editor_window)
    
    def paste_image_path(self):
        """Pegar ruta de imagen desde el portapapeles"""
        print("📋 Intentando pegar ruta de imagen...")
        
        try:
            # Obtener contenido del portapapeles
            clipboard_content = self.level_editor_window.clipboard_get()
            clipboard_content = clipboard_content.strip()
            
            if not clipboard_content:
                messagebox.showwarning("Portapapeles vacío", "No hay ninguna ruta en el portapapeles", parent=self.level_editor_window)
                return
            
            # Verificar si es una ruta válida
            if not os.path.exists(clipboard_content):
                messagebox.showwarning("Ruta inválida", f"La ruta no existe:\n{clipboard_content}", parent=self.level_editor_window)
                return
            
            # Verificar si es un archivo de imagen
            if not os.path.isfile(clipboard_content):
                messagebox.showwarning("No es archivo", "La ruta debe apuntar a un archivo de imagen", parent=self.level_editor_window)
                return
            
            # Intentar abrir como imagen
            try:
                test_img = Image.open(clipboard_content)
                test_img.verify()
            except:
                messagebox.showwarning("Archivo inválido", "El archivo no es una imagen válida", parent=self.level_editor_window)
                return
            
            # Buscar primer slot vacío
            empty_slot = -1
            for i in range(4):
                if self.image_paths[i] is None:
                    empty_slot = i
                    break
            
            if empty_slot == -1:
                # Preguntar si reemplazar
                result = messagebox.askyesno("Slots llenos", "Todos los slots están ocupados.\n¿Reemplazar imagen 1?", parent=self.level_editor_window)
                if result:
                    empty_slot = 0
                else:
                    return
            
            # Cargar imagen
            self.load_image_to_slot(clipboard_content, empty_slot)
            
            self.show_status_message(f"📋 Imagen pegada en slot {empty_slot + 1}")
            
        except tk.TclError:
            messagebox.showwarning("Error", "No se pudo acceder al portapapeles", parent=self.level_editor_window)
        except Exception as e:
            print(f"❌ Error pegando ruta: {e}")
            messagebox.showerror("Error", f"Error pegando ruta:\n{str(e)}", parent=self.level_editor_window)
    
    def select_image_for_slot(self, slot_index):
        """Seleccionar imagen para un slot específico"""
        print(f"📁 Seleccionando imagen para slot {slot_index + 1}...")
        
        try:
            # Usar el método existente select_image
            self.select_image(slot_index)
        except Exception as e:
            print(f"❌ Error seleccionando imagen: {e}")
            messagebox.showerror("Error", f"Error seleccionando imagen:\n{str(e)}", parent=self.level_editor_window)
    
    def load_image_to_slot(self, filepath, slot_index):
        """Cargar imagen en un slot específico con manejo robusto"""
        print(f"🎯 Cargando imagen en slot {slot_index + 1}: {os.path.basename(filepath)}")
        
        try:
            # Verificar que el archivo existe
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"El archivo no existe: {filepath}")
            
            # Abrir y procesar imagen
            with Image.open(filepath) as original_image:
                # Convertir a RGB si es necesario
                if original_image.mode not in ('RGB', 'RGBA'):
                    original_image = original_image.convert('RGB')
                
                # Crear copia para evitar problemas
                image_copy = original_image.copy()
                
                # Redimensionar manteniendo proporción
                display_size = (180, 135)
                image_copy.thumbnail(display_size, Image.Resampling.LANCZOS)
                
                # Crear imagen para CustomTkinter
                ctk_image = ctk.CTkImage(
                    light_image=image_copy,
                    dark_image=image_copy,
                    size=image_copy.size
                )
                
                # Actualizar la interfaz
                self.image_labels[slot_index].configure(
                    image=ctk_image,
                    text="",
                    fg_color="transparent"
                )
                
                # IMPORTANTE: Guardar referencia
                self.image_references[slot_index] = ctk_image
                
                # Guardar ruta
                self.image_paths[slot_index] = filepath
                
                # Actualizar botón
                filename_short = os.path.basename(filepath)
                if len(filename_short) > 12:
                    filename_short = filename_short[:9] + "..."
                
                self.image_buttons[slot_index].configure(
                    text=f"✅ {filename_short}",
                    fg_color="#4CAF50",
                    hover_color="#45a049"
                )
                
                # Actualizar indicador de estado
                if hasattr(self, 'image_status_labels') and slot_index < len(self.image_status_labels):
                    self.image_status_labels[slot_index].configure(
                        text="✅",
                        text_color="#4CAF50"
                    )
                
                if original_image: # Si la carga fue exitosa
                    self.image_paths[slot_index] = filepath # Esta es la ruta de archivo real
                    self.word_ui_dirty = True
                print(f"✅ Imagen cargada exitosamente en slot {slot_index + 1}")
                
                # Sonido de éxito
                try:
                    self.app.sound_manager.play_sound('correct')
                except:
                    pass
                
        except Exception as e:
            print(f"❌ Error cargando imagen en slot {slot_index + 1}: {e}")
            messagebox.showerror("Error", f"Error cargando imagen:\n{str(e)}", parent=self.level_editor_window)
            
            # Limpiar el slot en caso de error
            self.remove_image(slot_index)
    
    def setup_drag_drop(self, widget, slot_index):
        """Configurar drag & drop para un widget"""
        try:
            # Configurar eventos de arrastrar y soltar
            widget.drop_target_register(tk.DND_FILES)
            widget.dnd_bind('<<Drop>>', lambda e: self.handle_drop(e, slot_index))
            
            # Visual feedback
            widget.bind("<DragEnter>", lambda e: widget.configure(fg_color=("#d0d0d0", "#4b4b4b")))
            widget.bind("<DragLeave>", lambda e: widget.configure(fg_color="transparent"))
            
        except:
            # Si drag & drop no está disponible, solo configurar visual feedback
            print("⚠️ Drag & drop no disponible en este sistema")
            
            # Alternativa: hacer todo el frame clickeable
            def on_click(event):
                self.select_image_for_slot(slot_index)
            
            widget.bind("<Button-1>", on_click)
            widget.configure(cursor="hand2")
    
    def handle_drop(self, event, slot_index):
        """Manejar archivos arrastrados"""
        try:
            # Obtener archivos arrastrados
            files = event.data.split()
            
            if files:
                # Tomar el primer archivo
                filepath = files[0]
                
                # Limpiar la ruta (quitar llaves si las tiene)
                filepath = filepath.strip('{}')
                
                # Cargar la imagen
                self.load_image_to_slot(filepath, slot_index)
                
        except Exception as e:
            print(f"❌ Error manejando archivo arrastrado: {e}")
            messagebox.showerror("Error", f"Error al procesar archivo arrastrado:\n{str(e)}", parent=self.level_editor_window)
    
    def show_status_message(self, message):
        """Mostrar mensaje de estado temporal"""
        try:
            # Crear label temporal para mostrar mensaje
            if not hasattr(self, 'status_label'):
                self.status_label = ctk.CTkLabel(
                    self.level_editor_window,
                    text="",
                    font=ctk.CTkFont(size=12, weight="bold"),
                    fg_color="#4CAF50",
                    corner_radius=5,
                    text_color="white"
                )
            
            # Mostrar mensaje
            self.status_label.configure(text=f"  {message}  ")
            self.status_label.place(relx=0.5, rely=0.95, anchor="center")
            
            # Ocultar después de 3 segundos
            self.level_editor_window.after(3000, lambda: self.status_label.place_forget())
            
        except Exception as e:
            print(f"⚠️ Error mostrando mensaje de estado: {e}")
    
    def start_custom_level_preview(self, level_data):
        """Iniciar vista previa del nivel personalizado"""
        try:
            # Guardar temporalmente el nivel actual
            temp_level = {
                "metadata": level_data["metadata"].copy(),
                "words": []
            }
            
            # Copiar solo palabras válidas
            for word_data in level_data["words"]:
                if word_data.get("word", "").strip():
                    # Contar imágenes válidas
                    valid_images = sum(1 for img in word_data.get("images", []) if img is not None)
                    if valid_images > 0:
                        temp_level["words"].append(word_data.copy())
            
            if not temp_level["words"]:
                messagebox.showwarning("Sin palabras válidas", 
                    "No hay palabras con imágenes para mostrar en la vista previa", 
                    parent=self.level_editor_window)
                return
            
            # Mostrar información del nivel
            info_msg = f"📋 VISTA PREVIA DEL NIVEL\n\n"
            info_msg += f"Título: {temp_level['metadata'].get('title', 'Sin título')}\n"
            info_msg += f"Autor: {temp_level['metadata'].get('author', 'Anónimo')}\n"
            info_msg += f"Dificultad: {temp_level['metadata'].get('difficulty', 'Fácil')}\n"
            info_msg += f"Palabras: {len(temp_level['words'])}\n\n"
            info_msg += "Cierra esta ventana para continuar editando."
            
            messagebox.showinfo("Vista Previa", info_msg, parent=self.level_editor_window)
            
            # Aquí normalmente se iniciaría el juego con el nivel temporal
            # Por ahora solo mostramos la información
            
        except Exception as e:
            print(f"❌ Error en vista previa: {e}")
            messagebox.showerror("Error", f"Error al mostrar vista previa:\n{str(e)}", parent=self.level_editor_window)















    def add_debug_button(self, parent):
        """Agregar botón de debug para probar funcionalidad"""
        debug_btn = ctk.CTkButton(
            parent,
            text="🔧 DEBUG",
            command=self.run_debug_test,
            width=100,
            height=30,
            fg_color="#9C27B0"
        )
        debug_btn.pack(side="left", padx=10, pady=10)
    
    def run_debug_test(self):
        """Ejecutar pruebas de debug - VERSIÓN MEJORADA"""
        print("🔧 === EJECUTANDO PRUEBAS DE DEBUG MEJORADAS ===")
        
        # Test 1: Verificar componentes
        print(f"🔍 Componentes del editor:")
        print(f"  • Botones de imagen: {len(self.image_buttons)}")
        print(f"  • Labels de imagen: {len(self.image_labels)}")
        print(f"  • Referencias de imagen: {len(self.image_references)}")
        print(f"  • Rutas de imagen: {len(self.image_paths)}")
        print(f"  • Status labels: {len(self.image_status_labels) if hasattr(self, 'image_status_labels') else 'N/A'}")
        
        # Test 2: Verificar estado de cada slot
        print(f"🔍 Estado de slots:")
        for i in range(4):
            has_image = self.image_paths[i] is not None
            has_reference = self.image_references[i] is not None
            button_text = self.image_buttons[i].cget('text') if i < len(self.image_buttons) else 'N/A'
            print(f"  Slot {i+1}: Imagen={has_image}, Ref={has_reference}, Botón='{button_text}'")
        
        # Test 3: Probar funciones de carga
        print("🔍 Probando funciones...")
        
        # Test botón principal de examinar
        print("  • Testing open_file_browser...")
        try:
            # No ejecutar realmente, solo verificar que existe
            if hasattr(self, 'open_file_browser'):
                print("    ✅ open_file_browser existe")
            else:
                print("    ❌ open_file_browser no existe")
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        # Test función de pegar ruta
        print("  • Testing paste_image_path...")
        try:
            if hasattr(self, 'paste_image_path'):
                print("    ✅ paste_image_path existe")
            else:
                print("    ❌ paste_image_path no existe")
        except Exception as e:
            print(f"    ❌ Error: {e}")
        
        # Test 4: Probar carga de imagen de prueba con nuevo sistema
        print("🎨 Creando imagen de prueba con nuevo sistema...")
        try:
            success = self.create_advanced_test_image()
            print(f"  • Resultado: {'✅ Éxito' if success else '❌ Falló'}")
        except Exception as e:
            print(f"  • ❌ Error: {e}")
        
        # Test 5: Verificar ventana padre
        print(f"🔍 Ventana del editor:")
        if self.level_editor_window:
            try:
                exists = self.level_editor_window.winfo_exists()
                title = self.level_editor_window.title()
                geometry = self.level_editor_window.geometry()
                print(f"  • Existe: {exists}")
                print(f"  • Título: {title}")
                print(f"  • Geometría: {geometry}")
            except Exception as e:
                print(f"  • ❌ Error accediendo a ventana: {e}")
        else:
            print("  • ❌ Ventana no existe")
        
        # Test 6: Verificar directorios
        print(f"🔍 Verificando directorios:")
        test_dirs = [
            os.path.expanduser("~/Pictures"),
            os.path.expanduser("~/Desktop"), 
            os.getcwd()
        ]
        
        for directory in test_dirs:
            exists = os.path.exists(directory)
            readable = False
            if exists:
                try:
                    os.listdir(directory)
                    readable = True
                except:
                    pass
            print(f"  • {directory}: Existe={exists}, Legible={readable}")
        
        # Test 7: Test de filedialog
        print(f"🔍 Test de filedialog:")
        try:
            from tkinter import filedialog
            print("  • filedialog importado correctamente")
            
            # Verificar que podemos crear un diálogo (sin abrirlo)
            print("  • Capacidad de diálogo: Disponible")
        except Exception as e:
            print(f"  • ❌ Error con filedialog: {e}")
        
        print("🔧 === FIN DE PRUEBAS DE DEBUG ===")
        
        # Mostrar resumen en ventana
        self.show_debug_summary()
    
    def create_advanced_test_image(self):
        """Crear imagen de prueba avanzada"""
        try:
            print("🎨 Creando imagen de prueba avanzada...")
            
            from PIL import Image, ImageDraw, ImageFont
            
            # Crear imagen con gradiente
            test_image = Image.new('RGB', (240, 180), color='#2196F3')
            draw = ImageDraw.Draw(test_image)
            
            # Dibujar fondo con gradiente simple
            for y in range(180):
                color_intensity = int(255 * (1 - y / 180))
                color = (color_intensity // 4, color_intensity // 2, color_intensity)
                draw.line([(0, y), (240, y)], fill=color)
            
            # Dibujar elementos
            # Rectángulo principal
            draw.rectangle([20, 20, 220, 160], outline='white', width=3)
            
            # Círculo central
            draw.ellipse([80, 60, 160, 140], fill='white', outline='black', width=2)
            
            # Texto
            try:
                # Intentar usar fuente por defecto
                draw.text((120, 100), "PRUEBA\nAVANZADA", fill='black', anchor="mm", align="center")
            except:
                # Si falla, dibujar formas geométricas
                draw.polygon([(100, 80), (140, 80), (120, 120)], fill='red')
            
            # Cargar usando el nuevo sistema
            # Usar slot 0 para la prueba
            slot_index = 0
            
            # Redimensionar para display
            display_image = test_image.copy()
            display_image.thumbnail((200, 150), Image.Resampling.LANCZOS)
            
            # Crear CTkImage
            ctk_image = ctk.CTkImage(
                light_image=display_image,
                dark_image=display_image,
                size=display_image.size
            )
            
            # Aplicar a la interfaz usando el nuevo sistema
            self.image_labels[slot_index].configure(
                image=ctk_image,
                text="",
                fg_color="transparent"
            )
            
            # Actualizar referencias
            self.image_references[slot_index] = ctk_image
            self.image_paths[slot_index] = "IMAGEN_DE_PRUEBA_AVANZADA"
            
            # Actualizar botón
            self.image_buttons[slot_index].configure(
                text="✅ PRUEBA ADV",
                fg_color="#4CAF50"
            )
            
            # Actualizar status si existe
            if hasattr(self, 'image_status_labels') and len(self.image_status_labels) > slot_index:
                self.image_status_labels[slot_index].configure(
                    text="🧪",
                    text_color="#9C27B0"
                )
            
            print("✅ Imagen de prueba avanzada creada y aplicada")
            self.show_status_message("🧪 Imagen de prueba avanzada creada")
            
            return True
            
        except Exception as e:
            print(f"❌ Error creando imagen de prueba avanzada: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def show_debug_summary(self):
        """Mostrar resumen de debug en ventana"""
        try:
            debug_window = ctk.CTkToplevel(self.level_editor_window)
            debug_window.title("🔧 Resumen de Debug")
            debug_window.geometry("500x600")
            debug_window.resizable(True, True)
            debug_window.transient(self.level_editor_window)
            
            main_frame = ctk.CTkFrame(debug_window)
            main_frame.pack(fill="both", expand=True, padx=20, pady=20)
            
            # Título
            ctk.CTkLabel(
                main_frame,
                text="🔧 RESUMEN DE DEBUG",
                font=ctk.CTkFont(size=18, weight="bold")
            ).pack(pady=(15, 10))
            
            # Crear texto de resumen
            summary_text = "📊 ESTADO DEL EDITOR:\n\n"
            
            # Estado de componentes
            summary_text += f"🔧 Componentes:\n"
            summary_text += f"• Botones: {len(self.image_buttons)}/4\n"
            summary_text += f"• Labels: {len(self.image_labels)}/4\n"
            summary_text += f"• Referencias: {len(self.image_references)}/4\n"
            summary_text += f"• Status labels: {len(self.image_status_labels) if hasattr(self, 'image_status_labels') else 0}/4\n\n"
            
            # Estado de imágenes
            summary_text += f"🖼️ Estado de imágenes:\n"
            for i in range(4):
                has_image = self.image_paths[i] is not None
                status_icon = "✅" if has_image else "❌"
                file_name = "Sin imagen"
                if has_image:
                    if self.image_paths[i] == "IMAGEN_DE_PRUEBA_AVANZADA":
                        file_name = "Imagen de prueba"
                    else:
                        file_name = os.path.basename(self.image_paths[i])
                
                summary_text += f"• Slot {i+1}: {status_icon} {file_name}\n"
            
            summary_text += f"\n💡 MÉTODOS DISPONIBLES:\n"
            summary_text += f"• 📂 Examinar archivos: {'✅' if hasattr(self, 'open_file_browser') else '❌'}\n"
            summary_text += f"• 📋 Pegar ruta: {'✅' if hasattr(self, 'paste_image_path') else '❌'}\n"
            summary_text += f"• 🎯 Selección por slot: {'✅' if hasattr(self, 'select_image_for_slot') else '❌'}\n"
            summary_text += f"• 🎨 Carga robusta: {'✅' if hasattr(self, 'load_image_to_slot') else '❌'}\n"
            
            summary_text += f"\n🔍 PROBLEMAS COMUNES:\n"
            summary_text += f"• Si no se abre el diálogo: Usa '📂 EXAMINAR ARCHIVOS'\n"
            summary_text += f"• Si no aparece el teclado: Normal, está deshabilitado\n"
            summary_text += f"• Si falla la carga: Usa '📋 PEGAR RUTA'\n"
            summary_text += f"• Si persisten problemas: Reinicia el editor\n"
            
            # Textbox para mostrar el resumen
            textbox = ctk.CTkTextbox(
                main_frame,
                width=450,
                height=400,
                font=ctk.CTkFont(size=11),
                wrap="word"
            )
            textbox.pack(fill="both", expand=True, pady=10)
            textbox.insert("1.0", summary_text)
            textbox.configure(state="disabled")
            
            # Botón cerrar
            close_btn = ctk.CTkButton(
                main_frame,
                text="✅ CERRAR",
                command=debug_window.destroy,
                width=150,
                height=35
            )
            close_btn.pack(pady=10)
            
            print("🔧 Ventana de debug abierta")
            
        except Exception as e:
            print(f"❌ Error mostrando resumen de debug: {e}")
            messagebox.showerror("Error Debug", f"Error mostrando resumen:\n{e}", parent=self.level_editor_window)
    
    def create_level_info_panel(self, parent):
        ctk.CTkLabel(
            parent,
            text="📋 INFORMACIÓN DEL NIVEL",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
    
        ctk.CTkLabel(parent, text="📝 Título del nivel:").pack(pady=(10, 5))
        self.title_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Ej: Animales Domésticos",
            width=250,
            height=35
        )
        self.title_entry.pack(pady=(0, 10))
        self.setup_no_keyboard_entry(self.title_entry)
    
        ctk.CTkLabel(parent, text="👤 Autor:").pack(pady=(5, 5))
        self.author_entry = ctk.CTkEntry(
            parent,
            placeholder_text="Tu nombre",
            width=250,
            height=35
        )
        self.author_entry.pack(pady=(0, 10))
        self.setup_no_keyboard_entry(self.author_entry)
    
        ctk.CTkLabel(parent, text="📄 Descripción:").pack(pady=(5, 5))
        self.description_textbox = ctk.CTkTextbox(
            parent,
            width=250,
            height=80,
            wrap="word"
        )
        self.description_textbox.pack(pady=(0, 10))
    
        ctk.CTkLabel(parent, text="⭐ Dificultad:").pack(pady=(5, 5))
        self.difficulty_var = ctk.StringVar(value="Fácil")
        difficulty_menu = ctk.CTkOptionMenu(
            parent,
            variable=self.difficulty_var,
            values=["Fácil", "Medio", "Difícil", "Experto"],
            width=250,
            height=35
        )
        difficulty_menu.pack(pady=(0, 10))
    
        info_frame = ctk.CTkFrame(parent)
        info_frame.pack(fill="x", pady=10)
    
        ctk.CTkLabel(
            info_frame,
            text="📊 ESTADÍSTICAS",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
    
        self.stats_label = ctk.CTkLabel(
            info_frame,
            text="Palabras: 0\nCompleto: ❌",
            font=ctk.CTkFont(size=12),
            justify="left"
        )
        self.stats_label.pack(pady=(0, 10))
    
   
    
    def setup_no_keyboard_entry(self, entry_widget):
        try:
            entry_widget.bind("<FocusIn>", self.disable_virtual_keyboard)
            entry_widget.bind("<Button-1>", self.disable_virtual_keyboard)
            entry_widget.bind("<TouchpadPress>", self.disable_virtual_keyboard)
            entry_widget.configure(insertofftime=0)
            
            if hasattr(entry_widget, '_entry'):
                entry_widget._entry.bind("<FocusIn>", self.disable_virtual_keyboard)
                entry_widget._entry.configure(insertofftime=0)
        except Exception as e:
            print(f"⚠️ Error configurando entry sin teclado: {e}")
    
    def create_word_editor_panel(self, parent):
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=0)
        parent.grid_rowconfigure(1, weight=0)
        parent.grid_rowconfigure(2, weight=0)
        parent.grid_rowconfigure(3, weight=1)
        parent.grid_rowconfigure(4, weight=0)
        parent.grid_rowconfigure(5, weight=0)
        parent.grid_rowconfigure(6, weight=0)
        parent.grid_rowconfigure(7, weight=0)

        # Título principal
        title_main_label = ctk.CTkLabel(
            parent,
            text="✏️ EDITOR DE PALABRAS",
            font=ctk.CTkFont(size=16, weight="bold")
        )
        title_main_label.grid(row=0, column=0, pady=(15, 10), sticky="ew")

        # Información de palabra actual
        word_info_frame = ctk.CTkFrame(parent)
        word_info_frame.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="ew")
        self.word_info_label = ctk.CTkLabel(
            word_info_frame,
            text="Palabra 1 de 1",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        self.word_info_label.pack(pady=10)

        # Campos de palabra y pista
        word_and_hint_frame = ctk.CTkFrame(parent)
        word_and_hint_frame.grid(row=2, column=0, padx=20, pady=5, sticky="ew")
        
        ctk.CTkLabel(word_and_hint_frame, text="🔤 Palabra (respuesta):").pack(pady=(10, 5))
        self.word_entry = ctk.CTkEntry(
            word_and_hint_frame,
            placeholder_text="Ej: GATO",
            width=300,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.word_entry.pack(pady=(0, 10))
        self.word_entry.bind("<KeyRelease>", self.on_word_change)

        ctk.CTkLabel(word_and_hint_frame, text="💡 Pista (opcional):").pack(pady=(5, 5))
        self.hint_entry = ctk.CTkEntry(
            word_and_hint_frame,
            placeholder_text="Ej: Mascota felina que maúlla",
            width=300,
            height=35
        )
        self.hint_entry.pack(pady=(0, 15))

        # Marco de imágenes
        images_frame = ctk.CTkFrame(parent)
        images_frame.grid(row=3, column=0, padx=20, pady=5, sticky="nsew")

        # Header de imágenes
        images_header = ctk.CTkFrame(images_frame)
        images_header.pack(fill="x", padx=15, pady=(5, 5))

        ctk.CTkLabel(images_header, text="📸 CUATRO IMÁGENES", font=ctk.CTkFont(size=14, weight="bold")).pack(side="left")
        main_browse_btn = ctk.CTkButton(
            images_header,
            text="📂 EXAMINAR ARCHIVOS",
            command=self.open_file_browser,
            width=150,
            height=30,
            font=ctk.CTkFont(size=11, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        main_browse_btn.pack(side="right", padx=5)
        paste_path_btn = ctk.CTkButton(
            images_header,
            text="📋 PEGAR RUTA",
            command=self.paste_image_path,
            width=100,
            height=30,
            font=ctk.CTkFont(size=10),
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        paste_path_btn.pack(side="right", padx=5)

        # Grid de imágenes
        images_grid = ctk.CTkFrame(images_frame)
        images_grid.pack(expand=True, fill="both", padx=10, pady=5)

        # Inicializar listas
        self.image_frames = []
        self.image_labels = []
        self.image_buttons = []
        self.image_status_labels = []

        for i in range(4):
            row_img = i // 2
            col_img = i % 2

            img_frame = ctk.CTkFrame(images_grid)
            img_frame.grid(row=row_img, column=col_img, padx=5, pady=5, sticky="nsew")

            img_label = ctk.CTkLabel(
                img_frame, 
                text=f"📷\nIMAGEN {i+1}\nClick aquí", 
                width=160, 
                height=120, 
                fg_color=("#f0f0f0", "#2b2b2b"), 
                cursor="hand2", 
                font=ctk.CTkFont(size=10)
            )
            img_label.pack(pady=(10, 5), expand=True)

            # Hacer clickeable
            def make_label_clickable(label_widget, slot_idx):
                def on_click(event):
                    self.select_image_for_slot(slot_idx)
                    return "break"
                label_widget.bind("<Button-1>", on_click)
            make_label_clickable(img_label, i)

            slot_buttons_container = ctk.CTkFrame(img_frame, fg_color="transparent")
            slot_buttons_container.pack(pady=(5, 5))

            # Botón de selección
            def make_select_command(idx): 
                return lambda: self.select_image_for_slot(idx)
            select_btn = ctk.CTkButton(
                slot_buttons_container,
                text=f"📁 {i+1}",
                command=make_select_command(i),
                width=60,
                height=25,
                font=ctk.CTkFont(size=9, weight="bold"),
                fg_color="#2196F3",
                hover_color="#1976D2"
            )
            select_btn.pack(side="left", padx=2)

            # Indicador de estado
            status_label = ctk.CTkLabel(
                slot_buttons_container,
                text="❌",
                font=ctk.CTkFont(size=10),
                width=25,
                height=15
            )
            status_label.pack(side="left", padx=(3,3))

            # Botón de eliminar
            def make_remove_command(idx): 
                return lambda: self.remove_image(idx)
            remove_btn = ctk.CTkButton(
                slot_buttons_container,
                text="🗑️",
                command=make_remove_command(i),
                width=35,
                height=25,
                font=ctk.CTkFont(size=9),
                fg_color="#FF5722",
                hover_color="#E64A19"
            )
            remove_btn.pack(side="left", padx=2)

            # Guardar referencias
            self.image_frames.append(img_frame)
            self.image_labels.append(img_label)
            self.image_buttons.append(select_btn)
            self.image_status_labels.append(status_label)
            self.setup_drag_drop(img_label, i)

        images_grid.grid_rowconfigure(0, weight=1)
        images_grid.grid_rowconfigure(1, weight=1)
        images_grid.grid_columnconfigure(0, weight=1)
        images_grid.grid_columnconfigure(1, weight=1)

        # Separador
        separator = ctk.CTkFrame(parent, height=2, fg_color=("#d0d0d0", "#404040"))
        separator.grid(row=4, column=0, padx=20, pady=(20, 10), sticky="ew")

        # Botones de navegación (Siguiente ronda, Guardar, etc.)
        nav_frame = ctk.CTkFrame(parent, fg_color="transparent", height=60)
        nav_frame.grid(row=5, column=0, padx=20, pady=(10, 20), sticky="ew")
        nav_container = ctk.CTkFrame(nav_frame, fg_color="transparent")
        nav_container.pack(expand=True)
        
        nav_container.grid_columnconfigure(0, weight=1)
        nav_container.grid_columnconfigure(1, weight=1)
        nav_container.grid_columnconfigure(2, weight=1)
        nav_container.grid_columnconfigure(3, weight=1)

        self.prev_button = ctk.CTkButton(
            nav_container,
            text="⬅️ ANTERIOR",
            command=self.previous_word,
            width=120,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#607D8B",
            hover_color="#455A64"
        )
        self.prev_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.save_word_button = ctk.CTkButton(
            nav_container,
            text="💾 GUARDAR",
            command=self.save_current_word,
            width=140,
            height=40,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.save_word_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.next_button = ctk.CTkButton(
            nav_container,
            text="SIGUIENTE ➡️",
            command=self.next_word,
            width=120,
            height=40,
            font=ctk.CTkFont(size=12, weight="bold"),
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        self.next_button.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

        self.new_word_button = ctk.CTkButton(
            nav_container,
            text="➕ NUEVA RONDA",
            command=self.add_new_word,
            width=130,
            height=40,
            fg_color="#FF9800",
            hover_color="#F57C00",
            font=ctk.CTkFont(size=12, weight="bold")
        )
        self.new_word_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # Información adicional
        additional_info_label = ctk.CTkLabel(
            parent,
            text="💡 Usa '➕ NUEVA RONDA' para agregar más palabras al nivel",
            font=ctk.CTkFont(size=11),
            text_color="#888888"
        )
        additional_info_label.grid(row=6, column=0, pady=(5, 10), sticky="ew")

        # Estado de navegación
        self.nav_status_label = ctk.CTkLabel(
            parent,
            text="",
            font=ctk.CTkFont(size=10),
            text_color="#666666"
        )
        self.nav_status_label.grid(row=7, column=0, pady=(0, 10), sticky="ew")

        # Actualizar UI
        parent.update_idletasks()
        self.update_navigation_buttons()

    def create_action_buttons(self, parent):
        """Botones de acción principales mejorados"""
        print("🔨 Creando botones de acción...")
    
        # Frame contenedor principal
        buttons_container = ctk.CTkFrame(parent, fg_color="transparent")
        buttons_container.pack(fill="x", expand=True)
    
    # Frame izquierdo - Archivo
        file_frame = ctk.CTkFrame(buttons_container, fg_color="transparent")
        file_frame.pack(side="left", fill="y", padx=5, pady=5)
    
        new_btn = ctk.CTkButton(
            file_frame,
            text="🆕 NUEVO",
            command=self.new_level,
            width=120,
            height=35,
            font=ctk.CTkFont(size=11, weight="bold")
        )
        new_btn.pack(side="left", padx=3)
    
        load_btn = ctk.CTkButton(
            file_frame,
            text="📁 CARGAR",
            command=self.load_level,
            width=120,
            height=35,
            fg_color="#2196F3",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        load_btn.pack(side="left", padx=3)
    
    # Frame central - Guardar y Probar
        save_frame = ctk.CTkFrame(buttons_container, fg_color="transparent")
        save_frame.pack(side="left", fill="y", padx=5, pady=5)
    
    # Guardar nivel completo
        save_level_btn = ctk.CTkButton(
            save_frame,
            text="💾 GUARDAR NIVEL",
            command=self.guardar_nivel_completo,
            width=140,
            height=35,
            fg_color="#4CAF50",
            hover_color="#45a049",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        save_level_btn.pack(side="left", padx=3)
    
    # Probar nivel
        test_btn = ctk.CTkButton(
            save_frame,
            text="🎮 PROBAR",
            command=self.probar_nivel_creado,
            width=120,
            height=35,
            fg_color="#9C27B0",
            hover_color="#7B1FA2",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        test_btn.pack(side="left", padx=3)
    
    # Frame derecho - Compartir y Cerrar
        share_frame = ctk.CTkFrame(buttons_container, fg_color="transparent")
        share_frame.pack(side="right", fill="y", padx=5, pady=5)
    
        export_btn = ctk.CTkButton(
            share_frame,
            text="📤 EXPORTAR",
            command=self.export_level,
            width=120,
            height=35,
            fg_color="#FF9800",
            font=ctk.CTkFont(size=11, weight="bold")
        )   
        export_btn.pack(side="left", padx=3)
    
        close_btn = ctk.CTkButton(
            share_frame,
            text="❌ CERRAR",
            command=self.close_editor_safely,
            width=120,
            height=35,
            fg_color="#607D8B",
            font=ctk.CTkFont(size=11, weight="bold")
        )
        close_btn.pack(side="left", padx=3)
    
    # Agregar botón de debug si está en modo desarrollo
        if hasattr(self, 'debug_mode') and self.debug_mode:
            self.add_debug_button(buttons_container)
    
        print("✅ Botones de acción creados")
        print("🎯 Intentando agregar botón GUARDAR:", hasattr(self, "guardar_nivel_completo"))
        print("🎯 Intentando agregar botón PROBAR:", hasattr(self, "probar_nivel_creado"))




    def create_words_management_panel(self, parent):
        """Panel de gestión de palabras"""
        ctk.CTkLabel(
            parent,
            text="📝 PALABRAS DEL NIVEL",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Lista de palabras
        self.words_listbox = tk.Listbox(
            parent,
            bg="#2b2b2b",
            fg="white",
            selectbackground="#1f538d",
            font=("Arial", 12),
            height=15,
            width=25
        )
        self.words_listbox.pack(fill="both", expand=True, padx=10, pady=10)
        self.words_listbox.bind("<Double-Button-1>", self.select_word_from_list)
        
        # Botones de gestión
        manage_frame = ctk.CTkFrame(parent)
        manage_frame.pack(fill="x", padx=10, pady=5)
        
        add_word_btn = ctk.CTkButton(
            manage_frame,
            text="➕ NUEVA PALABRA",
            command=self.add_new_word,
            width=200,
            height=35,
            fg_color="#4CAF50"
        )
        add_word_btn.pack(pady=5)
        
        delete_word_btn = ctk.CTkButton(
            manage_frame,
            text="🗑️ ELIMINAR",
            command=self.delete_current_word,
            width=200,
            height=35,
            fg_color="#FF5722"
        )
        delete_word_btn.pack(pady=5)
        
        # Botones de vista previa
        preview_frame = ctk.CTkFrame(parent)
        preview_frame.pack(fill="x", padx=10, pady=(10, 5))
        
        ctk.CTkLabel(
            preview_frame,
            text="👁️ VISTA PREVIA",
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(10, 5))
        
        preview_btn = ctk.CTkButton(
            preview_frame,
            text="🔍 PROBAR NIVEL",
            command=self.preview_level,
            width=200,
            height=35,
            fg_color="#2196F3"
        )
        preview_btn.pack(pady=5)
        
        validate_btn = ctk.CTkButton(
            preview_frame,
            text="✅ VALIDAR",
            command=self.validate_level,
            width=200,
            height=35,
            fg_color="#FF9800"
        )
        validate_btn.pack(pady=(5, 10))
    
    
    
    def select_image(self, index):
        """Seleccionar imagen para una posición - VERSIÓN MEJORADA"""
        print(f"📁 Seleccionando imagen {index + 1}...")
    
        try:
            self.app.sound_manager.play_sound('click')
        except:
            pass
    
        filetypes = [
            ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
            ("Todos los archivos", "*.*")
        ]
    
        try:
        # Hacer ventana temporal topmost
            if self.level_editor_window:
                self.level_editor_window.attributes('-topmost', True)
                self.level_editor_window.update()
        
        # Abrir diálogo
            filename = filedialog.askopenfilename(
                parent=self.level_editor_window,
                title=f"Seleccionar imagen {index + 1}",
                filetypes=filetypes,
                initialdir=os.path.expanduser("~/Pictures")
        )
        
            # Restaurar ventana
            if self.level_editor_window:
                self.level_editor_window.attributes('-topmost', False)
        
            if not filename:
                return
        
        # Cargar imagen
            with Image.open(filename) as pil_image:
            # Convertir si es necesario
                if pil_image.mode not in ('RGB', 'RGBA'):
                    pil_image = pil_image.convert('RGB')
            
            # Crear copia y redimensionar
                img_copy = pil_image.copy()
                img_copy.thumbnail((160, 120), Image.Resampling.LANCZOS)
            
            # Crear CTkImage
                ctk_image = ctk.CTkImage(
                    light_image=img_copy,
                    dark_image=img_copy,
                    size=img_copy.size
                )
            
                # IMPORTANTE: Destruir y recrear el label para evitar errores
                if hasattr(self, 'image_labels') and index < len(self.image_labels):
                    old_label = self.image_labels[index]
                    parent = old_label.master
                    old_label.destroy()
                
                # Crear nuevo label con imagen
                    new_label = ctk.CTkLabel(
                        parent,
                        image=ctk_image,
                        text="",
                        width=160,
                        height=120,
                        cursor="hand2"
                    )
                    new_label.pack(pady=(10, 5))
                
                # Hacer clickeable
                    def on_click(event):
                        self.select_image_for_slot(index)
                        return "break"
                    new_label.bind("<Button-1>", on_click)
                
                    # Actualizar referencia
                    self.image_labels[index] = new_label
            
                # Guardar referencias
                self.image_references[index] = ctk_image
                self.image_paths[index] = filename
            
            # Actualizar botón
                fname = os.path.basename(filename)
                if len(fname) > 8:
                    fname = fname[:8] + "..."
                self.image_buttons[index].configure(
                    text=f"✅ {fname}",
                    fg_color="#4CAF50"
                )
            
                # Actualizar status
                if hasattr(self, 'image_status_labels'):
                    self.image_status_labels[index].configure(
                        text="✅",
                        text_color="#4CAF50"
                    )
            
                self.word_ui_dirty = True
                print(f"✅ Imagen {index + 1} cargada correctamente")
            
                # Sonido éxito
                try:
                    self.app.sound_manager.play_sound('correct')
                except:
                    pass
                
        except Exception as e:
            print(f"❌ Error cargando imagen: {e}")
            messagebox.showerror(
                "Error", 
                f"Error al cargar la imagen:\n{str(e)}", 
                parent=self.level_editor_window
            )
        
    def select_image_for_slot(self, slot_index):
        """Wrapper para select_image"""
        self.select_image(slot_index)




    def _persist_current_ui_word_to_level(self):
        """
        Persistir el estado actual de la UI (palabra, pista, imágenes)
        en self.current_level["words"][self.current_word_index]
        """
        print(f"💾 Persistiendo datos de UI a nivel (ronda {self.current_word_index})...")

        try:
            # Validar índice
            if not (0 <= self.current_word_index < len(self.current_level["words"])):
                print("⚠️ Índice de palabra inválido para persistir")
                return

            # Obtener datos de la UI
            word_str = self.word_entry.get().strip().upper()
            hint_str = self.hint_entry.get().strip()

            # Procesar imágenes de la UI
            images_data_for_json = []
            processed_images_count = 0

            # Obtener imágenes existentes en el nivel (para reutilizar si no cambiaron)
            existing_images_b64 = self.current_level["words"][self.current_word_index].get("images", [None]*4)

            for i in range(4):
                ui_image_path = self.image_paths[i]

                if ui_image_path and os.path.exists(ui_image_path):
                    # Nueva imagen de archivo - convertir a base64
                    try:
                        with open(ui_image_path, "rb") as f:
                            img_base64 = base64.b64encode(f.read()).decode()

                        images_data_for_json.append({
                            "data": img_base64,
                            "filename": os.path.basename(ui_image_path),
                            "original_path": ui_image_path,
                            "processed_date": datetime.now().isoformat(),
                            "format": os.path.splitext(ui_image_path)[1].lower()
                        })
                        processed_images_count += 1
                        print(f"  📷 Imagen {i+1} procesada: {os.path.basename(ui_image_path)}")

                    except Exception as e:
                        print(f"❌ Error procesando imagen {i+1} ({ui_image_path}): {e}")
                        images_data_for_json.append(None)

                elif (existing_images_b64 and i < len(existing_images_b64) and
                      existing_images_b64[i] and isinstance(existing_images_b64[i], dict) and
                      existing_images_b64[i].get("data")):
                    # Imagen existente válida - mantener
                    images_data_for_json.append(existing_images_b64[i])
                    processed_images_count += 1
                    print(f"  🔄 Imagen {i+1} mantenida de versión anterior")

                else:
                    # Slot vacío
                    images_data_for_json.append(None)
                    print(f"  📷 Slot {i+1} vacío")

            # Actualizar datos en la estructura del nivel
            target_word_obj = self.current_level["words"][self.current_word_index]
            target_word_obj["word"] = word_str
            target_word_obj["hint"] = hint_str
            target_word_obj["images"] = images_data_for_json
            target_word_obj["valid_images"] = processed_images_count
            target_word_obj["modified_date"] = datetime.now().isoformat()

            # Agregar metadatos adicionales
            target_word_obj["word_length"] = len(word_str)
            target_word_obj["has_hint"] = bool(hint_str.strip())

            print(f"✅ Datos persistidos: '{word_str}' con {processed_images_count} imágenes")

        except Exception as e:
            print(f"❌ Error en _persist_current_ui_word_to_level: {e}")
            raise # Re-raise the exception after logging




   #!/usr/bin/env python3
# -*- coding: utf-8 -*-

# SOLUCIÓN 1: REEMPLAZAR EL MÉTODO remove_image COMPLETO
    def remove_image(self, index):
        """Quitar imagen de una posición - VERSIÓN CORREGIDA"""
        print(f"🗑️ Quitando imagen del slot {index + 1}...")
    
        try:
            # Validar índice
            if not (0 <= index < 4):
                return
            
            # Limpiar la imagen del label de forma segura
            if hasattr(self, 'image_labels') and index < len(self.image_labels):
                label = self.image_labels[index]
            
                # IMPORTANTE: Primero destruir el widget actual y crear uno nuevo
                 # Esto evita el error "image doesn't exist"
                parent_frame = label.master
                label.destroy()
            
            # Crear nuevo label limpio
                new_label = ctk.CTkLabel(
                    parent_frame,
                    text=f"📷\nIMAGEN {index+1}\nClick aquí",
                    width=160,
                    height=120,
                    fg_color=("#f0f0f0", "#2b2b2b"),
                    cursor="hand2",
                    font=ctk.CTkFont(size=10)
                )
                new_label.pack(pady=(10, 5))
            
                # Hacer clickeable el nuevo label
                def on_click(event):
                    self.select_image_for_slot(index)
                    return "break"
                new_label.bind("<Button-1>", on_click)
            
                # Actualizar referencia
                self.image_labels[index] = new_label
        
            # Limpiar referencias
            if hasattr(self, 'image_references') and index < len(self.image_references):
                self.image_references[index] = None
            
            if hasattr(self, 'image_paths') and index < len(self.image_paths):
                self.image_paths[index] = None
        
            # Actualizar botón
            if hasattr(self, 'image_buttons') and index < len(self.image_buttons):
                self.image_buttons[index].configure(
                    text=f"📁 {index+1}", 
                    fg_color="#2196F3", 
                    hover_color="#1976D2"
                )

        # Actualizar status
            if hasattr(self, 'image_status_labels') and index < len(self.image_status_labels):
                self.image_status_labels[index].configure(
                    text="❌", 
                    text_color="#FF5722"
                )
        
            self.word_ui_dirty = True
            print(f"✅ Slot {index + 1} limpiado correctamente")
        
        # Sonido
            try:
                self.app.sound_manager.play_sound('wrong_place')
            except:
                pass
            
        except Exception as e:
            print(f"❌ Error en remove_image: {e}")

    def load_current_word(self):
        """Cargar datos de la palabra actual - VERSIÓN COMPLETA CORREGIDA"""
        print(f"🔄 Cargando palabra {self.current_word_index + 1}...")
    
    # Primero, limpiar todos los slots de imagen de forma segura
        for i in range(4):
            if hasattr(self, 'image_labels') and i < len(self.image_labels):
                old_label = self.image_labels[i]
                parent_frame = old_label.master
                old_label.destroy()
            
            # Crear nuevo label limpio
                new_label = ctk.CTkLabel(
                    parent_frame,
                    text=f"📷\nIMAGEN {i+1}\nClick aquí",
                    width=160,
                    height=120,
                    fg_color=("#f0f0f0", "#2b2b2b"),
                    cursor="hand2",
                    font=ctk.CTkFont(size=10)
                )
                new_label.pack(pady=(10, 5))
            
            # Hacer clickeable
                def make_click_handler(idx):
                    def on_click(event):
                        self.select_image_for_slot(idx)
                        return "break"
                    return on_click
            
                new_label.bind("<Button-1>", make_click_handler(i))
                self.image_labels[i] = new_label
        
        # Limpiar referencias
            if hasattr(self, 'image_references'):
                self.image_references[i] = None
            if hasattr(self, 'image_paths'):
                self.image_paths[i] = None
        
        # Resetear botones
            if hasattr(self, 'image_buttons') and i < len(self.image_buttons):
                self.image_buttons[i].configure(
                    text=f"📁 {i+1}", 
                    fg_color="#2196F3"
                )
        
        # Resetear status
            if hasattr(self, 'image_status_labels') and i < len(self.image_status_labels):
                self.image_status_labels[i].configure(
                    text="❌", 
                    text_color="#FF5722"
                )
    
    # Limpiar campos de texto
        if hasattr(self, 'word_entry'):
            self.word_entry.delete(0, tk.END)
        if hasattr(self, 'hint_entry'):
            self.hint_entry.delete(0, tk.END)
    
    # Si no hay palabras, crear una vacía
        if not self.current_level["words"]:
            self.current_level["words"].append({
                "word": "",
                "hint": "",
                "images": [None, None, None, None],
                "difficulty": self.difficulty_var.get() if hasattr(self, 'difficulty_var') else "Fácil",
                "created_date": datetime.now().isoformat(),
                "id": f"word_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                "valid_images": 0
            })
            self.current_word_index = 0
    
    # Validar índice
        if not (0 <= self.current_word_index < len(self.current_level["words"])):
            self.current_word_index = 0
    
    # Cargar datos de la palabra
        word_data = self.current_level["words"][self.current_word_index]
    
    # Cargar texto
        if hasattr(self, 'word_entry'):
            self.word_entry.insert(0, word_data.get("word", ""))
        if hasattr(self, 'hint_entry'):
            self.hint_entry.insert(0, word_data.get("hint", ""))
    
    # Cargar imágenes guardadas
        saved_images = word_data.get("images", [None] * 4)
        for i, img_data in enumerate(saved_images):
            if img_data and isinstance(img_data, dict) and img_data.get("data"):
                try:
                # Decodificar imagen base64
                    img_bytes = base64.b64decode(img_data["data"])
                    with io.BytesIO(img_bytes) as img_buffer:
                        pil_image = Image.open(img_buffer)
                        if pil_image.mode not in ('RGB', 'RGBA'):
                            pil_image = pil_image.convert('RGB')
                    
                    # Redimensionar
                        pil_image.thumbnail((160, 120), Image.Resampling.LANCZOS)
                    
                    # Crear CTkImage
                        ctk_image = ctk.CTkImage(
                            light_image=pil_image,
                            dark_image=pil_image,
                            size=pil_image.size
                        )
                    
                    # Aplicar imagen al label
                        self.image_labels[i].configure(
                            image=ctk_image,
                            text=""
                        )
                    
                        # Guardar referencias
                        self.image_references[i] = ctk_image
                        self.image_paths[i] = img_data.get("original_path", f"EMBEDDED_{i+1}")
                    
                        # Actualizar botón
                        filename = img_data.get("filename", f"imagen_{i+1}")
                        if len(filename) > 8:
                            filename = filename[:8] + "..."
                        self.image_buttons[i].configure(
                            text=f"✅ {filename}",
                            fg_color="#4CAF50"
                        )
                    
                        # Actualizar status
                        if hasattr(self, 'image_status_labels'):
                            self.image_status_labels[i].configure(
                                text="✅",
                                text_color="#4CAF50"
                            )
                        
                except Exception as e:
                    print(f"❌ Error cargando imagen {i+1}: {e}")
    
    # Actualizar información
        total = len(self.current_level["words"])
        if hasattr(self, 'word_info_label'):
            self.word_info_label.configure(
                text=f"Palabra/Ronda {self.current_word_index + 1} de {total}"
            )
    
    # Actualizar navegación
        if hasattr(self, 'prev_button'):
            self.prev_button.configure(
                state="normal" if self.current_word_index > 0 else "disabled"
            )
    
    # Actualizar listas
        self.update_words_list()
        self.update_stats()
        self.update_navigation_buttons()
    
    # Actualizar contador de rondas
        if hasattr(self, 'rounds_info_label'):
            self.rounds_info_label.configure(
                text=f"Total de rondas: {total}"
            )
    
        self.word_ui_dirty = False
        print(f"✅ Palabra {self.current_word_index + 1} cargada")




        

    
    def save_current_word(self):
        """Guardar palabra/ronda actual con validaciones completas y correcciones"""
        print("💾 Guardando palabra/ronda actual...")

    # Obtener datos de la UI
        word_str = self.word_entry.get().strip().upper()
        hint_str = self.hint_entry.get().strip()

    # Validación básica de palabra
        if not word_str:
            messagebox.showwarning("Palabra requerida",
                                "Por favor ingresa una palabra para esta ronda",
                                parent=self.level_editor_window)
            return False
    # Validar longitud de palabra
        if len(word_str) < 2:
            messagebox.showwarning("Palabra muy corta",
                             "La palabra debe tener al menos 2 letras",
                             parent=self.level_editor_window)
            return False
        if len(word_str) > 20:
            messagebox.showwarning("Palabra muy larga",
                             "La palabra no debe tener más de 20 letras",
                             parent=self.level_editor_window)
            return False
    # Validar que solo contenga letras
        if not word_str.isalpha():
            messagebox.showwarning("Palabra inválida",
                                "La palabra solo debe contener letras (sin números ni símbolos)",
                                parent=self.level_editor_window)
            return False

    # Validar imágenes en la UI
        num_actual_images_in_ui = sum(1 for path_or_data in self.image_paths if path_or_data is not None)

        if num_actual_images_in_ui == 0:
            if not messagebox.askyesno("Sin imágenes",
                                     "No has seleccionado ninguna imagen para esta ronda.\n\n"
                                     "Se recomienda tener al menos 1 imagen.\n\n"
                                     "¿Guardar palabra de todas formas?",
                                     parent=self.level_editor_window):
                return False
        elif num_actual_images_in_ui < 4:
            if not messagebox.askyesno("Imágenes incompletas",
                                     f"Solo hay {num_actual_images_in_ui} de 4 imágenes recomendadas.\n\n"
                                     f"Se sugiere tener 4 imágenes para una mejor experiencia.\n\n"
                                     f"¿Guardar de todas formas?",
                                     parent=self.level_editor_window):
                return False

        try:
        # Asegurar que existe la estructura de nivel
            if "words" not in self.current_level:
                self.current_level["words"] = []

        # Asegurar que existe la ronda actual
            while len(self.current_level["words"]) <= self.current_word_index:
                self.current_level["words"].append({
                    "word": "",
                    "hint": "",
                    "images": [None, None, None, None],
                    "difficulty": self.difficulty_var.get() if hasattr(self, 'difficulty_var') else "Fácil",
                    "created_date": datetime.now().isoformat(),
                    "id": f"word_{datetime.now().strftime('%Y%m%d%H%M%S%f')}",
                    "valid_images": 0,
                    "modified_date": datetime.now().isoformat()
                })

        # Persistir datos de la UI a la estructura del nivel
            self._persist_current_ui_word_to_level()

        # Verificar que se guardó correctamente
            saved_word_data = self.current_level["words"][self.current_word_index]
            final_saved_images_count = saved_word_data.get("valid_images", 0)

        # Actualizar metadatos del nivel
            if "metadata" not in self.current_level:
                self.current_level["metadata"] = {}

            self.current_level["metadata"]["last_modified"] = datetime.now().isoformat()
            self.current_level["metadata"]["total_words"] = len(self.current_level["words"])
            self.current_level["metadata"]["complete_words"] = sum(
                1 for w in self.current_level["words"]
                if w.get("word", "").strip() and w.get("valid_images", 0) > 0
            )

        # Actualizar interfaz
            self.update_words_list()
            self.update_stats()
            self.update_navigation_buttons()

        # Marcar que la UI está limpia
            self.word_ui_dirty = False

        # Sonido de éxito
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass

        # Mensaje de confirmación
            images_msg = f"con {final_saved_images_count} imágenes" if final_saved_images_count > 0 else "sin imágenes"
            messagebox.showinfo("✅ Ronda Guardada",
                                f"Ronda '{word_str}' guardada correctamente {images_msg}\n\n"
                                f"📊 Total de rondas en el nivel: {len(self.current_level['words'])}",
                                parent=self.level_editor_window)

            print(f"✅ Ronda guardada: '{word_str}' con {final_saved_images_count} imágenes")
            return True

        except Exception as e:
            print(f"❌ Error guardando ronda: {e}")
            messagebox.showerror("Error",
                                f"No se pudo guardar la ronda:\n\n{str(e)}",
                                parent=self.level_editor_window)
            return False

    def guardar_nivel_completo(self):
        """Guardar nivel completo con todas las rondas"""
        print("💾 Guardando nivel completo...")
    
    # Actualizar metadatos
        self.update_level_metadata()
    
    # Validar que hay al menos una ronda
        if not self.current_level["words"]:
            messagebox.showwarning("Sin rondas", "Agrega al menos una ronda antes de guardar", parent=self.level_editor_window)
            return False
    
    # Validar datos básicos
        if not self.validate_level_data():
            return False
    
    # Crear directorio si no existe
        levels_dir = "custom_levels"
        os.makedirs(levels_dir, exist_ok=True)
    
    # Generar nombre de archivo único
        title = self.current_level["metadata"]["title"] or "nivel_sin_titulo"
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
        filename = f"{safe_title}_{timestamp}.json"
        filepath = os.path.join(levels_dir, filename)
    
        try:
        # Agregar información adicional al nivel
            self.current_level["metadata"]["saved_date"] = datetime.now().isoformat()
            self.current_level["metadata"]["total_rounds"] = len(self.current_level["words"])
            self.current_level["metadata"]["complete_rounds"] = sum(
                1 for w in self.current_level["words"] 
                if w.get("word") and w.get("valid_images", 0) > 0
            )
        
        # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.current_level, f, indent=2, ensure_ascii=False)
        
        # Sonido de éxito
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass
        
            messagebox.showinfo("✅ Nivel Guardado", 
                f"Nivel guardado exitosamente:\n\n"
                f"📝 Título: {title}\n"
                f"🎯 Rondas: {len(self.current_level['words'])}\n"
                f"📁 Archivo: {filename}\n\n"
                f"¡Ya puedes jugar este nivel!", parent=self.level_editor_window)
        
            print(f"💾 Nivel guardado: {filepath}")
            return True
        
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar el nivel:\n{e}", parent=self.level_editor_window)
            print(f"❌ Error guardando nivel: {e}")
            return False
        

    def validate_level_data(self):
        """Validar datos del nivel antes de guardar"""
        metadata = self.current_level["metadata"]
    
    # Validar título
        if not metadata.get("title", "").strip():
            messagebox.showwarning("Título requerido", 
                "Por favor ingresa un título para el nivel", 
                parent=self.level_editor_window)
            return False
    
    # Validar que hay palabras
        if not self.current_level["words"]:
            messagebox.showwarning("Sin rondas", 
                "Agrega al menos una ronda al nivel", 
                parent=self.level_editor_window)
            return False
    
    # Contar rondas válidas
        valid_rounds = sum(
            1 for w in self.current_level["words"] 
            if w.get("word", "").strip() and w.get("valid_images", 0) > 0
        )
    
        if valid_rounds == 0:
            messagebox.showwarning("Sin rondas válidas", 
                "No hay rondas completas (con palabra e imágenes).\n\n"
                "Cada ronda necesita:\n• Una palabra\n• Al menos 1 imagen", 
                parent=self.level_editor_window)
            return False
    
    # Advertir si hay pocas rondas
        if valid_rounds < 3:
            if not messagebox.askyesno("Pocas rondas", 
                f"Solo hay {valid_rounds} rondas válidas.\n\n"
                f"Se recomienda tener al menos 3 rondas para un buen nivel.\n\n"
                f"¿Guardar de todas formas?", 
                parent=self.level_editor_window):
                return False
    
        return True


    
    def probar_nivel_creado(self):
        """Probar el nivel que se está creando - CORREGIDO SIN CAMBIAR GUARDADO"""
        print("🎮 Iniciando prueba del nivel...")

        # Guardar primero si hay cambios (usando TU método existente)
        if self.word_ui_dirty:
        # Usar tu método de guardado existente
            if hasattr(self, 'save_current_word'):
                self.save_current_word()

    # Validar que hay rondas para probar
        if not self.current_level["words"]:
            messagebox.showwarning("Sin rondas", 
                "Agrega al menos una ronda para probar el nivel", 
                parent=self.level_editor_window)
            return

    # Filtrar solo rondas válidas (usando TU estructura de datos)
        valid_rounds = []
        for word_data in self.current_level["words"]:
            word = word_data.get("word", "").strip()
        # Usar TU lógica de imágenes existente
            images = word_data.get("images", [])
            valid_images_count = 0
        
        # Contar imágenes válidas según TU sistema
            for img in images:
                if img is not None:
                # Tu sistema puede usar rutas de archivos o lo que sea
                    valid_images_count += 1
        
            if word and valid_images_count > 0:
                valid_rounds.append(word_data)

        if not valid_rounds:
            messagebox.showwarning("Sin rondas válidas", 
                "No hay rondas con palabra e imágenes para probar.",
                parent=self.level_editor_window)
            return

    # Crear nivel temporal para la prueba (usando TU estructura)
        test_level = {
            "metadata": self.current_level["metadata"].copy(),
            "words": valid_rounds.copy()
        }

        test_level["metadata"]["title"] = f"[PRUEBA] {test_level['metadata'].get('title', 'Nivel de prueba')}"
        test_level["metadata"]["is_test"] = True

        try:
        # Verificar si existe el método en la app principal
            if hasattr(self.app, 'start_custom_level'):
                self.app.start_custom_level(test_level)
                print("🎮 Nivel enviado a la app principal para prueba")
            else:
            # Mostrar información del nivel de prueba
                info_msg = f"🎮 MODO PRUEBA\n\n"
                info_msg += f"📝 Título: {test_level['metadata'].get('title', 'Sin título')}\n"
                info_msg += f"👤 Autor: {test_level['metadata'].get('author', 'Anónimo')}\n"
                info_msg += f"⭐ Dificultad: {test_level['metadata'].get('difficulty', 'Fácil')}\n"
                info_msg += f"🎯 Rondas válidas: {len(valid_rounds)}\n\n"
        
                info_msg += "📋 Palabras a probar:\n"
                for i, word in enumerate(valid_rounds[:5]):
                    info_msg += f"  {i+1}. {word['word']}\n"
        
                if len(valid_rounds) > 5:
                    info_msg += f"  ... y {len(valid_rounds)-5} más\n"
            
                info_msg += "\n✅ El nivel está listo para jugar"
        
                messagebox.showinfo("🎮 Modo Prueba", info_msg, parent=self.level_editor_window)
    
            try:
                self.app.sound_manager.play_sound('game_start')
            except:
                pass
    
            print(f"🎮 Modo prueba iniciado con {len(valid_rounds)} rondas")
    
        except Exception as e:
            messagebox.showerror("Error", 
                f"No se pudo iniciar la prueba:\n{e}", 
                parent=self.level_editor_window)
            print(f"❌ Error en modo prueba: {e}")


    
    
    def add_new_word(self):
        """Agregar nueva palabra después de persistir la actual."""
        if self.word_ui_dirty : # Solo persistir si hay cambios sin guardar
            # Podrías preguntar al usuario aquí si quiere guardar los cambios de la palabra actual.
            # Por ahora, lo persistimos automáticamente.
            print("ℹ️ Cambios detectados en la palabra UI actual, persistiendo antes de añadir nueva...")
            self._persist_current_ui_word_to_level()

        new_word_id = f"word_{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        self.current_level["words"].append({
            "word": "", "hint": "", "images": [None, None, None, None],
            "difficulty": self.difficulty_var.get(), # O tomar de la palabra actual, o global
            "created_date": datetime.now().isoformat(),
            "id": new_word_id,
            "valid_images": 0
        })
        
        self.current_word_index = len(self.current_level["words"]) - 1
        self.load_current_word() # Esto limpiará la UI y cargará la nueva palabra vacía
        self.update_words_list() # Asegurar que la nueva palabra aparezca
        self.update_stats()
        # self.word_ui_dirty ya es False por load_current_word
        
        try: self.app.sound_manager.play_sound('menu_select')
        except: pass
        print(f"➕ Nueva palabra (índice {self.current_word_index}) agregada y UI actualizada.")
    
    def delete_current_word(self):
        """Eliminar palabra actual"""
        if not self.current_level["words"]:
            return
        
        if messagebox.askyesno("Confirmar", "¿Eliminar la palabra actual?", parent=self.level_editor_window):
            if self.current_word_index < len(self.current_level["words"]):
                del self.current_level["words"][self.current_word_index]
                
                if self.current_word_index >= len(self.current_level["words"]):
                    self.current_word_index = max(0, len(self.current_level["words"]) - 1)
                
                self.load_current_word()
                self.update_words_list()
                self.update_stats()
                
                try:
                    self.app.sound_manager.play_sound('wrong_place')
                except:
                    pass
                
                print("🗑️ Palabra eliminada")
    
    def previous_word(self):
        """Palabra anterior"""
        if self.word_ui_dirty:
            self._persist_current_ui_word_to_level()
            
        if self.current_word_index > 0:
            self.current_word_index -= 1
            self.load_current_word()
            # ... sonido ...

    def next_word(self):
        """Siguiente palabra o añadir nueva si es la última."""
        if self.word_ui_dirty:
            self._persist_current_ui_word_to_level()
            
        if self.current_word_index < len(self.current_level["words"]) - 1:
            self.current_word_index += 1
            self.load_current_word()
        else:
            # Ya estamos en la última palabra, el "siguiente" crea una nueva.
            # La persistencia ya se hizo arriba.
            self.add_new_word() # add_new_word ya maneja la lógica de índice y carga
        # ... sonido ...


    def update_navigation_buttons(self):
        """Actualizar estado de botones de navegación"""
        try:
            total_words = len(self.current_level.get("words", []))

            # Botón anterior
            if hasattr(self, 'prev_button'):
                self.prev_button.configure(
                    state="normal" if self.current_word_index > 0 else "disabled"
                ) # Assuming prev_button has a configure method

            # Botón siguiente
            if hasattr(self, 'next_button'):
                self.next_button.configure(
                    state="normal" if self.current_word_index < total_words - 1 else "disabled"
                ) # Assuming next_button has a configure method

            # Actualizar texto de estado
            if hasattr(self, 'nav_status_label'):
                self.nav_status_label.configure(
                    text=f"Editando ronda {self.current_word_index + 1} de {total_words}"
                ) # Assuming nav_status_label has a configure method

            # Actualizar info de palabra actual
            if hasattr(self, 'word_info_label'):
                self.word_info_label.configure(
                    text=f"Ronda {self.current_word_index + 1} de {total_words}"
                ) # Assuming word_info_label has a configure method

        except Exception as e:
            print(f"❌ Error actualizando botones de navegación: {e}")












    def select_word_from_list(self, event=None):
        """Seleccionar palabra de la lista"""
        selection = self.words_listbox.curselection()
        if selection:
            new_selected_index = selection[0]
            if new_selected_index != self.current_word_index and self.word_ui_dirty:
                self._persist_current_ui_word_to_level()
            
            self.current_word_index = new_selected_index
            self.load_current_word()
            # ... sonido ...
    
   # REEMPLAZAR el método update_words_list completo




    def update_word_counter(self):
        """Actualizar contador de palabras en el título"""
        if hasattr(self, 'word_counter_label'):
            self.word_counter_label.configure(
                text=f"Palabra/Ronda {self.current_word_index + 1} de {len(self.current_level['words'])}"
            )

    def update_words_list(self):
        """Actualizar lista de palabras - VERSIÓN MEJORADA PARA 1 VS 1"""
        self.words_listbox.delete(0, tk.END)
    
        # Si no hay palabras, mostrar mensaje
        if not self.current_level["words"]:
            self.words_listbox.insert(tk.END, "📝 Sin palabras aún")
            self.words_listbox.insert(tk.END, "")
            self.words_listbox.insert(tk.END, "Haz click en")
            self.words_listbox.insert(tk.END, "➕ NUEVA")
            self.words_listbox.insert(tk.END, "para agregar")
            self.words_listbox.insert(tk.END, "la primera ronda")
            return
    
        # Mostrar cada palabra/ronda
        for i, word_data in enumerate(self.current_level["words"]):
            word = word_data.get("word", "")
            images_count = sum(1 for img in word_data.get("images", []) if img is not None)
        
            # Determinar estado visual
            if not word:
                status = "❌"
                word_display = "(vacía)"
                color_code = "#FF5722"  # Rojo
            elif images_count == 0:
                status = "⚠️"
                word_display = word
                color_code = "#FF9800"  # Naranja
            elif images_count < 4:
                status = "🔶"
                word_display = word
                color_code = "#FFC107"  # Amarillo
            else:
                status = "✅"
                word_display = word
                color_code = "#4CAF50"  # Verde
        
        # Formato mejorado para modo 1 vs 1
            ronda_text = f"{status} Ronda {i+1}: {word_display}"
            images_text = f"   📸 {images_count}/4 fotos"
        
        # Insertar en la lista
            self.words_listbox.insert(tk.END, ronda_text)
        
        # Colorear según estado (si es posible)
            try:
                if i == self.current_word_index:
                    # Resaltar ronda actual
                    self.words_listbox.itemconfig(i*2, {'bg': '#1f538d', 'fg': 'white'})
            except:
                pass
        
        # Agregar info de imágenes en línea separada
            self.words_listbox.insert(tk.END, images_text)
        
        # Agregar pista si existe
            hint = word_data.get("hint", "")
            if hint:
                self.words_listbox.insert(tk.END, f"   💡 {hint[:20]}...")
        
        # Línea separadora
            self.words_listbox.insert(tk.END, "─" * 25)
    
    # Actualizar contador de rondas
        if hasattr(self, 'rounds_info_label'):
            complete_rounds = sum(1 for w in self.current_level["words"] 
                            if w.get("word") and 
                            sum(1 for img in w.get("images", []) if img is not None) >= 1)
        
            self.rounds_info_label.configure(
                text=f"Total: {len(self.current_level['words'])} rondas\nCompletas: {complete_rounds}"
            )
    
    def update_stats(self):
        """Actualizar estadísticas del nivel"""
        try:
            words = self.current_level.get("words", [])
            total_words = len(words)

            # Contar rondas completas (con palabra Y al menos 1 imagen)
            complete_words = sum(
                1 for w in words
                if w.get("word", "").strip() and w.get("valid_images", 0) > 0
            )

            # Contar rondas perfectas (con palabra Y 4 imágenes)
            perfect_words = sum(
                1 for w in words
                if w.get("word", "").strip() and w.get("valid_images", 0) == 4
            )

            # Determinar si el nivel está listo
            is_complete = total_words >= 3 and complete_words == total_words
            complete_text = "✅ Listo" if is_complete else "❌ No listo"

            # Actualizar label de estadísticas
            if hasattr(self, 'stats_label'):
                stats_text = f"📊 ESTADÍSTICAS\n"
                stats_text += f"Rondas totales: {total_words}\n"
                stats_text += f"Rondas completas: {complete_words}\n"
                stats_text += f"Rondas perfectas: {perfect_words}\n"
                stats_text += f"Estado: {complete_text}"

                self.stats_label.configure(text=stats_text) # Assuming stats_label has a configure method (e.g., Tkinter Label)

            print(f"📊 Stats actualizadas: {complete_words}/{total_words} completas")

        except Exception as e:
            print(f"❌ Error actualizando estadísticas: {e}")

    
    def on_word_change(self, event=None):
        """Manejar cambios en el campo de palabra"""
        word = self.word_entry.get().upper()
    
        # Limitar longitud
        if len(word) > 20:
            self.word_entry.delete(20, tk.END)
    
    # Marcar que hay cambios sin guardar
        self.word_ui_dirty = True
    
    def reset_level(self):
        """Resetear el nivel a un estado vacío inicial - VERSIÓN COMPLETA"""
        print("🔄 Reiniciando el nivel...")
    
    # Reiniciar estructura de datos
        self.current_level = {
            "metadata": {
                "title": "",
                "author": "",
                "description": "",
                "difficulty": "Fácil",
                "created_date": datetime.now().isoformat(),
                "version": "1.0",
                "id": datetime.now().strftime("%Y%m%d_%H%M%S%f")
            },
            "words": []
        }
    
        self.current_word_index = 0
        self.image_paths = [None, None, None, None]
        self.image_references = [None, None, None, None]
        self.word_ui_dirty = False
    
    # Limpiar campos de la UI si existen
        if hasattr(self, 'title_entry'):
            self.title_entry.delete(0, tk.END)
            self.author_entry.delete(0, tk.END)
        
            if hasattr(self, 'description_textbox'):
                self.description_textbox.delete("1.0", tk.END)
        
            if hasattr(self, 'difficulty_var'):
                self.difficulty_var.set("Fácil")
        
        # Cargar primera palabra vacía
            self.load_current_word()
            self.update_words_list()
            self.update_stats()
    
        print("✅ Nivel reiniciado")

    
    def new_level(self):
        """Nuevo nivel"""
        if messagebox.askyesno("Nuevo Nivel", "¿Crear un nuevo nivel? Se perderán los cambios no guardados.", parent=self.level_editor_window):
            self.reset_level()
            
            try:
                self.app.sound_manager.play_sound('menu_select')
            except:
                pass
            
            print("🆕 Nuevo nivel creado")
    
    def save_level(self):
        """Guardar nivel con todas sus palabras/rondas"""
        print("💾 Guardando nivel...")
    
    # Guardar palabra actual si hay cambios
        if self.word_ui_dirty:
            self._persist_current_ui_word_to_level()
    
    # Actualizar metadatos
        self.update_level_metadata()
    
    # Validar datos
        if not self.validate_level_data():
            return False
    
    # Crear directorio si no existe
        levels_dir = "custom_levels"
        os.makedirs(levels_dir, exist_ok=True)
    
    # Generar nombre de archivo
        title = self.current_level["metadata"]["title"] or "nivel_sin_titulo"
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
        filename = f"{safe_title}_{timestamp}.json"
        filepath = os.path.join(levels_dir, filename)
    
        try:
        # Agregar información adicional
            self.current_level["metadata"]["saved_date"] = datetime.now().isoformat()
            self.current_level["metadata"]["total_words"] = len(self.current_level["words"])
            self.current_level["metadata"]["complete_words"] = sum(
                1 for w in self.current_level["words"] 
                if w.get("word") and w.get("valid_images", 0) > 0
            )
        
        # Guardar archivo
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.current_level, f, indent=2, ensure_ascii=False)
        
        # Sonido de éxito
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass
        
            messagebox.showinfo("✅ Nivel Guardado", 
                f"Nivel guardado exitosamente:\n\n"
                f"📝 Título: {title}\n"
                f"🎯 Rondas: {len(self.current_level['words'])}\n"
                f"📁 Archivo: {filename}",
                parent=self.level_editor_window)
        
            print(f"✅ Nivel guardado: {filepath}")
            return True
        
        except Exception as e:
            messagebox.showerror("Error", 
                f"No se pudo guardar el nivel:\n{e}", 
                parent=self.level_editor_window)
            print(f"❌ Error guardando nivel: {e}")
            return False
    
    def load_level(self):
        """Cargar nivel"""
        filetypes = [
            ("Niveles JSON", "*.json"),
            ("Paquetes 4F1P", "*.4f1p"),
            ("Todos los archivos", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            parent=self.level_editor_window,
            title="Cargar Nivel",
            filetypes=filetypes,
            initialdir="custom_levels"
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Si es un paquete exportado, extraer el nivel
                if "level" in data and "export_info" in data:
                    level_data = data["level"]
                else:
                    level_data = data
                
                self.current_level = level_data
                self.current_word_index = 0
                
                # Cargar metadatos
                metadata = self.current_level.get("metadata", {})
                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, metadata.get("title", ""))
                
                self.author_entry.delete(0, tk.END)
                self.author_entry.insert(0, metadata.get("author", ""))
                
                self.description_textbox.delete("1.0", tk.END)
                self.description_textbox.insert("1.0", metadata.get("description", ""))
                
                self.difficulty_var.set(metadata.get("difficulty", "Fácil"))
                
                # Cargar primera palabra
                self.load_current_word()
                self.update_words_list()
                self.update_stats()
                
                messagebox.showinfo("✅ Cargado", f"Nivel cargado exitosamente:\n{os.path.basename(filename)}", parent=self.level_editor_window)
                
                try:
                    self.app.sound_manager.play_sound('correct')
                except:
                    pass
                
                print(f"📁 Nivel cargado: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo cargar el nivel:\n{e}", parent=self.level_editor_window)
                print(f"❌ Error cargando nivel: {e}")
    
   
    
    def update_level_metadata(self):
        """Actualizar metadatos del nivel desde los campos de entrada"""
        if hasattr(self, 'title_entry'):
            self.current_level["metadata"]["title"] = self.title_entry.get().strip()
    
        if hasattr(self, 'author_entry'):
            self.current_level["metadata"]["author"] = self.author_entry.get().strip()
    
        if hasattr(self, 'description_textbox'):
            self.current_level["metadata"]["description"] = self.description_textbox.get("1.0", tk.END).strip()
    
        if hasattr(self, 'difficulty_var'):
            self.current_level["metadata"]["difficulty"] = self.difficulty_var.get()
    
        self.current_level["metadata"]["modified_date"] = datetime.now().isoformat()
    
    print("✅ Metadatos actualizados")
    
    def export_level(self):
        """Exportar nivel para compartir"""
        self.update_level_metadata()
        
        if not self.validate_level_data():
            return
        
        # Crear paquete exportable
        export_data = {
            "level": self.current_level,
            "export_info": {
                "exported_by": self.current_level["metadata"]["author"],
                "export_date": datetime.now().isoformat(),
                "game_version": "1.0",
                "format_version": "1.0"
            }
        }
        
        # Seleccionar ubicación para exportar
        title = self.current_level["metadata"]["title"]
        safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).rstrip()
        if not safe_title:
            safe_title = "nivel_exportado"
        
        filename = filedialog.asksaveasfilename(
            parent=self.level_editor_window,
            title="Exportar Nivel",
            defaultextension=".4f1p",
            filetypes=[
                ("Paquete 4F1P", "*.4f1p"),
                ("JSON", "*.json"),
                ("Todos los archivos", "*.*")
            ],
            initialfile=f"{safe_title}.4f1p"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(export_data, f, indent=2, ensure_ascii=False)
                
                messagebox.showinfo("✅ Exportado", 
                    f"Nivel exportado exitosamente:\n{os.path.basename(filename)}\n\n"
                    f"¡Ahora puedes compartir este archivo con otros jugadores!",
                    parent=self.level_editor_window)
                
                try:
                    self.app.sound_manager.play_sound('correct')
                except:
                    pass
                
                print(f"📤 Nivel exportado: {filename}")
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo exportar el nivel:\n{e}", parent=self.level_editor_window)
                print(f"❌ Error exportando nivel: {e}")
    
    def share_level(self):
        """Compartir nivel - Usar ventana modal en lugar de nueva ventana"""
        if not hasattr(self, 'level_editor_window') or not self.level_editor_window.winfo_exists():
            return
            
        self.show_share_dialog()
    
    def show_share_dialog(self):
        """Mostrar diálogo de compartir usando la misma ventana"""
        # Crear ventana modal
        share_dialog = ctk.CTkToplevel(self.level_editor_window)
        share_dialog.title("🌐 Compartir Nivel")
        share_dialog.geometry("500x400")
        share_dialog.resizable(False, False)
        
        # Hacer modal
        share_dialog.transient(self.level_editor_window)
        share_dialog.grab_set()
        
        # Centrar la ventana
        share_dialog.geometry("+%d+%d" % (
            self.level_editor_window.winfo_rootx() + 50,
            self.level_editor_window.winfo_rooty() + 50
        ))
        
        main_frame = ctk.CTkFrame(share_dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="🌐 OPCIONES DE COMPARTICIÓN",
            font=ctk.CTkFont(size=20, weight="bold")
        ).pack(pady=(15, 20))
        
        # Opción 1: Exportar archivo
        export_frame = ctk.CTkFrame(main_frame)
        export_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            export_frame,
            text="📤 EXPORTAR ARCHIVO",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            export_frame,
            text="Crea un archivo .4f1p que otros pueden descargar\ny importar en su juego",
            font=ctk.CTkFont(size=12)
        ).pack(pady=(0, 10))
        
        export_btn = ctk.CTkButton(
            export_frame,
            text="📁 EXPORTAR ARCHIVO",
            command=lambda: [self.export_level(), share_dialog.destroy()],
            width=200,
            height=40,
            fg_color="#4CAF50"
        )
        export_btn.pack(pady=(0, 15))
        
        # Info sobre funciones futuras
        info_frame = ctk.CTkFrame(main_frame)
        info_frame.pack(fill="x", padx=15, pady=10)
        
        ctk.CTkLabel(
            info_frame,
            text="🔧 PRÓXIMAMENTE",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 5))
        
        ctk.CTkLabel(
            info_frame,
            text="• Compartir en red local\n• Subir a servidor en línea\n• Galería de niveles de la comunidad",
            font=ctk.CTkFont(size=12),
            justify="left"
        ).pack(pady=(0, 15))
        
        # Botón cerrar
        close_btn = ctk.CTkButton(
            main_frame,
            text="❌ CERRAR",
            command=share_dialog.destroy,
            width=150,
            height=35,
            fg_color="#607D8B"
        )
        close_btn.pack(pady=15)
    
    def preview_level(self):
        """Vista previa del nivel"""
        self.update_level_metadata()
        
        if not self.current_level["words"]:
            messagebox.showwarning("Sin palabras", "Agrega al menos una palabra para probar el nivel", parent=self.level_editor_window)
            return
        
        try:
            # Verificar que el método existe en la app principal
            if hasattr(self.app, 'start_custom_level_preview'):
                self.app.start_custom_level_preview(self.current_level)
            else:
                messagebox.showinfo("Vista previa", "Función de vista previa en desarrollo", parent=self.level_editor_window)
            
            try:
                self.app.sound_manager.play_sound('game_start')
            except:
                pass
            
            print("🔍 Iniciando vista previa del nivel")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo iniciar la vista previa:\n{e}", parent=self.level_editor_window)
            print(f"❌ Error vista previa: {e}")
    
    def validate_level(self):
        """Validar nivel completo"""
        errors = []
        warnings = []
        
        # Validar metadatos
        metadata = self.current_level["metadata"]
        if not metadata.get("title", "").strip():
            errors.append("❌ Título del nivel requerido")
        
        if not metadata.get("author", "").strip():
            warnings.append("⚠️ Autor no especificado")
        
        # Validar palabras
        words = self.current_level["words"]
        if len(words) < 3:
            errors.append("❌ Se requieren al menos 3 palabras")
        
        for i, word_data in enumerate(words):
            word = word_data.get("word", "").strip()
            if not word:
                errors.append(f"❌ Palabra {i+1}: Respuesta requerida")
            
            images = word_data.get("images", [])
            valid_images = sum(1 for img in images if img is not None)
            if valid_images == 0:
                errors.append(f"❌ Palabra {i+1}: Se requiere al menos 1 imagen")
            elif valid_images < 4:
                warnings.append(f"⚠️ Palabra {i+1}: Solo tiene {valid_images}/4 imágenes")
            
            if word and len(word) < 2:
                warnings.append(f"⚠️ Palabra {i+1}: '{word}' es muy corta")
            elif word and len(word) > 15:
                warnings.append(f"⚠️ Palabra {i+1}: '{word}' es muy larga")
        
        # Mostrar resultados
        if errors:
            error_msg = "ERRORES ENCONTRADOS:\n\n" + "\n".join(errors)
            if warnings:
                error_msg += "\n\nADVERTENCIAS:\n\n" + "\n".join(warnings)
            
            messagebox.showerror("❌ Validación Fallida", error_msg, parent=self.level_editor_window)
            return False
        else:
            success_msg = "✅ ¡Nivel válido!\n\nTu nivel está listo para compartir."
            if warnings:
                success_msg += "\n\nADVERTENCIAS:\n\n" + "\n".join(warnings)
            
            messagebox.showinfo("✅ Validación Exitosa", success_msg, parent=self.level_editor_window)
            
            try:
                self.app.sound_manager.play_sound('correct')
            except:
                pass
            
            return True
    
    def close_editor(self):
        """Cerrar editor (método legacy para compatibilidad)"""
        self.close_editor_safely()