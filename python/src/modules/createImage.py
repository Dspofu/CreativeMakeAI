from tkinter import Image

def hash_tensor(tensor):
  import hashlib
  return hashlib.sha256(tensor.cpu().numpy().tobytes()).hexdigest()

def generate_click(torch, pipe, some_weight, prompt: str, negative_prompt: str, steps: int, cfg: float) -> Image | int:
  import psutil
  import os

  # Checagens de segurança
  if pipe is None:
    from src.modules.popup import alert
    alert("Erro: pipe não foi definido.")
    print("Erro: pipe não foi definido.")
    return 1

  if some_weight is None:
    from src.modules.popup import alert
    alert("Erro: some_weight não está definido.")
    print("Erro: some_weight não está definido.")
    return 1

  if not prompt.strip():
    from src.modules.popup import alert
    alert("Prompt não identificado.")
    print("Prompt não identificado.")
    return 1

  print(f"Hash da UNet: {hash_tensor(some_weight)}")
  print(f"VRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB")
  print(f"RAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB")

  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    print(f"\nStep {step_index+1} | Timestep: {timestep}")
    print(f"VRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB")
    print(f"RAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB")
    return {}

  try:
    image = pipe(
      prompt=prompt,
      negative_prompt=negative_prompt,
      num_inference_steps=steps,
      guidance_scale=cfg,
      callback_on_step_end=listen_steps
    ).images[0]
    print("Imagem gerada. Exibindo...")
    return image

  except Exception as e:
    print(f"Ocorreu um erro: {e}")
    return 1