from src.config import*
from tkinter import filedialog

# Função chamada ao clicar no botão
def select_model():
  global setTorch, setPipe, some_weight
  model_path = filedialog.askopenfilename(
    title="Selecionar Modelo",
    filetypes=[("Modelos .safetensors", "*.safetensors")]
  )
  if model_path:
    print("Iniciando pacotes.")
    import torch
    from diffusers import StableDiffusionXLPipeline
    setTorch = torch
    print("Carregando modelo.")
    setPipe = StableDiffusionXLPipeline.from_single_file(model_path, torch_dtype=torch.float16, variant="f16")
    print("Aplicando as otimizações.")
    try:
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
  print("Pronto para instruções.")

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
chackBox = ctk.CTkCheckBox(container_frame_temp, text="", command=active_temp_alert, fg_color="#0070BA", hover_color="#004B8D", checkbox_width=20, checkbox_height=20, corner_radius=5, bg_color=COR_FRAME)
chackBox.select(limit_temp)
chackBox.pack(side="left", padx=0, pady=0)
main_frame = ctk.CTkFrame(window, fg_color=COR_FRAME)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Prompt
ctk.CTkLabel(main_frame, text="Prompt:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(20, 5))
prompt_entry = ctk.CTkEntry(
  main_frame,
  width=400,
  height=40,
  font=("Arial", 14),
  fg_color=COR_INPUT,
  text_color=COR_TEXTO,
  border_width=0,
  corner_radius=8
)
prompt_entry.pack(padx=0, pady=(0, 20))

# Prompt Negativo
ctk.CTkLabel(main_frame, text="Prompt Negativo:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(0, 5))
negative_prompt_entry = ctk.CTkTextbox(
  main_frame,
  height=100,
  font=("Arial", 14),
  fg_color=COR_INPUT,
  text_color=COR_TEXTO,
  border_width=0,
  corner_radius=8
)
negative_prompt_entry.insert("0.0", negative_prompt)
negative_prompt_entry.pack(padx=0, pady=(0, 20), fill="both", expand=True)

# Steps
ctk.CTkLabel(main_frame, text="Steps:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(0, 5))
steps = ctk.CTkSlider(master=main_frame, from_=1, to=100, command=print, width=400)
steps.set(28)
steps.pack(anchor="w", padx=0, pady=(0, 20))

# CFG Scale
ctk.CTkLabel(main_frame, text="CFG Scale:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(0, 5))
cfg = ctk.CTkSlider(master=main_frame, from_=0.5, to=30, command=print, width=400)
cfg.set(4.5)
cfg.pack(anchor="w", padx=0, pady=(0, 20))

# Função de clique para gerar imagem
from src.modules.createImage import generate_click

def viwerImage():
  if setPipe is None or setTorch is None or some_weight is None:
    from src.modules.popup import error
    return error("Não houve modelo carregado.")
  image = generate_click(setTorch, setPipe, some_weight, limit_temp, prompt_entry.get(), negative_prompt_entry.get("1.0", "end-1c") or negative_prompt, int(steps.get()), round(cfg.get(), 1))
  if image == 1:
    return 1
  else:
    image_window = ctk.CTkToplevel(window)
    image_window.title("Imagem Gerada")
    image_window.geometry("1024x1024")
    image_window.resizable(False, False)
    image_window.configure(fg_color=COR_BG_JANELA)
    ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(1024, 1024))
    image_label = ctk.CTkLabel(image_window, image=ctk_image, text="")
    image_label.pack(expand=True, fill="both")

# Botão Gerar
generate_button = ctk.CTkButton(
  main_frame,
  text="Gerar Imagem",
  command=lambda: viwerImage(),
  font=("Arial", 14, "bold"),
  fg_color=COR_BOTAO,
  hover_color=COR_BOTAO_HOVER,
  height=40,
  corner_radius=8,
)
generate_button.pack(padx=20, pady=20, fill="x")
window.mainloop()