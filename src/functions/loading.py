import config
import time

active = False
progress_frame = None
progress_label = None
loading = None


def init_progress():
    global progress_frame, progress_label, loading

    progress_frame = config.ctk.CTkFrame(config.window, fg_color="transparent")

    progress_label = config.ctk.CTkLabel(
        progress_frame, text="Andamento: 0%"
    )
    progress_label.pack(side="left", padx=10)

    loading = config.ctk.CTkProgressBar(
        progress_frame, progress_color="#00BD00", mode="determinate"
    )
    loading.pack(side="left", padx=(0, 10))


def progress(percent: int):
    def _update():
        global active

        if not active:
            active = True
            progress_frame.pack(pady=0)
            loading.set(0)
            progress_label.configure(text="Andamento: 0%")

        elif percent >= 100:
            loading.set(1)
            progress_label.configure(text="Andamento: 100%")

            def _hide():
                progress_frame.pack_forget()
                global active
                active = False

            config.window.after(800, _hide)

        else:
            loading.set(percent / 100)
            progress_label.configure(text=f"Andamento: {percent}%")

    config.window.after(0, _update)
