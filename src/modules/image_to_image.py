StableDiffusionXLImg2ImgPipeline

pipe_texto = StableDiffusionXLPipeline.from_single_file("modelo.safetensors", ...)

pipe_img2img = StableDiffusionXLImg2ImgPipeline(
    vae=pipe_texto.vae,
    text_encoder=pipe_texto.text_encoder,
    text_encoder_2=pipe_texto.text_encoder_2,
    tokenizer=pipe_texto.tokenizer,
    tokenizer_2=pipe_texto.tokenizer_2,
    unet=pipe_texto.unet,
    scheduler=pipe_texto.scheduler
)

SAVE_DIR = "compiled_cache"
UNET_PATH = f"{SAVE_DIR}/unet.pt"
VAE_PATH = f"{SAVE_DIR}/vae.pt"

def save_model(pipe):
  os.makedirs(SAVE_DIR, exist_ok=True)
  print("Salvando modelos (UNet + VAE)...")
  torch.save(pipe.unet.state_dict(), UNET_PATH)
  torch.save(pipe.vae.state_dict(), VAE_PATH)
  print("Modelos salvos no cache.")

def load_cached_models(pipe):
  if not (os.path.exists(UNET_PATH) and os.path.exists(VAE_PATH)):
    print("Nenhum cache encontrado.")
    return False
  print("Carregando modelos do cache...")
  pipe.unet.load_state_dict(torch.load(UNET_PATH, map_location="cpu"))
  pipe.vae.load_state_dict(torch.load(VAE_PATH, map_location="cpu"))
  print("Cache carregado.")
  return True