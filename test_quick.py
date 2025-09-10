#!/usr/bin/env python3
# -*- coding: utf-8 -*-

print("=== PRUEBA RÁPIDA ===")

# Verificar que estamos en el directorio correcto
import os
print(f"📁 Directorio actual: {os.getcwd()}")

# Listar carpetas disponibles
print("\n📂 Carpetas disponibles:")
for item in os.listdir('.'):
    if os.path.isdir(item):
        print(f"  📂 {item}/")

print("\n🔍 Probando importaciones...")

# Probar importaciones
try:
    print("1. Importando MenuPrincipal...")
    from clientescreens.menu_principal import MenuPrincipal
    print("✅ MenuPrincipal OK")
except Exception as e:
    print(f"❌ MenuPrincipal error: {e}")

try:
    print("2. Importando SocketClient...")
    from clientenetwork.socket_client import SocketClient
    print("✅ SocketClient OK")
except Exception as e:
    print(f"❌ SocketClient error: {e}")

try:
    print("3. Importando SoundManager...")
    from clienteutils.sound_manager import SoundManager
    print("✅ SoundManager OK")
except Exception as e:
    print(f"❌ SoundManager error: {e}")

try:
    print("4. Importando AnimationManager...")
    from clienteutils.animation_manager import AnimationManager
    print("✅ AnimationManager OK")
except Exception as e:
    print(f"❌ AnimationManager error: {e}")

print("\n=== FIN PRUEBA RÁPIDA ===")