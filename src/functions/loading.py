import config
import time

active = False

# frame para agrupar barra + label
progress_frame = config.ctk.CTkFrame(config.window, fg_color="transparent")
progress_label = config.ctk.CTkLabel(progress_frame, text="Andamento: 0%")
progress_label.pack(side="left", padx=10, pady=0)

loading = config.ctk.CTkProgressBar(progress_frame, progress_color="#00BD00", mode="determinate")
loading.pack(side="left", padx=(0, 10), pady=0)

def progress(percent: int):
  global active

  if not active:
    active = True
    progress_frame.pack(pady=0)
    loading.set(0)
    progress_label.configure(text="Andamento: 0%")

  elif percent >= 100:
    loading.set(1)
    progress_label.configure(text="Andamento: 100%")
    time.sleep(0.8)
    progress_frame.pack_forget()
    active = False

  else:
    loading.set(percent/100)
    progress_label.configure(text=f"Andamento: {percent}%")