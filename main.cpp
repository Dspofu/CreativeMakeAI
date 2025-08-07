#ifdef _WIN32
#include <windows.h>
#include <iostream>
#include <d3d9.h>

#pragma comment(lib, "d3d9.lib")

bool loopOption(char& option, D3DADAPTER_IDENTIFIER9 adapterIdentifier) {
  system("cls");
  std::wcout << L"GPU detectada: " << adapterIdentifier.Description << L"\n\nAgora escolha entre 'instalar a configurar os pacotes automaticamentes' ou caso instalado anteriormente 'iniciar':\n[0] - Nao quero\n[1] - Iniciar programa\n[2] - Baixar pacotes\n\n> ";
  std::cin >> option;
  if (option != '0' && option != '1' && option != '2') return loopOption(option, adapterIdentifier);
  else return true;
}

bool loopQuest(char& quest) {
  system("cls");
  std::cout << "Verifique se este dispositivo possui o Python na versão 3.12.0 ou superior.\n\nVersão encontrada: ";
  system("python --version");
  std::cout << "\nConfirme se ele foi encontrado:\n[0] - Nao tenho\n[1] - Sim possuo\n\n> ";
  std::cin >> quest;
  if (quest != '1' && quest != '0') return loopQuest(quest);
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
          if (quest == '1') {
            char option;
            if (loopOption(option, adapterIdentifier)) {
              if (option == '1') {
                std::cout << "\n";
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