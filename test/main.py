import torch
import hashlib
import psutil
import os
import tkinter as tk
from diffusers import StableDiffusionXLPipeline
from PIL import ImageTk, Image

def hash_tensor(tensor):
  return hashlib.sha256(tensor.cpu().numpy().tobytes()).hexdigest()

# Caminho do checkpoint
ckpt_path = "E:/models/checkpoint/prefectPonyXL_v50.safetensors"
bg_frame = "#1e1e2f"
bg_input = "#1a1a28"
bg_window = "#1e1e2f"
fg_text = "white"

# Carrega o modelo base SDXL
pipe = StableDiffusionXLPipeline.from_single_file(
  ckpt_path,
  torch_dtype=torch.float16
)

pipe.enable_attention_slicing("auto")
pipe.vae.enable_tiling()
pipe.enable_model_cpu_offload()

some_weight = dict(pipe.unet.state_dict())['conv_in.weight']
print(f"Hash da UNet: {hash_tensor(some_weight)}\nVRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB\nRAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB")

# exit(0)
# GUI
window = tk.Tk()
window.title("v1.0.0 - CreativeMakeAI")
window.config(bg=bg_window)
window.geometry("600x400")
window.resizable(height=False, width=False)
main_frame = tk.Frame(window, bg=bg_frame, padx=30, pady=30)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Prompt
tk.Label(main_frame, text="Prompt:", font=("Arial", 12), bg=bg_frame, fg=fg_text).pack(anchor="w")
prompt_var = tk.StringVar()
tk.Entry(main_frame, textvariable=prompt_var, width=40, bg=bg_input, fg=fg_text, font=("Arial", 14), borderwidth=0, highlightthickness=0, insertbackground=fg_text).pack(pady=(5, 15), fill="x")

# Prompt negativo
tk.Label(main_frame, text="Prompt Negativo:", font=("Arial", 12), bg=bg_frame, fg=fg_text).pack(anchor="w")
negative_prompt_var = tk.StringVar()
tk.Entry(main_frame, textvariable=negative_prompt_var, width=40, bg=bg_input, fg=fg_text, font=("Arial", 14), borderwidth=0, highlightthickness=0, insertbackground=fg_text).pack(pady=(5, 15), fill="x")

# Função para moniotorar os steps
def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
  print(f"\nStep {step_index+1} | Timestep: {timestep}\nVRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB\nRAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB")
  return {}

# Função de click para gerar imagem
def generate_click():
  prompt = prompt_var.get()
  negative_prompt = negative_prompt_var.get()
  if not prompt.strip():
    print("Cancelado por falta de entrada.")
    return

  # Gera imagem
  image = pipe(
    prompt=prompt,
    negative_prompt=negative_prompt,
    num_inference_steps=70,
    guidance_scale=7.5,
    callback_on_step_end=listen_steps
  ).images[0]
  image.save("pony_result.png")
  print("Imagem salva como 'pony_result.png'.")
  newWindo = tk.Toplevel(window)
  newWindo.title("Image")
  newWindo.geometry("1024x1024")
  newWindo.resizable(height=False, width=False)

  # Exibir imagem na própria janela:
  img = ImageTk.PhotoImage(Image.open("pony_result.png").resize((1024, 1024)))
  panel = tk.Label(newWindo, image=img)
  panel.image = img
  panel.pack()

tk.Button(main_frame, text="Gerar Imagem", command=generate_click, bg="#4e4e6a", fg="white", font=("Arial", 12, "bold"), activebackground="#5e5e7f", activeforeground="white", cursor="hand2", bd=0, relief="flat", padx=10, pady=5).pack(pady=10, fill="x")

window.mainloop()