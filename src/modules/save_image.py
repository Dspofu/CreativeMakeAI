from tkinter import filedialog
from PIL.PngImagePlugin import PngInfo

def save_image(image, metadata: dict = None):
  file_path = filedialog.asksaveasfilename(
    defaultextension=".png",
    filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("Todos os arquivos", "*.*")],
    title="Salvar imagem gerada"
  )
  if not file_path: return

  if metadata and file_path.lower().endswith(".png"):
    png_info = PngInfo()

    # SD_Prompt Leitura de metadados
    compatible = (
      f"Prompt: {metadata.get('Prompt', '')}\n"
      f"Negative prompt: {metadata.get('Negative Prompt', '')}\n"
      f"Steps: {metadata.get('Steps', '')}, "
      f"Sampler: {metadata.get('Sampler:', '')}, "
      f"CFG scale: {metadata.get('CFG Scale', '')}, "
      f"Seed: {metadata.get('Seed', '')}, "
      f"Size: {metadata.get('Size', '')}, "
      f"Model hash: {metadata.get('Model hash', '')}, "
      f"Model: {metadata.get('Model', '')}, "
      f"Lora: {metadata.get('Lora', '')}, "
      f"Lora Scale: {metadata.get('Lora Scale', '')}, "
      "Generator: CreativeMakeAI"
    )

    png_info.add_text("parameters", compatible)
    png_info.add_text("Software", "CreativeMakeAI")
    image.save(file_path, pnginfo=png_info)
  else:
    image.save(file_path)

  print(f"Imagem salva em: {file_path}")