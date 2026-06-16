# Manual do contribuidor

Esse arquivo é um pequeno tutorial das features de python utilizadas no projeto e a estrutura básica do mesmo.
Sempre que encontrar alguma estrutura da linguagem que não conhece ou um arquivo que não sabe pra que serve, consulte esse manual. 
Sinta-se à vontade para adicionar informações novas aqui, isso ajuda a equipe como um todo a entender o projeto e continuar desenvolvendo.

## Features

### Doc strings

As 'Doc strings' são estruturas em python que permitem você descrever uma função, assim como um comentário, porem esse comentário irá aparecer sempre nas sugestões do seu editor de código quando for usar a função. É uma boa prática utilizá-las

> [!NOTE]
> **Boa prática:** sempre documente o seu código antes de fazer um push para o repositório. Você pode entender o que escreveu, mas a sua equipe provavelmente não. Faça bom uso das doc strings e dos comentários de código. 

Ex:

```python
def funcao():
  """
  Essa é uma doc string que documenta a sua função
  """
```

---

### Tipando variáveis e funções 

Uma estratégia para evitar erros durante o desenvolvimento é dizer explicitamente o tipo das variáveis e o tipo do retorno das funções.

Ex:

```python

# variavel: tipo = valor
var: int = 0 # diz explicitamente que var é um inteiro
var = "john" # isso gera um erro pois var so aceita inteiros

var2 = 0
var2 = "doe" # isso não gera um erro, pois a variavel tem o tipo dinâmico


# def funcao() -> tipo
def soma(a: int, b:int) -> int: # define que o valor retornado pela função será sempre um inteiro
  return a + b


# também pode ser usado com classes

class Pessoa:
  pass

pessoa: Pessoa # digo explicitamente que a variavel pessoa é do tipo Pessoa
pessoa = "pessoa" # isso gera um erro
pessoa = Pessoa() # isso está corredo pois instancia a classe Pessoa na variavel de tipo Pessoa
```

---

### Importações renomeadas

As vezes você vai querer fazer um import de um arquivo ou função a qual tem o mesmo nome de um variável local. Obviamente isso causa um erro pois duas coisas com o mesmo nome gera ambiguidade em python. Para resolver isso, você pode renomar as variáveis utilizando o comando `as`.

Ex:
```python
from core import sounds

sounds = ["som1", "som2"] # isso gera um erro pois agora existem duas coisas diferentes chamadas sounds.
```

Ao envés disso você pode fazer:

```python
from core import sounds as sons

sounds = ["som1", "som2"] # agora o import sounds foi renomado para sons e não gera mais um erro
```

---

### Arquivo \_\_init\_\_.py

O arquivo \_\_init\_\_.py tem a função de transformar aquela pasta onde ele está em um modulo python. Isso permite que você faça imports dos modulos dentro dessa pasta a partir de qualquer arquivo no seu código. Geralmente esse arquivo fica vazio.

Ele também pode ser usado para preencher pastas que ainda estão vazias mas futuramente teram alguma coisa. Isso pode ser útil para poder versionar suas pastas no github (pastas vazias são ignoradas pelo git e não são versionadas)

--- 

### Descompactando dicionários

Muitas vezes acontece de você ter uma função que recebe muitos parametros no seu projeto. Esse tipo de função costuma dar trabalho em suas chamadas pois passar cada paramentro manualmente pode gerar alguns erros (esquecer um parametro, etc.). Para isso existe uma técnica de descompactação utilizando o operador `**`. Veja o exemplo.

Ex:
```python
def soma(a, b, c, d, e, f) -> int:
  return a + b + c + d + e + f

a = 0
b = 2
c = 7
d = 5
e = 9
f = 0

soma(a, b, c, d, e, f) # isso até funciona, mas é bem deselegante

parametros = {"a": 0, "b": 2, "c": 7, "d": 5, "e": 9, "f":0}

soma(**parametros) # terá o mesmo resultado, porém o código fica mais organizado
```

Em geral, é muito útil quando todas as informações estão ligadas a um contexto (como variáveis de configuração ou propriedades de algum objeto).

Ex:
```python
WINDOW_SETUP = {
    "size": WINDOW_SIZE,
    "flags": 0,
    "depth": 0,
    "display": 0,
    "vsync": 1,
} # essas informações estão relacionadas pelo contexto da window

pygame.display.set_mode(**WINDOW_SETUP) # dessa forma você deixa o código legivel, organizado e fácil de dar manutenção

```

---

## Estrutura de arquivos
 
A estrutura de arquivos de um projeto é muito importante para a escalabilidade e para futuras correções, manutenção, etc. É sempre bom separar tudo em arquivos diferentes e saber onde cada pedaço do código se encaixa.
 
```
src
├── assets/
├── components/
├── core/
├── scenes/
└── utilities/
```
 
---
 
### main.py
 
É o arquivo que faz o boot do programa. Ele apenas inicializa e chama o `app.py` do núcleo.
 
---
 
### core/
 
Esse diretório é literalmente o núcleo do projeto. Tudo que faz o jogo funcionar de forma estrutural está aqui.
 
- **app.py** — Centraliza o loop principal do jogo (event loop: entradas de teclado/mouse, atualização de estado, renderização). Cada sistema pode ser definido em seu próprio arquivo; o `app.py` apenas os coordena.
- **assets.py** — Responsável por carregar e disponibilizar os recursos do jogo (imagens, fontes, sons) para o resto do código.
- **constants.py** — Constantes globais (valores que não mudam durante a execução) usadas em diversas partes do código. Centralize aqui para não precisar alterar o mesmo valor em vários lugares.
- **input.py** — Lida com as entradas do usuário (teclado, mouse). Separa essa responsabilidade do loop principal.
- **setup.py** — Faz as configurações iniciais do pygame antes do jogo começar.
---
 
### scenes/
 
Contém as cenas do jogo. Cada cena representa um estado de tela diferente.
 
- **scene.py** — Classe base que todas as cenas herdam. Define a interface comum (ex: `update`, `draw`).
- **menu.py** — Cena do menu principal.
- **game.py** — Cena principal do jogo em si.
- **pause.py** — Cena de pausa.
- **global.py** — Estado/dados globais compartilhados entre cenas.
---
 
### components/
 
Componentes reutilizáveis que podem ser agregados às entidades do jogo.
 
- **object.py** — Classe base para objetos do jogo.
- **animation.py** — Lida com animações de sprites (troca de frames, tempo, etc.).
- **motion.py** — Gerencia movimentação e física básica dos objetos.
- **camera.py** — Controla a câmera/viewport do jogo.
- **statemachine.py** — Implementa uma máquina de estados, usada para controlar o comportamento de entidades (ex: player andando, pulando, atacando).
---
 
### utilities/
 
Funções utilitárias que não pertencem a nenhum contexto específico do jogo.
 
- **math.py** — Funções matemáticas auxiliares.
- **sprite.py** — Funções de auxílio para manipulação de sprites.
---
 
### assets/
 
Todos os recursos estáticos do jogo.
 
```
assets/
├── fonts/          # Arquivos de fonte (.ttf)
│   └── Jersey10-Regular.ttf
├── img/            # Imagens e sprites
│   ├── coin.png
│   ├── heart.png / heart2.png / heart_sprite.png
│   ├── menu_sprite.png
│   └── white_bar.png
├── sfx/            # Efeitos sonoros
│   └── theme.ogg
├── icon.png        # Ícone do jogo
└── joystix.ttf     # Fonte adicional
```
