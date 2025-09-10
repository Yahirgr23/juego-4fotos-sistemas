#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configurador del entorno para 4 Fotos 1 Palabra
Crea las carpetas necesarias y archivos de configuración
"""

import os
import json
import numpy as np
import wave as wav_module
from datetime import datetime

def create_directory_structure():
    """Crear estructura de directorios"""
    print("📁 Creando estructura de directorios...")
    
    directories = [
        "assets",
        "assets/sounds",
        "assets/images",
        "custom_levels",
        "downloaded_levels",
        "temp",
        "backups"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ {directory}/")
    
    print("✅ Estructura de directorios creada")

def create_demo_music():
    """Crear archivo de música de fondo demo"""
    print("🎵 Creando música de fondo...")
    
    try:
        music_path = os.path.join("assets", "sounds", "background_music.wav")
        
        if os.path.exists(music_path):
            print("⚠️ Archivo de música ya existe, omitiendo...")
            return
        
        # Configuración de audio
        sample_rate = 22050
        duration = 60  # 1 minuto
        
        # Crear progresión de acordes relajante
        # Progresión: C - Am - F - G (I - vi - IV - V)
        chord_progression = [
            [261.63, 329.63, 392.00],  # C Major (C-E-G)
            [220.00, 261.63, 329.63],  # A Minor (A-C-E)
            [174.61, 220.00, 261.63],  # F Major (F-A-C)
            [196.00, 246.94, 293.66],  # G Major (G-B-D)
        ]
        
        total_samples = int(sample_rate * duration)
        wave_data = np.zeros(total_samples)
        
        # Generar cada acorde
        chord_duration = duration / len(chord_progression)
        samples_per_chord = int(sample_rate * chord_duration)
        
        for i, chord in enumerate(chord_progression):
            start_idx = i * samples_per_chord
            end_idx = min(start_idx + samples_per_chord, total_samples)
            
            # Tiempo para este acorde
            t = np.linspace(0, chord_duration, end_idx - start_idx, False)
            
            # Crear onda del acorde (suma de sinusoides)
            chord_wave = np.zeros(len(t))
            for freq in chord:
                # Onda sinusoidal con envolvente suave
                sine_wave = np.sin(2 * np.pi * freq * t)
                envelope = np.exp(-t * 0.5)  # Decaimiento suave
                chord_wave += sine_wave * envelope * 0.1  # Volumen bajo
            
            wave_data[start_idx:end_idx] = chord_wave
        
        # Aplicar fade in/out
        fade_samples = int(sample_rate * 2)  # 2 segundos de fade
        
        # Fade in
        if len(wave_data) > fade_samples * 2:
            fade_in = np.linspace(0, 1, fade_samples)
            wave_data[:fade_samples] *= fade_in
            
            # Fade out
            fade_out = np.linspace(1, 0, fade_samples)
            wave_data[-fade_samples:] *= fade_out
        
        # Convertir a 16-bit PCM
        wave_data = np.clip(wave_data, -1.0, 1.0)
        wave_data = (wave_data * 32767).astype(np.int16)
        
        # Guardar como archivo WAV
        with wav_module.open(music_path, 'w') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16 bits
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(wave_data.tobytes())
        
        print(f"✅ Música de fondo creada: {music_path}")
        print(f"   📊 Duración: {duration}s | Frecuencia: {sample_rate}Hz")
        
    except ImportError:
        print("⚠️ NumPy no disponible, creando archivo de música simple...")
        create_simple_music()
    except Exception as e:
        print(f"❌ Error creando música: {e}")

def create_simple_music():
    """Crear música simple sin NumPy"""
    try:
        music_path = os.path.join("assets", "sounds", "background_music.wav")
        
        # Crear un archivo WAV muy simple con un tono
        sample_rate = 22050
        duration = 10
        frequency = 220  # Nota A3
        
        import math
        
        samples = []
        for i in range(int(sample_rate * duration)):
            # Onda sinusoidal simple
            t = i / sample_rate
            sample = math.sin(2 * math.pi * frequency * t) * 0.1
            samples.append(int(sample * 32767))
        
        # Convertir a bytes
        wave_data = b''.join(sample.to_bytes(2, 'little', signed=True) for sample in samples)
        
        with wav_module.open(music_path, 'w') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(wave_data)
        
        print(f"✅ Música simple creada: {music_path}")
        
    except Exception as e:
        print(f"❌ Error")