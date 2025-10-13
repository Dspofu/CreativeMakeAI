import safetensors.torch
import config
import time
from tkinter import filedialog

from src.modules.loading import progress

# Função de carregar modelo
def select_model(model_button, generate_button, lora_listbox, model_lora, loaded_loras, lora_label, lora_scale):
  def worker():
    model_path = filedialog.askopenfilename(
      title="Selecionar Modelo",
      filetypes=[("Modelos .safetensors", "*.safetensors")]
    )
    if not model_path: return
    print("Procurando metadados")
    meta = safetensors.torch.safe_open(model_path, framework="pt", device="cpu").metadata()
    if meta: print(f"Metadados encontrados do modelo:\n{meta}")
    lora_listbox.set("")
    loaded_loras.clear()
    lora_listbox.configure(values=[])
    lora_label.configure(text="LoRA Scale: 0.75")
    lora_scale.set(0.75)
    progress(0)
    print("Iniciando pacotes.")
    config.window.title(f"{config.winTitle} | Carregando 1/2")
    model_button.configure(state="disabled", text="Preparando ambiente")
    import torch
    progress(30)
    config.window.title(f"{config.winTitle} | Carregando 2/2")
    model_button.configure(text="Preparando ajustes")
    from diffusers import StableDiffusionXLPipeline
    progress(50)
    config.setTorch = torch
    print("Carregando modelo.")
    model_button.configure(text="Carregando modelo")
    progress(70)
    try:
      config.window.title(f"{config.winTitle} | Otimizando")
      config.setPipe = StableDiffusionXLPipeline.from_single_file(model_path, torch_dtype=torch.float16, variant="fp16")
      print("Aplicando as otimizações.")
      model_button.configure(text="Otimizando modelo")
      progress(80)
      config.setTorch.backends.cuda.matmul.allow_tf32 = True
      progress(83)
      config.setPipe.enable_attention_slicing("auto")
      progress(85)
      config.setPipe.vae.enable_tiling()
      progress(88)
      config.setPipe.vae.to(dtype=config.setTorch.float16)
      progress(93)
      config.setPipe.unet.to(memory_format=config.setTorch.channels_last)
      # setPipe.unet = torch.compile(setPipe.unet, mode="reduce-overhead", fullgraph=True)
      progress(95)
      config.setPipe.enable_model_cpu_offload()
      progress(98)
      config.setPipe.set_progress_bar_config(disable=True)
      model_button.configure(text="Modelo carregado")
    except Exception as e:
      print(e)
      config.alert("Algo falhou, verifique o modelo e usa compatibilidade de CUDA ou versão dos drivers.")
      model_button.configure(state="normal", text="Falha no carregamento")
      generate_button.configure(state="disabled")
      model_lora.configure(state="disabled")
    finally:
      time.sleep(1.5)
      config.window.title(config.winTitle)
      generate_button.configure(state="normal")
      model_lora.configure(state="normal")
      model_button.configure(state="normal", text="Selecionar modelo")
      progress(100)
      print("Pronto para instruções.")
  config.threading.Thread(target=worker, daemon=True).start()