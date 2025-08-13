#ifdef _WIN32
#include <windows.h>
#include <iostream>
#include <sstream>
#include <cmath>
#include <d3d9.h>

#pragma comment(lib, "d3d9.lib")

bool loopOption(char& option, D3DADAPTER_IDENTIFIER9 adapterIdentifier, int memory) {
  system("cls");
  std::wstringstream ss;
  ss << L"Memória RAM: " << memory << L"GB o ideal seria ter 32GB de RAM";
  if (memory < 18) MessageBoxW(NULL, ss.str().c_str(), L"Pouca RAM no sistema", MB_ICONWARNING);
  else std::cout << "Memória RAM: " << memory << "GB" << std::endl;
  std::wcout << L"GPU: " << adapterIdentifier.Description << L"\n\nAgora escolha entre instalar os pacotes ou iniciar:\n[0] - Fechar\n[1] - Iniciar programa\n[2] - Instalar pacotes\n\n> ";
  std::cin >> option;
  if (option != '0' && option != '1' && option != '2') return loopOption(option, adapterIdentifier, memory);
  else return true;
}

bool loopQuest(char& quest) { // Tem que colocar uma opção de instalar e configurar tudo "https://github.com/Dspofu/CreativeMakeAI/archive/refs/heads/main.zip"
  system("cls");
  std::cout << "Verifique se este dispositivo possui o Python na versão 3.12.0 ou superior.\n\nVersão encontrada: ";
  system("python --version");
  std::cout << "\nConfirme se ele foi encontrado:\n[0] - Fechar\n[1] - Sim possuo\n[2] - Instalar Python\n\n> ";
  std::cin >> quest;
  if (quest != '0' && quest != '1' && quest != '2') return loopQuest(quest);
  else return true;
}

int main() {
  SetConsoleOutputCP(CP_UTF8);
  SetConsoleCP(CP_UTF8);

  MEMORYSTATUSEX memInfo;
  memInfo.dwLength = sizeof(memInfo);

  IDirect3D9 *d3d = Direct3DCreate9(D3D_SDK_VERSION);
  if (d3d) {
    D3DADAPTER_IDENTIFIER9 adapterIdentifier;
    if (SUCCEEDED(d3d->GetAdapterIdentifier(D3DADAPTER_DEFAULT, 0, &adapterIdentifier))) {
      if (adapterIdentifier.VendorId == 0x10DE) {
        if (GlobalMemoryStatusEx(&memInfo)) {
          int memory = std::round(memInfo.ullTotalPhys / (1024.0f * 1024.0f * 1024.0f));
          if (memory <= 8) {
            MessageBoxW(NULL, L"Nível de RAM muito baixo.\nPor motivo de segurança não será continuado o processo.", L"Pouca RAM no sistema", MB_ICONERROR);
            std::cout << "O recomendado seria ter 32GB de RAM e foram identificados somente: " << memory << "GB de RAM" << std::endl;
          }
          char quest;
          if (loopQuest(quest)) {
            if (quest == '1' || quest == '2') {
              if (quest == '2') system("winget install --id Python.Python.3.13 --version 3.13.6");
              char option;
              if (loopOption(option, adapterIdentifier, memory)) {
                if (option == '1') {
                  std::cout << "\nINICIANDO\n" << std::endl;
                  system(".\\venv\\Scripts\\python.exe -m main");
                  main();
                } else if (option == '2') {
                  system("python -m venv venv");
                  system(".\\venv\\Scripts\\python.exe -m pip install --upgrade pip");
                  system(".\\venv\\Scripts\\python.exe -m pip install --pre torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu128");
                  system(".\\venv\\Scripts\\python.exe -m pip install -r requirements.txt");
                  system(".\\venv\\Scripts\\python.exe -m pip list");
                  std::cout << "\nInicialize o venv para testar." << std::endl;
                }
              }
            }
          }
        } else {
          MessageBoxW(NULL, L"Sua Placa de video não é suportada.\nPor motivo de compatibilidade somente 'nvidia' é suportada.", L"Falha de incompatibilidade", MB_ICONERROR);
          std::cout << "Por motivo de compatibilidade somente 'nvidia' é suportada." << std::endl;
          return 0;
        }
      }
    }
    d3d->Release();
  } else return 1;
  return 0;
}
#else
int main() {
  std::cout << "Sistema Operacional não recomendando." << std::endl;
  return 0;
}
#endif