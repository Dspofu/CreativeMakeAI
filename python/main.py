import customtkinter as ctk

# Variaveis default
ckpt_path = "E:/models/checkpoint/prefectPonyXL_v50.safetensors"
# lora_path = "E:/models/checkpoint/LoRas/ellenjoePDXL_scarxzys.safetensors"
pipe = None

# Paleta de cores mantida
COR_BG_JANELA = "#1e1e2f"
COR_FRAME = "#1e1e2f"
COR_INPUT = "#1a1a28"
COR_TEXTO = "#FFFFFF"
COR_BOTAO = "#4e4e6a"
COR_BOTAO_HOVER = "#5e5e7f"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("v1.0.0 - CreativeMakeAI")
window.geometry("600x450")
window.resizable(False, False)
window.configure(fg_color=COR_BG_JANELA)

main_frame = ctk.CTkFrame(window, fg_color=COR_FRAME)
main_frame.place(relx=0.5, rely=0.5, anchor="center")

# Prompt
ctk.CTkLabel(main_frame, text="Prompt:", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(20, 5))
prompt_entry = ctk.CTkEntry(
  main_frame,
  width=400,
  height=40,
  font=("Arial", 14),
  fg_color=COR_INPUT,
  text_color=COR_TEXTO,
  border_width=0,
  corner_radius=8
)
prompt_entry.pack(padx=20, pady=(0, 20))

# Prompt Negativo
ctk.CTkLabel(main_frame, text="Prompt Negativo:", font=("Arial", 14)).pack(anchor="w", padx=20, pady=(0, 5))
negative_prompt_entry = ctk.CTkEntry(
  main_frame,
  width=400,
  height=40,
  font=("Arial", 14),
  fg_color=COR_INPUT,
  text_color=COR_TEXTO,
  border_width=0,
  corner_radius=8
)
negative_prompt_entry.pack(padx=20, pady=(0, 20))

# Função de hash
def hash_tensor(tensor):
  import hashlib
  return hashlib.sha256(tensor.cpu().numpy().tobytes()).hexdigest()

# Função de clique para gerar imagem
def generate_click():
  import torch
  # Carrega o modelo base SDXL
  from diffusers import StableDiffusionXLPipeline
  pipe = StableDiffusionXLPipeline.from_single_file(
    ckpt_path,
    torch_dtype=torch.float16,
    variant="f16"
  )

  # Otimizações
  torch.backends.cuda.matmul.allow_tf32 = True
  pipe.enable_attention_slicing("auto")
  pipe.vae.enable_tiling()
  pipe.enable_model_cpu_offload()

  import psutil
  import os
  some_weight = dict(pipe.unet.state_dict())['conv_in.weight']
  print(f"Hash da UNet: {hash_tensor(some_weight)}\nVRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB\nRAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB")

  # Função para monitorar os steps
  def listen_steps(pipe_instance, step_index, timestep, callback_kwargs) -> dict:
    print(f"\nStep {step_index+1} | Timestep: {timestep}\nVRAM: {torch.cuda.memory_allocated() / 1024**3:.2f}GB\nRAM: {psutil.Process(os.getpid()).memory_info().rss / 1024**3:.2f}GB")
    return {}

  prompt = prompt_entry.get()
  negative_prompt = negative_prompt_entry.get()

  if not prompt.strip():
      print("Cancelado por falta de entrada.")
      return
  
  # Desabilita o botão para evitar cliques múltiplos
  generate_button.configure(state="disabled", text="Gerando...")
  window.update_idletasks()

  try:
    # Gera imagem
    image = pipe(
        prompt=prompt,
        negative_prompt=negative_prompt,
        num_inference_steps=70,
        guidance_scale=7.5,
        callback_on_step_end=listen_steps
    ).images[0]
    print("Imagem gerada. Exibindo...")

    # Cria uma nova janela para a imagem usando CustomTkinter
    image_window = ctk.CTkToplevel(window)
    image_window.title("Imagem Gerada")
    image_window.geometry("1024x1024")
    image_window.resizable(False, False)
    image_window.configure(fg_color=COR_BG_JANELA)
    
    # Converte e exibe a imagem
    ctk_image = ctk.CTkImage(light_image=image, dark_image=image, size=(1024, 1024))
    image_label = ctk.CTkLabel(image_window, image=ctk_image, text="")
    image_label.pack(expand=True, fill="both")

  except Exception as e:
    print(f"Ocorreu um erro: {e}")
  finally:
    # Reabilita o botão após a conclusão
    generate_button.configure(state="normal", text="Gerar Imagem")

# Botão Gerar
generate_button = ctk.CTkButton(
  main_frame,
  text="Gerar Imagem",
  command=generate_click,
  font=("Arial", 14, "bold"),
  fg_color=COR_BOTAO,
  hover_color=COR_BOTAO_HOVER,
  height=40,
  corner_radius=8
)
generate_button.pack(padx=20, pady=20, fill="x")
window.mainloop()