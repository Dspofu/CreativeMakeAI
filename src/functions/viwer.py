import config
from src.modules.loading import progress
from src.modules.saveImage import save_image

# Função de clique para gerar imagem
def new_image_window(image, seed: int):
  img_width, img_height = image.size
  scale = min(512 / img_width, 512 / img_height)
  new_width = int(img_width * scale)
  new_height = int(img_height * scale)
  resized_image = image.resize((new_width, new_height), config.Image.LANCZOS)

  image_window = config.ctk.CTkToplevel(config.window)
  image_window.title(f"Imagem Gerada | Seed: {seed}")
  image_window.geometry(f"{512}x{512}")
  image_window.resizable(False, False)
  image_window.configure(fg_color=config.COR_FRAME)
  # Imagem exibida
  ctk_image = config.ctk.CTkImage(light_image=image, dark_image=image, size=(new_height, new_height))
  image_label = config.ctk.CTkLabel(image_window, image=ctk_image, text="")
  image_label.place(x=0, y=0)
  # Botão de salvar
  salvar_btn = config.ctk.CTkButton(image_window, text="Salvar", command=lambda: save_image(image), fg_color=config.COR_BOTAO, hover_color=config.COR_BOTAO_HOVER)
  salvar_btn.pack(padx=10, pady=10)

# Função para gerar a imagem
def viwerImage(generate_button, temperature_label, scale_image: str, prompt_entry: str, negative_prompt_entry: str, steps: int, cfg: float, seed_entry: int, lora_listbox, qtdImg: int):
  config.stop_img = False
  def worker():
    # Checagens de segurança
    if config.setPipe is None:
      config.error("Erro: pipe não foi definido.")
      print("Erro: pipe não foi definido.")
      return 1

    if not prompt_entry.get("1.0", "end-1c").strip():
      config.error("Prompt não identificado.")
      print("Prompt não identificado.")
      return 1
    if not any(x in scale_image for x in ["512x512", "1024x1024", "1920x1080", "2048x2048"]):
      config.error("Escala para imagem incorreta.")
      print("Escala para imagem incorreta.")
      return 1
    width=1024
    height=1024
    if scale_image == "512x512":
      width=512
      height=512
    elif scale_image == "1920x1080":
      width=1920
      height=1080
    elif scale_image == "2048x2048":
      width=2048
      height=2048

    progress(0)
    config.window.title(f"{config.winTitle} | Configurando")
    generate_button.configure(state="disabled", text="Configurando ambiente")
    selected_lora_name = lora_listbox.get()
    lora_to_apply = config.loaded_loras.get(selected_lora_name)
    lora_strength = 0.0
    try:
      progress(33)
      generate_button.configure(text="Ajustando modelo/LoRA's")
      config.setPipe.unload_lora_weights() 
      if lora_to_apply:
        lora_path = lora_to_apply["path"]
        lora_strength = lora_to_apply["cfg"]
        print(f"Aplicando LoRA '{selected_lora_name}' | CFG: {lora_strength}")
        config.setPipe.load_lora_weights(lora_path)

      progress(66)
      config.window.title(f"{config.winTitle} | Alocando na RAM")
      generate_button.configure(text="Carregando modelo na memória")
      from src.modules.createImage import generate_click
      try:
        seed_value = int(seed_entry.get())
        progress(100)
      except (ValueError, TypeError):
        config.window.title(config.winTitle)
        seed_value = -1
      for i in range(qtdImg):
        result = generate_click(generate_button, temperature_label, width, height, config.setTorch, config.setPipe, config.limit_temp, prompt_entry.get("1.0", "end-1c"), negative_prompt_entry.get("1.0", "end-1c") or config.negative_prompt, int(steps.get()), round(cfg.get(), 1), lora_strength, seed=seed_value, fila=qtdImg, positionFila=i)
        if result[0] == 1: return
        config.window.title(f"{config.winTitle} | Renderizando imagem")
        image, used_seed = result
        # seed_entry.delete(0, "end")
        # seed_entry.insert(0, str(used_seed))
        config.window.after(0, lambda: new_image_window(image, seed=used_seed))
    except Exception as e:
      config.window.title(config.winTitle)
      if config.stop_img:
        progress(100)
        print("\nTrabalho interrompido")
        return
      config.error(f"Ocorreu um erro na geração:\n{e}")
      print(f"Erro em viwerImage: {e}")
    finally:
      config.window.title(config.winTitle)
      config.window.configure(cursor="")
      generate_button.configure(state="normal", text="Gerar Imagem")
      temperature_label.configure(text="--°C", text_color="#D9D9D9")

  config.threading.Thread(target=worker, daemon=True).start()