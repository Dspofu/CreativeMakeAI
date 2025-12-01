import gc
import torch

def flush_memory():
  print("Liberando memória RAM e VRAM\n")
  gc.collect()
  if torch.cuda.is_available():
    torch.cuda.empty_cache()
    torch.cuda.ipc_collect()