import os
import config
import time
import gc
import torch
from tkinter import filedialog
from src.functions.loading import progress
from diffusers import StableDiffusionXLPipeline, StableDiffusionPipeline
from compel import Compel, ReturnedEmbeddingsType


def apply_global_optimizations():
  print("Aplicando otimizações NVIDIA")
  torch.backends.cuda.enable_flash_sdp(True)
  torch.backends.cuda.enable_mem_efficient_sdp(True)
  torch.backends.cuda.enable_math_sdp(False)
  torch.set_float32_matmul_precision("high")

def setup_low(pipe):
  print("Aplicando perfil Low Memory...")
  pipe.enable_model_cpu_offload()
  pipe.enable_attention_slicing("auto")
  pipe.disable_attention_slicing()
  pipe.disable_vae_slicing()
  pipe.disable_freeu()
  pipe.disable_vae_tiling()
  pipe.disable_xformers_memory_efficient_attention()

def setup_medium(pipe):
  print("Aplicando perfil Balanced...")
  pipe.to("cuda", dtype=torch.float16)
  pipe.enable_attention_slicing("auto")
  pipe.disable_attention_slicing()
  pipe.disable_vae_slicing()
  pipe.disable_freeu()
  pipe.disable_vae_tiling()
  pipe.disable_xformers_memory_efficient_attention()

def setup_high(pipe):
  print("Aplicando perfil High Performance...")
  pipe.to("cuda", dtype=torch.float16)
  pipe.disable_attention_slicing()
  pipe.disable_vae_slicing()
  pipe.disable_freeu()
  pipe.disable_vae_tiling()
  pipe.disable_xformers_memory_efficient_attention()

  torch._inductor.config.conv_1x1_as_mm = True
  torch._inductor.config.coordinate_descent_tuning = True
  torch._inductor.config.epilogue_fusion = False
  torch._inductor.config.coordinate_descent_check_all_directions = True


def select_model(model_button, generate_button, lora_listbox, model_lora, loaded_loras):
  def worker():
    model_path = filedialog.askopenfilename(
      title="Selecionar Modelo",
      filetypes=[("Modelos .safetensors", "*.safetensors")]
    )
    if not model_path:
      return

    if config.setPipe is not None:
      del config.setPipe
      config.setPipe = None
      print("Lixo removido!")

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

    vram_total = 0
    device = ""

    if torch.cuda.is_available():
      device = "cuda"
      apply_global_optimizations()
      vram_total = torch.cuda.get_device_properties(0).total_memory / 1024**2
      gpu_name = torch.cuda.get_device_name(0)
    else:
      device = "cpu"
      gpu_name = "CPU"

    print(f"Dispositivo: {gpu_name} | VRAM: {vram_total:.1f}MB")
    progress(30)

    try:
      if "xl" in model_path.lower() or True:

        pipe = StableDiffusionXLPipeline.from_single_file(
          model_path,
          torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
          use_safetensors=True
        )

        config.setCompel = Compel(
          tokenizer=[pipe.tokenizer, pipe.tokenizer_2],
          text_encoder=[pipe.text_encoder, pipe.text_encoder_2],
          returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
          requires_pooled=[False, True],
          device=device
        )

      else:
        pipe = StableDiffusionPipeline.from_single_file(
          model_path,
          torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
          use_safetensors=True
        )

        config.setCompel = Compel(
          tokenizer=pipe.tokenizer,
          text_encoder=pipe.text_encoder,
          device=device
        )

      config.model_path = model_path
      setattr(pipe, "model_path", model_path)
      config.setPipe = pipe

      progress(55)
      optimization_method = "Nenhum"

      if vram_total >= 12000:
        try:
          import importlib.util
          has_triton = importlib.util.find_spec("triton") is not None
          is_rtx = "RTX" in gpu_name.upper()

          if has_triton and is_rtx:
            model_button.configure(text="Compilando UNet (pode demorar)...")
            print(f"✓ GPU RTX detectada: {gpu_name}")
            print("Compilando UNet...")

            pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead", fullgraph=False)
            pipe.vae.forward = torch.compile(pipe.vae.forward, mode="max-autotune", fullgraph=True)

            optimization_method = "Compiled UNet"
            print("✓ Compilação concluída! UNet otimizado.")
          else:
            print("Compilação indisponível (requer Triton + RTX no Linux).")

        except Exception as e:
          print(f"Compilação desabilitada: {e}")

      progress(68)
      if hasattr(pipe, "vae"):
        if config.profile == "Low Memory":
          setup_low(pipe)
          print("Perfil Low Memory aplicado.")

        elif config.profile == "Balanced":
          setup_medium(pipe)
          print("Perfil Balanced aplicado.")

        else:
          setup_high(pipe)
          print("Perfil High Performance aplicado.")
      else:
        print("Pipeline inicializado usando cache.")

      progress(82)
      print(f"✓ Pipeline em {pipe.unet.dtype} | {pipe.text_encoder.dtype} | {pipe.vae.dtype}")

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