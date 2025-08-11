from tkinter import Image, Button

def hash_tensor(tensor):
  import hashlib
  return hashlib.sha256(tensor.cpu().numpy().tobytes()).hexdigest()

def generate_click(generate_button: Button, torch, pipe, limit_temp: bool, prompt: str, negative_prompt: str, steps: int, cfg: float, lora_scale) -> Image | int:
  import psutil
  import os
  from src.modules.coldGPU import safe_temp, reset_alert

  # Checagens de segurança
  if pipe is None:
    from src.modules.popup import error
    error("Erro: pipe não foi definido.")
    print("Erro: pipe não foi definido.")
    return 1

  if not prompt.strip():
    from src.modules.popup import error
    error("Prompt não identificado.")
    print("Prompt não identificado.")
    return 1

  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    print(f"Timestep: {timestep} | VRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB | RAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB | Steps: {step_index+1}/{steps}   ", end=("\r" if step_index < steps - 1 else '\n'), flush=True)
    generate_button.configure(text=f"Progresso: {step_index+1}/{steps}")
    if limit_temp:
      safe_temp(pipe=pipe_instance)
    return callback_kwargs

  try:
    image = pipe(
      prompt=prompt,
      negative_prompt=negative_prompt,
      num_inference_steps=steps,
      guidance_scale=cfg,
      cross_attention_kwargs={"scale": lora_scale},
      callback_on_step_end=listen_steps
    ).images[0]
    reset_alert()
    print("Imagem gerada.")
    return image

  except Exception as e:
    print(f"Ocorreu um erro: {e}")
    return 1