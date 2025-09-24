import os
from cx_Freeze import setup, Executable

def find_package(package_name):
  """
  Encontra o caminho de um pacote instalado.
  """
  try:
    # Importa o pacote para acessar suas propriedades
    package = __import__(package_name)
    return os.path.dirname(package.__file__)
  except (ImportError, AttributeError):
    print(f"Alerta, não foi possível encontrar a pasta da biblioteca '{package_name}', a compilação pode falhar.")
    return None

# Encontra caminhos das bibliotecas inteiras
transformers_path = find_package("transformers")
diffusers_path = find_package("diffusers")
include_files_list = ["assets/"]

if transformers_path:
  include_files_list.append((transformers_path, os.path.join("lib", "transformers")))
if diffusers_path:
  include_files_list.append((diffusers_path, os.path.join("lib", "diffusers")))

# Lista de dependências
packages = ["diffusers", "transformers", "accelerate", "safetensors", "peft", "PIL", "customtkinter", "pynvml", "torch", "os", "sys", "diffusers.pipelines", "transformers.models"]

# Opções de build
build_options = {
  "packages": packages,
  "includes": ["diffusers.pipelines.stable_diffusion_xl"],
  "include_files": include_files_list,
  "optimize": 2,
  # "excludes": ["tkinter"],
  "build_exe": "build/dist",
}

# Configuração do executável
executables = [
  Executable(
    script="main.py",
    base="Win32GUI",  # "Win32GUI" or None
    target_name="CreativeMakeAI.exe",
    icon="assets/images/icon_96px.ico"
  )
]

# Função principal
setup(
  name="CreativeMakeAI",
  version="0.1.0",
  description="CreativeMakeAI Beta",
  author="Gabriel P. Góes",
  url="https://github.com/Dspofu/CreativeMakeAI",
  license="MIT",
  long_description="CreativeMakeAI é uma ferramenta de geração de imagens por IA para diversão e aprendizado, deixo desejar o reconhecimento de meu projeto caso fosse inspirado a algo.",
  executables=executables,
  options={
    "build_exe": build_options,
    "bdist_msi": {
      "upgrade_code": "{9a9046de-651a-41ff-9411-4ab34f2b9800}",
      "add_to_path": False,
      "initial_target_dir": r"[ProgramFilesFolder]\CreativeMakeAI",
      "summary_data": {
        "author": "Gabriel P. Góes",
        "comments": "©2025 Gabriel P. Góes. Todos os direitos reservados.",
        "description": "Beta - Ferramenta avançada para geração de imagens criativa com IA",
        "keywords": "IA, Diffusion, Creative, Generator",
        "title": "CreativeMakeAI Beta",
      },
    }
  }
)