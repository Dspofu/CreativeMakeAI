import os
import time
import gc
import torch
from tkinter import filedialog
from diffusers.schedulers.scheduling_dpmsolver_multistep import DPMSolverMultistepScheduler
from config import*
from src.functions.detect_dtype import detect_dtype
from src.functions.loading import progress
from diffusers import StableDiffusionXLPipeline, StableDiffusionPipeline, FluxPipeline, ZImagePipeline, AutoPipelineForText2Image
from compel import Compel, ReturnedEmbeddingsType
from optimum.quanto import quantize, qfloat8, freeze, max_optimizer
from transformers import CLIPTextModel, CLIPTokenizer, T5EncoderModel, T5TokenizerFast, Qwen3Model

dtype_recommendation = detect_dtype()

def apply_global_optimizations():
  print("Aplicando otimizações NVIDIA")
  torch.set_float32_matmul_precision("high")
  torch.backends.cuda.matmul.allow_tf32 = True
  torch.backends.cudnn.allow_tf32 = True
  # torch.backends.cudnn.benchmark = True - Lento
  torch.backends.cuda.enable_flash_sdp(True)
  torch.backends.cuda.enable_mem_efficient_sdp(True)
  torch.backends.cuda.enable_math_sdp(False)

def setup_low(pipe: StableDiffusionXLPipeline):
  print("Aplicando perfil Low Memory...")
  pipe.vae.enable_slicing()
  pipe.vae.enable_tiling()
  pipe.enable_attention_slicing("auto")
  quantize(pipe.unet, weights=qfloat8)
  freeze(pipe.unet)
  quantize(pipe.text_encoder, weights=qfloat8)
  freeze(pipe.text_encoder)
  quantize(pipe.vae, weights=qfloat8)
  freeze(pipe.vae)
  pipe.enable_model_cpu_offload()

def setup_medium(pipe: StableDiffusionXLPipeline):
  print("Aplicando perfil Balanced...")
  pipe.disable_attention_slicing()
  pipe.vae.disable_slicing()
  quantize(pipe.unet, weights=qfloat8)
  freeze(pipe.unet)
  quantize(pipe.text_encoder, weights=qfloat8)
  freeze(pipe.text_encoder)
  quantize(pipe.vae, weights=qfloat8)
  freeze(pipe.vae)
  pipe.to("cuda")

def setup_high(pipe: StableDiffusionXLPipeline):
  print("Aplicando perfil High Performance...")
  pipe.disable_attention_slicing()
  pipe.vae.disable_slicing()
  pipe.to("cuda")
  # print("Compilação ativa!")
  # pipe.transformer.compile_repeated_blocks(fullgraph=True)
  # print(pipe.unet)
  # print("\n\n")
  # print(torch.compile(pipe.unet))
  # pipe.unet = torch.compile(pipe.unet)

def select_model(model_button, generate_button, lora_listbox, model_lora, loaded_loras):
  def worker():
    model_path = filedialog.askopenfilename(
      title="Selecionar Modelo",
      filetypes=[("Modelos .safetensors", "*.safetensors")]
    )
    if not model_path:
      return

    if data.use_pipe is not None:
      del data.use_pipe
      data.use_pipe = None
      print("Lixo removido!")

    gc.collect()
    if torch.cuda.is_available():
      torch.cuda.empty_cache()
      torch.cuda.ipc_collect()
      torch.cuda.synchronize()

    lora_listbox.set("")
    loaded_loras.clear()
    lora_listbox.configure(values=[])

    progress(10)
    config.window.title(f"{Window.winTitle} | Carregando...")
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
      torch._inductor.config.conv_1x1_as_mm = True
      torch._inductor.config.coordinate_descent_tuning = True
      torch._inductor.config.epilogue_fusion = False
      torch._inductor.config.coordinate_descent_check_all_directions = True

      if "xl" in model_path.lower() or (os.path.getsize(model_path) / 1024**2 >= 4500): # Para modelos SDXL
        try:
          print("Tentando SDXL")
          pipe = StableDiffusionXLPipeline.from_single_file(
            model_path,
            torch_dtype=dtype_recommendation,
            use_safetensors=True
          )
        except:
          try:
            print("Tentando Flux")
            text_encoder = Qwen3Model.from_pretrained(
              "Qwen/Qwen2.5-TextEncoder",
              dtype=dtype_recommendation
            ).to("cuda")

            pipe = FluxPipeline.from_single_file(
              model_path,
              text_encoder=text_encoder,
              torch_dtype=dtype_recommendation,
              use_safetensors=True
            )
          except:
            try:
              print("Tentando ZImage")
              text_encoder = Qwen3Model.from_pretrained(
                "Qwen/Qwen2.5-TextEncoder",
                dtype=dtype_recommendation
              ).to("cuda")

              pipe = ZImagePipeline.from_single_file(
                model_path,
                text_encoder=text_encoder,
                torch_dtype=dtype_recommendation,
                use_safetensors=True
              )
            except:
              config.alert("Não foi possivel achar um metodo de leitura compativel ao modelo correspondente\nVerifique se o modelo está completo.")
              return
        # pipe.transformer.compile_repeated_blocks(fullgraph=True)
        data.use_compel = Compel(
          tokenizer=[pipe.tokenizer, pipe.tokenizer_2],
          text_encoder=[pipe.text_encoder, pipe.text_encoder_2],
          returned_embeddings_type=ReturnedEmbeddingsType.PENULTIMATE_HIDDEN_STATES_NON_NORMALIZED,
          requires_pooled=[False, True],
          device=device
        )

        # pipe.unet.to(dtype=torch.float8_e5m2fnuz)
        # pipe.text_encoder.to(dtype=torch.float8_e5m2fnuz)
        # pipe.vae.to(dtype=torch.float8_e5m2fnuz)

        # pipe.scheduler = DPMSolverMultistepScheduler.from_config(
        #   pipe.scheduler.config, 
        #   use_karras_sigmas=True,
        #   algorithm_type="sde-dpmsolver++"
        # )

        # helper = DeepCacheSDHelper(pipe=pipe)
        # helper.set_params(
        #   cache_interval=3,
        #   cache_branch_id=0,
        # )
        # helper.enable()
        # helper.disable()
      else: # Para modeloes SD1 e SD2
        pipe = StableDiffusionPipeline.from_single_file(
          model_path,
          torch_dtype=dtype_recommendation,
          use_safetensors=True
        )

        data.use_compel = Compel(
          tokenizer=pipe.tokenizer,
          text_encoder=pipe.text_encoder,
          device=device
        )

      pipe.unet.to(memory_format=torch.channels_last)
      pipe.vae.to(memory_format=torch.channels_last)
      # pipe.transformer.set_attention_backend("flash")
      data.model_path = model_path
      setattr(pipe, "model_path", model_path)
      data.use_pipe = pipe

      progress(55)
      optimization_method = "Nenhum"

      if vram_total >= 12000:
        try:
          import importlib.util
          has_triton = importlib.util.find_spec("triton") is not None
          is_rtx = "RTX" in gpu_name.upper()

          if has_triton and is_rtx and False: # Defini como falso, pois to validando erros ainda
            model_button.configure(text="Compilando UNet (pode demorar)...")
            print(f"✓ GPU RTX detectada: {gpu_name}")
            print("Compilando UNet...")

            pipe.unet = torch.compile(pipe.unet, mode="reduce-overhead")
            pipe.text_encoder = torch.compile(pipe.text_encoder, mode="reduce-overhead")
            pipe.vae.forward = torch.compile(pipe.vae.forward, mode="max-autotune")

            optimization_method = "Compiled UNet"
            print("✓ Compilação concluída! UNet otimizado.")
          else:
            print("Compilação indisponível (requer Triton + RTX no Linux).")

        except Exception as e:
          print(f"Compilação desabilitada: {e}")

      progress(68)
      if data.profile == "Low Memory":
        setup_low(pipe)
        print("Perfil Low Memory aplicado.")
      elif data.profile == "Balanced":
        setup_medium(pipe)
        print("Perfil Balanced aplicado.")
      else:
        setup_high(pipe)
        print("Perfil High Performance aplicado.")

      progress(82)
      print(f"✓ Pipeline em {pipe.unet.dtype} | {pipe.text_encoder.dtype} | {pipe.vae.dtype}")

      progress(100)
      model_button.configure(text="Modelo Carregado")
      print(f"✓ Perfil: {data.profile} | Aceleração: {optimization_method}\n")

    except Exception as e:
      print(f"Erro Fatal: {e}")
      config.alert(f"Erro ao carregar modelo:\n{e}\nTente o perfil 'Low Memory'.")
      model_button.configure(state="normal", text="Erro")
      generate_button.configure(state="disabled")
      return

    finally:
      time.sleep(1)
      config.window.title(Window.winTitle)
      generate_button.configure(state="normal")
      model_lora.configure(state="normal")
      model_button.configure(state="normal", text="Selecionar modelo")

  config.threading.Thread(target=worker, daemon=True).start()