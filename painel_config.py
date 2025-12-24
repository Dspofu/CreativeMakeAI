from config import *
import torch

# Explicações de perfil
PERFIL_INFO = {
  "High Performance":
    "[MODO]\n  • Execução direta na GPU em FP16, sem mecanismos de economia de memória. Operações são executadas em blocos completos, com slicing e tiling desativados. Ativa otimizações internas do Torch Inductor para aumentar throughput.\n\n"
    "[VANTAGENS]\n  • Máximo desempenho e latência mínima.\n\n"
    "[DESVANTAGENS]\n  • Consumo elevado de VRAM, podendo causar OOM em GPUs menores.",

  "Balanced":
    "[MODO]\n  • Execução em FP16 na GPU com parâmetros seguros, sem otimizações agressivas. Mantém estabilidade e consumo moderado, adequado para placas intermediárias.\n\n"
    "[VANTAGENS]\n  • Boa performance com risco reduzido de falta de memória.\n\n"
    "[DESVANTAGENS]\n  • Não usa fusões avançadas nem kernels otimizados, resultando em menor velocidade máxima.",

  "Low Memory":
    "[MODO]\n  • CPU Offload automático, movendo partes do modelo para RAM e carregando módulos sob demanda. Reduz drasticamente o uso de VRAM, com custo de latência maior.\n\n"
    "[VANTAGENS]\n  • Permite rodar SDXL até em GPUs com 4–6 GB.\n\n"
    "[DESVANTAGENS]\n  • Transferência constante entre CPU e GPU aumenta bastante o tempo de geração."
}

list_perfil = list(PERFIL_INFO.keys())

def open_painel(parent):
  windowConfig = ctk.CTkToplevel(parent)
  width = 600
  height = 460 
  screen_width = windowConfig.winfo_screenwidth()
  screen_height = windowConfig.winfo_screenheight()
  x = int((screen_width / 2) - (width / 2))
  y = int((screen_height / 2) - (height / 2))
  
  windowConfig.geometry(f"{width}x{height}+{x}+{y}")
  windowConfig.title(f"{Window.winTitle} - Configuração de Perfil")
  windowConfig.resizable(False, False)
  windowConfig.configure(fg_color=Colors.COR_FRAME)
  
  # Foca a janela
  windowConfig.grab_set()
  windowConfig.focus_force()

  def select_ok():
    data.profile = profile_list.get()
    print(f"Perfil de execução definido: {data.profile}")
    windowConfig.destroy()

  def close_cancel():
    windowConfig.destroy()

  def update_description(choice):
    info_label.configure(text=PERFIL_INFO.get(choice, "Selecione um perfil de memória."))

  lbl_title = ctk.CTkLabel(windowConfig, text="Perfil de Performance", font=("Segoe UI", 18, "bold"), text_color="white")
  lbl_title.pack(pady=(20, 10))

  # Frame Central
  center_frame = ctk.CTkFrame(windowConfig, fg_color="transparent")
  center_frame.pack(fill="both", expand=True, padx=20)

  # Combobox de Seleção
  profile_list = ctk.CTkOptionMenu(center_frame, values=list_perfil, width=300, font=("Segoe UI", 13), command=update_description, state="readonly")
  profile_list.set(data.profile)
  profile_list.pack(pady=(5, 15))

  # Frame de Informação (Estilo Painel)
  info_frame = ctk.CTkFrame(center_frame, fg_color=Colors.COR_INPUT, corner_radius=8, border_width=1, border_color="#333333")
  info_frame.pack_propagate(False)
  info_frame.pack(fill="both", expand=True, pady=5)

  # Label de Descrição
  info_label = ctk.CTkLabel(info_frame, text=PERFIL_INFO.get(data.profile, PERFIL_INFO[data.profile]), font=("Segoe UI", 14), text_color="#DDDDDD", justify="left", wraplength=520, anchor="nw")
  info_label.pack(padx=20, pady=20, fill="both", expand=True)

  try:
    if torch.cuda.is_available():
      vram_bytes = torch.cuda.get_device_properties(0).total_memory
      vram_total = vram_bytes / 1024**2
      gpu_name = torch.cuda.get_device_name(0)

      recommendation = "Low Memory"
      if vram_total >= 18000:
        recommendation = "High Performance"
      elif vram_total >= 12000:
        recommendation = "Balanced"

      if not data.profile:
        data.profile = recommendation
        profile_list.set(recommendation)
        update_description(recommendation)

      hardware_text = f"GPU: {gpu_name} ({vram_total:.1f}MB VRAM)"
      rec_text = f"Recomendado: {recommendation}"
      color_hw = "#44FF44"
    else:
      hardware_text = "⚠️ Nenhuma placa Nvidia detectada."
      rec_text = "Modo de Segurança ativado (Low Memory)"
      color_hw = "#FF4444"
      data.profile = "Low Memory"
  except Exception as e:
    hardware_text = "Não foi possível ler as especificações do PC."
    rec_text = "Recomendação: Balanced"
    color_hw = "gray"

  # Footer
  footer_frame = ctk.CTkFrame(windowConfig, fg_color="transparent")
  footer_frame.pack(side="bottom", fill="x", padx=20, pady=10)

  # Infos de Hardware
  lbl_hw = ctk.CTkLabel(footer_frame, text=hardware_text, font=("Segoe UI", 11, "bold"), text_color=color_hw, anchor="w")
  lbl_hw.pack(fill="x")
  
  lbl_rec = ctk.CTkLabel(footer_frame, text=rec_text, font=("Segoe UI", 11), text_color="gray", anchor="w")
  lbl_rec.pack(fill="x", pady=(0, 10))

  confirm_btn = ctk.CTkButton(footer_frame, text="Aplicar", command=select_ok, font=("Segoe UI", 16, "bold"), height=30, fg_color=Colors.COR_BOTAO, hover_color=Colors.COR_BOTAO_HOVER, corner_radius=5)
  confirm_btn.pack(side="right", padx=(0, 5))

  windowConfig.wait_window()