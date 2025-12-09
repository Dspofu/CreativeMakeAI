import ctypes
try:
  ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('dspofu.creativemakeai.1.0')
except:
  pass

import os
import sys
import tkinter as tk
import customtkinter as ctk
import threading
from PIL import Image, ImageTk
from src.functions.flush_memory import*
from src.functions.popup import*

# Verificação de OS
if sys.platform != "win32":
  print("Este projeto foi idealizado para Windows 10+.")

# Log para executável
is_frozen = getattr(sys, 'frozen', False)
if is_frozen:
  print(f"Criando arquivo: {os.path.join(os.path.dirname(sys.executable), "log.txt")}")
  log_file = os.path.join(os.path.dirname(sys.executable), "log.txt")
  sys.stdout = open(log_file, "w", encoding="utf-8")
  sys.stderr = sys.stdout

winTitle = "CreativeMakeAI v0.2.0@BETA"
github = "https://github.com/Dspofu/CreativeMakeAI"

# Variáveis Globais
model_path = None
setPipe = None
setCompel = None
profile = "Balanced" 
limit_temp = False
stop_img = False
benchmark_sequence = False
loaded_loras = {}
negative_prompt = "blurry, low quality, out of focus, grainy, overexposed, underexposed, distorted, watermark, text deformed anatomy, incorrect limbs, broken hands, extra fingers, missing fingers, extra limbs, missing limbs, unnatural poses, warped proportions unrealistic facial features, blurred eyes, mutated face clothing clipping, skin-cloth blending, warped fabric, inconsistent textures messy background, crowded composition, noise, compression artifacts, unnatural lighting, distorted perspective"

# Cores
COR_FRAME = "#1e1e2f"
COR_INPUT = "#1a1a28"
COR_TEXTO = "#FFFFFF"
COR_BOTAO = "#0070BA"
COR_BOTAO_HOVER = "#004B8D"
COR_BOTAO_IMAGE = "#009900"
COR_BOTAO_IMAGE_CANCEL = "#DB0909"
COR_BOTAO_IMAGE_HOVER = "#008800"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()