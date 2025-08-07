## Instalação

Clone o repositório ou [clique aqui](https://github.com/Dspofu/CreativeMakeAI/archive/refs/heads/main.zip) para baixar o zip

```batch
git clone https://github.com/Dspofu/CreativeMakeAI.git
```

Para instalar e fazer uma breve verificação execute o arquivo `nvidia-gpu-5.0plus.bat`.<br>
A aplicação só vai funcionar caso possua uma placa de video `GPU - Nvidia` que tenha a *capacidade computacional* superior a `5.0`, por um requisito da versão do **cuda toolkit**.<br>
Caso queria saber a capacidade computacional de sua placa de video você pode consultar no [site da Nvidia](https://developer.nvidia.com/cuda-gpus).

#### Baixar os pacotes da aplicação. 

Seria ideal ler antes as [**recomendações**](#recomendações)

```batch
pip install -r requirements.txt
```

- Instalação rápida com a verificação simples é só executar o arquivo: `nvidia-gpu-5.0plus.bat`
- O instalador ainda não é compativel com distribiuções `Linux`
___

## Baixar modelos

Para baixar o modelo de IA para gerar imagem existem varios sites, [CivitAi](https://civitai.com/models) é um desses sites, nele eu recomendo que filtre por:

|Model status: `Checkpoint` | Checkpoint type: `All` | File fomart: `SafeTensor`
|---|---|---|

Após baixar o modelo, procure tambem as especificações de configuração recomendada para ele para depois inserir na aplicação.
OBS: Geralmente os modelos tem de 3GB a 15GB, então não se assuste com o tamanho do arquivo que foi baixado.

> Até o momento não tem compatibilidade com o modelo `LoRa`

___

## Recomendações

- Python: `3.13.1`
- pip: `25.1.1`
- GPU Nvidia: `RTX 3060 12GB` • OBS: `RTX 3050 8GB > GTX 1080 TI 11GB`

> Dica: em uma placa de video os modelos de IA tem um bom desempenho naquelas que possuem um alto numero de `tensor cores`, `Vram` e uma boa `arquitetura`, eu diria que se você é uma amante dessa área, que você use então modelos `RTX` que possuem no `mínimo 12GB de vram` para voce poder fugir para modelos ainda maiores que `15GB`

### Python
|Recurso|Versão|Compatibilidade|
|:---:|:---:|:---|
|Python|3.12.0|🟢 - Bibliotecas compativeis|
|Pip|24.3.1|🟢 - Funciona tranquilamente|

# 

### GPU

|Modelo|Fabricante|cuda|Compatibilidade|
|:---:|:---:|:---:|:---|
|RX|AMD| - |🟠 - Incompatível|
|ARC|Intel| - |🟠 - Incompatível|
|RTX|Nvidia|8.9|🟢 - Otimo para uso|
|GTX|Nvidia|5.0|🟡 - Para amador e paciente|

# 

### Sistema Geral

|Hardware|Fabricante|Modelo|
|:---:|:---:|:---|
|OS|Microsoft|Windows 10 Pro 'Latest'|
|CPU|AMD/Intel/'others'|2.3GHz 2/4|
|RAM|HyperX/'others'|32GB 3200MHz|
|GPU|Nvidia|RTX 2060 Super 8GB|
|SSD|Kingspec/SanDisk/'others'|240GB 5000Mb/s|

# 

#### Gerar o `venv` local para ficar armazenado as libs da aplicação.

```batch
python -m venv venv
```

#### Duas formas no terminal do `Windows` para acessar o `venv`

**Powershell**

```batch
.\venv\Scripts\Activate.ps1
```

**Cmd**

```batch
.\venv\Scripts\activate.bat
```

#### Verificar atualização do seu gerenciador de pacotes `pip`

```batch
.\venv\Scripts\python.exe -m pip install --upgrade pip
```

# 

(ヘ･_･)ヘ┳━┳ Give-me star, pls (╯‵□′)╯︵┻━┻
