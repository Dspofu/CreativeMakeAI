import random
from tkinter import Button
from config import*
from src.functions.loading import progress
from src.modules.load_model import StableDiffusionPipeline, StableDiffusionXLPipeline

def generate_image(generate_button: Button, temperature_label, width: int, height: int, torch, pipe: StableDiffusionXLPipeline | StableDiffusionPipeline, limit_temp: bool, prompt: str, negative_prompt: str, steps: int, cfg: float, lora_scale: float, seed: int, fila: int, positionFila: int):
  config.window.configure(cursor="watch")
  from src.functions.safe_temp import safe_temp

  used_seed = None

  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    progress(int(((step_index+1)*100)/steps))
    generate_button.configure(text=f"Gerando: {step_index+1}/{steps} | Fila: {positionFila+1}/{fila}")
    if limit_temp: safe_temp(pipe=pipe_instance, temp_label=temperature_label)
    if data.stop_img:
      pipe_instance._interrupt = True 
      return callback_kwargs
    return callback_kwargs

  try:
    if seed is None or seed == -1:
      seed = random.randint(0, 2**32 - 1)

    # Gerar Seed
    generator = torch.Generator(device="cpu").manual_seed(seed) # device = "cuda" if torch.cuda.is_available() else "cpu"
    used_seed = seed

    # compel_prompt, pooled_prompt = data.use_compel(prompt)
    # compel_negative_prompt, pooled_negative_prompt = data.use_compel(negative_prompt)

    image = pipe(
      width=width,
      height=height,
      prompt=prompt,
      negative_prompt=negative_prompt,
      # prompt_embeds=compel_prompt,
      # pooled_prompt_embeds=pooled_prompt,
      # negative_prompt_embeds=compel_negative_prompt,
      # negative_pooled_prompt_embeds=pooled_negative_prompt,
      num_inference_steps=steps,
      guidance_scale=cfg,
      cross_attention_kwargs={"scale": lora_scale},
      callback_on_step_end=listen_steps,
      generator=generator
    ).images[0]
    return image, used_seed

  except Exception as e:
    if data.stop_img:
      print("Geração interrompida pelo usuário.")
      return 1, -1
    config.alert(f"Erro na geração:\n{e}")
    print(f"Erro crítico: {e}")
    return 1, -1
  finally:
    progress(100)