import random
from tkinter import Image, Button

def hash_tensor(tensor):
  import hashlib
  return hashlib.sha256(tensor.cpu().numpy().tobytes()).hexdigest()

def generate_click(generate_button: Button, temperature_label, torch, pipe, limit_temp: bool, prompt: str, negative_prompt: str, steps: int, cfg: float, lora_scale, seed) -> Image | int:
  import psutil
  import os
  from src.modules.coldGPU import safe_temp, reset_alert

  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    print(f"Timestep: {timestep} | VRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB | RAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB | Steps: {step_index+1}/{steps}   ", end=("\r" if step_index < steps - 1 else '\n'), flush=True)
    generate_button.configure(text=f"Progresso: {step_index+1}/{steps}")
    if limit_temp:
      safe_temp(pipe=pipe_instance, temp_label=temperature_label)
    return callback_kwargs

  try:
    if seed is None or seed == -1:
      seed = random.randint(0, 2**32 - 1)
      print(f"Seed aleatória: {seed}")
    else:
      print(f"Usando a seed: {seed}")

    generator = torch.Generator(device="cuda").manual_seed(seed)
    image = pipe(
      prompt=prompt,
      negative_prompt=negative_prompt,
      num_inference_steps=steps,
      guidance_scale=cfg,
      cross_attention_kwargs={"scale": lora_scale},
      callback_on_step_end=listen_steps,
      generator=generator,
    ).images[0]

    used_seed = generator.initial_seed()
    return image, used_seed
  except Exception as e:
    print(f"Ocorreu um erro: {e}")
    temperature_label.configure(text="--°C")
    return 1, -1
  finally:
    reset_alert()
    print(f"Imagem gerada | Seed: {used_seed}")
    temperature_label.configure(text="--°C")