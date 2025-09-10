#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
TEST ESPECÍFICO PARA CARGA DE IMÁGENES
Ejecuta este archivo para probar todas las funciones de carga de imágenes
"""

print("🧪 === TEST DE CARGA DE IMÁGENES ===")

import os
import sys
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageDraw

# Agregar directorio actual al path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Configurar CustomTkinter
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class ImageLoadTest:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("🧪 Test de Carga de Imágenes")
        self.root.geometry("800x600")
        
        # Manager dummy
        self.sound_manager = self
        
        self.create_ui()
    
    def play_sound(self, sound_name):
        print(f"🔊 {sound_name}")
    
    def create_ui(self):
        """Crear interfaz de prueba"""
        main_frame = ctk.CTkFrame(self.root)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Título
        ctk.CTkLabel(
            main_frame,
            text="🧪 TEST DE CARGA DE IMÁGENES",
            font=ctk.CTkFont(size=24, weight="bold")
        ).pack(pady=20)
        
        # Información
        info_text = (
            "Este test verificará todas las funciones de carga de imágenes:\n\n"
            "✅ Importación del editor\n"
            "✅ Creación de imágenes de prueba\n"
            "✅ Apertura del editor\n"
            "✅ Test de todos los métodos de carga"
        )
        
        ctk.CTkLabel(
            main_frame,
            text=info_text,
            font=ctk.CTkFont(size=12),
            justify="center"
        ).pack(pady=20)
        
        # Botones de prueba
        buttons_frame = ctk.CTkFrame(main_frame)
        buttons_frame.pack(pady=20)
        
        # Test 1: Crear imágenes de prueba
        test1_btn = ctk.CTkButton(
            buttons_frame,
            text="1️⃣ CREAR IMÁGENES DE PRUEBA",
            command=self.create_test_images,
            width=250,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#4CAF50"
        )
        test1_btn.pack(pady=5)
        
        # Test 2: Abrir editor
        test2_btn = ctk.CTkButton(
            buttons_frame,
            text="2️⃣ ABRIR EDITOR MEJORADO",
            command=self.open_editor,
            width=250,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#2196F3"
        )
        test2_btn.pack(pady=5)
        
        # Test 3: Test de PIL
        test3_btn = ctk.CTkButton(
            buttons_frame,
            text="3️⃣ TEST DE PIL",
            command=self.test_pil,
            width=250,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#FF9800"
        )
        test3_btn.pack(pady=5)
        
        # Test 4: Test de filedialog
        test4_btn = ctk.CTkButton(
            buttons_frame,
            text="4️⃣ TEST DE FILEDIALOG",
            command=self.test_filedialog,
            width=250,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color="#9C27B0"
        )
        test4_btn.pack(pady=5)
        
        # Estado
        self.status_label = ctk.CTkLabel(
            main_frame,
            text="💤 Listo para ejecutar pruebas",
            font=ctk.CTkFont(size=14),
            text_color="#888888"
        )
        self.status_label.pack(pady=20)
        
        # Instrucciones
        instructions = (
            "📋 INSTRUCCIONES:\n\n"
            "1. Ejecuta las pruebas en orden\n"
            "2. En el editor, usa el botón '🔧 DEBUG' para verificar estado\n"
            "3. Prueba todos los métodos de carga:\n"
            "   • 📂 EXAMINAR ARCHIVOS\n"
            "   • 📋 PEGAR RUTA\n"
            "   • Click en las áreas de imagen\n"
            "   • Botones individuales IMG 1, IMG 2, etc.\n"
            "4. Si algo falla, revisa la consola para detalles"
        )
        
        ctk.CTkLabel(
            main_frame,
            text=instructions,
            font=ctk.CTkFont(size=11),
            justify="left",
            text_color="#cccccc"
        ).pack(pady=20, anchor="w")
    
    def create_test_images(self):
        """Crear imágenes de prueba en diferentes formatos"""
        self.status_label.configure(text="🎨 Creando imágenes de prueba...", text_color="#FF9800")
        self.root.update()
        
        try:
            # Crear directorio de prueba
            test_dir = "test_images"
            os.makedirs(test_dir, exist_ok=True)
            
            created_files = []
            
            # Imagen 1: PNG con texto
            img1 = Image.new('RGB', (300, 200), color='#FF5722')
            draw1 = ImageDraw.Draw(img1)
            draw1.rectangle([20, 20, 280, 180], outline='white', width=5)
            draw1.text((150, 100), "IMAGEN\nPRUEBA 1", fill='white', anchor="mm", align="center")
            
            file1 = os.path.join(test_dir, "prueba_1.png")
            img1.save(file1, "PNG")
            created_files.append(file1)
            
            # Imagen 2: JPG con formas
            img2 = Image.new('RGB', (300, 200), color='#4CAF50')
            draw2 = ImageDraw.Draw(img2)
            draw2.ellipse([50, 50, 250, 150], fill='white', outline='black', width=3)
            draw2.polygon([(150, 70), (200, 130), (100, 130)], fill='red')
            
            file2 = os.path.join(test_dir, "prueba_2.jpg")
            img2.save(file2, "JPEG", quality=95)
            created_files.append(file2)
            
            # Imagen 3: PNG con gradiente
            img3 = Image.new('RGB', (300, 200), color='#2196F3')
            draw3 = ImageDraw.Draw(img3)
            
            # Gradiente simple
            for y in range(200):
                color_val = int(255 * (1 - y / 200))
                color = (color_val // 3, color_val // 2, color_val)
                draw3.line([(0, y), (300, y)], fill=color)
            
            draw3.text((150, 100), "GRADIENTE", fill='white', anchor="mm")
            
            file3 = os.path.join(test_dir, "prueba_3.png")
            img3.save(file3, "PNG")
            created_files.append(file3)
            
            # Imagen 4: GIF
            img4 = Image.new('RGB', (300, 200), color='#9C27B0')
            draw4 = ImageDraw.Draw(img4)
            
            # Patrón de cuadros
            for x in range(0, 300, 30):
                for y in range(0, 200, 30):
                    if (x // 30 + y // 30) % 2 == 0:
                        draw4.rectangle([x, y, x+30, y+30], fill='white')
            
            draw4.text((150, 100), "PATRÓN", fill='black', anchor="mm")
            
            file4 = os.path.join(test_dir, "prueba_4.gif")
            img4.save(file4, "GIF")
            created_files.append(file4)
            
            # Mostrar resultado
            result_text = f"✅ {len(created_files)} imágenes creadas:\n"
            for file in created_files:
                result_text += f"  • {os.path.basename(file)}\n"
            
            result_text += f"\n📁 Ubicación: {os.path.abspath(test_dir)}"
            
            self.status_label.configure(text="✅ Imágenes de prueba creadas", text_color="#4CAF50")
            
            messagebox.showinfo("✅ Imágenes Creadas", result_text, parent=self.root)
            
            print("✅ Imágenes de prueba creadas exitosamente")
            for file in created_files:
                print(f"  📄 {file}")
            
        except Exception as e:
            error_msg = f"❌ Error creando imágenes: {e}"
            print(error_msg)
            self.status_label.configure(text="❌ Error creando imágenes", text_color="#FF5722")
            messagebox.showerror("Error", error_msg, parent=self.root)
    
    def open_editor(self):
        """Abrir el editor de niveles mejorado"""
        self.status_label.configure(text="🛠️ Abriendo editor...", text_color="#2196F3")
        self.root.update()
        
        try:
            from level_editor import LevelEditor
            
            editor = LevelEditor(self)
            editor.show_editor()
            
            self.status_label.configure(text="✅ Editor abierto", text_color="#4CAF50")
            
            messagebox.showinfo("🛠️ Editor Abierto", 
                "Editor abierto exitosamente!\n\n"
                "🔧 Cosas para probar:\n"
                "• Click en '🔧 DEBUG' para ver estado\n"
                "• Click en '📂 EXAMINAR ARCHIVOS'\n"
                "• Click en '📋 PEGAR RUTA'\n"
                "• Click en las áreas de imagen\n"
                "• Click en botones 'IMG 1', 'IMG 2', etc.\n\n"
                "📁 Usa las imágenes de 'test_images/' para probar",
                parent=self.root)
            
            print("🛠️ Editor de niveles abierto exitosamente")
            
        except ImportError as e:
            error_msg = f"❌ No se pudo importar LevelEditor: {e}"
            print(error_msg)
            self.status_label.configure(text="❌ Error importando editor", text_color="#FF5722")
            messagebox.showerror("Error", error_msg, parent=self.root)
            
        except Exception as e:
            error_msg = f"❌ Error abriendo editor: {e}"
            print(error_msg)
            self.status_label.configure(text="❌ Error abriendo editor", text_color="#FF5722")
            messagebox.showerror("Error", error_msg, parent=self.root)
    
    def test_pil(self):
        """Test específico de PIL"""
        self.status_label.configure(text="🎨 Probando PIL...", text_color="#FF9800")
        self.root.update()
        
        try:
            from PIL import Image, ImageDraw, ImageTk
            
            # Test 1: Crear imagen
            test_img = Image.new('RGB', (150, 100), color='#00BCD4')
            draw = ImageDraw.Draw(test_img)
            draw.text((75, 50), "PIL OK", fill='white', anchor="mm")
            
            # Test 2: Redimensionar
            test_img.thumbnail((100, 67), Image.Resampling.LANCZOS)
            
            # Test 3: Convertir para CTk
            ctk_img = ctk.CTkImage(light_image=test_img, size=test_img.size)
            
            # Mostrar en ventana
            test_window = ctk.CTkToplevel(self.root)
            test_window.title("🎨 Test PIL")
            test_window.geometry("250x200")
            
            img_label = ctk.CTkLabel(test_window, image=ctk_img, text="")
            img_label.pack(pady=20)
            
            ctk.CTkLabel(
                test_window,
                text="✅ PIL funciona correctamente",
                font=ctk.CTkFont(size=14, weight="bold"),
                text_color="#4CAF50"
            ).pack(pady=10)
            
            self.status_label.configure(text="✅ PIL funciona correctamente", text_color="#4CAF50")
            print("✅ Test de PIL exitoso")
            
        except Exception as e:
            error_msg = f"❌ Error en PIL: {e}"
            print(error_msg)
            self.status_label.configure(text="❌ Error en PIL", text_color="#FF5722")
            messagebox.showerror("Error PIL", error_msg, parent=self.root)
    
    def test_filedialog(self):
        """Test específico de filedialog"""
        self.status_label.configure(text="📂 Probando filedialog...", text_color="#FF9800")
        self.root.update()
        
        try:
            from tkinter import filedialog
            
            messagebox.showinfo("📂 Test FileDialog", 
                "Se abrirá el diálogo de selección de archivos.\n\n"
                "• Si se abre correctamente: ✅ Funciona\n"
                "• Si no se abre o da error: ❌ Problema\n\n"
                "Puedes cancelar el diálogo para continuar.",
                parent=self.root)
            
            # Intentar abrir diálogo
            filename = filedialog.askopenfilename(
                parent=self.root,
                title="Test de FileDialog - Selecciona cualquier archivo",
                filetypes=[
                    ("Imágenes", "*.png *.jpg *.jpeg *.gif *.bmp"),
                    ("Todos los archivos", "*.*")
                ]
            )
            
            if filename:
                result_msg = f"✅ FileDialog funciona correctamente\n\nArchivo seleccionado:\n{os.path.basename(filename)}"
                self.status_label.configure(text="✅ FileDialog OK", text_color="#4CAF50")
            else:
                result_msg = "✅ FileDialog se abrió correctamente\n(No se seleccionó archivo, pero eso es normal)"
                self.status_label.configure(text="✅ FileDialog OK (cancelado)", text_color="#4CAF50")
            
            messagebox.showinfo("Resultado", result_msg, parent=self.root)
            print("✅ Test de FileDialog exitoso")
            
        except Exception as e:
            error_msg = f"❌ Error en FileDialog: {e}"
            print(error_msg)
            self.status_label.configure(text="❌ Error en FileDialog", text_color="#FF5722")
            messagebox.showerror("Error FileDialog", 
                f"Error en FileDialog:\n{error_msg}\n\n"
                f"Esto puede explicar por qué no se abren los diálogos de selección.",
                parent=self.root)
    
    def run(self):
        print("🚀 Iniciando test de carga de imágenes...")
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = ImageLoadTest()
        app.run()
    except Exception as e:
        print(f"❌ Error crítico: {e}")
        import traceback
        traceback.print_exc()
        input("Presiona Enter para cerrar...")