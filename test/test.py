import threading
import time
import customtkinter as ctk

def carregar_app(status):
    splash.after(0, lambda: status.configure(text="Carregando dados..."))
    time.sleep(3)

    splash.after(0, lambda: status.configure(text="Pronto!"))
    time.sleep(1)

    splash.after(0, abrir_janela_principal)
    splash.after(0, splash.destroy)

def abrir_janela_principal():
    app = ctk.CTkToplevel(splash)
    app.title("App Principal")
    app.geometry("800x600")
    app.mainloop()

splash = ctk.CTk()
splash.title("Loading...")
splash.geometry("300x150")
splash.overrideredirect(True)

frame = ctk.CTkFrame(splash)
frame.pack(fill="both", expand=True)

lbl_title = ctk.CTkLabel(frame, text="teste")
lbl_title.pack(pady=(30, 10))

lbl_status = ctk.CTkLabel(frame, text="Iniciando")
lbl_status.pack(pady=5)

progress = ctk.CTkProgressBar(frame, mode="indeterminate")
progress.pack(pady=10)
progress.start()

threading.Thread(
    target=carregar_app,
    args=(lbl_status,),
    daemon=True
).start()

splash.mainloop()