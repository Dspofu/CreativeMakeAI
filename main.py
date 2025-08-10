from src.config import*
from tkinter import Image, filedialog
import time

# Função de carregar modelo
def select_model():
  def worker():
    global setTorch, setPipe, some_weight
    model_path = filedialog.askopenfilename(
      title="Selecionar Modelo",
      filetypes=[("Modelos .safetensors", "*.safetensors")]
    )
    if model_path:
      model_button.configure(state="disabled", text="Preparando ambiente")
      print("Iniciando pacotes.")
      import torch
      from diffusers import StableDiffusionXLPipeline
      setTorch = torch
      # import os
      print("Carregando modelo.")
      model_button.configure(state="disabled", text="Carregando modelo")
      # os.environ["CUDA_VISIBLE_DEVICES"] = "1"
      try:
        setPipe = StableDiffusionXLPipeline.from_single_file(model_path, torch_dtype=torch.float16, variant="f16")
        print("Aplicando as otimizações.")
        from src.modules.popup import alert
        setTorch.backends.cuda.matmul.allow_tf32 = True
        setPipe.enable_attention_slicing("auto")
        setPipe.vae.enable_tiling()
        setPipe.enable_model_cpu_offload()
        setPipe.set_progress_bar_config(disable=False)
        some_weight = dict(setPipe.unet.state_dict())['conv_in.weight']
      except Exception as e:
        print(e)
        alert("Algo falhou, verifique a compatibilidade de CUDA e versão dos drivers.")
        model_button.configure(state="normal", text="Falha no carregamento")
        generate_button.configure(state="disabled")
    model_button.configure(state="normal", text="Modelo carregado")
    generate_button.configure(state="normal")
    time.sleep(2.5)
    model_button.configure(state="normal", text="Selecionar modelo")
    print("Pronto para instruções.")
  threading.Thread(target=worker, daemon=True).start()

def active_temp_alert():
  global limit_temp
  limit_temp = not limit_temp

# Selecionar modelo
model_button = ctk.CTkButton(window, text="Selecionar modelo", command=select_model, font=("Arial", 12))
model_button.place(x=10, y=10)

# Botão de temperatura
container_frame_temp = ctk.CTkFrame(window, fg_color=COR_FRAME, border_width=0)
container_frame_temp.place(relx=1.1, rely=0.0, y=10, anchor="ne")
ctk.CTkLabel(container_frame_temp, text="Alerta de temperatura", font=("Arial", 12), bg_color=COR_FRAME, text_color="white").pack(side="left", padx=(0, 5), pady=0)
chackBox = ctk.CTkCheckBox(container_frame_temp, text="", command=active_temp_alert, fg_color=COR_BOTAO, hover_color=COR_BOTAO_HOVER, checkbox_width=20, checkbox_height=20, corner_radius=5, bg_color=COR_FRAME)
chackBox.select(limit_temp)
chackBox.pack(side="left", padx=0, pady=0)
main_frame = ctk.CTkFrame(window, fg_color=COR_FRAME)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Prompt
ctk.CTkLabel(main_frame, text="Prompt:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(20, 5))
prompt_entry = ctk.CTkEntry(main_frame, width=400, height=40, font=("Arial", 14), fg_color=COR_INPUT, text_color=COR_TEXTO, border_width=0, corner_radius=8)
prompt_entry.pack(padx=0, pady=(0, 20))

# Prompt Negativo
ctk.CTkLabel(main_frame, text="Prompt Negativo:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(0, 5))
negative_prompt_entry = ctk.CTkTextbox(main_frame, height=100, font=("Arial", 14), fg_color=COR_INPUT, text_color=COR_TEXTO, border_width=0, corner_radius=8)
negative_prompt_entry.insert("0.0", negative_prompt)
negative_prompt_entry.pack(padx=0, pady=(0, 20), fill="both", expand=True)

# Steps
ctk.CTkLabel(main_frame, text="Steps:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(0, 5))
steps = ctk.CTkSlider(master=main_frame, from_=1, to=100, command=lambda value: print(f"Steps: {int(value)}"), width=400)
steps.set(28)
steps.pack(anchor="w", padx=0, pady=(0, 20))

# CFG Scale
ctk.CTkLabel(main_frame, text="CFG Scale:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(0, 5))
cfg = ctk.CTkSlider(master=main_frame, from_=0.5, to=30, command=lambda value: print(f"CFG Scale: {round(value, 1)}"), width=400)
cfg.set(4.5)
cfg.pack(anchor="w", padx=0, pady=(0, 20))

def save_image(image: Image):
  file_path = filedialog.asksaveasfilename(
    defaultextension=".png",
    filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("Todos os arquivos", "*.*")],
    title="Salvar imagem gerada"
  )
  if file_path:
    image.save(file_path)
    print(f"Imagem salva em: {file_path}")

# Função de clique para gerar imagem
from src.modules.createImage import generate_click

def new_image_window(image):
  image_window = ctk.CTkToplevel(window)
  image_window.title("Imagem Gerada")
  image_window.geometry("1024x1024")
  image_window.resizable(False, False)
  image_window.configure(fg_color=COR_FRAME)
  # Imagem exibida
  ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(1024, 1024))
  image_label = ctk.CTkLabel(image_window, image=ctk_image, text="")
  image_label.place(x=0, y=0)
  # Botão de salvar
  salvar_btn = ctk.CTkButton(image_window, text="Salvar", command=lambda: save_image(image), fg_color=COR_BOTAO, hover_color=COR_BOTAO_HOVER, corner_radius=8)
  salvar_btn.place(relx=1.0, anchor="ne")

def viwerImage():
  if setPipe is None or setTorch is None or some_weight is None:
    from src.modules.popup import error
    return error("Não houve modelo carregado.")

  def worker():
    generate_button.configure(state="disabled", text="Iniciando processo")
    image = generate_click(generate_button, setTorch, setPipe, some_weight, limit_temp, prompt_entry.get(), negative_prompt_entry.get("1.0", "end-1c") or negative_prompt, int(steps.get()), round(cfg.get(), 1))
    if image == 1:
      generate_button.configure(state="normal", text="Gerar Imagem")
      return 1
    window.after(0, lambda: new_image_window(image))
    generate_button.configure(state="normal", text="Gerar Imagem")

  threading.Thread(target=worker, daemon=True).start()

# Botão Gerar Imagem
generate_button = ctk.CTkButton(main_frame, text="Gerar Imagem", command=lambda: viwerImage(), state="disabled", font=("Arial", 14, "bold"), fg_color=COR_BOTAO_IMAGE, hover_color=COR_BOTAO_IMAGE_HOVER, height=40, corner_radius=8)
generate_button.pack(padx=20, pady=20, fill="x")
window.mainloop()