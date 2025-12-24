print("Configurações base iniciadas\nLendo funções basicas")
import torch
from config import*
import pynvml

print("Funcionalidade de rederização de imagem")
from src.modules.use_model import use_model
print("Funcionalidade de compatibilidade com Lora's")
from src.modules.lora import list_lora, select_lora, unload_lora
print("Funcionalidade de carregamento de modelo")
from src.modules.load_model import select_model
print("Inicializando sistema de Plugins")
from src.modules.plugin_loader import load_plugins
print("Iniciando interface e leitura da GPU")
from src.functions.popup import *
from painel_config import open_painel

qtdImg = 1

window.geometry(f"520x780+{int((window.winfo_screenwidth() / 2) - (520 / 2))}+{int((window.winfo_screenheight() / 2) - (780 / 2))}")
window.title(Window.winTitle)
window.resizable(False, False)
window.configure(fg_color=Colors.COR_FRAME)

# Carregamento dos plugins
def reload_plugins():
  plugins_folder = os.path.join(os.path.dirname(__file__), "plugins")
  plugins = load_plugins(plugins_folder)
  for plugin in plugins:
    try:
      plugin.creative_module(window, tab_view) 
    except Exception as e:
      print(f"Falha no plugin: {e}")

def active_temp_alert():
  data.limit_temp = not data.limit_temp

def active_benchmark_sequence():
  if not torch.cuda.is_available():
    alert("Não foi possivel validar a tecnologia, se atente aos Drivers atualizados\n(CUDA é necessário)")
  else:
    data.benchmark_sequence = not data.benchmark_sequence

def stop_generation():
  data.stop_img = True

def entry_event(event, entry, slider):
  try:
    val = float(entry.get())
    slider.set(val)
  except ValueError:
    pass

def slider_steps(value):
  steps_entry.delete(0, "end")
  steps_entry.insert(0, str(int(value)))

def slider_cfg(value):
  cfg_entry.delete(0, "end")
  cfg_entry.insert(0, f"{value:.1f}")

def update_qtd_display():
  qtd_entry.configure(state="normal")
  qtd_entry.delete(0, "end")
  qtd_entry.insert(0, str(qtdImg))
  qtd_entry.configure(state="readonly")

def plusImage():
  global qtdImg
  if qtdImg >= 50: return
  qtdImg += 1
  update_qtd_display()

def lessImage():
  global qtdImg
  if qtdImg == 1: return
  qtdImg -= 1
  update_qtd_display()

def update_lora_scale(v):
  selected_lora = lora_listbox.get()
  if selected_lora in data.loaded_loras:
    rounded_value = round(float(v), 2)
    data.loaded_loras[selected_lora]["cfg"] = rounded_value
    lora_label.configure(text=f"Peso: {rounded_value}")

try:
  pynvml.nvmlInit()
  handle = pynvml.nvmlDeviceGetHandleByIndex(0)
  gpu_name = pynvml.nvmlDeviceGetName(handle)
except:
  gpu_name = "GPU N/A"

status_bar = ctk.CTkFrame(window, height=30, fg_color="#14141f", corner_radius=0)
status_bar.pack(fill="x", side="top")
ctk.CTkLabel(status_bar, text=f"  {gpu_name}", font=("Roboto", 10, "bold"), text_color="#E2FF3F").pack(side="left")

# Alerta de temperatura
temp_container = ctk.CTkFrame(status_bar, fg_color="transparent")
temp_container.pack(side="right", padx=10)
temperature_label = ctk.CTkLabel(temp_container, text="--°C", font=("Roboto", 11), text_color="white")
temperature_label.pack(side="left", padx=(0, 5))
alert_check = ctk.CTkCheckBox(temp_container, text="Alert", command=active_temp_alert, font=("Roboto", 10), text_color="#AAAAAA", fg_color=Colors.COR_BOTAO, hover_color=Colors.COR_BOTAO_HOVER, width=16, height=16, corner_radius=4)
alert_check.pack(side="left")

if data.limit_temp:
  alert_check.select()
else:
  alert_check.deselect()

# Botão para recarregar plugins
reload_container = ctk.CTkFrame(window, fg_color="transparent")
reload_container.pack(fill="x", padx=15, pady=(8, 0))

reload_btn = ctk.CTkButton(reload_container, text="Reload Plugins", command=reload_plugins, font=("Roboto", 11, "bold"), width=10, height=25, fg_color=Colors.COR_BOTAO, hover_color=Colors.COR_BOTAO_HOVER, corner_radius=6)
reload_btn.pack(anchor="w")

# Prompt
prompts_container = ctk.CTkFrame(window, fg_color="transparent")
prompts_container.pack(fill="x", padx=15, pady=(10, 5))

ctk.CTkLabel(prompts_container, text="PROMPT", font=("Roboto", 11, "bold"), text_color="#AAAAAA").pack(anchor="w", padx=2)
prompt_entry = ctk.CTkTextbox(prompts_container, height=80, font=("Roboto", 13), fg_color=Colors.COR_INPUT, text_color=Colors.COR_TEXTO, corner_radius=6, border_width=0)
prompt_entry.pack(fill="x", pady=2)

# Prompt Negativo
ctk.CTkLabel(prompts_container, text="NEGATIVE PROMPT", font=("Roboto", 11, "bold"), text_color="#AAAAAA").pack(anchor="w", padx=2)
negative_prompt_entry = ctk.CTkTextbox(prompts_container, height=100, font=("Roboto", 13), fg_color=Colors.COR_INPUT, text_color="#DDDDDD", corner_radius=6, border_width=0)
negative_prompt_entry.insert("0.0", data.negative_prompt)
negative_prompt_entry.pack(fill="x", pady=2)

tab_view = ctk.CTkTabview(window, width=480, height=300, fg_color=Colors.COR_INPUT, segmented_button_fg_color=Colors.COR_FRAME, segmented_button_selected_color=Colors.COR_BOTAO)
tab_view.pack(fill="both", expand=True, padx=15, pady=5)
tab_view.add("Simples")
tab_view.add("Avançado")

# Geração - Simples
tab_gen = tab_view.tab("Simples")
container_gen_simples = ctk.CTkFrame(tab_gen, fg_color="transparent")
container_gen_simples.pack(fill="both", expand=True, padx=2, pady=2)

# Selecionar modelo
model_row = ctk.CTkFrame(container_gen_simples, fg_color="transparent")
model_row.pack(fill="x", pady=(5, 5))
model_button = ctk.CTkButton(model_row, text="Selecionar Modelo (.safetensors)", command=lambda: select_model(model_button, generate_button, lora_listbox, model_lora, data.loaded_loras), font=("Roboto", 12), fg_color=Colors.COR_BOTAO, hover_color=Colors.COR_BOTAO_HOVER, height=30, corner_radius=6)
model_button.pack(side="left", fill="x", expand=True, padx=(0, 2))

# Limpar Cache
bt_limpar = ctk.CTkButton(model_row, text="Limpar Cache", command=lambda: config.flush_memory(), width=70, height=30, font=("Roboto", 10, "bold"), fg_color="#D26F1A", hover_color="#AD5D17", corner_radius=6)
bt_limpar.pack(side="right", padx=(2, 0))

row_res_seed = ctk.CTkFrame(container_gen_simples, fg_color="transparent")
row_res_seed.pack(fill="x", pady=2)

# Resolução
col_res = ctk.CTkFrame(row_res_seed, fg_color="transparent")
col_res.pack(fill="x", padx=2)

ctk.CTkLabel(col_res, text="Resolução (WxH)", font=("Roboto", 11, "bold")).pack(anchor="w", pady=2)

res_inputs = ctk.CTkFrame(col_res, fg_color="transparent")
res_inputs.pack(fill="x")

width_entry = ctk.CTkEntry(res_inputs, font=("Roboto", 12), fg_color=Colors.COR_FRAME, border_width=0, corner_radius=4, justify="center")
width_entry.pack(side="left", fill="x", expand=True)
width_entry.insert(0, "1024")

ctk.CTkLabel(res_inputs, text="x", text_color="#555").pack(side="left", padx=2)

height_entry = ctk.CTkEntry(res_inputs, font=("Roboto", 12), fg_color=Colors.COR_FRAME, border_width=0, corner_radius=4, justify="center")
height_entry.pack(side="left", fill="x", expand=True)
height_entry.insert(0, "1024")

# Seed
col_seed = ctk.CTkFrame(row_res_seed, fg_color="transparent")
col_seed.pack(fill="x", padx=2, pady=(6, 0))

ctk.CTkLabel(col_seed, text="Seed", font=("Roboto", 11, "bold")).pack(anchor="w", pady=2)

seed_entry = ctk.CTkEntry(col_seed, font=("Roboto", 12), fg_color=Colors.COR_FRAME, border_width=0, corner_radius=4)
seed_entry.pack(fill="x")
seed_entry.insert(0, "-1")

# Geração - Avançada
tab_advance = tab_view.tab("Avançado")
container_gen_advanced = ctk.CTkFrame(tab_advance, fg_color="transparent")
container_gen_advanced.pack(fill="both", expand=True, padx=2, pady=2)

row_sliders = ctk.CTkFrame(container_gen_advanced, fg_color="transparent")
row_sliders.pack(fill="x", pady=2)

# STEPS
group_steps = ctk.CTkFrame(row_sliders, fg_color="transparent")
group_steps.pack(fill="x", padx=2)

lbl_steps = ctk.CTkFrame(group_steps, fg_color="transparent")
lbl_steps.pack(fill="x")

ctk.CTkLabel(lbl_steps, text="Steps", font=("Roboto", 11, "bold")).pack(side="left")

steps_entry = ctk.CTkEntry(lbl_steps, width=40, height=20, fg_color=Colors.COR_FRAME, border_width=0, justify="center", font=("Roboto", 14))
steps_entry.pack(side="right")
steps_entry.insert(0, "28")
steps = ctk.CTkSlider(group_steps, from_=1, to=100, height=16, command=slider_steps)
steps.pack(fill="x", pady=2)
steps.set(28)
steps_entry.bind("<KeyRelease>", lambda e: entry_event(e, steps_entry, steps))

# CFG SCALE
group_cfg = ctk.CTkFrame(row_sliders, fg_color="transparent")
group_cfg.pack(fill="x", padx=2, pady=(6, 0))

lbl_cfg = ctk.CTkFrame(group_cfg, fg_color="transparent")
lbl_cfg.pack(fill="x")

ctk.CTkLabel(lbl_cfg, text="CFG Scale", font=("Roboto", 11, "bold")).pack(side="left")

cfg_entry = ctk.CTkEntry(lbl_cfg, width=40, height=20, fg_color=Colors.COR_FRAME, border_width=0, justify="center", font=("Roboto", 14))
cfg_entry.pack(side="right")
cfg_entry.insert(0, "4.5")
cfg = ctk.CTkSlider(group_cfg, from_=0.5, to=30, height=16, command=slider_cfg)
cfg.pack(fill="x", pady=2)
cfg.set(4.5)
cfg_entry.bind("<KeyRelease>", lambda e: entry_event(e, cfg_entry, cfg))

# DEEP_CACHE
group_deepcache = ctk.CTkFrame(row_sliders, fg_color="transparent")
group_deepcache.pack(fill="x", padx=2, pady=(6, 0))

lbl_dc = ctk.CTkFrame(group_deepcache, fg_color="transparent")
lbl_dc.pack(fill="x")

ctk.CTkLabel(lbl_dc, text="DeepCache Interval (1 = Off)", font=("Roboto", 11, "bold")).pack(side="left")

dc_entry = ctk.CTkEntry(lbl_dc, width=40, height=20, fg_color=Colors.COR_FRAME, border_width=0, justify="center", font=("Roboto", 14))
dc_entry.pack(side="right")
dc_entry.insert(0, "1")

def slider_dc_event(value):
  v = int(value)
  dc_entry.delete(0, "end")
  dc_entry.insert(0, str(v))
  data.cache_interval = v

# Slider: De 1 a 10 (geralmente acima de 4 a perda de qualidade é alta)
dc_slider = ctk.CTkSlider(group_deepcache, from_=1, to=10, height=16, command=slider_dc_event)
dc_slider.pack(fill="x", pady=2)
dc_slider.set(1)
dc_entry.bind("<KeyRelease>", lambda e: entry_event(e, dc_entry, dc_slider))

# Lora
lora_group = ctk.CTkFrame(container_gen_advanced, fg_color="transparent")
lora_group.pack(fill="x", pady=(0, 6))

ctk.CTkLabel(lora_group, text="Gerenciador de LoRAs", font=("Roboto", 11, "bold")).pack(anchor="w", pady=(0, 2))
lora_card = ctk.CTkFrame(lora_group, fg_color=Colors.COR_FRAME, corner_radius=8)
lora_card.pack(fill="x", pady=2)

lora_top = ctk.CTkFrame(lora_card, fg_color="transparent")
lora_top.pack(fill="x", padx=5, pady=(5, 2))
lora_label = ctk.CTkLabel(lora_top, text="Peso: 0.75", font=("Roboto", 11), width=65, anchor="w")
lora_label.pack(side="left")
lora_scale = ctk.CTkSlider(lora_top, from_=0.1, to=1.0, height=16, command=lambda value: update_lora_scale(v=value))
lora_scale.set(0.75)
lora_scale.pack(side="left", fill="x", expand=True, padx=5)

lora_bot = ctk.CTkFrame(lora_card, fg_color="transparent")
lora_bot.pack(fill="x", padx=5, pady=(0, 5))
lora_listbox = ctk.CTkComboBox(lora_bot, values=[], height=24, font=("Roboto", 11), command=lambda lora_name: list_lora(lora_name, lora_label, lora_scale), state="readonly")
lora_listbox.pack(side="left", fill="x", expand=True, padx=(0, 5))

model_lora = ctk.CTkButton(lora_bot, text="+", state="disabled", width=30, height=24, font=("Roboto", 14), command=lambda: select_lora(lora_listbox, model_lora, lora_label, lora_scale), fg_color=Colors.COR_BOTAO, hover_color=Colors.COR_BOTAO_HOVER)
model_lora.pack(side="left", padx=(0, 5))

remove_lora_button = ctk.CTkButton(lora_bot, text="Remover", width=60, height=24, fg_color="#5e1b1b", hover_color="#802020", font=("Roboto", 14), command=lambda: unload_lora(lora_listbox, lora_label, lora_scale))
remove_lora_button.pack(side="right")

row_checks = ctk.CTkFrame(container_gen_advanced, fg_color="transparent")
row_checks.pack(fill="x", pady=(10, 2))
chk_sequenc = ctk.CTkCheckBox(row_checks, text="Mult-Imagens (Experimental)", command=active_benchmark_sequence, font=("Roboto", 11), text_color="#DDDDDD", fg_color=Colors.COR_BOTAO, hover_color=Colors.COR_BOTAO_HOVER, corner_radius=4, height=20)
chk_sequenc.pack(side="left")

if data.benchmark_sequence:
  chk_sequenc.select()
else:
  chk_sequenc.deselect()

# Botão de Gerar
footer_dock = ctk.CTkFrame(window, height=80, fg_color=Colors.COR_FRAME)
footer_dock.pack(side="bottom", fill="x")
footer_dock.pack_propagate(False)
action_area = ctk.CTkFrame(footer_dock, fg_color=Colors.COR_INPUT, corner_radius=15)
action_area.pack(fill="both", expand=True, padx=15, pady=15)

qtd_frame = ctk.CTkFrame(action_area, fg_color="transparent")
qtd_frame.pack(side="left", padx=5, pady=2)
qtd_entry = ctk.CTkEntry(qtd_frame, width=35, height=40, font=("Arial", 16, "bold"), justify="center", fg_color="transparent", border_width=0)
qtd_entry.pack(side="left")
qtd_entry.insert(0, "1")
qtd_entry.configure(state="readonly")
btns_qtd = ctk.CTkFrame(qtd_frame, fg_color="transparent")
btns_qtd.pack(side="left", padx=2)
btn_up = ctk.CTkButton(btns_qtd, text="▲", width=20, height=16, fg_color="#333", hover_color="#555", corner_radius=3, command=plusImage, font=("Arial", 6))
btn_up.pack(pady=(0, 1))
btn_down = ctk.CTkButton(btns_qtd, text="▼", width=20, height=16, fg_color="#333", hover_color="#555", corner_radius=3, command=lessImage, font=("Arial", 6))
btn_down.pack()

ctk.CTkButton(action_area, text="STOP", command=stop_generation, font=("Roboto", 12, "bold"), fg_color="#802020", hover_color="#501010", height=35, width=60, corner_radius=8).pack(side="left", padx=(2, 5))
generate_button = ctk.CTkButton(action_area, text="GERAR IMAGEM", command=lambda: use_model(generate_button, temperature_label, f"{width_entry.get()}x{height_entry.get()}", prompt_entry, negative_prompt_entry, steps, cfg, seed_entry, lora_listbox, qtdImg=qtdImg), state="disabled", font=("Roboto", 15, "bold"), fg_color=Colors.COR_BOTAO, hover_color=Colors.COR_BOTAO_HOVER, height=40, corner_radius=8)
generate_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

window.withdraw()
open_painel(window)
window.update()
window.deiconify()
window.mainloop()