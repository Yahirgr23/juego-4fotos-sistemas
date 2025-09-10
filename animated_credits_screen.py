#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import customtkinter as ctk
import tkinter as tk
import pygame
import numpy as np
import threading
import time
import math
import random

class AnimatedCreditsScreen:
    def __init__(self, parent_app):
        self.app = parent_app
        self.credits_window = None
        self.animation_running = False
        self.current_animation_step = 0
        self.total_animation_steps = 9
        self.synth_sounds = {}
        
        # Colores para animaciones
        self.colors = {
            'primary': "#4CAF50",
            'secondary': "#2196F3", 
            'accent': "#FF9800",
            'gold': "#FFD700",
            'purple': "#9C27B0",
            'cyan': "#00BCD4"
        }
        
        # Crear sonidos sintéticos
        self.create_synthetic_sounds()
    
    def create_synthetic_sounds(self):
        """Crear sonidos sintéticos usando pygame y numpy"""
        print("🎵 Creando sonidos sintéticos para créditos...")
        
        try:
            # Configuración de audio
            sample_rate = 22050
            
            # 1. Sonido de aparición (sweep up)
            duration = 0.5
            frames = int(duration * sample_rate)
            sweep_up = np.zeros((frames, 2))
            
            for i in range(frames):
                progress = i / frames
                freq = 220 + (880 * progress)  # De 220Hz a 1100Hz
                envelope = np.sin(np.pi * progress) * 0.3  # Envelope suave
                wave = np.sin(2 * np.pi * freq * i / sample_rate) * envelope
                sweep_up[i] = [wave, wave]
            
            self.synth_sounds['appear'] = pygame.sndarray.make_sound((sweep_up * 32767).astype(np.int16))
            
            # 2. Sonido de brillo (chime)
            duration = 0.8
            frames = int(duration * sample_rate)
            chime = np.zeros((frames, 2))
            
            freqs = [523, 659, 784, 1047]  # C5, E5, G5, C6 (acorde C mayor)
            for i in range(frames):
                progress = i / frames
                envelope = np.exp(-progress * 3) * 0.2  # Decay exponencial
                
                wave = 0
                for freq in freqs:
                    wave += np.sin(2 * np.pi * freq * i / sample_rate)
                
                wave *= envelope
                chime[i] = [wave, wave]
            
            self.synth_sounds['sparkle'] = pygame.sndarray.make_sound((chime * 32767).astype(np.int16))
            
            # 3. Sonido de whoosh (viento)
            duration = 1.0
            frames = int(duration * sample_rate)
            whoosh = np.zeros((frames, 2))
            
            for i in range(frames):
                progress = i / frames
                # Ruido filtrado que simula viento
                noise = np.random.normal(0, 0.1)
                freq = 150 + (100 * np.sin(progress * np.pi * 4))
                envelope = np.sin(np.pi * progress) * 0.15
                
                wave = noise * envelope + np.sin(2 * np.pi * freq * i / sample_rate) * envelope * 0.3
                whoosh[i] = [wave, wave]
            
            self.synth_sounds['whoosh'] = pygame.sndarray.make_sound((whoosh * 32767).astype(np.int16))
            
            # 4. Sonido de éxito (fanfare corto)
            duration = 1.2
            frames = int(duration * sample_rate)
            fanfare = np.zeros((frames, 2))
            
            melody = [523, 659, 784, 1047, 1319]  # C5, E5, G5, C6, E6
            note_duration = frames // len(melody)
            
            for note_idx, freq in enumerate(melody):
                start_frame = note_idx * note_duration
                end_frame = min(start_frame + note_duration, frames)
                
                for i in range(start_frame, end_frame):
                    note_progress = (i - start_frame) / note_duration
                    envelope = np.sin(np.pi * note_progress) * 0.25
                    wave = np.sin(2 * np.pi * freq * i / sample_rate) * envelope
                    fanfare[i] = [wave, wave]
            
            self.synth_sounds['fanfare'] = pygame.sndarray.make_sound((fanfare * 32767).astype(np.int16))
            
            # 5. Sonido de ambiente (pad suave)
            duration = 3.0
            frames = int(duration * sample_rate)
            ambient = np.zeros((frames, 2))
            
            base_freqs = [65, 82, 98, 131]  # C2, E2, G2, C3
            for i in range(frames):
                progress = i / frames
                envelope = 0.08  # Muy suave
                
                wave = 0
                for freq in base_freqs:
                    wave += np.sin(2 * np.pi * freq * i / sample_rate)
                    wave += np.sin(2 * np.pi * freq * 2 * i / sample_rate) * 0.3  # Harmónico
                
                wave *= envelope
                ambient[i] = [wave, wave]
            
            self.synth_sounds['ambient'] = pygame.sndarray.make_sound((ambient * 32767).astype(np.int16))
            
            print(f"✅ {len(self.synth_sounds)} sonidos sintéticos creados")
            
        except Exception as e:
            print(f"❌ Error creando sonidos sintéticos: {e}")
            # Crear sonidos silenciosos como fallback
            silent = np.zeros((1000, 2), dtype=np.int16)
            silent_sound = pygame.sndarray.make_sound(silent)
            for sound_name in ['appear', 'sparkle', 'whoosh', 'fanfare', 'ambient']:
                self.synth_sounds[sound_name] = silent_sound
    
    def play_synth_sound(self, sound_name, volume=0.5):
        """Reproducir sonido sintético"""
        try:
            if sound_name in self.synth_sounds:
                sound = self.synth_sounds[sound_name]
                sound.set_volume(volume)
                sound.play()
                print(f"🎵 Reproduciendo sonido sintético: {sound_name}")
        except Exception as e:
            print(f"❌ Error reproduciendo sonido sintético: {e}")
    
    def show_credits(self):
        """Mostrar pantalla de créditos animada"""
        print("🎬 Iniciando pantalla de créditos animada...")
        
        # Crear ventana de créditos
        self.credits_window = ctk.CTkToplevel(self.app.root)
        self.credits_window.title("4 Fotos 1 Palabra - Créditos")
        self.credits_window.geometry("1000x700")
        self.credits_window.resizable(False, False)
        self.credits_window.configure(fg_color="#0a0a0a")
        
        # Centrar ventana
        self.center_credits_window()
        
        # Hacer ventana modal y en primer plano
        self.credits_window.transient(self.app.root)
        self.credits_window.grab_set()
        self.credits_window.attributes('-topmost', True)
        
        # Frame principal con fondo negro
        self.main_frame = ctk.CTkFrame(
            self.credits_window, 
            fg_color="#000000",
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Configurar grid para centrado
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Container para elementos animados
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        self.content_frame.grid(row=0, column=0, sticky="nsew")
        
        # Lista para almacenar elementos animados
        self.animated_elements = []
        
        # Iniciar animación
        self.animation_running = True
        self.current_animation_step = 0
        
        # Reproducir sonido ambiente de fondo
        self.play_synth_sound('ambient', 0.3)
        
        # Iniciar secuencia de animación
        self.start_animation_sequence()
        
        # Configurar evento de cierre
        self.credits_window.protocol("WM_DELETE_WINDOW", self.close_credits)
        
        # Auto-cerrar después de 12 segundos
        self.credits_window.after(12000, self.auto_close_credits)
        
        print("✅ Pantalla de créditos iniciada")
    
    def center_credits_window(self):
        """Centrar ventana de créditos"""
        self.credits_window.update_idletasks()
        width = 1000
        height = 700
        x = (self.credits_window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.credits_window.winfo_screenheight() // 2) - (height // 2)
        self.credits_window.geometry(f"{width}x{height}+{x}+{y}")
    
    def start_animation_sequence(self):
        """Iniciar secuencia de animación paso a paso"""
        if not self.animation_running or not self.credits_window.winfo_exists():
            return
    
        print(f"🎬 Paso de animación: {self.current_animation_step + 1}/{self.total_animation_steps}")
    
        if self.current_animation_step == 0:
            self.animate_title_appear()
        elif self.current_animation_step == 1:
            self.animate_subtitle_appear()
        elif self.current_animation_step == 2:
            self.animate_sparkles()
        elif self.current_animation_step == 3:
            self.animate_developer_1()
        elif self.current_animation_step == 4:
            self.animate_developer_2()
        elif self.current_animation_step == 5:
            self.animate_developer_3()  # ← NUEVO PASO
        elif self.current_animation_step == 6:
            self.animate_shine_effect()
        elif self.current_animation_step == 7:
            self.animate_final_message()
        elif self.current_animation_step == 8:  # ← Incrementado
            self.animate_skip_button()
    
        self.current_animation_step += 1
    
    # Programar siguiente paso
        if self.current_animation_step < 9:  # ← Incrementado total de pasos
            delay = 1500 if self.current_animation_step <= 2 else 1200
            self.credits_window.after(delay, self.start_animation_sequence)
    
    def animate_title_appear(self):
        """Animación del título principal"""
        self.play_synth_sound('appear', 0.6)
        
        # Título principal con efecto de aparición
        title_label = ctk.CTkLabel(
            self.content_frame,
            text="🎮 4 FOTOS 1 PALABRA",
            font=ctk.CTkFont(size=42, weight="bold"),
            text_color=self.colors['gold']
        )
        title_label.place(relx=0.5, rely=0.2, anchor="center")
        
        self.animated_elements.append(title_label)
        
        # Efecto de aparición gradual
        self.fade_in_element(title_label, 0)
    
    def animate_subtitle_appear(self):
        """Animación del subtítulo"""
        self.play_synth_sound('whoosh', 0.4)
        
        subtitle_label = ctk.CTkLabel(
            self.content_frame,
            text="DUELO 1 vs 1",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors['cyan']
        )
        subtitle_label.place(relx=0.5, rely=0.3, anchor="center")
        
        self.animated_elements.append(subtitle_label)
        self.fade_in_element(subtitle_label, 0)
    
    def animate_sparkles(self):
        """Animación de destellos"""
        self.play_synth_sound('sparkle', 0.5)
        
        # Crear múltiples elementos de destello
        sparkle_positions = [
            (0.15, 0.25), (0.85, 0.25), (0.25, 0.15), (0.75, 0.15),
            (0.1, 0.35), (0.9, 0.35), (0.5, 0.1)
        ]
        
        for i, (x, y) in enumerate(sparkle_positions):
            sparkle = ctk.CTkLabel(
                self.content_frame,
                text="✨",
                font=ctk.CTkFont(size=20),
                text_color=self.colors['gold']
            )
            sparkle.place(relx=x, rely=y, anchor="center")
            
            self.animated_elements.append(sparkle)
            
            # Animación con delay escalonado
            self.credits_window.after(i * 100, lambda s=sparkle: self.pulse_element(s))
    
    def animate_developer_1(self):
        """Animación del primer desarrollador"""
        self.play_synth_sound('appear', 0.5)
    
    # Texto "Desarrollado por:"
        dev_label = ctk.CTkLabel(
            self.content_frame,
            text="💻 DESARROLLADO POR:",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors['primary']
        )
        dev_label.place(relx=0.5, rely=0.42, anchor="center")  # ← Subido un poco
    
    # Nombre del primer desarrollador - CENTRADO
        name1_label = ctk.CTkLabel(
            self.content_frame,
            text="🌟 YAHIR GAMBOA ROSAS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['secondary']
        )
        name1_label.place(relx=0.5, rely=0.48, anchor="center")  # ← CENTRADO
    
        self.animated_elements.extend([dev_label, name1_label])
    
    # Animaciones con delay - SIN deslizamiento, solo fade in
        self.fade_in_element(dev_label, 0)
        self.credits_window.after(300, lambda: self.fade_in_element(name1_label, 0))


    def animate_developer_2(self):
        """Animación del segundo desarrollador"""
        self.play_synth_sound('appear', 0.5)
    
    # Nombre del segundo desarrollador - CENTRADO
        name2_label = ctk.CTkLabel(
            self.content_frame,
            text="🚀 ANGEL JOATZIN FONSECA",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['purple']
        )
        name2_label.place(relx=0.5, rely=0.54, anchor="center")  # ← CENTRADO
    
        self.animated_elements.append(name2_label)
    # Solo fade in, sin deslizamiento
        self.fade_in_element(name2_label, 0)


    def animate_developer_3(self):
        """Animación del tercer desarrollador"""
        self.play_synth_sound('appear', 0.5)
    
    # Nombre del tercer desarrollador - CENTRADO
        name3_label = ctk.CTkLabel(
            self.content_frame,
            text="⚡ EDUARDO MÁRQUEZ PRISCILIANO",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['accent']  # Color naranja
        )
        name3_label.place(relx=0.5, rely=0.6, anchor="center")  # ← CENTRADO
    
        self.animated_elements.append(name3_label)
        self.fade_in_element(name3_label, 0)


    
    
    def animate_shine_effect(self):
        """Efecto de brillo en los nombres"""
        self.play_synth_sound('fanfare', 0.6)
    
    # Crear efecto de brillo que se mueve - REPOSICIONADO
        shine_label = ctk.CTkLabel(
            self.content_frame,
            text="✨ ⭐ ✨",
            font=ctk.CTkFont(size=24),
            text_color=self.colors['gold']
        )
        shine_label.place(relx=0.5, rely=0.52, anchor="center")  # ← Centrado entre nombres
    
        self.animated_elements.append(shine_label)
        self.bounce_element(shine_label)

    
    def animate_final_message(self):
        """Animación del mensaje final"""
        self.play_synth_sound('whoosh', 0.4)
    
        final_label = ctk.CTkLabel(
            self.content_frame,
            text="🎉 ¡GRACIAS POR JUGAR! 🎉",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors['accent']
        )
        final_label.place(relx=0.5, rely=0.72, anchor="center")  # ← Bajado para dar espacio
    
    # Año
        year_label = ctk.CTkLabel(
            self.content_frame,
            text="© 2024",
            font=ctk.CTkFont(size=14),
            text_color=self.colors['primary']
        )
        year_label.place(relx=0.5, rely=0.78, anchor="center")  # ← Bajado
    
        self.animated_elements.extend([final_label, year_label])
    
        self.fade_in_element(final_label, 0)
        self.credits_window.after(500, lambda: self.fade_in_element(year_label, 0))
    
    def animate_skip_button(self):
        """Animación del botón para saltar"""
        skip_button = ctk.CTkButton(
            self.content_frame,
            text="⏭️ CONTINUAR",
            command=self.close_credits,
            width=150,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=self.colors['primary'],
            hover_color=self.colors['secondary']
        )
        skip_button.place(relx=0.5, rely=0.87, anchor="center")  # ← Bajado
    
        self.animated_elements.append(skip_button)
        self.pulse_element(skip_button)

    
    # Efectos de animación
    def fade_in_element(self, element, step):
        """Efecto de aparición gradual"""
        if not self.animation_running or not element.winfo_exists():
            return
        
        alpha = min(1.0, step / 10.0)
        
        # Simular transparencia cambiando el color
        if step < 10:
            self.credits_window.after(50, lambda: self.fade_in_element(element, step + 1))
    
    def slide_in_element(self, element, direction):
        """Efecto de deslizamiento"""
        if not self.animation_running or not element.winfo_exists():
            return
        
        start_x = -200 if direction == 'left' else 1200
        target_x = 500  # Centro
        
        def animate_position(step):
            if not self.animation_running or not element.winfo_exists():
                return
            
            if step <= 20:
                progress = step / 20.0
                # Easing out
                progress = 1 - (1 - progress) ** 3
                current_x = start_x + (target_x - start_x) * progress
                
                element.place(x=current_x, rely=element.place_info()['rely'], anchor="center")
                self.credits_window.after(25, lambda: animate_position(step + 1))
        
        animate_position(0)
    
    def pulse_element(self, element):
        """Efecto de pulsación"""
        if not self.animation_running or not element.winfo_exists():
            return
        
        def animate_pulse(step):
            if not self.animation_running or not element.winfo_exists():
                return
            
            if step <= 40:
                # Crear efecto de pulsación con seno
                scale = 1.0 + 0.1 * math.sin(step * 0.3)
                
                # Simular escalado cambiando el tamaño de fuente si es posible
                try:
                    current_font = element.cget('font')
                    if hasattr(current_font, 'configure'):
                        base_size = 20
                        new_size = int(base_size * scale)
                        element.configure(font=ctk.CTkFont(size=new_size))
                except:
                    pass
                
                self.credits_window.after(50, lambda: animate_pulse(step + 1))
        
        animate_pulse(0)
    
    def bounce_element(self, element):
        """Efecto de rebote"""
        if not self.animation_running or not element.winfo_exists():
            return
        
        base_y = 0.56
        
        def animate_bounce(step):
            if not self.animation_running or not element.winfo_exists():
                return
            
            if step <= 30:
                # Movimiento de rebote
                bounce = abs(math.sin(step * 0.4)) * 0.03
                new_y = base_y - bounce
                
                element.place(relx=0.5, rely=new_y, anchor="center")
                self.credits_window.after(50, lambda: animate_bounce(step + 1))
        
        animate_bounce(0)
    
    def auto_close_credits(self):
        """Cerrar créditos automáticamente"""
        if self.animation_running and self.credits_window and self.credits_window.winfo_exists():
            print("⏰ Auto-cerrando créditos...")
            self.close_credits()
    
    def close_credits(self):
        """Cerrar pantalla de créditos"""
        print("✅ Cerrando créditos...")
    
        self.animation_running = False
    
    # Detener todos los sonidos sintéticos
        try:
            pygame.mixer.stop()
        except:
            pass
    
    # Destruir ventana
        if self.credits_window:
            try:
                self.credits_window.destroy()
            except:
                pass
            finally:
                self.credits_window = None
    
    # Limpiar elementos
        self.animated_elements.clear()
    
        print("🎮 Iniciando menú principal...")
    
    # 🎬 LLAMAR AL MÉTODO CORRECTO
        if hasattr(self.app, 'show_menu_after_credits'):
            self.app.show_menu_after_credits()
        elif hasattr(self.app, 'create_working_menu'):
            self.app.create_working_menu()

# Función para integrar en tu main.py
def show_credits_before_app(app):
    """Mostrar créditos antes de la aplicación principal"""
    credits = AnimatedCreditsScreen(app)
    credits.show_credits()
    return credits