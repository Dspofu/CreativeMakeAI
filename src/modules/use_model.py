import os
import torch
import time
from config import*
from DeepCache import DeepCacheSDHelper
from src.functions.viwer_window import viwer_window
from src.functions.flush_memory import*
from src.functions.loading import progress

# Cache de Hash
cached_model_hash = {"path": None, "hash": None}

def use_model(generate_button, temperature_label, scale_image: str, prompt_entry: str, negative_prompt_entry: str, steps: int, cfg: float, seed_entry: int, lora_listbox, qtdImg: int):
  data.stop_img = False

  def worker():
    try:
      if data.benchmark_sequence:
        print("Aplicando calculo performático para multiplas imagens.")
        torch.backends.cudnn.benchmark = True

      if data.use_pipe is None:
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
      lora_to_apply = data.loaded_loras.get(selected_lora_name)
      lora_strength = 0.0
      data.use_pipe.unload_lora_weights()
      if lora_to_apply:
        lora_path = lora_to_apply["path"]
        lora_strength = lora_to_apply["cfg"]
        print(f"Aplicando LoRA '{selected_lora_name}'")
        try:
          data.use_pipe.load_lora_weights(lora_path)
        except:
          return config.alert("Esse LORA possui parâmentros que por padrão não são compativeis com o modelo atual.")

      # Controle do DeepCache
      try:
        current_helper = getattr(data, 'active_helper', None)
        if current_helper is not None:
          print("Limpando cache anterior...")
          current_helper.disable()
          data.active_helper = None
        if data.cache_interval > 1:
          print(f"Ativando DeepCache: {data.cache_interval}")
          helper = DeepCacheSDHelper(pipe=data.use_pipe)
          helper.set_params(cache_interval=data.cache_interval, cache_branch_id=0)
          helper.enable()
          data.active_helper = helper
          print(f"✓ DeepCache aplicado com intervalo de: \"{data.cache_interval}\".")
      except Exception as e:
        print(f"Erro ao manipular DeepCache: {e}")
        data.active_helper = None

      from src.modules.generate_image import generate_image

      # Seed Input
      try:
        seed_input = int(seed_entry.get())
      except:
        seed_input = -1

      model_path = getattr(config, "model_path", None)

      # Loop de geração
      for i in range(qtdImg):
        if data.stop_img:
          print("Detectada parada antes da geração.")
          break

        prompt_text = prompt_entry.get("1.0", "end-1c")
        neg_prompt = negative_prompt_entry.get("1.0", "end-1c") or data.negative_prompt
        steps_val = int(steps.get())
        cfg_val = round(cfg.get(), 1)

        # Seed incremental
        current_seed = seed_input
        if seed_input != -1 and i > 0:
          current_seed = seed_input + i

        start_time = time.time()

        # Chama a geração
        result = generate_image(generate_button, temperature_label, width, height, torch, data.use_pipe, data.limit_temp, prompt_text, neg_prompt, steps_val, cfg_val, lora_strength, seed=current_seed, fila=qtdImg, positionFila=i)

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
        config.window.after(0, lambda img=image, meta=metadata: viwer_window(img, meta))

    except Exception as e:
      config.error(f"Erro Fatal: {e}")
      print(f"Erro no worker: {e}")
    finally:
      flush_memory()
      config.window.title(Window.winTitle)
      config.window.configure(cursor="")
      generate_button.configure(state="normal", text="Gerar Imagem")
      temperature_label.configure(text="--°C", text_color="#D9D9D9")
      progress(100)

  config.threading.Thread(target=worker, daemon=True).start()