import random
from tkinter import Button
from diffusers import StableDiffusionXLPipeline
import config
from src.modules.loading import progress

def generate_click(generate_button: Button, temperature_label, width: int, height: int, torch, pipe: StableDiffusionXLPipeline, limit_temp: bool, prompt: str, negative_prompt: str, steps: int, cfg: float, lora_scale: float, seed: int, fila: int, positionFila: int):
  config.window.configure(cursor="watch")
  from src.modules.safe_temp import safe_temp

  used_seed = None

  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    progress(int(((step_index+1)*100)/steps))
    generate_button.configure(text=f"Gerando: {step_index+1}/{steps} | Fila: {positionFila+1}/{fila}")
    if limit_temp: safe_temp(pipe=pipe_instance, temp_label=temperature_label)
    if config.stop_img:
      pipe_instance._interrupt = True 
      return callback_kwargs
    return callback_kwargs

  try:
    if seed is None or seed == -1:
      seed = random.randint(0, 2**32 - 1)

    # Gerar Seed
    generator = torch.Generator(device="cpu").manual_seed(seed) # device = "cuda" if torch.cuda.is_available() else "cpu"
    used_seed = seed

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
      print("Geração interrompida pelo usuário.")
      return 1, -1
    config.alert(f"Erro na geração:\n{e}")
    print(f"Erro crítico: {e}")
    return 1, -1

  finally:
    if temperature_label:
      temperature_label.configure(text="--°C", text_color="#D9D9D9")