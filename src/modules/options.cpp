#include "options.h"

bool loopQuest(char& quest) {
  system("cls");
  std::cout << "Verifique se este dispositivo possui o Python na versão 3.12.0 ou superior.\n\nVersão encontrada: ";
  system("python --version");
  std::cout << "\nConfirme se ele foi encontrado:\n[0] - Fechar\n[1] - Sim possuo\n[2] - Instalar Python\n\n> ";
  std::cin >> quest;
  if (quest != '0' && quest != '1' && quest != '2') return loopQuest(quest);
  else return true;
}

void loopOption(D3DADAPTER_IDENTIFIER9 adapterIdentifier, int memory) {
  system("cls");
  std::wstringstream ss;
  ss << L"Memória RAM: " << memory << L"GB o ideal seria ter 32GB de RAM";
  if (memory < 18) MessageBoxW(NULL, ss.str().c_str(), L"Pouca RAM no sistema", MB_ICONWARNING);
  std::cout << "Memória RAM: " << memory << "GB" << std::endl;
  wprintf(L"GPU: %s\n\nAgora escolha entre instalar os pacotes ou iniciar:\n[0] - Fechar\n[1] - Iniciar programa\n[2] - Instalar pacotes\n[3] - *Baixar projeto*\n\n> ", adapterIdentifier.Description);
}

void option2() {
  system("python -m venv venv");
  system(".\\venv\\Scripts\\python.exe -m pip install --upgrade pip");
  system(".\\venv\\Scripts\\python.exe -m pip install -r requirements.txt");
  system(".\\venv\\Scripts\\python.exe -m pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu128");
  system(".\\venv\\Scripts\\python.exe -m pip list");
  printf("\nInicialize o venv para testar.\n");
}