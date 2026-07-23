# ⌨️ Guia de Atalhos Personalizados - VS Code (Nobara/Hyprland)

Este arquivo registra a configuração exata e os atalhos do ambiente atual de desenvolvimento, mapeados para evitar conflitos com os comandos globais do gerenciador de janelas Hyprland.

## 🚀 Execução e Produtividade

- **`Ctrl + Enter`**: Executa o código atual diretamente no terminal (Configurado via Code Runner).
- **`Ctrl + \`**: Abre o chat do terminal (Ferramenta IA do GitHub Copilot).
- **`Ctrl + Shift + P`**: Abre a Paleta de Comandos global do VS Code (Acesso a configurações e extensões).

## 🎨 Formatação e Código Limpo

- **`Ctrl + Alt + F`**: Formata o arquivo atual de forma segura (Remapeado para não conflitar com as _dots_ do Hyprland).
- **Salvamento Automático**: O editor salva as alterações do arquivo no disco assim que perde o foco da janela (`onFocusChange`). Não é necessário apertar `Ctrl + S` antes de rodar o código.

## 🛠️ Ecossistema de Formatadores Ativos

O sistema identifica automaticamente a extensão do arquivo aberto e aplica a engine de formatação ideal:

- **Python (`.py`)**: Formatado via **Ruff** (limpa o código e organiza as linhas de `import` automaticamente ao salvar).
- **C / C++ (`.c`, `.cpp`)**: Formatado via **Clang-Format** utilizando o padrão de estilo visual da Google.
- **Java (`.java`)**: Formatado via engine da Red Hat utilizando o padrão de estilo visual da Google.
- **Web / Configurações (`.html`, `.css`, `.js`, `.json`, `.md`)**: Formatados universalmente via **Prettier**.
