from src.config import*
from tkinter import messagebox

def error(mensagem: str):
  root = tk.Tk()
  root.withdraw()
  messagebox.showerror("Erro", mensagem)
  root.destroy()

def alert(mensagem: str):
  root = tk.Tk()
  root.withdraw()
  messagebox.showwarning("Alerta", mensagem)
  root.destroy()