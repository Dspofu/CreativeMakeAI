import config
import time
from tkinter import filedialog

# Função de carregar LoRA
def select_lora(lora_listbox, model_lora, lora_label, lora_scale):
  new_lora_path = filedialog.askopenfilename(
    title="Selecionar LoRA",
    filetypes=[("Modelos .safetensors", "*.safetensors")]
  )
  if not new_lora_path: return
  try:
    model_lora.configure(state="disabled", text="Registrando LoRA")
    filename = new_lora_path.split('/')[-1]
    config.loaded_loras[filename] = { "path": new_lora_path, "cfg": 0.75 }
    print(f"LoRA '{filename}' registrado.")
    lora_listbox.configure(values=list(config.loaded_loras.keys()))
    lora_listbox.set(filename)
    list_lora(filename, lora_label, lora_scale)
  except Exception as e:
    config.error("Falha ao tentar registrar o LoRA\nTalvez ele não seja compatível.")
    print(f"Falha ao registrar LoRA: {e}")
  finally:
    model_lora.configure(state="disabled", text=f"LoRA carregado com sucesso")
    time.sleep(1.5)
    model_lora.configure(state="normal", text="Adicionar LoRA")

# Função para deletar o LoRA
def unload_lora(lora_listbox, lora_label, lora_scale):
  selected_lora = lora_listbox.get()
  if selected_lora in config.loaded_loras:
    del config.loaded_loras[selected_lora]
    new_values = list(config.loaded_loras.keys())
    lora_listbox.configure(values=new_values)

    if new_values:
      lora_listbox.set(new_values[0])
      list_lora(new_values[0], lora_label, lora_scale)
    else:
      lora_listbox.set("")
      lora_label.configure(text="LoRA Scale: 0.75")
      lora_scale.set(0.75)
    print(f"LoRA '{selected_lora}' removido da memória.")
  else:
    print(f"LoRA '{selected_lora}' não está carregado.")

# Função para pegar CFG na listas de LoRA
def list_lora(lora_name, lora_label, lora_scale):
  if lora_name in config.loaded_loras:
    cfg_value = config.loaded_loras[lora_name]['cfg']
    lora_label.configure(text=f"LoRA Scale: {cfg_value}")
    lora_scale.set(cfg_value)