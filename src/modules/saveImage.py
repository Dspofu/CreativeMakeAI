from tkinter import Image, filedialog

# Função de salvar imagem
def save_image(image: Image):
  file_path = filedialog.asksaveasfilename(
    defaultextension=".png",
    filetypes=[("PNG Files", "*.png"), ("JPEG Files", "*.jpg"), ("Todos os arquivos", "*.*")],
    title="Salvar imagem gerada"
  )
  if file_path:
    image.save(file_path)
    print(f"Imagem salva em: {file_path}")