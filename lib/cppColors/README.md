# Colored letters

## Colors Table

| Color Name     | Method        | Color Code  |
|----------------|---------------|-------------|
| **BLACK**      | `Colors::BLACK`      | `\x1b[30m`  |
| **RED**        | `Colors::RED`        | `\x1b[31m`  |
| **GREEN**      | `Colors::GREEN`      | `\x1b[32m`  |
| **YELLOW**     | `Colors::YELLOW`     | `\x1b[33m`  |
| **BLUE_DARK**  | `Colors::BLUE_DARK`  | `\x1b[34m`  |
| **PURPLE**     | `Colors::PURPLE`     | `\x1b[35m`  |
| **BLUE**       | `Colors::BLUE`       | `\x1b[36m`  |
| **GRAY**       | `Colors::GRAY`       | `\x1b[90m`  |
| **CYAN**       | `Colors::CYAN`       | `\x1b[96m`  |
| **BLUE_ROYAL** | `Colors::BLUE_ROYAL` | `\x1b[94m`  |
| **PINK**       | `Colors::PINK`       | `\x1b[95m`  |
| **DEFAULT**    | `Colors::DEFAULT`    | `\x1b[0m`   |

# 

### Select language - Selecionar linguagem

<details>
  <summary style="font-size: 12px"><strong>ENG</strong></summary>

This repository contains a set of terminal color definitions using ANSI codes. The `colors.cpp` file defines a series of strings that can be used to apply colors to text in the terminal.

## Available Colors

The colors are defined in the `Colors` class and can be used as follows:

- **BLACK**: `\x1b[30m` — Black color
- **RED**: `\x1b[31m` — Red color
- **GREEN**: `\x1b[32m` — Green color
- **YELLOW**: `\x1b[33m` — Yellow color
- **BLUE_DARK**: `\x1b[34m` — Dark blue color
- **PURPLE**: `\x1b[35m` — Purple color
- **BLUE**: `\x1b[36m` — Blue color
- **GRAY**: `\x1b[90m` — Gray color
- **CYAN**: `\x1b[96m` — Cyan color
- **BLUE_ROYAL**: `\x1b[94m` — Royal blue color
- **PINK**: `\x1b[95m` — Pink color
- **DEFAULT**: `\x1b[0m` — Default terminal color (reset)

## How to Use

To use the colors, simply include the corresponding code for the desired color in any text you print to the terminal. Here is an example of how to use the colors defined in the `colors.cpp` file:

### Example usage:

```cpp
#include "./Colors/colors.h"
#include <iostream>

int main() {
  system("@echo off"); // Quick method to enable the use of ANSI codes
  // Example of using the defined colors
  std::cout << Colors::RED << "This is a red text!" << Colors::DEFAULT << std::endl;
  std::cout << Colors::GREEN << "This is a green text!" << Colors::DEFAULT << std::endl;
  std::cout << Colors::BLUE_ROYAL << "This is a royal blue text!" << Colors::DEFAULT << std::endl;
  return 0;
}
```
</details>

# 

<details>
  <summary style="font-size: 12px"><strong>PT-BR</strong></summary>

Este repositório contém um conjunto de definições de cores para terminal, utilizando códigos ANSI. O arquivo `colors.cpp` define uma série de strings que podem ser usadas para aplicar cores ao texto no terminal.

## Cores Disponíveis

As cores estão definidas na classe `Colors` e podem ser usadas da seguinte maneira:

- **BLACK**: `\x1b[30m` — Cor preta
- **RED**: `\x1b[31m` — Cor vermelha
- **GREEN**: `\x1b[32m` — Cor verde
- **YELLOW**: `\x1b[33m` — Cor amarela
- **BLUE_DARK**: `\x1b[34m` — Cor azul escuro
- **PURPLE**: `\x1b[35m` — Cor roxa
- **BLUE**: `\x1b[36m` — Cor azul
- **GRAY**: `\x1b[90m` — Cor cinza
- **CYAN**: `\x1b[96m` — Cor ciano
- **BLUE_ROYAL**: `\x1b[94m` — Cor azul royal
- **PINK**: `\x1b[95m` — Cor rosa
- **DEFAULT**: `\x1b[0m` — Cor padrão do terminal (reset)

## Como Usar

Para usar as cores, basta incluir o código correspondente ao estilo desejado em qualquer texto que você imprimir no terminal. Aqui está um exemplo de como usar as cores definidas no arquivo `colors.cpp`:

### Exemplo de uso:

```cpp
#include "./Colors/colors.h"
#include <iostream>

int main() {
  system("@echo off"); // Metodo rapido para ativar o uso de códigos ANSI"
  // Exemplo de uso das cores definidas
  std::cout << Colors::RED << "Este é um texto em vermelho!" << Colors::DEFAULT << std::endl;
  std::cout << Colors::GREEN << "Este é um texto em verde!" << Colors::DEFAULT << std::endl;
  std::cout << Colors::BLUE_ROYAL << "Este é um texto em azul royal!" << Colors::DEFAULT << std::endl;
  return 0;
}
```
</details>