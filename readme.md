## Documentação/Guia Oficiais
[Pagina de guia e documentação em construção](https://pofuserver.com/creativeMakeAI)

## Instalação

[Clique aqui](https://github.com/Dspofu/CreativeMakeAI/releases/download/0.1.0/CreativeMakeAI-Beta.zip) para baixar o projeto

- O programa é seguro, mas não possui um certificado indexado, por isso o seu OS pode detecta-lo como possivel ameaça.

<details>
  <summary><h3><strong>Dev Build Commands</strong> 👈</h3></summary>

Comando para build do `.cpp`

```batch
g++ -static main.cpp -o installer_start.exe -lole32 -loleaut32 -luuid -lshell32 -lshlwapi -lwininet -static-libgcc -static-libstdc++ -ld3d9
```

Comando para build do `.py` usando `cx_Freeze` ou `pyinstaller`

**cx_Freeze**
```batch
python build.py build -v
```

**pyinstaller**
```batch
pyinstaller --name "CreativeMakeAI" --windowed --onefile --icon="assets/images/icon_24px.ico" --add-data="assets;assets" --collect-all="transformers" --collect-all="diffusers" main.py
```

</details>

Para uma breve verificação simples execute o arquivo `varificar.exe`.<br>
A aplicação só vai funcionar caso possua uma placa de video `GPU - Nvidia` que tenha a *capacidade computacional* superior a `5.0`, por um requisito da versão do **cuda toolkit**.<br>
Caso queria saber a capacidade computacional de sua placa de video você pode consultar no [site da Nvidia](https://developer.nvidia.com/cuda-gpus).

___

## Após ter tudo baixado é só iniciar

##### Exemplo de versões anteriores
<image src="assets/images/example.gif">

- Sistema de `Alerta de temperatura` funciona como um recurso de espera, conforme esquenta ela espera para gerar a próxima etapa.
- Os modelos LoRA's devem ser selecionados para alterar o estilo para o qual deseja.
- O recorso de `gerar varias imagens` vai fazer com que a GPU trabalhe por mais tempo, recomendo deixar o `Alerta de Temperatura` ativo.
- O `log.txt` vai conter registros de andamentos e erros, lá você pode encontrar tambem a `seed` das imagens que estão sendo geradas.

<image src="assets/images/example.png" style="width: 350px">

___

## Baixar modelos

Para baixar o modelo de IA para gerar imagem existem varios sites, [Hugging Face](https://huggingface.co/models?pipeline_tag=text-to-image&library=safetensors&sort=trending) ou [CivitAi](https://civitai.com/models) é um desses sites, para o CivitAi eu recomendo que filtre por:

|Model status: `Checkpoint` | Checkpoint type: `All` | File fomart: `SafeTensor`
|---|---|---|

Após baixar o modelo, procure tambem as especificações de configuração recomendada para ele para depois inserir na aplicação.
OBS: Geralmente os modelos tem de 3GB a 15GB, então não se assuste com o tamanho do arquivo que foi baixado.

___

## Recomendações Minimas

- GPU Nvidia: `RTX 2060 super` • OBS: `RTX 3050 8GB > GTX 1080 TI 11GB`
- RAM: (2x16) 32GB - 3200MHz

> Dica: Em uma placa de video os modelos de IA tem um bom desempenho naquelas que possuem um alto numero de `tensor cores`, `Vram` e uma boa `arquitetura`, eu diria que se você é uma amante dessa área, que você use então modelos `RTX` que possuem no `mínimo 12GB de vram` para desfrutar de modelos mais complexos que `15GB`

> [!NOTE]  
> Impostante notar que geralmente o software consume em média (~9GB) de Ram em modelos médios de 6GB

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
|CPU|AMD/Intel/'others'|3.0GHz 2/4|
|RAM|HyperX/'others'|32GB 3200MHz|
|GPU|Nvidia|RTX 2060 Super 8GB|
|SSD|Kingspec/SanDisk/'others'|240GB 5000Mb/s|

# 

(ヘ･_･)ヘ┳━┳ Give-me star, pls (╯‵□′)╯︵┻━┻
