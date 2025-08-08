print("Carregando bibliotecas")
import torch
if not torch.cuda.is_available():
  from src.modules.popup import alert
  alert("Status de GPU indisponível ou incompatível.\nVerifique os drivers.")
else:
  print(f"Versão 'cuda toolkit' {torch.version.cuda}\nListagem disponível {torch.cuda.get_arch_list()}")