# 🐍 Python do Zero - Guia de Estudos da Letícia

## Capítulo 1: O Shebang e Execução de Scripts no Linux

Quando criamos arquivos de script em Python dentro do ecossistema Linux, podemos configurar o sistema para executar o código diretamente pelo terminal, sem a necessidade de digitar `python3` antes do nome do arquivo.

### 1. O que é o Shebang (`#!`)?

O Shebang é a primeira linha absoluta de um código. Ela indica ao kernel do Linux qual interpretador deve ser chamado para ler as linhas de texto a seguir.

- **Sintaxe correta e universal:**

```python
#!/usr/bin/env python3
print("Olá, mundo!")
```

- **Por que usamos `/usr/bin/env python3`?**
  Em vez de colocar o caminho fixo do Python (que pode mudar entre distribuições), o comando `env` pesquisa nas variáveis de ambiente do seu sistema onde o executável do Python 3 está ativo (seja no Fedora, Nobara ou Arch).

### 2. Como dar Permissão de Execução no Terminal

Mesmo com o Shebang correto, o Linux bloqueia a execução direta de novos arquivos por segurança. Para liberar o arquivo, usamos o utilitário `chmod` no terminal da pasta:

```bash
chmod +x meu_script.py
```

_(A flag `+x` significa "adicionar permissão de execução")_

### 3. Como Rodar o Arquivo Liberado

Após dar a permissão, você pode disparar o script usando o caminho relativo do diretório atual:

```bash
./meu_script.py
```

---

_Nota: Em arquivos que servem apenas como módulos/bibliotecas secundárias (que serão importados por outros arquivos), o uso do Shebang não é necessário._
