## Instalação

Caso possua uma placa de video `GPU` que tenha a *capacidade computacional* superior a `5.0` ela ira funcionar, e para instalar esse complemento execute o arquivo `nvidia-gpu-5.0plus.bat`.
> Isso é na verdade um detalhe que deve ser observado ao decorrer da versão do **cuda toolkit** e a **capacidade computacional** da sua placa de video, para saber se sua `GPU` tem a capacidade computacional de pelo menos `5.0` você pode consultar no [site da Nvidia](https://developer.nvidia.com/cuda-gpus).

#### Baixar os pacotes da aplicação. 
> Seria ideal antes ler as [**recomendações**](#recomendações)

```batch
pip install -r requirements.txt
```

## Requisitos mínimos

- Python: `3.12.0+`
- pip: `24.3.1+`
- GPU Nvidia: `RTX 2060` `GTX 1080 TI 11GB > RTX 2050`

## Recomendações

- Python: `3.13.1`
- pip: `25.1.1`
- GPU Nvidia: `RTX 3060 12GB` • `RTX 3050 8GB > GTX 1080 TI 11GB`

#### Gerar o `venv` local para ficar armazenado as libs da aplicação.

```batch
python -m venv venv
```

#### Duas formas no terminal do `Windows` para acessar o `venv`

```batch
.\venv\Scripts\Activate.ps1

.\venv\Scripts\activate.bat
```

#### Verificar atualização do seu gerenciador de pacotes `pip`

```batch
.\venv\Scripts\python.exe -m pip install --upgrade pip
```
