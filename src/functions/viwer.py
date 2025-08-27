import config
from src.modules.saveImage import save_image

# Função de clique para gerar imagem
def new_image_window(image):
  image_window = config.ctk.CTkToplevel(config.window)
  image_window.title("Imagem Gerada")
  image_window.geometry("1024x1024")
  image_window.resizable(False, False)
  image_window.configure(fg_color=config.COR_FRAME)
  # Imagem exibida
  ctk_image = config.ctk.CTkImage(light_image=image, dark_image=image, size=(1024, 1024))
  image_label = config.ctk.CTkLabel(image_window, image=ctk_image, text="")
  image_label.place(x=0, y=0)
  # Botão de salvar
  salvar_btn = config.ctk.CTkButton(image_window, text="Salvar", command=lambda: save_image(image), fg_color=config.COR_BOTAO, hover_color=config.COR_BOTAO_HOVER)
  salvar_btn.pack(padx=10, pady=10)

# Função para gerar a imagem
def viwerImage(generate_button, temperature_label, prompt_entry, negative_prompt_entry, steps, cfg, seed_entry, lora_listbox):
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
    generate_button.configure(state="disabled", text="Configurando ambiente")
    selected_lora_name = lora_listbox.get()
    lora_to_apply = config.loaded_loras.get(selected_lora_name)
    lora_strength = 0.0
    try:
      generate_button.configure(text="Ajustando modelo/LoRA's")
      config.setPipe.unload_lora_weights() 
      if lora_to_apply:
        lora_path = lora_to_apply["path"]
        lora_strength = lora_to_apply["cfg"]
        print(f"Aplicando LoRA '{selected_lora_name}' | CFG: {lora_strength}")
        config.setPipe.load_lora_weights(lora_path)

      generate_button.configure(text="Carregando modelo na memória")
      from src.modules.createImage import generate_click
      try:
        seed_value = int(seed_entry.get())
      except (ValueError, TypeError):
        seed_value = -1
      result = generate_click(generate_button, temperature_label, config.setTorch, config.setPipe, config.limit_temp, prompt_entry.get("1.0", "end-1c"), negative_prompt_entry.get("1.0", "end-1c") or config.negative_prompt, int(steps.get()), round(cfg.get(), 1), lora_strength, seed=seed_value)
      if result[0] == 1: return
      image, used_seed = result
      # seed_entry.delete(0, "end")
      # seed_entry.insert(0, str(used_seed))
      config.window.after(0, lambda: new_image_window(image))
    except Exception as e:
      config.error(f"Ocorreu um erro na geração:\n{e}")
      print(f"Erro em viwerImage: {e}")
    finally:
      generate_button.configure(state="normal", text="Gerar Imagem")

  config.threading.Thread(target=worker, daemon=True).start()