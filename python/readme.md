## Instalação

Caso possua uma placa de video `GPU` entre as series `GTX 10xx` e `RTX 40xx` execute o arquivo `nvidia-gpu(GTX10xx-RTX40xx).bat`, mas se for da serie `RTX 50xx` execute o arquivo `nvidia-gpu(RTX50xx).bat`.
> Isso é na verdade um detalhe que deve ser observado ao decorrer da versão do **cuda** instalada nas placas de video, as versões de **cuda** `12.8` seria correspondente a serie `RTX 50` e enquanto a versão `12.1` do **cuda** seria das GPU's antecessoras até o momento.

#### Baixar os pacotes da aplicação. 
> Seria ideal antes ler as [**recomendações**](#recomendações)

```batch
pip install -r requirements.txt
```

## Recomendações

- Python: `3.13.1`
- pip: `24.3.1+`

#### Gerar o `venv` local para ficar armazenado as libs da aplicação.

```batch
python -m venv venv
```

#### Comando no terminal do `Windows` para acessar o `venv`
```batch
.\venv\Scripts\Activate.ps1
```

#### Varificar atualização do seu gerenciador de pacotes `pip`

```batch
.\venv\Scripts\python.exe -m pip install --upgrade pip
```