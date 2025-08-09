import pynvml
import time
from src.modules.popup import alert

critical_temp = False

def reset_alert():
  global critical_temp
  critical_temp = False

def safe_temp(pipe, gpu: int = 0):
  global critical_temp
  try:
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu)
    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

    if temp >= 90:
      pipe.enable_sequential_cpu_offload()
      alert(f"Acerto crítico, GPU marcou '{temp}°C', a recomendação é não realizar mais o uso da placa para estes fins ou ser feita um limpeza e troca dos condutores térmicos para a carcaça.")
      time.sleep(3)
    elif temp >= 85:
      pipe.enable_sequential_cpu_offload()
      time.sleep(2)
    elif temp >= 75:
      pipe.enable_model_cpu_offload()
      time.sleep(1)
    elif temp >= 70:
      pipe.enable_model_cpu_offload()
      if not critical_temp:
        alert(f"Sua GPU atingiu o limite para iniciar o processo de resfiamento.\nAtualmente com '{temp}°C', deste modo, o processo sofrera pausas continuas até a redução de temperatura ser feita.")
        critical_temp = True
      time.sleep(0.5)
    else:
      pipe.enable_model_cpu_offload()
  except pynvml.NVMLError as error:
    print(f"Erro NVML: {error}")
  finally:
    pynvml.nvmlShutdown()