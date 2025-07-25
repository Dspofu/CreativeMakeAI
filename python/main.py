import torch
from diffusers import StableDiffusionXLPipeline
from safetensors.torch import load_file
import tkinter as tk

# GUI
# window = tk.Tk()
# window.title("v1.0.0 - CreativeMakeAI")
# window.geometry("400x300")

# tk.Label(window, text="Prompt:", font=("Arial", 12)).pack(pady=10)
# prompt_var = tk.StringVar()
# prompt_entry = tk.Entry(window, textvariable=prompt_var)
# prompt_entry.pack(pady=10)

def generate_click():
    ckpt_path = "E:/models/checkpoint/prefectPonyXL_v50.safetensors"

    pipe = StableDiffusionXLPipeline.from_pretrained(
        "stabilityai/stable-diffusion-xl-base-1.0",
        torch_dtype=torch.float16,
        variant="fp16",
    ).to("cuda")

    weights = load_file(ckpt_path)

    def load_weights_into_module(module, prefix):
        module_weights = {k[len(prefix):]: v for k, v in weights.items() if k.startswith(prefix)}
        missing, unexpected = module.load_state_dict(module_weights, strict=False)
        print(f"{prefix}: Missing: {len(missing)}, Unexpected: {len(unexpected)}")

    load_weights_into_module(pipe.unet, "unet.")
    load_weights_into_module(pipe.text_encoder, "text_encoder.")
    load_weights_into_module(pipe.text_encoder_2, "text_encoder_2.")
    load_weights_into_module(pipe.vae, "vae.")

    prompt = prompt_var.get()
    image = pipe(prompt).images[0]
    image.save("pony_result.png")

# tk.Button(window, text="Gerar imagem", command=generate_click).pack(pady=20)

# window.mainloop()