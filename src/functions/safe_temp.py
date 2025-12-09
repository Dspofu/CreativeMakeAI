import pynvml
from src.functions.popup import alert
import time

critical_temp = False

def reset_alert():
  global critical_temp; critical_temp = False

def safe_temp(pipe, temp_label, gpu: int = 0):
  global critical_temp
  try:
    pynvml.nvmlInit()
    handle = pynvml.nvmlDeviceGetHandleByIndex(gpu)
    temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)

    temp_label.configure(text=f"{temp}°C", text_color="#78F801")
    if temp >= 90:
      # pipe.enable_sequential_cpu_offload()
      alert(f"Acerto crítico, GPU marcou '{temp}°C', a recomendação é não realizar mais o uso da placa para estes fins ou ser feita um limpeza e troca dos condutores térmicos para a carcaça.")
      temp_label.configure(text_color="#F80101")
      time.sleep(1)
    elif temp >= 85:
      # pipe.enable_sequential_cpu_offload()
      temp_label.configure(text_color="#F84301")
      time.sleep(0.7)
    elif temp >= 75:
      # pipe.enable_model_cpu_offload()
      temp_label.configure(text_color="#F85C01")
      time.sleep(0.5)
    elif temp >= 70:
      # pipe.enable_model_cpu_offload()
      temp_label.configure(text_color="#F8D301")
      if not critical_temp:
        alert(f"Sua GPU atingiu o limite para iniciar o processo de resfiamento.\nAtualmente com '{temp}°C', deste modo, o processo sofrera pausas continuas até a redução de temperatura ser feita.")
        critical_temp = True
      time.sleep(0.2)
    elif temp >= 60:
      temp_label.configure(text_color="#95F801")
    # else:
      # pipe.enable_model_cpu_offload()
  except pynvml.NVMLError as error:
    temp_label.configure(text_color="#D9D9D9")
    print(f"Erro NVML: {error}")
  finally:
    pynvml.nvmlShutdown()