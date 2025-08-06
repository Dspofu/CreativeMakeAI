#ifdef _WIN32
#include <windows.h>
#include <iostream>
#include <d3d9.h>

#pragma comment(lib, "d3d9.lib")

bool loopOption(char& option, D3DADAPTER_IDENTIFIER9 adapterIdentifier) {
  system("cls");
  std::wcout << L"GPU detectada: " << adapterIdentifier.Description << L"\n\nInstalar e configurar os pacotes automaticamentes:\n[y] - Baixar pacotes\n[n] - Nao quero baixar\n\n> ";
  std::cin >> option;
  if (option != 'y' && option != 'n') return loopOption(option, adapterIdentifier);
  else return true;
}

bool loopQuest(char& quest) {
  system("cls");
  std::cout << "Verifique se este dispositivo possui o Python na versão 3.12.0 ou superior\n" << std::endl;
  system("python --version");
  std::cout << "\nConfirme se ele tem no dispositivo:\n[y] - Sim possuo\n[n] - Nao tenho e vou baixar\n\n> ";
  std::cin >> quest;
  if (quest != 'y' && quest != 'n') return loopQuest(quest);
  else return true;
}

int main() {
  SetConsoleOutputCP(CP_UTF8);
  SetConsoleCP(CP_UTF8);

  IDirect3D9 *d3d = Direct3DCreate9(D3D_SDK_VERSION);
  if (d3d) {
    D3DADAPTER_IDENTIFIER9 adapterIdentifier;
    if (SUCCEEDED(d3d->GetAdapterIdentifier(D3DADAPTER_DEFAULT, 0, &adapterIdentifier))) {
      if (adapterIdentifier.VendorId == 0x10DE) {
        char quest;
        if (loopQuest(quest)) {
          if (quest == 'y') {
            char option;
            if (loopOption(option, adapterIdentifier)) {
              if (option = 'y') {
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
        std::cout << "Por motivo de compatibilidade a GPU tem que ser uma 'nvidia'." << std::endl;
        return 0;
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