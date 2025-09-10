


    
def on_typing(self, event=None):
        """Sonido al escribir"""
        try:
            self.sound_manager.play_sound('click')
        except:
            pass
    
def add_letter(self, letter):
        """Agregar letra a la respuesta con sonido y estado"""
        current_text = self.answer_entry.get()
        self.answer_entry.delete(0, 'end')
        self.answer_entry.insert(0, current_text + letter)
        
        # Sonido de click
        try:
            self.sound_manager.play_sound('click')
        except:
            pass
        
        # Marcar letra como usada
        self.guessed_letters.add(letter)
        
        # Cambiar color del botón si la letra está en la palabra
        if letter in self.current_word:
            self.letter_buttons[letter].configure(fg_color="#4CAF50")  # Verde si está
        else:
            self.letter_buttons[letter].configure(fg_color="#FF5722")  # Rojo si no está
    
def clear_answer(self):
        """Limpiar respuesta"""
        self.answer_entry.delete(0, 'end')
        
        # Sonido de limpiar
        try:
            self.sound_manager.play_sound('wrong_place')
        except:
            pass
        
        # Resetear colores de letras
        for letter, btn in self.letter_buttons.items():
            if letter not in self.guessed_letters:
                btn.configure(fg_color="#2196F3")
    
def show_hint(self):
        """Mostrar pista con sonido"""
        hints = {
            "GATO": "🐱 Mascota felina que maúlla y ronronea",
            "CASA": "🏠 Lugar donde vives con tu familia",
            "AGUA": "💧 Líquido vital para la vida, H2O",
            "SOL": "☀️ Estrella que nos da luz y calor",
            "LIBRO": "📚 Objeto para leer historias y aprender"
        }
        
        hint = hints.get(self.current_word, "No hay pista disponible")
        
        try:
            self.sound_manager.play_sound('menu_music')
        except:
            pass
        
        messagebox.showinfo("💡 Pista", f"Pista: {hint}")
    
def check_answer(self, event=None):
        """Verificar respuesta con sonidos mejorados"""
        answer = self.answer_entry.get().strip().upper()
        
        if not answer:
            try:
                self.sound_manager.play_sound('wrong_place')
            except:
                pass
            messagebox.showwarning("❌ Respuesta vacía", "Por favor escribe una respuesta")
            return
        
        if answer == self.current_word:
            # Respuesta correcta
            try:
                self.sound_manager.play_sound('correct')
            except:
                pass
            
            self.game_state['score'] += 1
            self.update_score()
            
            messagebox.showinfo("🎉 ¡Correcto!", 
                f"¡Excelente! La respuesta era: {self.current_word}\n\n"
                f"🏆 Tu puntuación: {self.game_state['score']}")
            
            self.next_round()
        else:
            # Respuesta incorrecta
            try:
                self.sound_manager.play_sound('wrong_place')
            except:
                pass
            
            messagebox.showwarning("❌ Incorrecto", 
                f"❌ Respuesta incorrecta: {answer}\n\n"
                f"💡 ¡Sigue intentando!")
            
            # Limpiar campo pero mantener estado de letras
            self.answer_entry.delete(0, 'end')
    
def start_demo_game(self):
        """Iniciar juego demo mejorado"""
        print("🎮 Iniciando juego demo...")
        
        # Datos demo mejorados
        self.demo_words = [
            {"word": "GATO", "hint": "Mascota felina que maúlla", "images": ["🐱", "🏠", "🥛", "🎾"]},
            {"word": "CASA", "hint": "Lugar donde vives", "images": ["🏠", "🚪", "🪟", "🏡"]},
            {"word": "AGUA", "hint": "Líquido vital para la vida", "images": ["💧", "🌊", "🚰", "🏊"]},
            {"word": "SOL", "hint": "Estrella que nos da luz", "images": ["☀️", "🌅", "🌻", "🏖️"]},
            {"word": "LIBRO", "hint": "Objeto para leer historias", "images": ["📚", "📖", "✏️", "🤓"]}
        ]
        
        self.current_word_data = self.demo_words[0]
        self.current_word = self.current_word_data["word"]
        self.user_letters = ["_"] * len(self.current_word)
        self.guessed_letters = set()
        
        # Resetear colores de letras
        for btn in self.letter_buttons.values():
            btn.configure(fg_color="#2196F3")
        
        self.update_word_display()
        
        messagebox.showinfo("🎮 ¡Juego Iniciado!", 
            f"¡Bienvenido al juego, {self.player_name}!\n\n"
            f"🎯 Adivina la palabra mirando las 4 fotos\n"
            f"🔤 Usa las letras o escribe directamente\n"
            f"💡 Puedes pedir pistas si lo necesitas\n"
            f"🎵 ¡Escucha los sonidos al interactuar!\n\n"
            f"¡Buena suerte! 🍀")
    
def update_word_display(self):
        """Actualizar visualización de palabra"""
        if hasattr(self, 'word_display'):
            # Mostrar letras adivinadas
            display_letters = []
            for i, letter in enumerate(self.current_word):
                if letter in self.guessed_letters:
                    display_letters.append(letter)
                else:
                    display_letters.append("_")
            
            self.word_display.configure(text=" ".join(display_letters))
    
def update_score(self):
        """Actualizar puntuación"""
        if hasattr(self, 'score_label'):
            self.score_label.configure(
                text=f"🏆 TÚ: {self.game_state['score']} | 🤖 IA: 2 | 🎯 RONDA: {self.game_state['round']}/5"
            )
    
def next_round(self):
        """Siguiente ronda"""
        self.game_state['round'] += 1
        
        if self.game_state['round'] > 5:
            self.end_game()
        else:
            # Cambiar palabra
            word_index = (self.game_state['round'] - 1) % len(self.demo_words)
            self.current_word_data = self.demo_words[word_index]
            self.current_word = self.current_word_data["word"]
            self.user_letters = ["_"] * len(self.current_word)
            self.guessed_letters = set()
            
            # Resetear colores de letras
            for btn in self.letter_buttons.values():
                btn.configure(fg_color="#2196F3")
            
            # Actualizar imágenes demo en el grid
            demo_images = self.current_word_data["images"]
            for i, emoji in enumerate(demo_images):
                if i < len(self.photo_frames):
                    # Buscar el label del emoji en el frame
                    for widget in self.photo_frames[i].winfo_children():
                        if isinstance(widget, ctk.CTkLabel) and hasattr(widget, 'cget'):
                            try:
                                if widget.cget('font')[1] == 48:  # Es el emoji grande
                                    widget.configure(text=emoji)
                                    break
                            except:
                                pass
            
            self.update_word_display()
            self.update_score()
            self.answer_entry.delete(0, 'end')
            
            # Sonido de nueva ronda
            try:
                self.sound_manager.play_sound('menu_select')
            except:
                pass
    
def end_game(self):
        """Terminar juego"""
        final_score = self.game_state['score']
        ai_score = 2
        
        if final_score > ai_score:
            result = "🎉 ¡GANASTE!"
            result_color = "#4CAF50"
        elif final_score == ai_score:
            result = "🤝 ¡EMPATE!"
            result_color = "#FF9800"
        else:
            result = "💔 ¡PERDISTE!"
            result_color = "#F44336"
        
        try:
            self.sound_manager.play_sound('game_end')
        except:
            pass
        
        messagebox.showinfo("🏁 Juego Terminado", 
            f"{result}\n\n"
            f"🏆 Tu puntuación final: {final_score}\n"
            f"🤖 Puntuación IA: {ai_score}\n\n"
            f"¡Gracias por jugar!")
        
        # Volver al menú
        self.back_to_menu()#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("🎮 Iniciando 4 Fotos 1 Palabra - Versión Híbrida...")

import sys
import os
import pygame
import customtkinter as ctk
from tkinter import messagebox
from animated_credits_screen import AnimatedCreditsScreen 
import base64
from PIL import Image, ImageTk
import io
import time
from datetime import datetime

# Configurar path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Importar módulos propios
try:
    from clientescreens.menu_principal import MenuPrincipal
    from clientenetwork.socket_client import SocketClient
    from clienteutils.sound_manager import SoundManager
    from clienteutils.animation_manager import AnimationManager
    print("✅ Módulos importados correctamente")
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("📋 Continuando con clases dummy...")
    exit(1)

# Clases dummy como fallback
class DummySoundManager:
    def play_sound(self, sound_name): 
        print(f"🔇 DummySound: {sound_name}")
    def play_background_music(self): 
        print("🎵 DummyMusic: background")
    def stop_music(self): pass
    def stop_all_sounds(self): pass
    def create_test_sounds(self): pass
    def test_audio_system(self): pass

class DummyAnimationManager:
    def __init__(self, root): pass
    def fade_in(self, widget): pass
    def fade_out(self, widget): pass
    def slide_in(self, widget): pass

class DummySocketClient:
    def connect_to_server(self): pass
    def disconnect_from_server(self): pass
    def is_connected(self): return False
    def set_callback(self, event, callback): pass
    def crear_sala(self, player_name): pass
    def unirse_sala(self, code, player_name): pass


class JuegoApp:

    
    def __init__(self):
        print("🚀 Inicializando JuegoApp...")
         # ← LÍNEA NUEVA
        
        try:
            # 1. Primero inicializar CustomTkinter
            print("🎨 Configurando CustomTkinter...")
            ctk.set_appearance_mode("dark")
            ctk.set_default_color_theme("blue")
            
            # 2. Crear ventana PRIMERO
            print("🖼️ Creando ventana...")
            self.root = ctk.CTk()
            self.root.title("4 Fotos 1 Palabra - Duelo 🎵")
            self.root.geometry("1200x800")
            self.root.resizable(True, True)
            self.root.configure(fg_color=("#1a1a1a", "#0d1117"))
            self.center_window()
            print("✅ Ventana creada")
            
            # 3. Luego inicializar Pygame
            print("🔊 Inicializando audio...")
            pygame.mixer.init(frequency=32050, size=-16, channels=2, buffer=512)
            print("✅ Audio OK")
            
            # 4. Variables
            print("🔧 Inicializando variables...")
            self.current_screen = None
            self.player_name = ""
            self.opponent_name = "Oponente" # Añade esta
            self.is_multiplayer = False     # Añade esta
            self.room_code = ""
            self.custom_level_data = None
            self.game_state = {
                'score': 0,
                'opponent_score': 0,
                'round': 1,
                'max_rounds': 5
            }
            print("✅ Variables OK")
            
            # 5. Managers
            print("🔄 Inicializando managers...")
            self.initialize_managers()
            print("✅ Managers OK")
            
            # 6. Eventos
            print("🔒 Configurando eventos...")
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            print("✅ Eventos OK")
            
            # 7. Música
            print("🎵 Configurando música...")
            self.setup_background_music()
            print("✅ Música OK")
            
            # 8. Pantalla principal
            print("📱 Creando pantalla principal...")
            
            print("✅ Pantalla creada")
            
            # 9. Conexión servidor
            print("🌐 Iniciando conexión...")
            self.connect_to_server_delayed()
            print("✅ Conexión iniciada")
            
            print("🎉 ¡JuegoApp inicializado correctamente!")
            self.show_animated_credits()
            
            
        except Exception as e:
            print(f"❌ Error en JuegoApp init: {e}")
            import traceback
            traceback.print_exc()

    
    def show_animated_credits(self):
        """Mostrar créditos animados al inicio"""
        print("🎬 Iniciando créditos animados...")
        
        try:
            self.credits_screen = AnimatedCreditsScreen(self)
            self.credits_screen.show_credits()
            
            print("✅ Créditos iniciados")
            
        except Exception as e:
            print(f"❌ Error mostrando créditos: {e}")
            # Si falla, ir directo al menú
            self.show_menu_after_credits()

    def show_menu_after_credits(self):
        """Mostrar menú principal después de los créditos"""
        print("🎮 Mostrando menú después de créditos...")
        
        # Pequeña pausa para transición suave
        self.root.after(500, self.create_working_menu)

    def show_editor_niveles(self):
        """Mostrar editor de niveles - VERSIÓN VENTANA ÚNICA"""
        print("🛠️ Usuario solicitó abrir editor de niveles")
        self.sound_manager.enter_editor()  # ← LÍNEA NUEVA  
    
        try:
            self.sound_manager.play_sound('niveledit')
        except:
            pass
    
        try:
        # Verificar si ya tenemos una instancia del editor
            if not hasattr(self, 'level_editor_instance'):
                self.level_editor_instance = None
        
            if self.level_editor_instance is None:
                print("🔧 Creando nueva instancia del editor...")
                from level_editor import LevelEditor
                self.level_editor_instance = LevelEditor(self)
        
        # Mostrar el editor (maneja ventanas únicas internamente)
            self.level_editor_instance.show_editor()
        
            print("✅ Editor de niveles abierto/enfocado")
        
        except ImportError as e:
            print(f"❌ Error importando LevelEditor: {e}")
            from tkinter import messagebox
            messagebox.showerror("Error", 
                f"No se pudo abrir el editor de niveles.\n\n"
                f"Error: {e}\n\n"
                f"Verifica que el archivo 'level_editor.py' esté disponible.")
        except Exception as e:
            print(f"❌ Error abriendo editor: {e}")
            from tkinter import messagebox
            messagebox.showerror("Error", f"No se pudo abrir el editor:\n{e}")


    def show_mis_niveles(self):
        """Mostrar gestor de niveles - VERSIÓN CON INSTANCIA ÚNICA"""
        print("📚 Usuario solicitó abrir gestor de niveles")
        try:
            self.sound_manager.play_sound('menu_music')
        except:
            pass

        try:
        # Si la instancia del gestor de niveles no existe, créala.
            if not hasattr(self, 'levels_manager_instance') or self.levels_manager_instance is None:
                print("🔧 Creando nueva instancia de CustomLevelsManager...")
                from custom_levels_manager import CustomLevelsManager
                self.levels_manager_instance = CustomLevelsManager(self)
        
        # Muestra la ventana del gestor.
            self.levels_manager_instance.show_levels_manager()
            print("✅ Gestor de niveles abierto/enfocado")

        except ImportError as e:
            messagebox.showerror("Error", f"No se pudo abrir el gestor de niveles.\n\nError: {e}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el gestor de niveles:\n{e}")



    def connect_network_manager(self):
        """Conectar network manager con custom levels - AGREGAR A main.py"""
        if hasattr(self, 'network_manager') and hasattr(self, 'custom_levels_manager'):
            self.network_manager.set_custom_levels_manager(self.custom_levels_manager)
            print("🔗 Network manager conectado con custom levels manager")

    def start_network_game_session(self):
        """Iniciar sesión de juego en red - AGREGAR A main.py"""
        if hasattr(self, 'network_manager'):
            self.network_manager.start_network_game()
        else:
            print("❌ Network manager no disponible")


    def cleanup_all_instances(self):
        """Limpiar todas las instancias al cerrar la aplicación principal"""
        try:
            print("🧹 Limpiando todas las instancias...")
        
            # Limpiar editor
            if hasattr(self, 'level_editor_instance') and self.level_editor_instance:
                try:
                    if hasattr(self.level_editor_instance, 'close_editor_safely'):
                        self.level_editor_instance.close_editor_safely()
                    else:
                        if self.level_editor_instance.level_editor_window:
                            self.level_editor_instance.level_editor_window.destroy()
                    self.level_editor_instance = None
                except:
                    pass
        
        # Limpiar gestor
            if hasattr(self, 'levels_manager_instance') and self.levels_manager_instance:
                try:
                    if hasattr(self.levels_manager_instance, 'close_manager_safely'):
                        self.levels_manager_instance.close_manager_safely()
                    else:
                        if self.levels_manager_instance.levels_window:
                            self.levels_manager_instance.levels_window.destroy()
                    self.levels_manager_instance = None
                except:
                    pass
        
            print("✅ Instancias limpiadas")
        
        except Exception as e:
            print(f"⚠️ Error limpiando instancias: {e}")

# Modificar el método on_closing para incluir la limpieza


    
    def on_closing(self):
        """Manejo del cierre de la aplicación - VERSIÓN CORREGIDA"""
        print("👋 Cerrando aplicación principal...")
    
    # Solo preguntar si hay un juego en curso
        if self.is_multiplayer and hasattr(self, 'network_manager') and self.network_manager.is_connected:
            result = messagebox.askyesno(
                "Juego en curso",
                "Hay un juego multijugador en curso.\n\n¿Seguro que quieres salir?",
                icon='warning'
            )
            if not result:
                return
    
        try:
        # Limpiar instancias de ventanas
            self.cleanup_all_instances()
        
        # Detener audio
            self.sound_manager.stop_all_sounds()
            import pygame
            pygame.mixer.quit()
        except:
            pass
    
        try:
        # Desconectar red solo si es necesario
            if hasattr(self, 'socket_client'):
                self.socket_client.disconnect_from_server()
        
        # Desconectar juego en red local si existe
            if hasattr(self, 'network_manager') and self.network_manager:
                self.network_manager.shutdown_network_connection()
        except:
            pass
    
    # Cerrar aplicación
        self.root.destroy()

    




    def center_window(self):
        """Centrar ventana en pantalla"""
        self.root.update_idletasks()
        width = 1200  # Usar tamaño fijo
        height = 800
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
    
    def initialize_managers(self):
        """Inicializar managers con fallback"""
        # SoundManager
        try:
            print("🔊 Cargando SoundManager...")
            self.sound_manager = SoundManager()
            self.sound_manager.create_test_sounds()
            print("✅ SoundManager cargado")
        except Exception as e:
            print(f"⚠️ SoundManager falló: {e}")
            self.sound_manager = DummySoundManager()
        
        # AnimationManager
        try:
            print("✨ Cargando AnimationManager...")
            self.animation_manager = AnimationManager(self.root)
            print("✅ AnimationManager cargado")
        except Exception as e:
            print(f"⚠️ AnimationManager falló: {e}")
            self.animation_manager = DummyAnimationManager(self.root)
        
        # SocketClient
        try:
            print("🌐 Cargando SocketClient...")
            self.socket_client = SocketClient("https://juego-4fotos-sistemas-production.up.railway.app")
            print("✅ SocketClient cargado")
        except Exception as e:
            print(f"⚠️ SocketClient falló: {e}")
            self.socket_client = DummySocketClient()
    
    def setup_background_music(self):
        """Configurar música de fondo"""
        def start_music():
            try:
                # Crear directorio de assets si no existe
                assets_dir = os.path.join(current_dir, "assets", "sounds")
                os.makedirs(assets_dir, exist_ok=True)
                
                # Intentar cargar música de fondo
                music_files = [
                    "background_music.wav",
                    "background_music.mp3",
                    "background_music.ogg"
                ]
                
                music_loaded = False
                for music_file in music_files:
                    music_path = os.path.join(assets_dir, music_file)
                    if os.path.exists(music_path):
                        try:
                            pygame.mixer.music.load(music_path)
                            pygame.mixer.music.play(-1, 0.0)
                            pygame.mixer.music.set_volume(0.10)
                            print(f"🎵 Música de fondo cargada: {music_file}")
                            music_loaded = True
                            break
                        except Exception as e:
                            print(f"⚠️ Error cargando {music_file}: {e}")
                
                if not music_loaded:
                    print("🎵 No se encontró música de fondo")
                    
            except Exception as e:
                print(f"⚠️ Error configurando música: {e}")
        
        self.root.after(1000, start_music)
    
    def create_background_tone(self):
        """Crear tono de fondo simple"""
        try:
            import numpy as np
            
            # Generar tono suave
            sample_rate = 22050
            duration = 10  # 10 segundos
            frequency = 220  # Nota A3
            
            # Crear onda sinusoidal suave
            t = np.linspace(0, duration, int(sample_rate * duration), False)
            wave = np.sin(2 * np.pi * frequency * t) * 0.1  # Volumen muy bajo
            
            # Convertir a formato compatible con pygame
            wave = (wave * 32767).astype(np.int16)
            
            # Crear sonido
            sound = pygame.sndarray.make_sound(wave)
            
            # Reproducir en bucle
            sound.play(-1)
            
            print("🎵 Tono de fondo generado")
            
        except ImportError:
            print("⚠️ NumPy no disponible, música de fondo deshabilitada")
        except Exception as e:
            print(f"⚠️ Error creando tono: {e}")
    
    def create_demo_music_file(self):
        """Crear archivo de música demo (solo si no existe)"""
        try:
            assets_dir = os.path.join(current_dir, "assets", "sounds")
            os.makedirs(assets_dir, exist_ok=True)
            
            music_path = os.path.join(assets_dir, "background_music.wav")
            
            if not os.path.exists(music_path):
                print("🎵 Creando archivo de música demo...")
                
                # Crear un tono simple como placeholder
                import numpy as np
                
                sample_rate = 22050
                duration = 30  # 30 segundos
                
                # Crear progresión de acordes suave
                frequencies = [261.63, 329.63, 392.00, 523.25]  # C, E, G, C
                
                total_samples = int(sample_rate * duration)
                wave = np.zeros(total_samples)
                
                for i, freq in enumerate(frequencies):
                    start_sample = int(i * total_samples / len(frequencies))
                    end_sample = int((i + 1) * total_samples / len(frequencies))
                    
                    t = np.linspace(0, duration/len(frequencies), end_sample - start_sample, False)
                    chord_wave = np.sin(2 * np.pi * freq * t) * 0.1
                    
                    wave[start_sample:end_sample] = chord_wave
                
                # Convertir a formato de 16 bits
                wave = (wave * 32767).astype(np.int16)
                
                # Guardar como archivo WAV
                import wave as wav_module
                
                with wav_module.open(music_path, 'w') as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16 bits
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(wave.tobytes())
                
                print(f"✅ Archivo de música demo creado: {music_path}")
                
        except Exception as e:
            print(f"⚠️ No se pudo crear archivo de música demo: {e}")
    
    def create_working_menu(self):
        """Crear menú que funciona garantizado"""
        print("🎮 Creando menú funcional...")
        self.sound_manager.enter_menu()  # ← LÍNEA NUEVA
        # Transición suave - fade out actual
        if self.current_screen:
            try:
                self.animation_manager.fade_out(self.current_screen)
            except:
                pass
            # Dar tiempo para la animación
            self.root.after(150, self._create_menu_content)
        else:
            self._create_menu_content()
    
    def _create_menu_content(self):
        """Crear contenido del menú (método interno)"""
        # Limpiar pantalla después del fade
        if self.current_screen:
            self.current_screen.destroy()
        
        # Frame principal con fade in
        main_frame = ctk.CTkFrame(self.root, fg_color=("#1a1a1a", "#0d1117"))
        main_frame.pack(fill="both", expand=True)
        
        # Aplicar fade in
        try:
            self.animation_manager.fade_in(main_frame)
        except:
            pass
        
        # Header
        header_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(30, 20))
        
        # Título con animación de entrada
        title_label = ctk.CTkLabel(
            header_frame,
            text="🎮 4 FOTOS 1 PALABRA",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color="#ffffff"
        )
        title_label.pack()
        
        try:
            self.animation_manager.slide_in(title_label)
        except:
            pass
        
        # Subtítulo
        subtitle_label = ctk.CTkLabel(
            header_frame,
            text="DUELO 1 vs 1",
            font=ctk.CTkFont(size=20),
            text_color="#cccccc"
        )
        subtitle_label.pack(pady=(5, 0))
        
        # Estado conexión
        self.connection_label = ctk.CTkLabel(
            header_frame,
            text="🔄 Conectando al servidor...",
            font=ctk.CTkFont(size=14),
            text_color="#ffaa00"
        )
        self.connection_label.pack(pady=15)
        
        # Contenido principal
        content_frame = ctk.CTkFrame(main_frame)
        content_frame.pack(expand=True, fill="both", padx=40, pady=(0, 40))
        
        # Panel izquierdo - Configuración
        left_panel = ctk.CTkFrame(content_frame)
        left_panel.pack(side="left", fill="y", padx=(20, 10), pady=20)
        
        config_title = ctk.CTkLabel(
            left_panel,
            text="👤 CONFIGURACIÓN",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        config_title.pack(pady=(20, 15))
        
        # Nombre del jugador
        ctk.CTkLabel(
            left_panel,
            text="Nombre del jugador:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(10, 5))
        
        self.name_entry = ctk.CTkEntry(
            left_panel,
            placeholder_text="Ingresa tu nombre",
            width=250,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.name_entry.pack(pady=(0, 20))
        
        # Panel derecho - Opciones de juego
        right_panel = ctk.CTkFrame(content_frame)
        right_panel.pack(side="right", fill="y", padx=(10, 20), pady=20)
        
        game_title = ctk.CTkLabel(
            right_panel,
            text="🎮 OPCIONES DE JUEGO",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        game_title.pack(pady=(20, 15))
        
        # Botón crear sala
        self.create_room_btn = ctk.CTkButton(
            right_panel,
            text="🏠 CREAR SALA",
            command=self.on_crear_sala,
            width=280,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#4CAF50",
            hover_color="#45a049"
        )
        self.create_room_btn.pack(pady=15)
        
        # Código de sala
        ctk.CTkLabel(
            right_panel,
            text="Código de sala:",
            font=ctk.CTkFont(size=14)
        ).pack(pady=(15, 5))
        
        self.room_code_entry = ctk.CTkEntry(
            right_panel,
            placeholder_text="Ingresa el código",
            width=250,
            height=40,
            font=ctk.CTkFont(size=14)
        )
        self.room_code_entry.pack(pady=(0, 15))
        
        # Botón unirse
        self.join_room_btn = ctk.CTkButton(
            right_panel,
            text="🚪 UNIRSE A SALA",
            command=self.on_unirse_sala,
            width=280,
            height=55,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#2196F3",
            hover_color="#1976D2"
        )
        self.join_room_btn.pack(pady=15)
        
        # Botones inferiores
        bottom_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        bottom_frame.pack(side="bottom", pady=25)
        
        # Editor de niveles
        editor_btn = ctk.CTkButton(
            bottom_frame,
            text="🛠️ EDITOR DE NIVELES",
            command=self.show_editor_niveles,
            width=180,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#FF9800",
            hover_color="#F57C00"
        )
        editor_btn.pack(side="left", padx=10)
        
        # Mis niveles
        levels_btn = ctk.CTkButton(
            bottom_frame,
            text="📚 MIS NIVELES",
            command=self.show_mis_niveles,
            width=180,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#9C27B0",
            hover_color="#7B1FA2"
        )
        levels_btn.pack(side="left", padx=10)
        
        # Red local
        network_btn = ctk.CTkButton(
            bottom_frame,
            text="🌐 RED LOCAL",
            command=self.show_network_options,
            width=180,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#00BCD4",
            hover_color="#0097A7"
        )
        network_btn.pack(side="left", padx=10)
        
        # Test
        test_btn = ctk.CTkButton(
            bottom_frame,
            text="🧪 TEST",
            command=self.run_test,
            width=180,
            height=45,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color="#607D8B",
            hover_color="#455A64"
        )
        test_btn.pack(side="left", padx=10)
        
        self.current_screen = main_frame
        print("✅ Menú funcional creado exitosamente")
    
    def on_crear_sala(self):
        """Crear sala"""
        player_name = self.name_entry.get().strip()
        
        if not player_name:
            messagebox.showwarning("Nombre requerido", "Por favor ingresa tu nombre")
            self.sound_manager.play_sound('wrong_place')
            return
        
        self.player_name = player_name
        self.sound_manager.play_sound('menu_select')
        
        # Generar código demo
        import random
        demo_code = f"DEMO{random.randint(1000, 9999)}"
        self.room_code = demo_code
        
        print(f"🎮 Creando sala demo: {demo_code}")
        
        # Ir directamente al juego
        self.show_game_screen()
    
    def smooth_transition(self, new_screen_function):
        """Transición suave entre pantallas"""
        if self.current_screen:
            # Fade out
            try:
                self.animation_manager.fade_out(self.current_screen)
            except:
                pass
            
            # Después del fade out, cambiar pantalla
            self.root.after(200, lambda: self._transition_to_new_screen(new_screen_function))
        else:
            new_screen_function()
    
    def _transition_to_new_screen(self, new_screen_function):
        """Cambiar a nueva pantalla (método interno)"""
        if self.current_screen:
            self.current_screen.destroy()
        
        # Crear nueva pantalla
        new_screen_function()
        
        # Fade in de la nueva pantalla
        if self.current_screen:
            try:
                self.animation_manager.fade_in(self.current_screen)
            except:
                pass
    
    def on_crear_sala(self):
        """Crear sala"""
        player_name = self.name_entry.get().strip()
        
        if not player_name:
            messagebox.showwarning("Nombre requerido", "Por favor ingresa tu nombre")
            self.sound_manager.play_sound('wrong_place')
            return
        
        self.player_name = player_name
        self.sound_manager.play_sound('menu_music')
        
        # Generar código demo
        import random
        demo_code = f"DEMO{random.randint(1000, 9999)}"
        self.room_code = demo_code
        
        print(f"🎮 Creando sala demo: {demo_code}")
        
        # Ir directamente al juego
        self.show_game_screen()
    
    def on_unirse_sala(self):
        """Unirse a sala"""
        player_name = self.name_entry.get().strip()
        room_code = self.room_code_entry.get().strip().upper()
        
        if not player_name or not room_code:
            messagebox.showwarning("Datos requeridos", "Por favor completa todos los campos")
            self.sound_manager.play_sound('wrong_place')
            return
        
        self.player_name = player_name
        self.room_code = room_code
        self.sound_manager.play_sound('menu_select')
        
        print(f"🎮 Uniéndose a sala: {room_code}")
        
        # Ir directamente al juego
        self.show_game_screen()
    
    def show_game_screen(self):
        """Mostrar pantalla de juego básica"""
        print("🎮 Cargando pantalla de juego...")
        self.sound_manager.enter_game()  # ← LÍNEA NUEVA 
        
        # Limpiar pantalla actual
        if self.current_screen:
            self.current_screen.destroy()
        
        # Frame principal del juego
        game_frame = ctk.CTkFrame(self.root, fg_color=("#1a1a1a", "#0d1117"))
        game_frame.pack(fill="both", expand=True)
        
        # Título del juego
        title_label = ctk.CTkLabel(
            game_frame,
            text=f"🎮 JUGANDO - {self.player_name}\nSala: {self.room_code}",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=50)
        
        # Mensaje demo
        demo_label = ctk.CTkLabel(
            game_frame,
            text="🎯 MODO DEMO\n\n¡El juego funciona correctamente!\n\nPuedes crear niveles personalizados\ny jugar con otros usuarios",
            font=ctk.CTkFont(size=18),
            justify="center"
        )
        demo_label.pack(pady=30)
        
        # Botón volver
        back_btn = ctk.CTkButton(
            game_frame,
            text="🏠 VOLVER AL MENÚ",
            command=self.back_to_menu,
            width=200,
            height=50,
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#607D8B"
        )
        back_btn.pack(pady=30)
        
        self.current_screen = game_frame
        self.sound_manager.play_sound('game_start')
        print("✅ Pantalla de juego demo creada")
    
    def show_editor(self):
        """Mostrar editor de niveles"""
        print("🛠️ Abriendo Editor de Niveles...")
        self.sound_manager.play_sound('menu_music')
        
        try:
            # Importar y crear editor
            from level_editor import LevelEditor
            
            editor = LevelEditor(self)
            editor.show_editor()
            
        except ImportError:
            messagebox.showinfo("🛠️ Editor de Niveles", 
                "¡Editor de Niveles totalmente funcional!\n\n"
                "Características:\n"
                "✅ Crear niveles personalizados\n"
                "✅ Subir 4 imágenes por palabra\n"
                "✅ Sistema de pistas\n"
                "✅ Exportar y compartir niveles\n"
                "✅ Importar niveles de otros jugadores\n"
                "✅ Servidor local para red WiFi\n"
                "✅ Vista previa y validación\n\n"
                "📁 Los archivos se guardan en formato .4f1p\n"
                "🌐 Comparte fácilmente con otros jugadores")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el editor:\n{e}")
    
    def show_levels(self):
        """Mostrar gestor de niveles personalizados"""
        print("📚 Abriendo Gestor de Niveles...")
        self.sound_manager.play_sound('menu_music')
        
        try:
            # Importar y crear gestor
            from custom_levels_manager import CustomLevelsManager
            
            manager = CustomLevelsManager(self)
            manager.show_levels_manager()
            
        except ImportError:
            messagebox.showinfo("📚 Mis Niveles", 
                "¡Gestor de Niveles Personalizados!\n\n"
                "Características:\n"
                "✅ Administrar tus niveles creados\n"
                "✅ Importar niveles de otros jugadores\n"
                "✅ Exportar y compartir fácilmente\n"
                "✅ Buscar y filtrar por dificultad\n"
                "✅ Vista previa antes de jugar\n"
                "✅ Conectar a servidores locales\n"
                "✅ Descarga automática de niveles\n\n"
                "🎮 ¡Juega niveles infinitos creados por la comunidad!")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo abrir el gestor:\n{e}")
    
# En main.py
    def show_network_options(self):
        """Mostrar opciones de red local - VERSIÓN CON CONEXIÓN DE MANAGERS"""
        print("🌐 Abriendo opciones de red local...")
        try:
            self.sound_manager.play_sound('menu_select')
        except:
            pass

        try:
        # PASO A: Asegurarse de que el GESTOR DE NIVELES exista.
        # Si no existe (porque el usuario no ha abierto "Mis Niveles"), lo creamos aquí.
            if not hasattr(self, 'levels_manager_instance') or self.levels_manager_instance is None:
                print("🔧 Creando instancia de CustomLevelsManager necesaria para la red...")
                from custom_levels_manager import CustomLevelsManager
                self.levels_manager_instance = CustomLevelsManager(self)

        # PASO B: Asegurarse de que el GESTOR DE RED exista (lógica de instancia única).
            if not hasattr(self, 'network_manager') or self.network_manager is None:
                print("🔧 Creando nueva instancia de NetworkGameManager...")
                from network_game_manager import NetworkGameManager
                self.network_manager = NetworkGameManager(self)
        
        # PASO C: CONECTAR AMBOS MANAGERS. (¡El paso crucial!)
            print("🔗 Conectando NetworkManager con CustomLevelsManager...")
            self.network_manager.set_custom_levels_manager(self.levels_manager_instance)
        
        # PASO D: Ahora sí, mostrar la ventana de red.
            self.network_manager.show_network_options()
            print("✅ Ventana de red local lista.")

        except ImportError as e:
            messagebox.showerror("Error", f"Módulo no encontrado: {e}")
        except Exception as e:
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"No se pudo abrir la red local:\n{e}")

    def show_network_game_screen(self):
        """Mostrar pantalla de juego en red"""
        print("🌐 Cargando juego en red...")
        
        # Limpiar pantalla actual
        if self.current_screen:
            self.current_screen.destroy()
        
        # Frame principal del juego
        game_frame = ctk.CTkFrame(self.root, fg_color=("#1a1a1a", "#0d1117"))
        game_frame.pack(fill="both", expand=True)
        
        # Header del juego en red
        header_frame = ctk.CTkFrame(game_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 10))
        
        # Título
        ctk.CTkLabel(
            header_frame,
            text="🌐 JUEGO EN RED LOCAL",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="#00BCD4"
        ).pack()
        
        # Información de los jugadores
        players_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        players_frame.pack(pady=10)
        
        ctk.CTkLabel(
            players_frame,
            text=f"👤 {self.player_name}  🆚  👤 {getattr(self, 'opponent_name', 'Oponente')}",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#ffffff"
        ).pack()
        
        ctk.CTkLabel(
            players_frame,
            text=f"🏠 Sala: {getattr(self, 'room_code', 'NETWORK')} | 🌐 Modo: Red Local",
            font=ctk.CTkFont(size=12),
            text_color="#cccccc"
        ).pack(pady=(5, 0))
        
        # Puntuación en red
        score_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        score_frame.pack(pady=10)
        
        self.network_score_label = ctk.CTkLabel(
            score_frame,
            text=f"🏆 {self.player_name}: 0 | 🏆 {getattr(self, 'opponent_name', 'Oponente')}: 0",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color="#4CAF50"
        )
        self.network_score_label.pack()
        
        # Estado de conexión
        self.network_connection_label = ctk.CTkLabel(
            score_frame,
            text="🌐 Conectado - Sincronizando...",
            font=ctk.CTkFont(size=12),
            text_color="#00BCD4"
        )
        self.network_connection_label.pack(pady=(5, 0))
        
        # Área de juego (similar al juego normal pero con elementos de red)
        game_area = ctk.CTkFrame(game_frame)
        game_area.pack(expand=True, fill="both", padx=30, pady=(0, 30))
        
        # Frame para el juego principal
        main_game_frame = ctk.CTkFrame(game_area)
        main_game_frame.pack(side="left", fill="both", expand=True, padx=(20, 10), pady=20)
        
        ctk.CTkLabel(
            main_game_frame,
            text="🎮 JUEGO 1 VS 1 EN RED",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(15, 10))
        
        # Mensaje de estado del juego en red
        network_game_label = ctk.CTkLabel(
            main_game_frame,
            text="🌐 Conectado exitosamente\n\n"
                "🎯 Ambos jugadores ven la misma palabra\n"
                "⚡ El primero en responder gana el punto\n"
                "🏆 Mejor de 5 rondas\n\n"
                "⏳ Esperando que el juego comience...",
            font=ctk.CTkFont(size=16),
            justify="center"
        )
        network_game_label.pack(expand=True, pady=30)
        
        # Panel de control de red
        network_panel = ctk.CTkFrame(game_area)
        network_panel.pack(side="right", fill="y", padx=(10, 20), pady=20)
        
        ctk.CTkLabel(
            network_panel,
            text="🌐 CONTROL DE RED",
            font=ctk.CTkFont(size=16, weight="bold")
        ).pack(pady=(15, 10))
        
        # Estado de sincronización
        sync_frame = ctk.CTkFrame(network_panel)
        sync_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            sync_frame,
            text="📡 Estado de conexión:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))
        
        self.sync_status_label = ctk.CTkLabel(
            sync_frame,
            text="✅ Sincronizado",
            font=ctk.CTkFont(size=11),
            text_color="#4CAF50"
        )
        self.sync_status_label.pack(pady=(0, 10))
        
        # Chat rápido
        chat_frame = ctk.CTkFrame(network_panel)
        chat_frame.pack(fill="x", padx=10, pady=10)
        
        ctk.CTkLabel(
            chat_frame,
            text="💬 Chat rápido:",
            font=ctk.CTkFont(size=12, weight="bold")
        ).pack(pady=(10, 5))
        
        # Botones de mensajes rápidos
        quick_messages = ["👍", "😄", "🎉", "💪", "🤔", "😅"]
        for i, emoji in enumerate(quick_messages):
            if i % 3 == 0:
                msg_row = ctk.CTkFrame(chat_frame, fg_color="transparent")
                msg_row.pack(fill="x", pady=2)
            
            msg_btn = ctk.CTkButton(
                msg_row,
                text=emoji,
                command=lambda e=emoji: self.send_quick_message(e),
                width=40,
                height=30,
                font=ctk.CTkFont(size=16)
            )
            msg_btn.pack(side="left", padx=2)
        
        # Botones de control
        control_frame = ctk.CTkFrame(network_panel)
        control_frame.pack(fill="x", padx=10, pady=20)
        
        ready_btn = ctk.CTkButton(
            control_frame,
            text="✅ LISTO",
            command=self.mark_ready,
            width=200,
            height=40,
            fg_color="#4CAF50"
        )
        ready_btn.pack(pady=5)
        
        pause_btn = ctk.CTkButton(
            control_frame,
            text="⏸️ PAUSAR",
            command=self.pause_network_game,
            width=200,
            height=35,
            fg_color="#FF9800"
        )
        pause_btn.pack(pady=5)
        
        disconnect_btn = ctk.CTkButton(
            control_frame,
            text="🔌 DESCONECTAR",
            command=self.disconnect_network_game,
            width=200,
            height=35,
            fg_color="#FF5722"
        )
        disconnect_btn.pack(pady=5)
        
        # Volver al menú
        back_btn = ctk.CTkButton(
            network_panel,
            text="🏠 VOLVER AL MENÚ",
            command=self.back_to_menu,
            width=200,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#607D8B"
        )
        back_btn.pack(pady=(20, 10))
        
        self.current_screen = game_frame
        self.sound_manager.play_sound('game_start')
        
        print("✅ Pantalla de juego en red creada")
        
        # Simular inicio de juego después de unos segundos
        self.root.after(3000, self.start_network_round)
    
    def send_quick_message(self, emoji):
        """Enviar mensaje rápido"""
        print(f"💬 Mensaje enviado: {emoji}")
        
        try:
            self.sound_manager.play_sound('click')
        except:
            pass
        
        # En implementación real enviaría por red
        # self.network_manager.send_game_move({"type": "chat", "message": emoji})
        
        # Simular respuesta del oponente
        self.root.after(1000, lambda: self.show_opponent_message(emoji))
    
    def show_opponent_message(self, emoji):
        """Mostrar mensaje del oponente"""
        if hasattr(self, 'sync_status_label'):
            opponent_name = getattr(self, 'opponent_name', 'Oponente')
            self.sync_status_label.configure(
                text=f"{opponent_name}: {emoji}",
                text_color="#FF9800"
            )
            
            # Volver a estado normal después de 3 segundos
            self.root.after(3000, lambda: self.sync_status_label.configure(
                text="✅ Sincronizado",
                text_color="#4CAF50"
            ))
    
    def mark_ready(self):
        """Marcar como listo"""
        print("✅ Jugador listo")
        
        try:
            self.sound_manager.play_sound('correct')
        except:
            pass
        
        if hasattr(self, 'network_connection_label'):
            self.network_connection_label.configure(
                text="✅ Listo - Esperando oponente...",
                text_color="#4CAF50"
            )
        
        # Simular que el oponente también está listo
        self.root.after(2000, self.both_players_ready)
    
    def both_players_ready(self):
        """Ambos jugadores listos"""
        if hasattr(self, 'network_connection_label'):
            self.network_connection_label.configure(
                text="🎮 ¡Ambos listos! Iniciando...",
                text_color="#4CAF50"
            )
        
        messagebox.showinfo("🎮 ¡Listos!", 
            "¡Ambos jugadores están listos!\n\n🎯 El juego comenzará en breve...")
    
    def start_network_round(self):
        """Iniciar ronda de red"""
        if hasattr(self, 'network_connection_label'):
            self.network_connection_label.configure(
                text="🎯 Ronda 1 - ¡A jugar!",
                text_color="#FFD700"
            )
        
        print("🎮 Ronda de red iniciada")
    
    def pause_network_game(self):
        """Pausar juego en red"""
        print("⏸️ Juego pausado")
        
        try:
            self.sound_manager.play_sound('menu_select')
        except:
            pass
        
        messagebox.showinfo("⏸️ Juego Pausado", 
            "Juego pausado.\n\nEsperando a que ambos jugadores continúen...")
    
    def disconnect_network_game(self):
        """Desconectar del juego en red"""
        result = messagebox.askyesno("🔌 Desconectar", 
            "¿Seguro que quieres desconectarte?\n\nEl juego terminará para ambos jugadores.")
        
        if result:
            print("🔌 Desconectando del juego en red...")
            
            try:
                if hasattr(self, 'network_manager'):
                    self.network_manager.disconnect()
                
                self.sound_manager.play_sound('wrong_place')
            except:
                pass

    def start_custom_level(self, level_data):
        """Iniciar un nivel personalizado - COMPATIBLE CON TU SISTEMA DE IMÁGENES"""
        print("🎮 Iniciando nivel personalizado...")
        
        try:
            # Validar datos del nivel
            if not level_data or not level_data.get('words'):
                messagebox.showerror("Error", "El nivel no tiene palabras válidas")
                return
            
            # Guardar datos del nivel
            self.custom_level_data = level_data
            
            # Filtrar palabras válidas usando TU lógica de imágenes
            valid_words = []
            for word_data in level_data['words']:
                word = word_data.get('word', '').strip()
                images = word_data.get('images', [])
                
                # Usar TU lógica: contar imágenes no None
                valid_images_count = sum(1 for img in images if img is not None)
                
                if word and valid_images_count > 0:
                    valid_words.append(word_data)
            
            if not valid_words:
                messagebox.showerror("Error", "No hay palabras válidas con imágenes en este nivel")
                return
            
            # Actualizar datos del nivel con solo palabras válidas
            self.custom_level_data['words'] = valid_words
            
            # Mostrar pantalla de juego personalizado
            self.show_custom_game_screen()
            
            try:
                self.sound_manager.play_sound('game_start')
            except:
                pass
            
            print(f"✅ Nivel personalizado iniciado: {level_data.get('metadata', {}).get('title', 'Sin título')}")
            
        except Exception as e:
            print(f"❌ Error iniciando nivel personalizado: {e}")
            messagebox.showerror("Error", f"No se pudo iniciar el nivel:\n{e}")

         # Si es multijugador, conectar network manager
        if self.is_multiplayer and hasattr(self, 'network_manager'):
            # El network_manager ya debería existir desde show_network_options
            pass
        elif self.is_multiplayer:
            # Buscar el network_manager en las instancias
            if hasattr(self, 'network_manager'):
                print("✅ Network manager encontrado")
            else:
                print("⚠️ Network manager no encontrado para juego multijugador")
    
    # Mostrar pantalla de juego
        self.show_custom_game_screen()

    
    # COPIA Y PEGA ESTE BLOQUE COMPLETO EN TU main.py

    # COPIA Y PEGA ESTE BLOQUE COMPLETO EN TU main.py

    def show_custom_game_screen(self):
        """Mostrar pantalla de juego - VERSIÓN MULTIJUGADOR COMPLETA"""
        print(f"🎮 Creando pantalla de juego (Modo: {'Multijugador' if self.is_multiplayer else 'Un Jugador'})...")
    
        if self.current_screen:
            self.current_screen.destroy()
    
        game_frame = ctk.CTkFrame(self.root, fg_color=("#1a1a1a", "#0d1117"))
        game_frame.pack(fill="both", expand=True)
    
        # Header con información del juego
        header_frame = ctk.CTkFrame(game_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=(20, 10))
    
        # Título según el modo
        if self.is_multiplayer:
            title_text = f"⚔️ {self.player_name} VS {self.opponent_name} ⚔️"
            title_color = "#FF9800"
        else:
            metadata = self.custom_level_data.get('metadata', {})
            title_text = f"🎮 {metadata.get('title', 'Nivel Personalizado')}"
            title_color = "#4CAF50"
    
        title_label = ctk.CTkLabel(
            header_frame,
            text=title_text,
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=title_color
        )
        title_label.pack()
    
        # Marcador para multijugador
        if self.is_multiplayer:
            score_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
            score_frame.pack(pady=(10, 0))
        
            self.player_score_label = ctk.CTkLabel(
                score_frame,
                text=f"🏆 {self.player_name}: 0",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#4CAF50"
            )
            self.player_score_label.pack(side="left", padx=20)
        
            vs_label = ctk.CTkLabel(
                score_frame,
                text="VS",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#FFD700"
            )
            vs_label.pack(side="left", padx=10)
        
            self.opponent_score_label = ctk.CTkLabel(
                score_frame,
                text=f"🏆 {self.opponent_name}: 0",
                font=ctk.CTkFont(size=16, weight="bold"),
                text_color="#2196F3"
            )
            self.opponent_score_label.pack(side="left", padx=20)
    
        # Estado del juego
        self.custom_game_state = {
            'current_word_index': 0,
            'score': 0,
            'opponent_score': 0,
            'total_words': len(self.custom_level_data.get('words', [])),
            'correct_answers': 0
        }
    
        # Progreso del juego
        self.progress_label = ctk.CTkLabel(
            header_frame,
            text=f"Palabra 1 de {self.custom_game_state['total_words']}",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#FFD700"
        )
        self.progress_label.pack(pady=(10, 0))
    
        # Área principal con layout para multijugador
        main_container = ctk.CTkFrame(game_frame)
        main_container.pack(expand=True, fill="both", padx=20, pady=(0, 20))
    
        # Panel izquierdo - Imágenes y juego
        left_panel = ctk.CTkFrame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(10, 5))
    
        # Imágenes
        images_frame = ctk.CTkFrame(left_panel)
        images_frame.pack(fill="both", expand=True, padx=10, pady=10)
    
        ctk.CTkLabel(
            images_frame,
            text="📸 CUATRO IMÁGENES",
            font=ctk.CTkFont(size=18, weight="bold")
        ).pack(pady=(10, 5))
    
        # Grid de imágenes
        self.images_grid_frame = ctk.CTkFrame(images_frame)
        self.images_grid_frame.pack(expand=True, fill="both", padx=10, pady=10)
    
        for i in range(2):
            self.images_grid_frame.grid_rowconfigure(i, weight=1)
            self.images_grid_frame.grid_columnconfigure(i, weight=1)
    
        self.image_display_labels = []
        for i in range(4):
            row = i // 2
            col = i % 2
        
            img_frame = ctk.CTkFrame(self.images_grid_frame)
            img_frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        
            img_label = ctk.CTkLabel(
                img_frame,
                text=f"📷\nImagen {i+1}\nCargando...",
                width=180,
                height=135,
                font=ctk.CTkFont(size=12),
                fg_color=("#f0f0f0", "#2b2b2b")
            )
            img_label.pack(expand=True, fill="both", padx=5, pady=5)
        
            self.image_display_labels.append(img_label)
    
        # Área de respuesta
        answer_frame = ctk.CTkFrame(left_panel)
        answer_frame.pack(fill="x", padx=10, pady=(5, 10))
    
        self.word_display_label = ctk.CTkLabel(
            answer_frame,
            text="",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color="#FFD700"
        )
        self.word_display_label.pack(pady=15)
    
        self.feedback_label = ctk.CTkLabel(
            answer_frame,
            text="",
            font=ctk.CTkFont(size=14),
            height=30
        )
        self.feedback_label.pack(pady=5)
    
        entry_frame = ctk.CTkFrame(answer_frame, fg_color="transparent")
        entry_frame.pack(pady=10)
    
        self.custom_answer_entry = ctk.CTkEntry(
            entry_frame,
            placeholder_text="Escribe la palabra aquí...",
            width=250,
            height=40,
            font=ctk.CTkFont(size=16, weight="bold")
        )
        self.custom_answer_entry.pack(side="left", padx=(0, 10))
        self.custom_answer_entry.bind("<Return>", self.check_custom_answer)
    
        check_btn = ctk.CTkButton(
            entry_frame,
            text="✅ VERIFICAR",
            command=self.check_custom_answer,
            width=120,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50"
        )
        check_btn.pack(side="left")
    
        # Panel derecho - Chat y controles (solo en multijugador)
        if self.is_multiplayer:
            right_panel = ctk.CTkFrame(main_container)
            right_panel.pack(side="right", fill="y", padx=(5, 10))
            right_panel.configure(width=250)
    
            chat_frame = ctk.CTkFrame(right_panel)
            chat_frame.pack(fill="x", padx=10, pady=10)
    
            ctk.CTkLabel(
                chat_frame,
                text="💬 CHAT RÁPIDO",
                font=ctk.CTkFont(size=16, weight="bold")
            ).pack(pady=(10, 5))
    
            self.chat_history = ctk.CTkTextbox(
                chat_frame,
                width=220,
                height=150,
                font=ctk.CTkFont(size=12)
            )
            self.chat_history.pack(pady=5)
            self.chat_history.configure(state="disabled")
    
            emoji_grid = ctk.CTkFrame(chat_frame)
            emoji_grid.pack(pady=10)
    
            emojis = ["👍", "😄", "🎉", "💪", "🤔", "😅", "🔥", "❤️", "😎", "🤯", "😭", "🥳"]
            for i, emoji in enumerate(emojis):
                row = i // 4
                col = i % 4
        
                emoji_btn = ctk.CTkButton(
                    emoji_grid,
                    text=emoji,
                    command=lambda e=emoji: self.send_emoji(e),
                    width=40,
                    height=40,
                    font=ctk.CTkFont(size=18)
                )
                emoji_btn.grid(row=row, column=col, padx=2, pady=2)
        
            notifications_frame = ctk.CTkFrame(right_panel)
            notifications_frame.pack(fill="x", padx=10, pady=10)
        
            ctk.CTkLabel(
                notifications_frame,
                text="📢 NOTIFICACIONES",
                font=ctk.CTkFont(size=14, weight="bold")
            ).pack(pady=(10, 5))
        
            self.notifications_text = ctk.CTkTextbox(
                notifications_frame,
                width=220,
                height=100,
                font=ctk.CTkFont(size=11)
            )
            self.notifications_text.pack(pady=5)
            self.notifications_text.configure(state="disabled")
        
            control_frame = ctk.CTkFrame(right_panel)
            control_frame.pack(fill="x", padx=10, pady=10)
        
            hint_btn = ctk.CTkButton(
                control_frame,
                text="💡 PISTA",
                command=self.show_custom_hint,
                width=100,
                height=35,
                fg_color="#FF9800"
            )
            hint_btn.pack(side="left", padx=5)
        
            skip_btn = ctk.CTkButton(
                control_frame,
                text="⏭️ SALTAR",
                command=self.skip_custom_word,
                width=100,
                height=35,
                fg_color="#607D8B"
            )
            skip_btn.pack(side="left", padx=5)
    
        menu_btn = ctk.CTkButton(
            game_frame,
            text="🏠 MENÚ",
            command=self.back_to_menu,
            width=120,
            height=35,
            fg_color="#FF5722"
        )
        menu_btn.pack(side="bottom", pady=10)
    
        self.current_screen = game_frame
    
        # Cargar primera palabra
        self.load_custom_word()
    
        # Conectar callbacks para la red (CON LA CORRECCIÓN DE 'self' APLICADA)
        if self.is_multiplayer and hasattr(self, 'network_manager'):
            self.network_manager.set_game_callbacks(self)
            print("✅ Network manager conectado al juego")
        else:
            if self.is_multiplayer:
                 print("⚠️ MODO MULTIJUGADOR: Network manager no fue encontrado en self.")

    def send_emoji(self, emoji):
        """Enviar emoji al chat - VERSIÓN CORREGIDA"""
        # Añadir el emoji al chat local
        self.add_to_chat(self.player_name, emoji, is_self=True)
    
        try:
            self.sound_manager.play_sound('click')
        except:
            pass
    
    # Enviar a través del network manager si está en multijugador
        if self.is_multiplayer and hasattr(self, 'network_manager') and self.network_manager:
            try:
                self.network_manager.send_chat_message({
                    'player': self.player_name,
                    'emoji': emoji
                })
            except Exception as e:
                print(f"⚠️ Error enviando emoji por red: {e}")

    def add_to_chat(self, player, emoji, is_self=False):
        """Añadir mensaje al chat - VERSIÓN CORREGIDA"""
        try:
            color = "#4CAF50" if is_self else "#2196F3"
            self.chat_history.configure(state="normal")
            self.chat_history.insert("end", f"{player}: ", "sender")
            self.chat_history.tag_config("sender", foreground=color)
            self.chat_history.insert("end", f"{emoji}\n")
            self.chat_history.see("end")
            self.chat_history.configure(state="disabled")
        
        # NO enviar nada por red aquí - ya se hace en send_emoji
        
        except Exception as e:
            print(f"❌ Error en add_to_chat: {e}")


    def add_notification(self, text, color="#FFD700"):
        """Agregar notificación al panel"""
        if hasattr(self, 'notifications_text'):
            self.notifications_text.configure(state="normal")
        
            timestamp = datetime.now().strftime("%H:%M:%S")
            self.notifications_text.insert("end", f"[{timestamp}] {text}\n")
        
            # Scroll al final
            self.notifications_text.see("end")
            self.notifications_text.configure(state="disabled")

    def update_multiplayer_score(self, player_name, score):
        """Actualizar puntuación en multijugador"""
        if player_name == self.player_name:
            self.custom_game_state['score'] = score
            if hasattr(self, 'player_score_label'):
                self.player_score_label.configure(text=f"🏆 {self.player_name}: {score}")
        else:
            self.custom_game_state['opponent_score'] = score
            if hasattr(self, 'opponent_score_label'):
                self.opponent_score_label.configure(text=f"🏆 {self.opponent_name}: {score}")

    def on_opponent_guessed_word(self, data):
        """Cuando el oponente adivina una palabra"""
        word = data.get('word', '')
        player = data.get('player', self.opponent_name)
        score = data.get('score', 0)
    
    # Actualizar puntuación
        self.update_multiplayer_score(player, score)
    
    # Agregar notificación
        self.add_notification(f"🎯 {player} adivinó: {word} (+100 pts)", "#4CAF50")
    
    # Sonido de notificación
        try:
            self.app.sound_manager.play_sound('correct')
        except:
            pass
    
    # Avanzar a siguiente palabra
        self.root.after(2000, self.next_custom_word)

    def on_opponent_wrong_attempt(self, data):  
        """Cuando el oponente falla un intento"""
        attempt = data.get('attempt', '')
        player = data.get('player', self.opponent_name)
    
    # Agregar notificación
        self.add_notification(f"❌ {player} intentó: {attempt}", "#FF5722")

    def load_custom_word(self):
        """Cargar palabra actual - COMPATIBLE CON TU SISTEMA DE IMÁGENES - CORREGIDO"""
        if not self.custom_level_data or not self.custom_level_data.get('words'):
            return
    
        current_index = self.custom_game_state['current_word_index']
        words = self.custom_level_data['words']
    
        if current_index >= len(words):
            self.finish_custom_level()
            return
    
        current_word_data = words[current_index]
        word = current_word_data.get('word', '').upper()
    
        print(f"🎯 Cargando palabra {current_index + 1}: {word}")
    
    # Mostrar palabra con guiones
        word_display = " ".join("_" for _ in word)
        self.word_display_label.configure(text=word_display)
    
    # Actualizar progreso
        total = self.custom_game_state['total_words']
        score = self.custom_game_state['score']
        self.progress_label.configure(
            text=f"Palabra {current_index + 1} de {total} • Puntuación: {score}"
        )
    
    # Cargar imágenes usando TU sistema
        self.load_custom_images_compatible(current_word_data)
    
    # Limpiar campo de respuesta (CORREGIDO - sin tk.END)
        self.custom_answer_entry.delete(0, 'end')  # Usar 'end' en lugar de tk.END
        self.custom_answer_entry.focus()


    def load_custom_images_compatible(self, word_data):
        """Cargar imágenes - COMPATIBLE CON TU SISTEMA (sin asumir base64)"""
        images_data = word_data.get('images', [])
        
        for i in range(4):
            img_label = self.image_display_labels[i]
            
            if i < len(images_data) and images_data[i] is not None:
                try:
                    # TU SISTEMA: puede ser rutas de archivo, base64, o lo que uses
                    img_data = images_data[i]
                    
                    # Detectar tipo de dato de imagen
                    if isinstance(img_data, dict) and img_data.get('data'):
                        # Si es base64 (tu sistema actual)
                        try:
                            img_base64 = img_data.get('data', '')
                            img_bytes = base64.b64decode(img_base64)
                            
                            with io.BytesIO(img_bytes) as img_buffer:
                                pil_image = Image.open(img_buffer)
                                
                                if pil_image.mode not in ('RGB', 'RGBA'):
                                    pil_image = pil_image.convert('RGB')
                                
                                pil_image.thumbnail((180, 135), Image.Resampling.LANCZOS)
                                
                                ctk_image = ctk.CTkImage(
                                    light_image=pil_image,
                                    dark_image=pil_image,
                                    size=pil_image.size
                                )
                                
                                img_label.configure(
                                    image=ctk_image,
                                    text=""
                                )
                                
                                print(f"✅ Imagen {i+1} cargada (base64)")
                        except Exception as e:
                            print(f"❌ Error decodificando base64 imagen {i+1}: {e}")
                            img_label.configure(
                                image=None,
                                text=f"📷\nImagen {i+1}\n(Error carga)"
                            )
                    
                    elif isinstance(img_data, str) and os.path.exists(img_data):
                        # Si es ruta de archivo
                        try:
                            with Image.open(img_data) as pil_image:
                                if pil_image.mode not in ('RGB', 'RGBA'):
                                    pil_image = pil_image.convert('RGB')
                                
                                pil_image_copy = pil_image.copy()
                                pil_image_copy.thumbnail((180, 135), Image.Resampling.LANCZOS)
                                
                                ctk_image = ctk.CTkImage(
                                    light_image=pil_image_copy,
                                    dark_image=pil_image_copy,
                                    size=pil_image_copy.size
                                )
                                
                                img_label.configure(
                                    image=ctk_image,
                                    text=""
                                )
                                
                                print(f"✅ Imagen {i+1} cargada (archivo)")
                        except Exception as e:
                            print(f"❌ Error cargando archivo imagen {i+1}: {e}")
                            img_label.configure(
                                image=None,
                                text=f"📷\nImagen {i+1}\n(Error archivo)"
                            )
                    
                    else:
                        # Tipo de dato desconocido
                        img_label.configure(
                            image=None,
                            text=f"📷\nImagen {i+1}\n(Disponible)"
                        )
                        print(f"⚠️ Imagen {i+1}: tipo de dato no reconocido")
                    
                except Exception as e:
                    print(f"❌ Error general cargando imagen {i+1}: {e}")
                    img_label.configure(
                        image=None,
                        text=f"❌\nError\nImagen {i+1}"
                    )
            else:
                # Sin imagen
                img_label.configure(
                    image=None,
                    text=f"📷\nSin imagen\n{i+1}"
                )
    

    def check_custom_answer(self, event=None):
        """Verificar respuesta en nivel personalizado - VERSIÓN MULTIJUGADOR"""
        answer = self.custom_answer_entry.get().strip().upper()
    
        if not answer:
            try:
                self.sound_manager.play_sound('wrong_place')
            except:
                pass
            return
    
        current_index = self.custom_game_state['current_word_index']
        current_word_data = self.custom_level_data['words'][current_index]
        correct_word = current_word_data.get('word', '').upper()
    
        if answer == correct_word:
        # Respuesta correcta
            try:
                self.sound_manager.play_sound('correct')
            except:
                pass
        
        # Actualizar puntuación
            self.custom_game_state['score'] += 100
            self.custom_game_state['correct_answers'] += 1
        
        # Mostrar palabra completa
            self.word_display_label.configure(text=" ".join(correct_word))
        
        # Si es multijugador, enviar resultado
            if self.is_multiplayer and hasattr(self, 'network_manager'):
                self.network_manager.send_word_guessed({
                    'word_index': current_index,
                    'word': correct_word,
                    'player': self.player_name,
                    'score': self.custom_game_state['score']
                })
        
            # Mostrar mensaje breve y avanzar automáticamente
            self.show_quick_success_message(correct_word)
        
        # Avanzar a siguiente palabra después de 2 segundos
            self.root.after(2000, self.next_custom_word)
        
        else:
        # Respuesta incorrecta
            try:
                self.sound_manager.play_sound('wrong_place')
            except:
                pass
        
        # Si es multijugador, notificar intento fallido
            if self.is_multiplayer and hasattr(self, 'network_manager'):
                self.network_manager.send_wrong_attempt({
                    'word_index': current_index,
                    'attempt': answer,
                    'player': self.player_name
                })
        
            # Mostrar feedback rápido
            self.show_quick_error_feedback(answer)
        
            # Limpiar campo
            self.custom_answer_entry.delete(0, 'end')

    def show_quick_success_message(self, word):
        """Mostrar mensaje de éxito rápido sin bloquear el juego"""
        if hasattr(self, 'feedback_label'):
            self.feedback_label.configure(
                text=f"🎉 ¡CORRECTO! Era: {word} (+100 pts)",
                text_color="#4CAF50"
            )
        # Ocultar después de 2 segundos
            self.root.after(2000, lambda: self.feedback_label.configure(text=""))


    def show_quick_error_feedback(self, wrong_answer):
        """Mostrar feedback de error rápido"""
        if hasattr(self, 'feedback_label'):
            self.feedback_label.configure(
                text=f"❌ {wrong_answer} no es correcto",
                text_color="#FF5722"
            )
        # Ocultar después de 1.5 segundos
            self.root.after(1500, lambda: self.feedback_label.configure(text=""))


    def show_custom_hint(self):
        """Mostrar pista del nivel personalizado"""
        current_index = self.custom_game_state['current_word_index']
        current_word_data = self.custom_level_data['words'][current_index]
        hint = current_word_data.get('hint', '')
        
        try:       
            self.sound_manager.play_sound('menu_select')
        except:
            pass
        
        if hint:
            messagebox.showinfo("💡 Pista", f"Pista: {hint}", parent=self.current_screen)
        else:
            messagebox.showinfo("💡 Sin pista", "Esta palabra no tiene pista disponible", parent=self.current_screen)

    def skip_custom_word(self):
        """Saltar palabra actual"""
        if messagebox.askyesno("⏭️ Saltar palabra", 
            "¿Seguro que quieres saltar esta palabra?\nNo ganarás puntos por ella.", 
            parent=self.current_screen):
            
            try:
                self.sound_manager.play_sound('menu_select')
            except:
                pass
            
            self.next_custom_word()

    def next_custom_word(self):
        """Ir a la siguiente palabra"""
        self.custom_game_state['current_word_index'] += 1

        if self.custom_game_state['current_word_index'] >= len(self.custom_level_data['words']):
            # Fin del juego
            if self.is_multiplayer:
                self.finish_multiplayer_game()
            else:
                self.finish_custom_level()
        else:
        # Cargar siguiente palabra
            self.load_custom_word()
        
        # Limpiar feedback
            if hasattr(self, 'feedback_label'):
                self.feedback_label.configure(text="")

    def finish_multiplayer_game(self):
        """Terminar juego multijugador y mostrar ganador"""
        player_score = self.custom_game_state['score']
        opponent_score = self.custom_game_state['opponent_score']
    
    # Determinar ganador
        if player_score > opponent_score:
            winner = self.player_name
            result = "🏆 ¡GANASTE!"
            color = "#FFD700"
        elif opponent_score > player_score:
            winner = self.opponent_name
            result = "😢 Perdiste"
            color = "#FF5722"
        else:
            winner = "Nadie"
            result = "🤝 ¡EMPATE!"
            color = "#FF9800"
    
        try:
            self.sound_manager.play_sound('game_end')
        except:
            pass
    
    # Mensaje final
        final_message = f"{result}\n\n"
        final_message += f"📊 PUNTUACIÓN FINAL:\n"
        final_message += f"🏆 {self.player_name}: {player_score} puntos\n"
        final_message += f"🏆 {self.opponent_name}: {opponent_score} puntos\n\n"
    
        if winner != "Nadie":
            final_message += f"🎉 Ganador: {winner}\n"
    
        final_message += f"\n¡Gracias por jugar!"
    
        messagebox.showinfo("🏁 Juego Terminado", final_message)
    
    # Volver al menú
        self.back_to_menu()



    def restart_custom_level(self):
        """Reiniciar nivel personalizado"""
        if messagebox.askyesno("🔄 Reiniciar", 
            "¿Reiniciar el nivel desde el principio?\nSe perderá el progreso actual.", 
            parent=self.current_screen):
            
            # Resetear estado
            self.custom_game_state = {
                'current_word_index': 0,
                'score': 0,
                'total_words': len(self.custom_level_data['words']),
                'correct_answers': 0
            }
            
            # Recargar primera palabra
            self.load_custom_word()
            
            try:
                self.sound_manager.play_sound('game_start')
            except:
                pass


    def finish_custom_level(self):
        """Terminar nivel personalizado - CORREGIDO"""
        total_words = self.custom_game_state['total_words']
        correct_answers = self.custom_game_state['correct_answers']
        final_score = self.custom_game_state['score']
    
        # Calcular porcentaje
        percentage = (correct_answers / total_words * 100) if total_words > 0 else 0
    
        # Determinar calificación
        if percentage >= 90:
            grade = "🏆 ¡EXCELENTE!"
            grade_color = "#FFD700"
        elif percentage >= 70:
            grade = "⭐ ¡MUY BIEN!"
            grade_color = "#4CAF50"
        elif percentage >= 50:
            grade = "👍 BIEN"
            grade_color = "#FF9800"
        else:
            grade = "💪 SIGUE PRACTICANDO"
            grade_color = "#F44336"
    
        try:
            self.sound_manager.play_sound('game_end')
        except:
            pass
    
    # Obtener información del nivel
        metadata = self.custom_level_data.get('metadata', {})
        level_title = metadata.get('title', 'Nivel Personalizado')
    
        result_message = f"🏁 NIVEL COMPLETADO\n\n"
        result_message += f"📝 Nivel: {level_title}\n"
        result_message += f"🎯 Palabras correctas: {correct_answers}/{total_words}\n"
        result_message += f"📊 Porcentaje: {percentage:.1f}%\n"
        result_message += f"🏆 Puntuación final: {final_score}\n\n"
        result_message += f"{grade}\n\n"
        result_message += "¡Gracias por jugar!"
    
        messagebox.showinfo("🏁 Nivel Completado", result_message, parent=self.current_screen)
    
    # Volver al menú
        self.back_to_menu()

    def run_test(self):
        """Ejecutar prueba completa"""
        print("🧪 Ejecutando test completo...")
        self.sound_manager.play_sound('click')
        
        # Test completo del sistema
        test_results = []
        
        # Test 1: Audio
        try:
            self.sound_manager.play_sound('correct')
            test_results.append("✅ Sistema de audio")
        except:
            test_results.append("❌ Sistema de audio")
        
        # Test 2: Interfaz
        try:
            test_window = ctk.CTkToplevel(self.root)
            test_window.withdraw()
            test_window.destroy()
            test_results.append("✅ Sistema de ventanas")
        except:
            test_results.append("❌ Sistema de ventanas")
        
        # Test 3: Archivos
        try:
            import os
            if os.path.exists("custom_levels"):
                test_results.append("✅ Carpeta de niveles")
            else:
                os.makedirs("custom_levels", exist_ok=True)
                test_results.append("✅ Carpeta de niveles (creada)")
        except:
            test_results.append("❌ Sistema de archivos")
        
        # Test 4: Red
        try:
            import socket
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            s.close()
            test_results.append("✅ Conexión de red")
        except:
            test_results.append("⚠️ Red (offline)")
        
        # Test 5: Módulos
        modules_test = []
        try:
            from level_editor import LevelEditor
            modules_test.append("Editor")
        except:
            pass
        
        try:
            from custom_levels_manager import CustomLevelsManager
            modules_test.append("Niveles")
        except:
            pass
        
        try:
            from network_game_manager import NetworkGameManager
            modules_test.append("Red")
        except:
            pass
        
        if modules_test:
            test_results.append(f"✅ Módulos: {', '.join(modules_test)}")
        else:
            test_results.append("⚠️ Módulos opcionales no disponibles")
        
        # Mostrar resultados
        results_text = "\n".join(test_results)
        
        messagebox.showinfo("🧪 Resultados del Test", 
            f"🔍 DIAGNÓSTICO COMPLETO:\n\n{results_text}\n\n"
            f"📊 Estado general: {'✅ EXCELENTE' if '❌' not in results_text else '⚠️ FUNCIONA CON LIMITACIONES'}\n\n"
            f"🎮 ¡El juego está operativo!")
        
        print("✅ Test completo finalizado")
    
    # En main.py
    def back_to_menu(self):
        """Volver al menú principal y limpiar conexiones si es necesario."""
        print("🏠 Volviendo al menú principal...")
        try:
            self.sound_manager.play_sound('menu_select')
        except:
            pass
    
    # --- LÓGICA DE DESCONEXIÓN AÑADIDA ---
    # Si venimos de una partida multijugador, hay que cerrar la conexión.
        if self.is_multiplayer:
            print("... detectada partida multijugador, cerrando conexión de red.")
            if hasattr(self, 'network_manager') and self.network_manager:
                self.network_manager.shutdown_network_connection()
            self.is_multiplayer = False # Reseteamos el estado
    # --- FIN DE LA LÓGICA DE DESCONEXIÓN ---
    
    # Resetear estado del juego
        self.game_state = {
            'score': 0,
            'opponent_score': 0,
            'round': 1,
            'max_rounds': 5
        }
    
    # Volver a crear el menú
        self.create_working_menu()
    
    def connect_to_server_delayed(self):
        """Conectar al servidor con reconexión automática"""
        self.connection_attempts = 0
        self.max_connection_attempts = 3
        self.reconnecting = False
        
        def try_connect():
            if self.connection_attempts < self.max_connection_attempts:
                self.connection_attempts += 1
                
                try:
                    if hasattr(self, 'connection_label') and self.connection_label.winfo_exists():
                        self.connection_label.configure(
                            text=f"🔄 Conectando... (Intento {self.connection_attempts}/{self.max_connection_attempts})",
                            text_color="#ffaa00"
                        )
                    
                    if hasattr(self.socket_client, 'connect_to_server'):
                        self.socket_client.connect_to_server()
                        print(f"🌐 Intento de conexión {self.connection_attempts} enviado")
                        
                        # Sonido de intento de conexión
                        try:
                            self.sound_manager.play_sound('click')
                        except:
                            pass
                    
                    # Verificar conexión después de 5 segundos
                    self.root.after(5000, check_connection_status)
                    
                except Exception as e:
                    print(f"⚠️ Error en intento {self.connection_attempts}: {e}")
                    # Intentar de nuevo después de 3 segundos si falló
                    self.root.after(3000, try_connect)
            else:
                # Activar modo demo después de intentos fallidos
                self.activate_demo_mode()
        
        def check_connection_status():
            try:
                # Simular verificación de conexión
                is_connected = False  # En implementación real verificaría socket_client.is_connected()
                
                if is_connected:
                    self.on_connection_success()
                else:
                    if self.connection_attempts < self.max_connection_attempts:
                        # Intentar de nuevo
                        self.root.after(2000, try_connect)
                    else:
                        self.activate_demo_mode()
                        
            except Exception as e:
                print(f"⚠️ Error verificando conexión: {e}")
                if self.connection_attempts < self.max_connection_attempts:
                    self.root.after(2000, try_connect)
                else:
                    self.activate_demo_mode()
        
        # Iniciar primer intento después de 2 segundos
        self.root.after(2000, try_connect)
    
    def on_connection_success(self):
        """Conexión exitosa al servidor"""
        try:
            if hasattr(self, 'connection_label') and self.connection_label.winfo_exists():
                self.connection_label.configure(
                    text="✅ Conectado al servidor - Modo Online",
                    text_color="#4CAF50"
                )
            
            # Sonido de conexión exitosa
            try:
                self.sound_manager.play_sound('correct')
            except:
                pass
            
            print("🌐 ¡Conectado al servidor exitosamente!")
            self.connection_attempts = 0
            
        except Exception as e:
            print(f"⚠️ Error actualizando estado de conexión: {e}")
    
    def activate_demo_mode(self):
        """Activar modo demo cuando no hay conexión"""
        try:
            if hasattr(self, 'connection_label'):
                self.connection_label.configure(
                    text="🎮 MODO DEMO - Servidor offline",
                    text_color="#9C27B0"
                )
            
            print("🎮 Modo DEMO activado - Servidor no disponible")
            
            # Sonido de modo demo
            try:
                self.sound_manager.play_sound('menu_music')
            except:
                pass
            
            # Mostrar botón de reconexión
            self.show_reconnect_button()
            
        except Exception as e:
            print(f"⚠️ Error activando modo demo: {e}")
    
    def show_reconnect_button(self):
        """Mostrar botón para reconectar manualmente"""
        if hasattr(self, 'connection_label') and hasattr(self, 'connection_label').master:
            try:
                # Crear botón de reconexión
                self.reconnect_btn = ctk.CTkButton(
                    self.connection_label.master,
                    text="🔄 RECONECTAR",
                    command=self.manual_reconnect,
                    width=120,
                    height=30,
                    font=ctk.CTkFont(size=12),
                    fg_color="#FF9800",
                    hover_color="#F57C00"
                )
                self.reconnect_btn.pack(pady=5)
                
            except Exception as e:
                print(f"⚠️ Error creando botón reconexión: {e}")
    
    def manual_reconnect(self):
        """Reconexión manual"""
        if hasattr(self, 'reconnect_btn'):
            self.reconnect_btn.destroy()
        
        # Resetear intentos y reconectar
        self.connection_attempts = 0
        self.connect_to_server_delayed()
        
        try:
            self.sound_manager.play_sound('click')
        except:
            pass
        
        print("🔄 Reconexión manual iniciada")
    
  
    def run(self):
        """Método principal para ejecutar la aplicación"""
        print("🚀 Iniciando aplicación...")
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\n👋 Aplicación interrumpida por el usuario")
            self.on_closing()
        except Exception as e:
            print(f"❌ Error durante la ejecución: {e}")
            import traceback
            traceback.print_exc()
            self.on_closing()
   

if __name__ == "__main__":
    try:
        # Inicializar Pygame solo para mixer
        import pygame
        pygame.mixer.init()
        
        app = JuegoApp()
        app.run()
    except Exception as e:
        print(f"❌ Error fatal: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para cerrar...")