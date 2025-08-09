print("Carregando bibliotecas")
import torch
if not torch.cuda.is_available():
  from src.modules.popup import alert
  alert("Status de GPU indisponível ou incompatível.\nVerifique os drivers.")
else:
  for i in range(torch.cuda.device_count()):
    print(i, torch.cuda.get_device_name(i))
  print(f"Versão 'cuda toolkit' {torch.version.cuda}\nListagem disponível {torch.cuda.get_arch_list()}")