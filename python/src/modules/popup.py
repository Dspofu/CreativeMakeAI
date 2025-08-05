from src.config import*
from tkinter import messagebox

def alert(mensagem: str):
  root = tk.Tk()
  root.withdraw()
  messagebox.showerror("Erro", mensagem)
  root.destroy()