import config
import time
from tkinter import filedialog

# Função de carregar modelo
def select_model(model_button, generate_button, lora_listbox, model_lora, loaded_loras, lora_label, lora_scale):
  def worker():
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
    model_button.configure(text="Configurando pesos")
    from diffusers import StableDiffusionXLPipeline
    config.setTorch = torch
    print("Carregando modelo.")
    model_button.configure(text="Carregando modelo")
    try:
      config.setPipe = StableDiffusionXLPipeline.from_single_file(model_path, torch_dtype=torch.float16, variant="fp16")
      print("Aplicando as otimizações.")
      model_button.configure(text="Otimizando modelo")
      config.setTorch.backends.cuda.matmul.allow_tf32 = True
      config.setPipe.enable_attention_slicing("auto")
      config.setPipe.vae.enable_tiling()
      config.setPipe.vae.to(dtype=config.setTorch.float16)
      config.setPipe.unet.to(memory_format=config.setTorch.channels_last)
      # setPipe.unet = torch.compile(setPipe.unet, mode="reduce-overhead", fullgraph=True)
      config.setPipe.enable_model_cpu_offload()
      config.setPipe.set_progress_bar_config(disable=True)
      model_button.configure(text="Modelo carregado")
    except Exception as e:
      print(e)
      config.alert("Algo falhou, verifique o modelo e compatibilidade do CUDA e versão dos drivers.")
      model_button.configure(state="normal", text="Falha no carregamento")
      generate_button.configure(state="disabled")
      model_lora.configure(state="disabled")
    finally:
      time.sleep(1.5)
      generate_button.configure(state="normal")
      model_lora.configure(state="normal")
      model_button.configure(state="normal", text="Selecionar modelo")
      print("Pronto para instruções.")
  config.threading.Thread(target=worker, daemon=True).start()