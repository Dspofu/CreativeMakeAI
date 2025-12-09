import os
import importlib.util
import sys

def load_plugins(pasta_plugins):
  plugins = []
  if not os.path.exists(pasta_plugins):
    os.makedirs(pasta_plugins)

  print(f"Buscando plugins em: {pasta_plugins}")
  for files in os.listdir(pasta_plugins):
    if files.endswith(".py"):
      folder = os.path.join(pasta_plugins, files)
      name = files[:-3] # Remove o .py

      try:
        spec = importlib.util.spec_from_file_location(name, folder)
        modulo = importlib.util.module_from_spec(spec)
        sys.modules[name] = modulo
        spec.loader.exec_module(modulo)

        # Verifica função de entrada 'creative_module'
        if hasattr(modulo, "creative_module"):
          # modulo.creative_module() 
          plugins.append(modulo)
          print(f"[OK] Plugin \"{name}\" carregado!")
        else:
          print(f"[!] Ignorado \"{name}\": função \"creative_module\" não encontrada.")
      except Exception as e:
        print(f"[ERRO] Falha ao carregar \"{name}\": {e}")

  return plugins