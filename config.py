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
from src.modules.flush_memory import*
from src.modules.popup import*

# Verificação de OS
if sys.platform != "win32":
  print("Este projeto foi idealizado para Windows 10+.")

# Log para executável
is_frozen = getattr(sys, 'frozen', False)
if is_frozen:
  log_file = os.path.join(os.path.dirname(sys.executable), "log.txt")
  sys.stdout = open(log_file, "w", encoding="utf-8")
  sys.stderr = sys.stdout

winTitle = "CreativeMakeAI v0.2.0@BETA"
github = "https://github.com/Dspofu/CreativeMakeAI"

# Variáveis Globais
model_path = None
setPipe = None
profile = "Balanced" 
limit_temp = True
stop_img = False
loaded_loras = {}
negative_prompt = "blurry, low quality, low resolution, out of focus, overexposed, underexposed, grainy, distorted, watermark, text, signature, frame, oversaturated, unrealistic proportions, deformed anatomy, incorrect limb positioning, broken hands, extra fingers, overlapping limbs, blurred eyes, unrealistic facial features, extra limbs, missing body parts, messy background, crowded composition, noise, compression artifacts, cartoonish, overly stylized, unnatural poses, distorted perspectives, unnatural lighting, disproportionate body parts, body parts passing through clothing, clothing blending into skin, unnatural folds in clothing, floating accessories, misaligned clothing, warped fabric, inconsistent textures in clothing, skeleton visible through clothing, unintentionally see-through clothing, excessive wrinkles, unrealistic body-cloth interactions"

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