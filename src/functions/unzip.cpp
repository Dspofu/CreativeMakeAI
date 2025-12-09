#include "unzip.h"

bool unzip() {
  std::filesystem::path path = std::filesystem::current_path();
  std::filesystem::path file = path;
  file /= "project.zip";
  const wchar_t* zipPath = file.c_str();
  CoInitialize(NULL);

  IShellDispatch* pShell = NULL;
  Folder* pZip = NULL;
  Folder* pDest = NULL;

  HRESULT hr = CoCreateInstance(CLSID_Shell, NULL, CLSCTX_INPROC_SERVER, IID_PPV_ARGS(&pShell));

  if (FAILED(hr)) {
    printf("Erro ao iniciar Shell\n");
    return false;
  }

  VARIANT vZip, vDest, vOpt;
  VariantInit(&vZip);
  VariantInit(&vDest);
  VariantInit(&vOpt);

  vZip.vt = VT_BSTR;
  vZip.bstrVal = SysAllocString(zipPath);

  vDest.vt = VT_BSTR;
  vDest.bstrVal = SysAllocString(path.c_str());

  pShell->NameSpace(vZip, &pZip);
  pShell->NameSpace(vDest, &pDest);

  if (!pZip || !pDest) {
    std::cout << pZip << "  " << pDest << std::endl;
    printf("Erro ao abrir ZIP ou pasta destino\n");
    return false;
  }

  FolderItems* pItems = NULL;
  pZip->Items(&pItems);

  VARIANT vItem;
  VariantInit(&vItem);
  vItem.vt = VT_DISPATCH;
  vItem.pdispVal = pItems;

  vOpt.vt = VT_I4;
  vOpt.lVal = FOF_NOCONFIRMATION | FOF_SILENT;

  pDest->CopyHere(vItem, vOpt);

  SysFreeString(vZip.bstrVal);
  SysFreeString(vDest.bstrVal);

  if (pItems) pItems->Release();
  if (pZip) pZip->Release();
  if (pDest) pDest->Release();
  if (pShell) pShell->Release();

  CoUninitialize();

  printf("Pasta descompactada!\n");
  return true;
}