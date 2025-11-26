import random
from tkinter import Image, Button
from diffusers import StableDiffusionXLPipeline
import config
from src.modules.loading import progress
import gc # Garbage Collector

def hash_tensor(tensor):
  import hashlib
  return hashlib.sha256(tensor.cpu().numpy().tobytes()).hexdigest()

def generate_click(generate_button: Button, temperature_label, width: int, height: int, torch, pipe: StableDiffusionXLPipeline, limit_temp: bool, prompt: str, negative_prompt: str, steps: int, cfg: float, lora_scale: float, seed: int, fila: int, positionFila: int) -> Image | int:
  config.window.configure(cursor="watch")
  from src.modules.safe_temp import safe_temp
  used_seed = None

  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    progress(int(((step_index+1)*100)/steps))
    generate_button.configure(text=f"Gerando: {step_index+1}/{steps} | Fila: {positionFila+1}/{fila}")
    if limit_temp: safe_temp(pipe=pipe_instance, temp_label=temperature_label)
    if config.stop_img: return callback_kwargs
    return callback_kwargs

  try:
    # Lógica da Seed
    if seed is None or seed == -1:
      seed = random.randint(0, 2**32 - 1)
      print(f"\nSeed aleatória: {seed}")
    else:
      print(f"\nUsando a seed: {seed}")

    config.window.title(f"{config.winTitle} | Configurando parâmetros")
    generator = torch.Generator(device="cuda").manual_seed(seed)
    used_seed = seed 

    # Gera a imagem
    config.window.title(f"{config.winTitle} | Gerando")
    image = pipe(
      width=width,
      height=height,
      prompt=prompt,
      negative_prompt=negative_prompt,
      num_inference_steps=steps,
      guidance_scale=cfg,
      cross_attention_kwargs={"scale": lora_scale},
      callback_on_step_end=listen_steps,
      generator=generator
    ).images[0]

    return image, used_seed

  except Exception as e:
    if config.stop_img:
      print("Processo interrompido pelo usuário.")
      return 1, -1
    
    error_str = str(e)
    if "triton" in error_str.lower():
      config.alert("Erro de Compilação (Triton):\nRecurso não suportado no Windows.\nTroque o perfil para Balanced/Low.")
    else:
      config.alert(f"Ocorreu um erro na geração:\n{e}")
      print(f"Ocorreu um erro: {e}")
      
    return 1, -1

  finally:
    if temperature_label:
      temperature_label.configure(text="--°C", text_color="#D9D9D9")
    
    # Limpeza agressiva de memória
    print("Limpando cache de memória pós-geração...")
    gc.collect() # Limpa RAM Python
    if torch.cuda.is_available():
      torch.cuda.empty_cache() # Limpa VRAM alocada mas não usada
      torch.cuda.ipc_collect()