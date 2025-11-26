import config
import time
import gc 
import torch
from tkinter import filedialog
from src.modules.loading import progress
from diffusers import StableDiffusionXLPipeline, EulerAncestralDiscreteScheduler

def select_model(model_button, generate_button, lora_listbox, model_lora, loaded_loras, lora_label, lora_scale):
  def worker():
    model_path = filedialog.askopenfilename(
      title="Selecionar Modelo",
      filetypes=[("Modelos .safetensors", "*.safetensors")]
    )
    if not model_path: return

    # Limpeza do Pipe/memória
    if config.setPipe is not None:
      del config.setPipe
      config.setPipe = None
    gc.collect()
    if torch.cuda.is_available():
      torch.cuda.empty_cache()
      torch.cuda.ipc_collect()

    lora_listbox.set("")
    loaded_loras.clear()
    lora_listbox.configure(values=[])
    
    progress(10)
    config.window.title(f"{config.winTitle} | Carregando...")
    model_button.configure(state="disabled", text="Analisando Hardware...")
    
    config.setTorch = torch
    
    # Detecção de Hardware
    vram_total = 0
    gpu_name = "CPU"
    if torch.cuda.is_available():
      # Otimizações para NVIDIA
      torch.backends.cudnn.benchmark = True 
      torch.backends.cuda.matmul.allow_tf32 = True
      vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
      gpu_name = torch.cuda.get_device_name(0)
    
    print(f"Hardware detectado: {gpu_name} | VRAM: {vram_total:.1f}GB")
    progress(30)
    
    try:
      # Se tiver pouca VRAM (<6GB) usa FP16. Se for CPU usa float32.
      dtype_load = torch.float16 if torch.cuda.is_available() else torch.float32
      
      pipe = StableDiffusionXLPipeline.from_single_file(
        model_path, 
        torch_dtype=dtype_load, 
        variant="fp16", 
        use_safetensors=True
      )

      # Scheduler Euler para velocidade
      pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
      
      config.model_path = model_path
      setattr(pipe, "model_path", model_path)
      config.setPipe = pipe

      model_button.configure(text="Otimizando Pipeline...")
      progress(60)      
      optimization_method = "Nenhum"
      
      # Xformers (Melhor para GTX 1000/RTX 2000/3000)
      try:
        pipe.enable_xformers_memory_efficient_attention()
        optimization_method = "Xformers"
      except Exception:
        try:
          optimization_method = "PyTorch 2 SDPA (Nativo)"
        except:
          pass
      # Se for Perfil "Low Memory" e não conseguiu Xformers, ativa Slicing.
      if config.profile == "Low Memory" and optimization_method == "Nenhum":
        pipe.enable_attention_slicing()
        optimization_method = "Attention Slicing (Lento/Seguro)"

      print(f"Método de aceleração ativo: {optimization_method}")

      # VAE otimizado
      if hasattr(pipe, "vae"):
        pipe.vae.to(dtype=torch.float16)
        if config.profile == "Low Memory":
          pipe.enable_vae_tiling()
          pipe.enable_vae_slicing()
          pipe.enable_model_cpu_offload()
        elif config.profile == "Balanced":
          pipe.disable_vae_tiling()
          pipe.enable_vae_slicing()
          pipe.enable_model_cpu_offload()
        else: # High Performance
          pipe.disable_vae_tiling()
          pipe.disable_vae_slicing()
          pipe.to("cuda")
      progress(100)
      model_button.configure(text="Modelo Carregado")
      print(f"Perfil: {config.profile} | Aceleração: {optimization_method}")
      
    except Exception as e:
      print(f"Erro Fatal: {e}")
      config.alert(f"Erro ao carregar modelo:\n{e}\nTente o perfil 'Low Memory'.")
      model_button.configure(state="normal", text="Erro")
      generate_button.configure(state="disabled")
      return

    finally:
      time.sleep(1)
      config.window.title(config.winTitle)
      generate_button.configure(state="normal")
      model_lora.configure(state="normal")
      model_button.configure(state="normal", text="Selecionar modelo")
  
  config.threading.Thread(target=worker, daemon=True).start()