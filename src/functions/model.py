import config
import time
import gc
import torch
from tkinter import filedialog
from src.modules.loading import progress
from diffusers import StableDiffusionXLPipeline

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

    # Detecção de Hardware
    vram_total = 0
    gpu_name = "CPU"
    if torch.cuda.is_available():
      # Otimizações para NVIDIA
      torch.backends.cudnn.benchmark = True
      torch.backends.cuda.matmul.allow_tf32 = True
      vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**3
      gpu_name = torch.cuda.get_device_name(0)

    print(f"Dispositivo: {gpu_name} | VRAM: {vram_total:.1f}GB")
    progress(30)

    try:
      pipe = StableDiffusionXLPipeline.from_single_file(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        use_safetensors=True
      )

      config.model_path = model_path
      setattr(pipe, "model_path", model_path)
      config.setPipe = pipe

      model_button.configure(text="Otimizando Pipeline...")
      optimization_method = "Nenhum"
      progress(60)

      pytorch_version = tuple(map(int, torch.__version__.split('.')[:2]))
      if pytorch_version >= (2, 0):
        # PyTorch 2.0+ usa SDPA
        optimization_method = "PyTorch 2 SDPA"
        print("Usando SDPA nativo (Xformers Desabilitado)")
      else:
        try:
          pipe.enable_xformers_memory_efficient_attention()
          optimization_method = "Xformers"
          print("Usando Xformers (PyTorch < 2.0)")
        except Exception:
          pass
        finally:
          progress(70)

      if config.profile == "Low Memory" and optimization_method == "Nenhum":
        pipe.enable_attention_slicing()
        optimization_method = "Attention Slicing (Lento/Seguro)"

      print(f"Método de aceleração ativo: {optimization_method}")

      # Configuração do VAE
      if hasattr(pipe, "vae"):
        print("Configurando pipeline...")

        # Remove watermark para evitar delay extra
        if hasattr(pipe, "watermark"):
          pipe.watermark = None

        # Aplicar perfil de memória
        if config.profile == "Low Memory":
          pipe.enable_vae_tiling()
          pipe.enable_vae_slicing()
          pipe.enable_model_cpu_offload()
          print("Perfil Low Memory: VAE tiling + slicing + CPU offload")

        elif config.profile == "Balanced":
          # Balanced agora desativa slicing para evitar delay no final
          pipe.disable_vae_tiling()
          pipe.disable_vae_slicing()
          pipe.enable_model_cpu_offload()
          print("Perfil Balanced: VAE slicing OFF (Rapido) + CPU offload")

        else:  # High Performance
          pipe.disable_vae_tiling()
          pipe.disable_vae_slicing()
          pipe.to("cuda")
          print("Perfil High Performance: Tudo na VRAM")
        
        progress(77)

        pipe.vae.to(dtype=torch.float16)
        print(f"✓ Pipeline em {torch.get_default_dtype()}")
        progress(89)

        if pytorch_version >= (2, 0) and vram_total >= 12:
          try:
            import importlib.util
            has_triton = importlib.util.find_spec("triton") is not None
            is_rtx = "RTX" in gpu_name.upper()

            if has_triton and is_rtx:
              model_button.configure(text="Compilando UNet (pode demorar)...")
              print(f"✓ GPU RTX detectada: {gpu_name}")
              print("Compilando UNet - primeira geração lenta")

              pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=False)
              optimization_method += " + Compiled UNet"
              print("✓ UNet compilado! Próximas gerações serão 20-30% mais rápidas")
            else:
              print(f"ℹ Compilação desabilitada (requer Triton + Linux)")

          except Exception as e:
            print(f"Compilação desabilitada: {e}")

      progress(100)
      model_button.configure(text="Modelo Carregado")
      print(f"✓ Perfil: {config.profile} | Aceleração: {optimization_method}\n")

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