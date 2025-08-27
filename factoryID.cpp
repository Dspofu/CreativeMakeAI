#include <iostream>
#include <string>
#include <d3d9.h>

#pragma comment(lib, "d3d9.lib")

int main() {
  IDirect3D9 *d3d = Direct3DCreate9(D3D_SDK_VERSION);
  if (d3d) {
    D3DADAPTER_IDENTIFIER9 adapterIdentifier;
    if (d3d->GetAdapterCount() > 1) {
      for (int i = 0; i < d3d->GetAdapterCount(); i++) {
        D3DADAPTER_IDENTIFIER9 adapterIdentifierLoop;
        if (SUCCEEDED(d3d->GetAdapterIdentifier(i, 0, &adapterIdentifierLoop))) {
          std::cout << "GPU's: " << adapterIdentifierLoop.Description << " | ID fabricante: " << adapterIdentifierLoop.VendorId << std::endl;
        }
      }
      printf("\n");
    }
    if (SUCCEEDED(d3d->GetAdapterIdentifier(D3DADAPTER_DEFAULT, 0, &adapterIdentifier))) {
      std::cout << "GPU padrao: \"" << adapterIdentifier.Description << "\" | ID fabricante: " << adapterIdentifier.VendorId;
      d3d->Release();
    }
  }
  system("pause > nul");
  return 0;
}