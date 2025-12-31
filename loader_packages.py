def load_torch():
  print("Recurso de leitura do modelo")
  import torch
  return torch

def load_model_selector():
  print("Funcionalidade de carregamento de modelo")
  from src.modules.load_model import select_model
  return select_model

def load_image_renderer():
  print("Funcionalidade de rederização de imagem")
  from src.modules.initialization_model import initialization_model
  return initialization_model

def load_lora_system():
  print("Funcionalidade de compatibilidade com Lora's")
  from src.modules.lora import list_lora, select_lora, unload_lora
  return list_lora, select_lora, unload_lora

def load_plugins_system():
  print("Inicializando sistema de Plugins")
  from src.modules.plugin_loader import load_plugins
  return load_plugins

def load_gpu_monitor():
  print("Iniciando interface e leitura da GPU")
  import pynvml
  return pynvml