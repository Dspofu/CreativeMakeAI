import torch

def detect_dtype():
  # NVIDIA or AMD(ROCm)
  if torch.cuda.is_available():
    cuda = torch.cuda.get_device_properties(0)
    major, minor = cuda.major, cuda.minor
    if major >= 8 and torch.cuda.is_bf16_supported():
      return torch.bfloat16
    else:
      return torch.float16

  # AMD
  if torch.version.hip is not None:
    return torch.float16

  # 3. Intel Arc
  if torch.xpu.is_available():
    if torch.xpu.is_bf16_supported():
      return torch.bfloat16
    return torch.float16

  # 4. Apple Silicon (M1/M2/M3/M4)
  if torch.mps.is_available():
    return torch.bfloat16

  return torch.float32