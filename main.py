from config import*
from src.functions.viwer import viwerImage
from src.functions.lora import list_lora, select_lora, unload_lora
from src.functions.model import select_model
from src.modules.popup import*

# Função para ativar ou desativar o limitador por temperatura
def active_temp_alert():
  global limit_temp
  limit_temp = not limit_temp

# Selecionar modelo
model_button = ctk.CTkButton(window, text="Selecionar modelo", command=lambda: select_model(model_button, generate_button, lora_listbox, model_lora, loaded_loras, lora_label, lora_scale), font=("Arial", 12))
model_button.place(x=10, y=10)

# Temperatura
temperature_label = ctk.CTkLabel(window, text="--°C", font=("Arial", 12), bg_color=COR_FRAME, text_color="white")
temperature_label.place(relx=1.0, rely=0.0, y=8, x=-45, anchor="ne")

# Alerta de temperatura
ctk.CTkLabel(window, text="Alerta de temperatura:", font=("Arial", 14)).pack(anchor="ne", padx=80, pady=8)

# Checkbox de temperatura
checkBox = ctk.CTkCheckBox(window, text="", command=active_temp_alert, fg_color=COR_BOTAO, hover_color=COR_BOTAO_HOVER, checkbox_width=20, checkbox_height=20, corner_radius=5, bg_color=COR_FRAME)
checkBox.select(limit_temp)
checkBox.place(relx=1.12, rely=0.0, y=10, x=0, anchor="ne")

# Container inputs
main_frame = ctk.CTkFrame(window, fg_color=COR_FRAME)
main_frame.place(relx=0.5, rely=0.54, anchor="center")

# Prompt
ctk.CTkLabel(main_frame, text="Prompt:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=0)
prompt_entry = ctk.CTkTextbox(main_frame, width=400, height=80, font=("Arial", 14), fg_color=COR_INPUT, text_color=COR_TEXTO, border_width=0, corner_radius=8)
prompt_entry.pack(padx=0, pady=(0, 20), fill="both", expand=True)

# Prompt Negativo
ctk.CTkLabel(main_frame, text="Prompt Negativo:", font=("Arial", 14)).pack(anchor="w", padx=0, pady=(0, 5))
negative_prompt_entry = ctk.CTkTextbox(main_frame, height=100, font=("Arial", 14), fg_color=COR_INPUT, text_color=COR_TEXTO, border_width=0, corner_radius=8)
negative_prompt_entry.insert("0.0", negative_prompt)
negative_prompt_entry.pack(padx=0, pady=(0, 20), fill="both", expand=True)

# Steps
steps_label = ctk.CTkLabel(main_frame, text="Steps: 28", font=("Arial", 14))
steps_label.pack(anchor="w", padx=0, pady=(0, 5))
steps = ctk.CTkSlider(master=main_frame, from_=1, to=100, command=lambda value: steps_label.configure(text=f"Steps: {int(value)}"))
steps.set(28)
steps.pack(anchor="w", padx=0, pady=(0, 20), fill="both")

# CFG Scale
cfg_label = ctk.CTkLabel(main_frame, text="CFG Scale: 4.5", font=("Arial", 14))
cfg_label.pack(anchor="w", padx=0, pady=(0, 5))
cfg = ctk.CTkSlider(master=main_frame, from_=0.5, to=30, command=lambda value: cfg_label.configure(text=f"CFG Scale: {round(value, 1)}"))
cfg.set(4.5)
cfg.pack(anchor="w", padx=0, pady=(0, 20), fill="both")

# Container do Seed e Escala
container_seed_scale = ctk.CTkFrame(main_frame, fg_color="transparent")
container_seed_scale.pack(anchor="w", padx=0, pady=(0, 20))

# Seed
ctk.CTkLabel(container_seed_scale, text="Seed:", font=("Arial", 14)).pack(side="left", padx=(0,10))
seed_entry = ctk.CTkEntry(container_seed_scale, width=150, font=("Arial", 14), fg_color=COR_INPUT, text_color=COR_TEXTO, border_width=0, corner_radius=8)
seed_entry.pack(side="left")
seed_entry.insert(0, "-1")

# Resoluções
ctk.CTkLabel(container_seed_scale, text="Escala da imagem:", font=("Arial", 14)).pack(side="left", padx=(45, 5))
scale_listbox = ctk.CTkComboBox(container_seed_scale, values=["512x512", "1024x1024", "1920x1080", "2048x2048"], width=100, command=lambda lora_name: list_lora(lora_name, lora_label, lora_scale), state="readonly")
scale_listbox.set("1024x1024")
scale_listbox.pack(side="left", pady=0, fill="both")

# Container LoRA's
container_lora = ctk.CTkFrame(main_frame, fg_color=COR_FRAME)
container_lora.pack(anchor="w", padx=0, pady=(0, 20))

# Frame para botão de adicionar LoRA
lora_control_frame = ctk.CTkFrame(container_lora, fg_color="transparent")
lora_control_frame.pack(anchor="w", pady=(0, 20), fill="x")

# Botão para adicionar LoRA
model_lora = ctk.CTkButton(lora_control_frame, text="Adicionar LoRA", state="disabled", command=lambda: select_lora(lora_listbox, model_lora, lora_label, lora_scale), font=("Arial", 12))
model_lora.pack(side="left", padx=(0, 10))

# Label de CFG do LoRA
lora_label = ctk.CTkLabel(lora_control_frame, text="LoRA Scale: 0.75", font=("Arial", 14))
lora_label.pack(side="left", padx=(0, 10))

# Input de CFG para o LoRA
def update_lora_scale(v):
  selected_lora = lora_listbox.get()
  if selected_lora in loaded_loras:
    rounded_value = round(float(v), 2)
    loaded_loras[selected_lora]["cfg"] = rounded_value
    lora_label.configure(text=f"LoRA Scale: {rounded_value}")

lora_scale = ctk.CTkSlider(lora_control_frame, from_=0.1, to=1.0, command=lambda value: update_lora_scale(v=value))
lora_scale.set(0.75)
lora_scale.pack(side="left")

# Frame para lista de LoRAs
lora_list_frame = ctk.CTkFrame(container_lora, fg_color="transparent")
lora_list_frame.pack(anchor="w", fill="x")

# Lista de modelos LoRA carregados
lora_listbox = ctk.CTkComboBox(lora_list_frame, values=[], width=300, command=lambda lora_name: list_lora(lora_name, lora_label, lora_scale), state="readonly")
lora_listbox.pack(side="left", padx=(0, 10), pady=(0, 10))

# Botão para remover LoRA
remove_lora_button = ctk.CTkButton(lora_list_frame, text="Remover", command=lambda: unload_lora(lora_listbox, lora_label, lora_scale))
remove_lora_button.pack(side="left", pady=(0, 10), fill="both")

# Botão Gerar Imagem
generate_button = ctk.CTkButton(main_frame, text="Gerar Imagem", command=lambda: viwerImage(generate_button, temperature_label, prompt_entry, negative_prompt_entry, steps, cfg, seed_entry, lora_listbox), state="disabled", font=("Arial", 14, "bold"), fg_color=COR_BOTAO_IMAGE, hover_color=COR_BOTAO_IMAGE_HOVER, height=40, corner_radius=8)
generate_button.pack(padx=20, pady=20, fill="x")

window.mainloop()