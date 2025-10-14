import random
from tkinter import Image, Button
from diffusers import StableDiffusionXLPipeline
import config
from src.modules.loading import progress

def hash_tensor(tensor):
  import hashlib
  return hashlib.sha256(tensor.cpu().numpy().tobytes()).hexdigest()

def generate_click(generate_button: Button, temperature_label, width: int, height: int, torch, pipe: StableDiffusionXLPipeline, limit_temp: bool, prompt: str, negative_prompt: str, steps: int, cfg: float, lora_scale: float, seed: int, fila: int, positionFila: int) -> Image | int:
  config.window.configure(cursor="watch")
  import psutil
  import os
  from src.modules.safe_temp import safe_temp, reset_alert

  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    config.window.title(f"{config.winTitle} | Gerando imagem")
    print(f"Timestep: {timestep} | VRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB | RAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB | Steps: {step_index+1}/{steps}   ", end=("\r" if step_index < steps - 1 else '\n'), flush=True)
    progress(int(((step_index+1)*100)/steps))
    generate_button.configure(text=f"Progresso: {step_index+1}/{steps} | Fila: {positionFila+1}/{fila}")

    if config.stop_img: return
    if limit_temp: safe_temp(pipe=pipe_instance, temp_label=temperature_label)
    return callback_kwargs

  try:
    if seed is None or seed == -1:
      seed = random.randint(0, 2**32 - 1)
      print(f"Seed aleatória: {seed}")
    else:
      print(f"Usando a seed: {seed}")

    config.window.title(f"{config.winTitle} | Configurando parâmetros")
    generator = torch.Generator(device="cuda").manual_seed(seed)
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

    used_seed = generator.initial_seed()
    return image, used_seed
  except Exception as e:
    if config.stop_img: return 1, -1
    print(f"Ocorreu um erro: {e}")
    return 1, -1
  finally:
    # reset_alert()
    if 'used_seed' in locals(): print(f"Imagem gerada | Seed: {used_seed}")
    else: print("Falha, seed não gerada corretamente.")
    temperature_label.configure(text="--°C", text_color="#D9D9D9")