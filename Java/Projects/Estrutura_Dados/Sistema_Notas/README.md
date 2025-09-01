# Projeto Apl2 – Atualização de Sistema de Notas em Java

Este projeto em Java foi desenvolvido como parte de uma atividade prática de Estruturas de Dados. Ele visa modernizar um sistema legado de controle de notas utilizado por escolas, substituindo a estrutura de dados antiga por uma representação mais adequada e robusta usando listas duplamente encadeadas.

## 📚 Objetivo

Substituir a estrutura legada baseada em listas simplesmente encadeadas por uma nova estrutura que:

- Uso de listas **duplamente encadeadas**.
- Converte os dados antigos de alunos e notas para um novo formato mais seguro.
- Aplica filtros (por nota, média, ausência).
- Gera um novo arquivo CSV.
- Imprime todas as transformações no terminal.

---

## 🛠️ Tecnologias Utilizadas

- Linguagem: Java (JDK 24.0.1)
- Estrutura: Projeto modular em `src/` com pacotes
- IDE recomendada: IntelliJ, VS Code com Extensão Java
- Execução via terminal com `javac` e `java`

---

## 📂 Estrutura do Projeto

```bash
Projeto_2/
├── dados.txt                 # Base de dados original (legado)
├── dados.csv                 # Arquivo gerado com dados atualizados
├── src/
│   ├── MainApl2.java         # Classe principal
│   └── apl2/
│       ├── NodeOriginal.java         # Nó legado (fornecido)
│       ├── LinkedListOriginal.java   # Lista legada (fornecido)
│       ├── Node.java                 # Novo nó (implementado)
│       ├── DLinkedList.java          # Lista duplamente encadeada (implementado)
│       ├── Operation.java            # Lógica de transformação e filtros (implementado)
│       └── Data.java                 # Leitura e escrita de arquivos texto (fornecido)
