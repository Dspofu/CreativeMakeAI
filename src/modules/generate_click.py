import random
from tkinter import Image, Button
from diffusers import StableDiffusionXLPipeline
import config
from src.modules.loading import progress
import gc # Necessário para o Garbage Collector

def hash_tensor(tensor):
  import hashlib
  return hashlib.sha256(tensor.cpu().numpy().tobytes()).hexdigest()

def generate_click(generate_button: Button, temperature_label, width: int, height: int, torch, pipe: StableDiffusionXLPipeline, limit_temp: bool, prompt: str, negative_prompt: str, steps: int, cfg: float, lora_scale: float, seed: int, fila: int, positionFila: int) -> Image | int:
  config.window.configure(cursor="watch")
  import psutil
  import os
  from src.modules.safe_temp import safe_temp, reset_alert
  used_seed = None

  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    config.window.title(f"{config.winTitle} | Gerando imagem")
    
    # Monitoramento (apenas print, não afeta lógica)
    if torch.cuda.is_available():
      vram_gb = torch.cuda.memory_allocated() / 1024**3
    else:
      vram_gb = 0
        
    ram_gb = psutil.Process(os.getpid()).memory_info().rss / 1024**3
    
    print(f"Timestep: {timestep} | VRAM: {vram_gb:.2f}GB | RAM: {ram_gb:.2f}GB | Steps: {step_index+1}/{steps}   ", end=("\r" if step_index < steps - 1 else '\n'), flush=True)
    progress(int(((step_index+1)*100)/steps))
    generate_button.configure(text=f"Progresso: {step_index+1}/{steps} | Fila: {positionFila+1}/{fila}")

    if config.stop_img: return
    if limit_temp: safe_temp(pipe=pipe_instance, temp_label=temperature_label)
    return callback_kwargs

  try:
    # Lógica da Seed
    if seed is None or seed == -1:
      seed = random.randint(0, 2**32 - 1)
      print(f"Seed aleatória: {seed}")
    else:
      print(f"Usando a seed: {seed}")

    config.window.title(f"{config.winTitle} | Configurando parâmetros")
    
    # Generator manual para garantir reprodutibilidade
    # Se usar CPU offload, o generator precisa ser CPU ou CUDA dependendo de onde o tensor inicial é criado.
    # O Diffusers geralmente lida bem com generator="cuda" mesmo com offload.
    generator = torch.Generator(device="cuda").manual_seed(seed)
    used_seed = seed 

    # Gera a imagem
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
    # --- BLOCO DE SEGURANÇA CRÍTICO ---
    # Reseta UI
    if temperature_label:
      temperature_label.configure(text="--°C", text_color="#D9D9D9")
    
    # Limpeza agressiva de memória para evitar o "Crash de desligamento"
    # Isso devolve a memória para o Sistema Operacional e para a GPU
    print("Limpando cache de memória pós-geração...")
    gc.collect() # Limpa RAM Python
    if torch.cuda.is_available():
      torch.cuda.empty_cache() # Limpa VRAM alocada mas não usada
      torch.cuda.ipc_collect()
    # ----------------------------------