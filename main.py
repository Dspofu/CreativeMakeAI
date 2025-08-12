from src.config import*
from tkinter import Image, filedialog
import time
from src.modules.popup import*

# Função de carregar modelo
def select_model():
  def worker():
    global setTorch, setPipe
    model_path = filedialog.askopenfilename(
      title="Selecionar Modelo",
      filetypes=[("Modelos .safetensors", "*.safetensors")]
    )
    if not model_path: return
    lora_listbox.set("")
    loaded_loras.clear()
    lora_listbox.configure(values=[])
    lora_label.configure(text="LoRA Scale: 0.75")
    lora_scale.set(0.75)
    model_button.configure(state="disabled", text="Preparando ambiente")
    print("Iniciando pacotes.")
    import torch
    from diffusers import StableDiffusionXLPipeline
    setTorch = torch
    print("Carregando modelo.")
    model_button.configure(state="disabled", text="Carregando modelo")
    try:
      setPipe = StableDiffusionXLPipeline.from_single_file(model_path, torch_dtype=torch.float16, variant="fp16")
      print("Aplicando as otimizações.")
      torch.backends.cuda.matmul.allow_tf32 = True
      setPipe.enable_attention_slicing("auto")
      setPipe.vae.enable_tiling()
      setPipe.enable_model_cpu_offload()
      setPipe.set_progress_bar_config(disable=True)
      model_button.configure(state="normal", text="Modelo carregado")
      generate_button.configure(state="normal")
      model_lora.configure(state="normal")
    except Exception as e:
      print(e)
      alert("Algo falhou, verifique o modelo e compatibilidade do CUDA e versão dos drivers.")
      model_button.configure(state="normal", text="Falha no carregamento")
      generate_button.configure(state="disabled")
      model_lora.configure(state="disabled")
    finally:
      time.sleep(1.5)
      model_button.configure(state="normal", text="Selecionar modelo")
      print("Pronto para instruções.")
  threading.Thread(target=worker, daemon=True).start()

# Função de carregar LoRA
def select_lora():
  global loaded_loras
  new_lora_path = filedialog.askopenfilename(
    title="Selecionar LoRA",
    filetypes=[("Modelos .safetensors", "*.safetensors")]
  )
  if not new_lora_path: return
  try:
    model_lora.configure(state="disabled", text="Registrando LoRA")
    filename = new_lora_path.split('/')[-1]
    loaded_loras[filename] = { "path": new_lora_path, "cfg": 0.75 }
    print(f"LoRA '{filename}' registrado.")
    lora_listbox.configure(values=list(loaded_loras.keys()))
    lora_listbox.set(filename)
    list_lora(filename)
    model_lora.configure(state="disabled", text=f"LoRA carregado com sucesso")
  except Exception as e:
    error("Falha ao tentar registrar o LoRA\nTalvez ele não seja compatível.")
    print(f"Falha ao registrar LoRA: {e}")
  finally:
    time.sleep(1.5)
    model_lora.configure(state="normal", text="Adicionar LoRA")

# Função para deletar o LoRA
def unload_lora():
  global loaded_loras
  selected_lora = lora_listbox.get()
  if selected_lora in loaded_loras:
    del loaded_loras[selected_lora]
    new_values = list(loaded_loras.keys())
    lora_listbox.configure(values=new_values)

    if new_values:
      lora_listbox.set(new_values[0])
      list_lora(new_values[0])
    else:
      lora_listbox.set("")
      lora_label.configure(text="LoRA Scale: 0.75")
      lora_scale.set(0.75)
    print(f"LoRA '{selected_lora}' removido da memória.")
  else:
    print(f"LoRA '{selected_lora}' não está carregado.")

# Função para pegar CFG na listas de LoRA
def list_lora(lora_name):
  if lora_name in loaded_loras:
    cfg_value = loaded_loras[lora_name]['cfg']
    lora_label.configure(text=f"LoRA Scale: {cfg_value}")
    lora_scale.set(cfg_value)

# Função para ativar ou desativar o limitador por temperatura
def active_temp_alert():
  global limit_temp
  limit_temp = not limit_temp

# Função de salvar imagem
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
  salvar_btn = ctk.CTkButton(image_window, text="Salvar", command=lambda: save_image(image), fg_color=COR_BOTAO, hover_color=COR_BOTAO_HOVER)
  salvar_btn.pack(padx=10, pady=10)

# Função para gerar a imagem
def viwerImage():
  def worker():
    global setPipe
    generate_button.configure(state="disabled", text="Configurando ambiente")
    selected_lora_name = lora_listbox.get()
    lora_to_apply = loaded_loras.get(selected_lora_name)
    lora_strength = 0.0
    try:
      generate_button.configure(text="Ajustando modelo/LoRA's")
      setPipe.unload_lora_weights() 
      if lora_to_apply:
        lora_path = lora_to_apply["path"]
        lora_strength = lora_to_apply["cfg"]
        print(f"Aplicando LoRA '{selected_lora_name}' | CFG: {lora_strength}")
        setPipe.load_lora_weights(lora_path)

      generate_button.configure(text="Carregando modelo na memória")
      from src.modules.createImage import generate_click
      try:
        seed_value = int(seed_entry.get())
      except (ValueError, TypeError):
        seed_value = -1
      result = generate_click(
        generate_button, setTorch, setPipe, limit_temp, 
        prompt_entry.get("1.0", "end-1c"), negative_prompt_entry.get("1.0", "end-1c") or negative_prompt, 
        int(steps.get()), round(cfg.get(), 1),
        lora_strength,
        seed=seed_value,
      )
      if result[0] == 1: return
      image, used_seed = result
      # seed_entry.delete(0, "end")
      # seed_entry.insert(0, str(used_seed))
      window.after(0, lambda: new_image_window(image))
    except Exception as e:
      error(f"Ocorreu um erro na geração:\n{e}")
      print(f"Erro em viwerImage: {e}")
    finally:
      generate_button.configure(state="normal", text="Gerar Imagem")

  threading.Thread(target=worker, daemon=True).start()

# Selecionar modelo
model_button = ctk.CTkButton(window, text="Selecionar modelo", command=select_model, font=("Arial", 12))
model_button.place(x=10, y=10)

# Botão de temperatura
container_frame_temp = ctk.CTkFrame(window, fg_color=COR_FRAME, border_width=0)
container_frame_temp.place(relx=1.0, rely=0.0, y=10, anchor="ne")
ctk.CTkLabel(container_frame_temp, text="Alerta de temperatura", font=("Arial", 12), bg_color=COR_FRAME, text_color="white").pack(side="left", padx=(0, 5))
checkBox = ctk.CTkCheckBox(container_frame_temp, text="", command=active_temp_alert, fg_color=COR_BOTAO, hover_color=COR_BOTAO_HOVER, checkbox_width=20, checkbox_height=20, corner_radius=5, bg_color=COR_FRAME)
checkBox.select(limit_temp)
checkBox.pack(side="left", padx=0)

# Container inputs
main_frame = ctk.CTkFrame(window, fg_color=COR_FRAME)
main_frame.place(relx=0.5, rely=0.54, anchor="center")

# Prompt
ctk.CTkLabel(main_frame, text="Prompt:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=0)
prompt_entry = ctk.CTkTextbox(main_frame, width=400, height=80, font=("Arial", 14), fg_color=COR_INPUT, text_color=COR_TEXTO, border_width=0, corner_radius=8)
prompt_entry.pack(padx=0, pady=(0, 20), fill="both", expand=True)

# Prompt Negativo
ctk.CTkLabel(main_frame, text="Prompt Negativo:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(0, 5))
negative_prompt_entry = ctk.CTkTextbox(main_frame, height=100, font=("Arial", 14), fg_color=COR_INPUT, text_color=COR_TEXTO, border_width=0, corner_radius=8)
negative_prompt_entry.insert("0.0", negative_prompt)
negative_prompt_entry.pack(padx=0, pady=(0, 20), fill="both", expand=True)

# Steps
steps_label = ctk.CTkLabel(main_frame, text="Steps: 28", font=("Arial", 14))
steps_label.pack(anchor="w", padx=0, pady=(0, 5))
steps = ctk.CTkSlider(master=main_frame, from_=1, to=100, command=lambda value: steps_label.configure(text=f"Steps: {int(value)}"))
steps.set(28)
steps.pack(anchor="w", padx=0, pady=(0, 20), fill="both")

# CFG Scale
cfg_label = ctk.CTkLabel(main_frame, text="CFG Scale: 4.5", font=("Arial", 14))
cfg_label.pack(anchor="w", padx=0, pady=(0, 5))
cfg = ctk.CTkSlider(master=main_frame, from_=0.5, to=30, command=lambda value: cfg_label.configure(text=f"CFG Scale: {round(value, 1)}"))
cfg.set(4.5)
cfg.pack(anchor="w", padx=0, pady=(0, 20), fill="both")

seed_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
seed_frame.pack(anchor="w", padx=0, pady=(0, 20))

ctk.CTkLabel(seed_frame, text="Seed:", font=("Arial", 14)).pack(side="left", padx=(0,10))
seed_entry = ctk.CTkEntry(seed_frame, width=150, font=("Arial", 14), fg_color=COR_INPUT, text_color=COR_TEXTO, border_width=0, corner_radius=8)
seed_entry.pack(side="left")
seed_entry.insert(0, "-1")

# Container LoRA's
container_lora = ctk.CTkFrame(main_frame, fg_color=COR_FRAME)
container_lora.pack(anchor="w", padx=0, pady=(0, 20))

# Frame para botão de adicionar LoRA
lora_control_frame = ctk.CTkFrame(container_lora, fg_color="transparent")
lora_control_frame.pack(anchor="w", pady=(0, 20), fill="x")

# Botão para adicionar LoRA
model_lora = ctk.CTkButton(lora_control_frame, text="Adicionar LoRA", state="disabled", command=select_lora, font=("Arial", 12))
model_lora.pack(side="left", padx=(0, 10))

# Label de CFG do LoRA
lora_label = ctk.CTkLabel(lora_control_frame, text="LoRA Scale: 0.75", font=("Arial", 14))
lora_label.pack(side="left", padx=(0, 10))

# Input de CFG para o LoRA
def update_lora_scale(v):
  selected_lora = lora_listbox.get()
  if selected_lora in loaded_loras:
    rounded_value = round(float(v), 2)
    loaded_loras[selected_lora]["cfg"] = rounded_value
    lora_label.configure(text=f"LoRA Scale: {rounded_value}")

lora_scale = ctk.CTkSlider(lora_control_frame, from_=0.1, to=1.0, command=update_lora_scale)
lora_scale.set(0.75)
lora_scale.pack(side="left")

# Frame para lista de LoRAs
lora_list_frame = ctk.CTkFrame(container_lora, fg_color="transparent")
lora_list_frame.pack(anchor="w", fill="x")

# Lista de modelos LoRA carregados
lora_listbox = ctk.CTkComboBox(lora_list_frame, values=[], width=300, command=list_lora, state="readonly")
lora_listbox.pack(side="left", padx=(0, 10), pady=(0, 10))

# Botão para remover LoRA
remove_lora_button = ctk.CTkButton(lora_list_frame, text="Remover", command=unload_lora)
remove_lora_button.pack(side="left", pady=(0, 10), fill="both")

# Botão Gerar Imagem
generate_button = ctk.CTkButton(main_frame, text="Gerar Imagem", command=viwerImage, state="disabled", font=("Arial", 14, "bold"), fg_color=COR_BOTAO_IMAGE, hover_color=COR_BOTAO_IMAGE_HOVER, height=40, corner_radius=8)
generate_button.pack(padx=20, pady=20, fill="x")

window.mainloop()