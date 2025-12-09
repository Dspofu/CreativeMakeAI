import os
import torch
import config
import time
from src.functions.flush_memory import*
from src.functions.loading import progress
from src.functions.save_image import save_image

# Cache de Hash
cached_model_hash = {"path": None, "hash": None}

def new_image_window(image, meta: dict[str, any]):
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

  salvar_btn = config.ctk.CTkButton(image_window, text="Salvar Imagem", command=lambda: save_image(image, meta), fg_color=config.COR_BOTAO, hover_color=config.COR_BOTAO_HOVER, bg_color="transparent", height=32, font=("Arial", 12, "bold"))
  salvar_btn.place(relx=0.5, rely=0.95, anchor="s")

  tempo_texto = meta.get("Generation Time", "--")
  time_label = config.ctk.CTkLabel(image_window, text=f"Tempo: {tempo_texto}", font=("Segoe UI", 12, "bold"), text_color="white", fg_color="#000000", corner_radius=6, padx=8, pady=4, bg_color="transparent")
  time_label.place(relx=0.97, rely=0.03, anchor="ne")

def viwerImage(generate_button, temperature_label, scale_image: str, prompt_entry: str, negative_prompt_entry: str, steps: int, cfg: float, seed_entry: int, lora_listbox, qtdImg: int):
  config.stop_img = False

  def worker():
    try:
      if config.benchmark_sequence:
        print("Aplicando calculo performático para multiplas imagens.")
        torch.backends.cudnn.benchmark = True

      if config.setPipe is None:
        config.error("Erro: pipe não foi definido.")
        return 1

      if not prompt_entry.get("1.0", "end-1c").strip():
        config.error("Prompt não identificado.")
        return 1

      # Definição de Resolução
      scale = scale_image.split("x")
      width, height = int(scale[0]), int(scale[1])
      generate_button.configure(state="disabled", text="Configurando ambiente")

      # LoRA
      selected_lora_name = lora_listbox.get()
      lora_to_apply = config.loaded_loras.get(selected_lora_name)
      lora_strength = 0.0

      # Setup Inicial (Voltando ao original: Unload sempre que inicia)
      config.setPipe.unload_lora_weights()
      if lora_to_apply:
        lora_path = lora_to_apply["path"]
        lora_strength = lora_to_apply["cfg"]
        print(f"Aplicando LoRA '{selected_lora_name}'")
        config.setPipe.load_lora_weights(lora_path)

      from src.modules.generate_click import generate_click

      # Seed Input
      try:
        seed_input = int(seed_entry.get())
      except:
        seed_input = -1

      model_path = getattr(config, "model_path", None)

      # Loop de geração
      for i in range(qtdImg):
        if config.stop_img:
          print("Detectada parada antes da geração.")
          break

        prompt_text = prompt_entry.get("1.0", "end-1c")
        neg_prompt = negative_prompt_entry.get("1.0", "end-1c") or config.negative_prompt
        steps_val = int(steps.get())
        cfg_val = round(cfg.get(), 1)

        # Seed incremental
        current_seed = seed_input
        if seed_input != -1 and i > 0:
          current_seed = seed_input + i

        start_time = time.time()

        # Chama a geração
        result = generate_click(generate_button, temperature_label, width, height, torch, config.setPipe, config.limit_temp, prompt_text, neg_prompt, steps_val, cfg_val, lora_strength, seed=current_seed, fila=qtdImg, positionFila=i)

        if isinstance(result, int) and result == 1: 
          print("Processo interrompido.")
          return

        image, used_seed = result
        elapsed_time = time.time() - start_time 
        print(f"Imagem {i+1}/{qtdImg} | Seed: {used_seed} | Duração: {elapsed_time:.2f}s\n")

        metadata = {
          "Prompt": prompt_text,
          "Negative Prompt": neg_prompt,
          "Steps": steps_val,
          "CFG Scale": cfg_val,
          "Seed": used_seed,
          "Size": f"{width}x{height}",
          "Model": os.path.splitext(os.path.basename(model_path))[0] if model_path else "Unknown",
          "Lora": selected_lora_name or "None",
          "Generation Time": f"{elapsed_time:.2f}s"
        }
        config.window.after(0, lambda img=image, meta=metadata: new_image_window(img, meta))

    except Exception as e:
      config.error(f"Erro Fatal: {e}")
      print(f"Erro no worker: {e}")
    finally:
      flush_memory()
      config.window.title(config.winTitle)
      config.window.configure(cursor="")
      generate_button.configure(state="normal", text="Gerar Imagem")
      temperature_label.configure(text="--°C", text_color="#D9D9D9")
      progress(100)

  config.threading.Thread(target=worker, daemon=True).start()