print("Carregando bibliotecas")
import torch
if torch.cuda.is_available():
  from src.modules.popup import alert
  alert("Status de GPU indisponível ou incompatível.")
else:
  print(f"Versão 'cuda toolkit' {torch.version.cuda}\nListagem disponível {torch.cuda.get_arch_list()}")
  import os
  def loop():
    option = input("Deseja instalar os complementos para o funcionamento?\n- y [yes]\n- n [no]\n> ")
    if option == "y" or option == "n":
      if option == "y":
        if os.name == "nt":
          os.system("nvidia-gpu-5.0plus.bat")
        else:
          print("Sem compatibilidade ainda.")
    else:
      loop()
  loop()