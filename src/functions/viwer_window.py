from config import*
from src.functions.save_image import save_image

def viwer_window(image, meta: dict[str, any]):
  img_width, img_height = image.size
  scale = min(512 / img_width, 512 / img_height)
  new_width = int(img_width * scale)
  new_height = int(img_height * scale)

  image_preview = image.resize((new_width, new_height), config.Image.BILINEAR)

  image_window = config.ctk.CTkToplevel(config.window)
  image_window.title(f"Resultado | Seed: {meta['Seed']}")
  image_window.geometry(f"{new_width}x{new_height}")
  image_window.resizable(False, False)
  image_window.configure(fg_color="black")

  ctk_image = config.ctk.CTkImage(light_image=image_preview, dark_image=image_preview, size=(new_width, new_height))
  image_label = config.ctk.CTkLabel(image_window, image=ctk_image, text="")
  image_label.place(x=0, y=0)

  salvar_btn = config.ctk.CTkButton(image_window, text="Salvar Imagem", command=lambda: save_image(image, meta), fg_color=Colors.COR_BOTAO, hover_color=Colors.COR_BOTAO_HOVER, bg_color="transparent", height=32, font=("Arial", 12, "bold"))
  salvar_btn.place(relx=0.5, rely=0.95, anchor="s")

  tempo_texto = meta.get("Generation Time", "--")
  time_label = config.ctk.CTkLabel(image_window, text=f"Tempo: {tempo_texto}", font=("Segoe UI", 12, "bold"), text_color="white", fg_color="#000000", corner_radius=6, padx=8, pady=4, bg_color="transparent")
  time_label.place(relx=0.97, rely=0.03, anchor="ne")