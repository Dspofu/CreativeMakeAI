import pynvml
import popup
import time

critical_temp = False

def reset_alert():
  global critical_temp
  critical_temp = False

def safe_temp(pipe, gpu: int = 0): # Consigo fazer duas GPU's trabalharem se eu ficar alternando, mas a vram é um problema para compartilhar o modelo
  temp = pynvml.nvmlDeviceGetTemperature(handle=pynvml.nvmlDeviceGetHandleByIndex(gpu), sensor=pynvml.NVML_TEMPERATURE_GPU)
  if temp >= 90:
    pipe.enable_sequential_cpu_offload()
    popup.alert(f"Acerto crítico, GPU marcou '{temp}°C', a recomendação é não realizar mais o uso da placa para estes fins ou ser feita um limpeza e troca dos condutores térmicos para a carcaça.")
    time.sleep(18)
  elif temp >= 85:
    pipe.enable_sequential_cpu_offload()
    time.sleep(15)
  elif temp >= 75:
    pipe.enable_model_cpu_offload()
    time.sleep(12)
  elif temp >= 70:
    pipe.enable_model_cpu_offload()
    if critical_temp == False:
      popup.alert(f"Sua GPU atingiu o limite para iniciar o processo de resfiamento.\nAtualmente com '{temp}°C', deste modo, o processo sofrera pausas continuas até a redução de temperatura ser feita.")
      critical_temp = True
    time.sleep(8)
  else:
    pipe.enable_model_cpu_offload()