import safetensors.torch
import config
import time
import gc 
from tkinter import filedialog
from src.modules.loading import progress
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler 

def select_model(model_button, generate_button, lora_listbox, model_lora, loaded_loras, lora_label, lora_scale):
  def worker():
    model_path = filedialog.askopenfilename(
      title="Selecionar Modelo",
      filetypes=[("Modelos .safetensors", "*.safetensors")]
    )
    if not model_path: return

    # Limpeza da memória
    if config.setPipe is not None:
      del config.setPipe
      config.setPipe = None
      gc.collect()
      if config.setTorch and config.setTorch.cuda.is_available():
        config.setTorch.cuda.empty_cache()

    print("Procurando metadados")
    meta = safetensors.torch.safe_open(model_path, framework="pt", device="cpu").metadata()
    if meta: print(f"Metadados encontrados:\n{meta}")
    
    lora_listbox.set("")
    loaded_loras.clear()
    lora_listbox.configure(values=[])
    lora_label.configure(text="LoRA Scale: 0.75")
    lora_scale.set(0.75)
    
    progress(0)
    config.window.title(f"{config.winTitle} | Carregando...")
    model_button.configure(state="disabled", text="Preparando ambiente")
    
    import torch
    config.setTorch = torch
    
    # Otimização de Kernel (Velocidade Pura)
    if torch.cuda.is_available():
      torch.backends.cudnn.benchmark = True 

    progress(30)
    model_button.configure(text="Lendo Safetensors")
    progress(50)
    
    try:
      config.window.title(f"{config.winTitle} | Inicializando Pipeline")
      
      pipe = StableDiffusionXLPipeline.from_single_file(
        model_path, 
        torch_dtype=torch.float16, 
        variant="fp16", 
        use_safetensors=True
      )

      # Scheduler DPM++ 2M Karras (Rápido)
      pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        pipe.scheduler.config, 
        use_karras_sigmas=True,
        algorithm_type="dpmsolver++"
      )
      
      config.model_path = model_path
      setattr(pipe, "model_path", model_path)
      config.setPipe = pipe

      print(f"Diretório do modelo: {model_path}")
      model_button.configure(text="Aplicando Perfil")
      progress(80)
      print(f"Aplicando o perfil: \"{config.profile}\"")
      
      if config.profile == "High Performance":
        # Muita VRAM não precisa de Tiling.
        config.setPipe.to("cuda")
        config.setPipe.disable_vae_slicing()
        config.setPipe.disable_vae_tiling()

      elif config.profile == "Balanced":
        config.setPipe.enable_model_cpu_offload()
        config.setPipe.enable_vae_slicing() # Slicing por segurança
        config.setPipe.disable_vae_tiling() # Sem Tiling para velocidade

      else: # Low Memory
        config.setPipe.enable_sequential_cpu_offload()
        config.setPipe.enable_vae_slicing()
        config.setPipe.enable_vae_tiling()

      progress(98)
      config.setPipe.set_progress_bar_config(disable=True)
      model_button.configure(text="Modelo carregado")
      
    except Exception as e:
      print(e)
      config.alert("Algo falhou. Tente o perfil 'Low Memory' se estiver travando.")
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
      print("Pronto.")
  
  config.threading.Thread(target=worker, daemon=True).start()