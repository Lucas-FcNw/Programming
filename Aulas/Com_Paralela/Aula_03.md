# Aula 03 -- Professor Jean: teoria e Mario: lab

---

**JEAN**

Usa o arquivo aula 02


**Onde o paralelismo se esconde?**

Podemos explorar o paralelismo em diferentes níveis de granularidade:
**Nível de instrução (ILP)**: Múltiplas instruções em uma única thread executando ao mesmo tempo. (superescalar, pipeline)

**Nível de Dados (DLP)**: A mesma instrução splicada a múltiplos dados diferentes. O coração de arquiteturas *SIMD* e *GPUs*

**Nível de thread (TLP)**: Múltiplas threads de um emsmo processo execitando concorrentemente. (processadores multicore)

**Nível de Processo (PLP)**: Múltiplos processos independentes rodando no sistema. É a base de clsuters e comp_distríbuida.

As difernetes arquiteruras de hardware existente são justamente para explorar essas diferenças.

Matriz é um exemplo de algo extremamente paralelizável, por exemplo tendo Matriz A;B;C, para calcular C00 eu não dependo de C01, C10, C11.

Paralelismo de tarefas, tarefas distintas rodando ao mesmo tempo.



**Pesquisar como calcular overhead, ganho e afins, pois as vezes o paralelismo pode ser melhor mas ter um overhead tão maior que não vale usar.**




<img width="836" height="271" alt="image" src="https://github.com/user-attachments/assets/cd6bb345-dcb8-49a8-bd9d-f1f7cbb60b15" />


**SISD**: O computador sequencial clássico.
**SIMD** e **MIMD**: As duas categorias mais importantes para a computação paralela atual. Elas que serão mais estudadas.

**MIMD** será o principal quando se trata de paralelismo.


---

### MIMD: O modelo de memória compartilhada


<img width="992" height="706" alt="image" src="https://github.com/user-attachments/assets/e310ba1f-691d-4461-8215-33697e3471fa" />


**Multiprocessadores** ou **multicores** conectados a uma única memória principal.

**Modelo de programação dominante**: Threads (pThreads, OpenMP)

Para memória compartilhada podemos usar Threads, já 



Memória compartilhada, são assim pois se tiver mais de um processador, ou um unico com inumeros cores tem uma memória única dividida entre todos.


Em multiprocessadores a memória compartilhada não é uniforme, a distancia física doss barramentos importam. Os processadores tendem a buscar as memórias(barramentos) mais próximos, chamado de memória primária.

Existe um protocolo para um processador acessar a memória de um barramento secundário.



Duas principais memórias compartilhadas: **UMA** e **NUMA**

| Característica / Aspecto | UMA (Uniform Memory Access) | NUMA (Non-Uniform Memory Access) |
| :--- | :--- | :--- |
| **Tempo de Acesso à Memória** | (Aproximadamente) o mesmo para todos os processadores. | Acessar a memória local é rápido. Acessar a memória de outro processador é lento. |
| **Organização Física** | Compartilhada de forma uniforme. | Fisicamente distribuída em bancos, cada um “perto” de um processador. |
| **Facilidade de Programação** | Mais simples de programar, pois não precisamos nos preocupar com a “localidade” dos dados. | Mais complexa, pois a localidade dos dados afeta diretamente o desempenho. |
| **Uso Típico** | Típico em desktops com CPUs multicores. | Típico de servidores com múltiplos soquetes de CPU. |




O BO da memória compartilhada é a **Coerência de Cache**

Uma **CPU** multicore, cada **core** possui sua própia cache **L1/L2**. Se o núcle A lê a variável X (valor = 5) de memória principal, ele a armaezena em sua cache. Se o núcleo B fizer o mesmo, ele também terá uma cópia de **X**.
**GERANDO RACE CONDITION**


##### E se o núcleo A atualizar a cópia de X para 10?

- A cópia do núcleo B fica **desatualizada**.
- A memória principal também está **desatualizada**.
- O sistema precisa **garantir** que todas as cópias de X sejam consistentes. Isso é o **problema de coerência em cache**.

A solução (hardware): Protocolos de coêrencia de Cache, como snooping e directory-based, que "escutam"o barramento e invalidam ou atualizam cópias obsoletas. *tráfego de coêrencia pode impactar a performance*

### Snooping

Voltar e anotar depois






#### Os 4 estados de coêrencia do cache


Voltar e anotar depois









##### Onde os daods estão em qual estado?

# Cenário

Duas CPUs (A e B) operam sobre a posição de memória X (valor inicial 0).

| Atividade da CPU | Atividade no Barramento | Cache A | Cache B | Memória X |
|---|---|---|---|---|
| Inicial | - | - | - | 0 |
| **CPU A lê X** | **Cache miss para X** | E (0) | - | 0 |
| → Cache A busca X da memória. Como ninguém mais tem, fica em **Exclusive (E)**. | | | | |
| **CPU B lê X** | **Cache miss para X** | S (0) | S (0) | 0 |
| → Cache A vê o snoop (Bus Rd) e muda de E para **Shared (S)**. Cache B também fica em S. | | | | |
| **CPU A escreve 1 em X** | **Invalidação para X** | M (1) | I | 0 |
| → A faz Bus RdX para obter exclusividade. B invalida sua cópia. A escreve e fica em **Modified (M)**. Memória desatualizada. | | | | |
| **CPU B lê X** | **Cache miss para X** | S (1) | S (1) | 1 |
| → B faz Bus Rd. A vê o snoop, **fornece o dado atualizado** para B e para a memória (write-back). Ambas ficam em S. | | | | |

> **Observação crucial:** No último passo, quem forneceu o dado para B foi a **cache A**, não a memória! Isso é o **cache-to-cache transfer** e reduz a latência.


###### Directory-Based

Porque 2, simples Snooping não escala bem em multi-processadores, o barramento vira um gargalo absurdo. o Snooping é bom em multicore.

E como funciona o DB?

O diretório funciona como um catálogo de uma biblioteca, ele mantém um registro de qual processador "pegou emprestado" (em cache) cada  bloco de memória.

##### Cenário


<img width="1192" height="602" alt="image" src="https://github.com/user-attachments/assets/fcec25cd-26e6-4812-94ff-1e82aefe9fce" />


-1 CPU-A quer escrever em Y. Ela envia um pedido ao diretório.
-2 O diretóirio consulta seus registros e vê que a CPU-C tem uma cópia de Y.
-3 O diretório envia uma mensagem de invalidação diertamente e exclusivamente para a CPU-C
-4 Após a confirmção o diretório autoriza a CPU-A a escrever.

*Muito usado em sistemas de alta performance com muitos núcleos e múltiplas CPUs, como servidores e supercomputadores*



<img width="1555" height="618" alt="image" src="https://github.com/user-attachments/assets/90150fb7-97b7-4cde-84a5-e7d197f9f093" />





#### MIMD: Módulo de memória *distribuida*

Também conhecido como multicomputador ou sistema distribuído.

<img width="1222" height="798" alt="image" src="https://github.com/user-attachments/assets/8575fd70-f251-4965-a709-06b87e4348c4" />

- Cada processador tem sua própria memória privada. Não existe espaço de endereçãmento global.
- A comunicação não é implícita, ela **deve** ser explícita.
- Modelos de programação dominantes: Passagem de Mensagens, geralmente com a biblioteca MPI.

Ex: Clusters, Grids e supercomputradores (*top500.org*)  


#### O paradigma da Passagem de Mensagens

Como não há memória compartilhada, a cooperação entre os nós ocorre através do envio e recebimento explicito de mensagens via rede.

<img width="1680" height="132" alt="image" src="https://github.com/user-attachments/assets/5b11d088-4c67-4208-a7e7-7282980b9c3f" />

- O progamador é responsável por:
  - Orquestrar a comunicação: Inserir chamadas send() e recv() no código para trocar
  - informações quando necessário.
  - Sincronizar: ex: um recv() bloqueante.
*Este modelo é mais complexo de programar, mas supera a principal limitação da memória compartilhada: a escalabilidade computacional.*

#### Memória Distribuída: Vantagens e Desvantagens

  | **Vantagens** | **Desvantagens** |
|---|---|
| **Altamente Escalável:** A memória total e o poder de computação crescem linearmente com o número de processadores. | **Programação Complexa:** O programador deve gerenciar explicitamente a distribuição de dados e a comunicação. |
| **Custo-Benefício:** Pode ser construído com hardware de prateleira (*commodity hardware*), como em um cluster de PCs. | **Overhead de Comunicação:** A latência e a largura de banda da rede são fatores críticos de desempenho. |
| **Sem Problemas de Coerência:** Como não há caches compartilhadas, não há necessidade de protocolos de coerência complexos. | **Depuração Difícil:** Depurar um programa distribuído em múltiplas máquinas é um desafio significativo. |



##### SIMD Simple Instruction, Multiple Data

O Conceito:
- Em vez de ter vários processadores fazendo coisas distintas, temos míltiplas unidades de processamento rodando a mesma instrução, ao memso tempo mas em dados diferentes.
- Ideal para para problemas com alto paralelismo de dados. gpGPUs

**Aplicações Típicas:**
- Processamento de Imagens e vídeos.
- Computação gráfica
- Álgebra Linear e Simulações
- Machine Learning

Tudo que for mais pesado manda para a GPU.

<img width="1410" height="747" alt="image" src="https://github.com/user-attachments/assets/10c352ee-dfb8-4af8-806f-1314c26cd9e2" />


| **Vantagens** | **Desvantagens** |
|---|---|
| **Desempenho Massivo:** Potencial para TERAFlops de poder de computação para problemas adequados. | **Modelo de Programação Restrito.** |
| **Eficiência Energética:** Altíssimo desempenho por Watt. | **Overhead de Transferência:** Mover dados entre a memória da CPU e da GPU (através do barramento PCIe) é um grande gargalo. |
| **Largura de Banda de Memória:** Possuem memória dedicada de altíssima largura de banda (GDDR/HBM). | **Nicho de Aplicação:** Nem todos os problemas podem ser mapeados eficientemente para o modelo SIMD. |


<img width="1320" height="320" alt="image" src="https://github.com/user-attachments/assets/52961241-63dd-45e5-bf55-059fabdc7b33" />

*O mundo real é híbrido: Um supercomputador moderno é um cluster (memória distribuída) de nós, onde cada nó possui múltiplas CPUs multicore (memória compartilhada) e múltiplos aceleradores GPU (SIMD)*








































