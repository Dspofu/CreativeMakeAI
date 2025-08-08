import tkinter as tk
import customtkinter as ctk

# Configurações para o modelo
setTorch = None
setPipe = None
some_weight = None
limit_temp = True
negative_prompt = "blurry, low quality, low resolution, out of focus, overexposed, underexposed, grainy, distorted, watermark, text, signature, frame, oversaturated, unrealistic proportions, deformed anatomy, incorrect limb positioning, broken hands, extra fingers, overlapping limbs, blurred eyes, unrealistic facial features, extra limbs, missing body parts, messy background, crowded composition, noise, compression artifacts, cartoonish, overly stylized, unnatural poses, distorted perspectives, unnatural lighting, disproportionate body parts, body parts passing through clothing, clothing blending into skin, unnatural folds in clothing, floating accessories, misaligned clothing, warped fabric, inconsistent textures in clothing, skeleton visible through clothing, unintentionally see-through clothing, excessive wrinkles, unrealistic body-cloth interactions"
steps = 28
cfg = 4.5

# Paleta de cores mantida
COR_BG_JANELA = "#1e1e2f"
COR_FRAME = "#1e1e2f"
COR_INPUT = "#1a1a28"
COR_TEXTO = "#FFFFFF"
COR_BOTAO = "#4e4e6a"
COR_BOTAO_HOVER = "#5e5e7f"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("v1.0.0@BETA - CreativeMakeAI")
window.geometry("700x600")
window.resizable(False, False)
window.configure(fg_color=COR_BG_JANELA)