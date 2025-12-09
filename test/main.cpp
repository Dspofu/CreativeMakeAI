#ifdef _WIN32
#include <windows.h>
#include <iostream>
#include <sstream>
#include <string>
#include <cmath>
#include <wininet.h>
#include <shlobj.h>
#include <shlwapi.h>
#include <fstream>
#include <filesystem>
#include <d3d9.h>

#include "src/modules/unzip.h"
#include "src/modules/progress.h"
#include "src/modules/options.h"

#pragma comment(lib, "wininet.lib")
#pragma comment(lib, "d3d9.lib")
#pragma comment(lib, "shell32.lib")
#pragma comment(lib, "ole32.lib")
#pragma comment(lib, "shlwapi.lib") 

int main() {
  SetConsoleOutputCP(CP_UTF8);
  SetConsoleCP(CP_UTF8);

  MEMORYSTATUSEX memInfo;
  memInfo.dwLength = sizeof(memInfo);

  IDirect3D9 *d3d = Direct3DCreate9(D3D_SDK_VERSION);
  if (d3d) {
    D3DADAPTER_IDENTIFIER9 adapterIdentifier;
    for (int i = 0; i < d3d->GetAdapterCount(); i++) {
      D3DADAPTER_IDENTIFIER9 adapterIdentifierLoop;
      std::cout << adapterIdentifierLoop.Description << " | " << adapterIdentifierLoop.DeviceName << std::endl;
    }
    
    if (SUCCEEDED(d3d->GetAdapterIdentifier(D3DADAPTER_DEFAULT, 0, &adapterIdentifier))) {
      if (adapterIdentifier.VendorId == 0x10DE) { // AMD: 4098
        if (GlobalMemoryStatusEx(&memInfo)) {
          int memory = std::round(memInfo.ullTotalPhys / (1024.0f * 1024.0f * 1024.0f));
          if (memory <= 8) {
            std::wstringstream content;
            content << L"Processo encerrado por falta de memória RAM\nForam encontrados somente: " << memory << "GB de RAM.";
            MessageBoxW(NULL, content.str().c_str(), L"Pouca RAM no sistema", MB_ICONERROR);
            std::cout << "O recomendado seria ter 32GB de RAM e foram identificados somente: " << memory << "GB de RAM." << std::endl;
            return 1;
          } else {
            char quest;
            if (loopQuest(quest)) {
              if (quest == '1' || quest == '2') {
                if (quest == '2') system("winget install --id Python.Python.3.13 --version 3.13.6");
                char option;
                for(;;) {
                  loopOption(adapterIdentifier, memory);
                  std::cin >> option;
                  std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
                  if (option == '0') break;
                  else if (option == '1') {
                    std::cout << "\nINICIANDO\n" << std::endl;
                    system(".\\venv\\Scripts\\python.exe -m main");
                  } else if (option == '2') option2();
                  else if (option == '3') {
                    HINTERNET hInternet = InternetOpenW(L"CreativeMakeAI Installer", INTERNET_OPEN_TYPE_DIRECT, NULL, NULL, 0);
                    if (!hInternet) {
                      printf("Falha ao inicializar WinINet\n");
                      continue;
                    }
                    const wchar_t *url = L"https://github.com/Dspofu/CreativeMakeAI/archive/refs/heads/main.zip";
                    HINTERNET hUrl = InternetOpenUrlW(hInternet, url, NULL, 0, INTERNET_FLAG_RELOAD, 0);
                    if (!hUrl) {
                      printf("Falha ao abrir a URL\n");
                      InternetCloseHandle(hInternet);
                      continue;
                    }

                    DWORD fileSize = 0;
                    DWORD sizeSize = sizeof(fileSize);
                    HttpQueryInfoW(hUrl, HTTP_QUERY_CONTENT_LENGTH | HTTP_QUERY_FLAG_NUMBER, &fileSize, &sizeSize, NULL);

                    std::ofstream file("project.zip", std::ios::binary | std::ios::trunc);
                    if (!file.is_open()) {
                      printf("Falha ao criar o arquivo .zip\n");
                      InternetCloseHandle(hUrl);
                      InternetCloseHandle(hInternet);
                      continue;
                    } else printf("Baixando arquivos\n");

                    char buffer[4096];
                    DWORD bytesRead = 0;
                    DWORD totalRead = 0;
                    int ifPercent = 0;
                    char spinner[] = "/-\\|";
                    int spinner_idx = 0;

                    // O loop principal de download
                    while (InternetReadFile(hUrl, buffer, sizeof(buffer), &bytesRead) && bytesRead > 0) {
                      file.write(buffer, bytesRead);
                      totalRead += bytesRead;
                      if (fileSize > 0) {
                        int percent = static_cast<int>(((double)totalRead * 100.0) / fileSize);
                        if (ifPercent != percent) {
                          ifPercent = percent;
                          progressBar(ifPercent);
                        }
                      } else {
                        printf("\r%c (%.2f MB)", spinner[spinner_idx], (double)totalRead / (1024 * 1024));
                        spinner_idx = (spinner_idx + 1) % 4;
                      }
                    }
                    printf("\rDownload concluído com %.2f MB baixados.           \n", (double)totalRead / (1024 * 1024));

                    file.close();
                    InternetCloseHandle(hUrl);
                    InternetCloseHandle(hInternet);

                    printf("Pressione alguma tecla para descompactar projeto.\n");
                    system("pause > nul");
                    unzip();

                    std::filesystem::path zipPath = std::filesystem::current_path() / "project.zip";
                    try {
                      if (std::filesystem::exists(zipPath)) {
                        std::filesystem::remove(zipPath);
                        std::cout << "Arquivo deletado: " << zipPath.string() << std::endl;
                      } else printf("Arquivo não encontrado.\n");
                    }
                    catch (std::filesystem::filesystem_error &e) {
                      std::cerr << "Erro ao deletar: " << e.what() << std::endl;
                    }
                    printf("Execute o arquivo 'nvidia-gpu-5.0plus.bat' na pasta criada.");
                    system("pause > nul");
                    exit(0);
                  }
                }
              }
            }
          }
        }
      } else {
        MessageBoxW(NULL, L"Sua Placa de video não é suportada.\nPor motivo de compatibilidade somente 'nvidia' é suportada.", L"Falha de incompatibilidade", MB_ICONERROR);
        std::cout << "Por motivo de compatibilidade somente 'nvidia' é suportada." << std::endl;
        return 1;
      }
      d3d->Release();
    } else return 1;
    return 0;
  }
}
#else
int main() {
  std::cout << "Sistema Operacional não recomendando." << std::endl;
  return 0;
}
#endif