import os
import torch
from diffusers import StableDiffusionXLPipeline
from safetensors.torch import load_file
import tkinter as tk
from PIL import ImageTk, Image
import hashlib

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
  "E:/models/checkpoint/prefectPonyXL_v50.safetensors",
  torch_dtype=torch.float16
)
# pipe = StableDiffusionXLPipeline.from_pretrained(
#   "stabilityai/stable-diffusion-xl-base-1.0",
#   torch_dtype=torch.float16,
#   variant="fp16",
#   use_safetensors=True,
#   low_cpu_mem_usage=True,
# )

# Ativa slicing de atenção (economiza MUITA VRAM)
pipe.enable_attention_slicing("auto")
# Tiling do VAE (ajuda em imagens grandes)
pipe.vae.enable_tiling()
# Offload do modelo (descarrega parte pra RAM)
pipe.enable_model_cpu_offload()
# Envia o pipeline pra GPU (parte do modelo fica na RAM)
# pipe.to("cuda")

# Exemplo: hash de algum peso da UNet
some_weight = dict(pipe.unet.state_dict())['conv_in.weight']
print("Hash da UNet:", hash_tensor(some_weight))

# Carrega pesos do checkpoint
weights = load_file(ckpt_path)

# Função para aplicar os pesos em cada parte do modelo
def load_weights_into_module(module, prefix):
  module_weights = {k[len(prefix):]: v for k, v in weights.items() if k.startswith(prefix)}
  missing, unexpected = module.load_state_dict(module_weights, strict=False)
  print(f"\n\n{prefix}: Missing: {len(missing)}, Unexpected: {len(unexpected)}")

# Aplica pesos nos componentes
load_weights_into_module(pipe.unet, "unet.")
# load_weights_into_module(pipe.text_encoder, "text_encoder.")
# load_weights_into_module(pipe.text_encoder_2, "text_encoder_2.")
# load_weights_into_module(pipe.vae, "vae.")

print(int(torch.cuda.memory_allocated() / 1024**2) / 1000, "GB usados")
# print(int(torch.cuda.memory_reserved() / 1024**2) / 1000, "GB reservados")
# del pipe
# torch.cuda.empty_cache()
# torch.cuda.ipc_collect()

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
  # os.system('cls' if os.name == 'nt' else 'clear')
  print(f"\nStep {step_index} | Timestep: {timestep}\n{int(torch.cuda.memory_allocated() / 1024**2) / 1000}GB Used\n{int(torch.cuda.memory_reserved() / 1024**2) / 1000}GB")
  return {}

# Função de click para gerar imagem
def generate_click():
  prompt = prompt_var.get()
  negative_prompt = negative_prompt_var.get()
  if not prompt.strip():
    print("Digite um prompt!")
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