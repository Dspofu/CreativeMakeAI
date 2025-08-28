import ctypes
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('dspofu.creativemakeai.1.0' )

import tkinter as tk
import customtkinter as ctk
import threading
from PIL import Image, ImageTk
from src.modules.popup import*

# Configurações para o modelo
setTorch = None
setPipe = None
limit_temp = True
loaded_loras = {}
negative_prompt = "blurry, low quality, low resolution, out of focus, overexposed, underexposed, grainy, distorted, watermark, text, signature, frame, oversaturated, unrealistic proportions, deformed anatomy, incorrect limb positioning, broken hands, extra fingers, overlapping limbs, blurred eyes, unrealistic facial features, extra limbs, missing body parts, messy background, crowded composition, noise, compression artifacts, cartoonish, overly stylized, unnatural poses, distorted perspectives, unnatural lighting, disproportionate body parts, body parts passing through clothing, clothing blending into skin, unnatural folds in clothing, floating accessories, misaligned clothing, warped fabric, inconsistent textures in clothing, skeleton visible through clothing, unintentionally see-through clothing, excessive wrinkles, unrealistic body-cloth interactions"

# Paleta de cores mantida
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
window.geometry(f"500x700+{int((window.winfo_screenwidth() / 2) - (500 / 2))}+{int((window.winfo_screenheight() / 2) - (700 / 2))}")
window.title("v1.0.0@BETA - CreativeMakeAI")
window.resizable(False, False)
window.configure(fg_color=COR_FRAME)
try:
  window.iconbitmap('assets\\images\\icon_24px.ico')
except Exception as e:
  error(f"Erro na inicialização da janela: {e}")
  print(f"Erro na inicialização da janela: {e}")