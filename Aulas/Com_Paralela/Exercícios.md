## Lista de Exercícios Preparatórios para a Avaliação 1

Computação Paralela

Dr. Jean M. Laine

## Resumo

Esta lista de exercícios foi elaborada com base no conteúdo das Aulas 01 a 04 e dos Laboratórios 01 a 05. O objetivo é fornecer um guia de estudos completo, com questões teóricas e práticas de nível semelhante ao que será cobrado na avaliação. As questões foram projetadas para exigir raciocínio, interpretação e a aplicação dos conceitos aprendidos.

## Sumário


## 1 Tópico 1: Fundamentos e Motivações

## Questão 1 (Conceitual)

Explique, com suas próprias palavras, o que foi o fenômeno conhecido como “O Fim do Almoço Grátis” na indústria de software. Quais foram os três “muros” (barreiras físicas) que levaram a esse ponto de inflexão e como a indústria de hardware respondeu a esse desafio?

> O fim do “almoço grátis” refere-se à mudança em que, no passado,
> aumentar a velocidade do processador era suficiente para melhorar o
> desempenho em geral. Porém, chegamos a um ponto em que estamos muito
> próximos do teto dessa solução.
>
> A partir disso, começaram a buscar o uso de mais núcleos e threads,
> permitindo dividir o trabalho em várias partes e executá-las em paralelo,
> causando ganho de performance. Porém, esse ganho também possui um limite.


## Questão 2 (Raciocínio)

Um colega seu, de outro curso, afirma: “Meu computador tem um processador de 8 núcleos, então ele é 8 vezes mais rápido que um computador antigo de 1 núcleo”. Você, como estudante de Computação Paralela, sabe que essa afirmação é simplista e geralmente incorreta. Elabore uma resposta para seu colega explicando por que um programa serial tradicional não se beneficia do hardware multicore e qual é a principal mudança de paradigma necessária para extrair desempenho de processadores modernos. Use a “Analogia da Cozinha Paralela”para ilustrar sua explicação.

## Questão 3 (Pesquisa)

A Lei de Moore, embora ainda válida em termos de densidade de transistores, não se traduz mais em desempenho de single-thread. Pesquise sobre o conceito de Dark Silicon. O que é, e como ele se relaciona diretamente com o fim da Escala de Dennard e a ascensão das arquiteturas multicore e de aceleradores especializados (como GPUs e TPUs)?

## Questão 4 (Conceitual)

Diferencie os conceitos de Paralelismo e Concorrência. Um programa pode ser concorrente sem ser paralelo? E pode ser paralelo sem ser concorrente? Dê um exemplo prático para ilustrar sua resposta (pense em um sistema com um único núcleo vs. múltiplos núcleos).

## Questão 5 (Raciocínio)

Discuta os dois grandes objetivos da programação paralela: resolver um problema mais rápido (strong scaling) e resolver um problema maior (weak scaling). Para cada um dos cenários abaixo, identifique qual objetivo é o principal:

- 1. Uma empresa de efeitos visuais precisa renderizar o próximo filme da Pixar, que tem o dobro de complexidade do anterior, mas o prazo de entrega continua o mesmo.

- 2. Um jogador de e-sports quer que seu jogo de tiro em primeira pessoa rode com a maior taxa de quadros (FPS) possível para ter o menor tempo de resposta.

## 2 Tópico 2: Arquiteturas e Métricas de Desempenho

## Questão 6 (Cálculo e Análise - Lei de Amdahl)

Você está trabalhando em um sistema de simulação de partículas que leva 500 segundos para executar. Uma análise de desempenho (profiling) revelou a seguinte distribuição de tempo:

-  Carregamento de dados iniciais (serial): 40 segundos

-  Cálculo de interações entre partículas (paralelizável): 450 segundos

-  Consolidação e gravação dos resultados (serial): 10 segundos


Responda:

- 1. Qual a fração paralelizável (F) do programa?

- 2. Qual é o speedup máximo teórico que pode ser alcançado, segundo a Lei de Amdahl?

- 3. Qual o speedup esperado ao executar a simulação em um sistema com 32 núcleos?

## Questão 7 (Conceitual e Comparativa)

Explique a principal diferença filosófica entre a Lei de Amdahl e a Lei de Gustafson-Barsis. Descreva os conceitos de Escalabilidade Forte e Escalabilidade Fraca, associando cada um à lei correspondente e explicando em que tipo de problema cada perspectiva é mais relevante.

## Questão 8 (Classificação e Justificativa)

Com base na Taxonomia de Flynn, classifique as seguintes arquiteturas e justifique sua resposta, descrevendo o fluxo de instruções e dados:

- 1. Um processador Intel Core i9 moderno.

- 2. Uma GPU NVIDIA RTX 4090 executando um shader para renderizar sombras.

- 3. O supercomputador “Frontier”, que é um cluster de nós de computação.

## Questão 9 (Análise de Arquitetura)

Discuta a principal diferença entre sistemas de memória compartilhada (UMA/NUMA) e sistemas de memória distribuída. Compare os dois modelos em termos de:

-  Modelo de programação (como os programadores interagem com a memória).

-  Mecanismo de comunicação entre unidades de processamento.

-  Vantagens e desvantagens em relação à escalabilidade e complexidade de programação.

## Questão 10 (Raciocínio - Arquitetura)

Em uma arquitetura NUMA, um programador descuidado implementou um algoritmo de soma de vetor onde a thread executando no Núcleo 0 processa a metade final do vetor (que está na memória local do Núcleo 1), enquanto a thread no Núcleo 1 processa a metade inicial (que está na memória local do Núcleo 0). Qual será o impacto dessa decisão no desempenho do programa? Justifique sua resposta.

## Questão 11 (Cálculo e Análise - Métricas)

Um programa serial executa em 120 segundos. A tabela abaixo mostra o tempo de execução da sua versão paralela com diferentes números de processadores. Complete a tabela calculando o Speedup e a Eficiência para cada caso. A partir de quantos processadores a adição de mais hardware começa a se tornar ineficiente?

## Questão 12 (Pesquisa)

Explique o que é um protocolo de coerência de cache do tipo snooping (como o MESI). Por que ele é eficaz em sistemas com poucos núcleos, mas não escala bem para sistemas com dezenas ou centenas de núcleos?


|   | Processadores (p) Tempo Paralelo (s) Speedup (S) Eficiência (E) |   |   |
| --- | --- | --- | --- |
| 1 | 120.0 | ? | ? |
| 2 | 65.0 | ? | ? |
| 4 | 35.0 | ? | ? |
| 8 | 20.0 | ? | ? |
| 16 | 15.0 | ? | ? |

## 3 Tópico 3: Processos, IPC e Threads

## Questão 13 (Análise de Código - fork())

Analise o trecho de código C abaixo. Supondo que a chamada ‘fork()‘ nunca falhe, quantas vezes a mensagem ”Computação Paralela”será impressa na tela? Justifique sua resposta desenhando a árvore de processos criada.

```
1 #include <stdio.h>
2 #include <unistd.h>
3
4 int main() {
5 fork();
6 fork();
7 printf("Computação Paralela\n");
8 return 0;
9 }
10
```

*Listing 1: Análise de fork()*

## Questão 14 (Conceitual - Processos vs. Threads)

Descreva as diferenças fundamentais entre um processo e uma thread em um sistema operacional POSIX. Foque sua resposta na forma como eles gerenciam a memória (o que é compartilhado e o que é privado) e no custo computacional associado à criação e troca de contexto de cada um.

## Questão 15 (Programação Prática - IPC com pipe())

Você precisa modificar um programa paralelo que usa fork() para encontrar o menor valor em um grande vetor de inteiros. Cada processo filho analisa uma fatia do vetor e encontra o mínimo local. Descreva, em alto nível (sem precisar escrever o código completo), como você usaria pipes para que o processo pai colete o mínimo local de cada filho e determine o mínimo global. Quantos pipes seriam necessários? Quem escreveria e quem leria em cada pipe?

## Questão 16 (Análise de Problema - Condição de Corrida)

No Guia do Laboratório 04, o primeiro exemplo (‘race condition.c‘) demonstra uma condição de corrida ao incrementar um contador global. Explique detalhadamente por que a operação ‘counter++‘ não é atômica e como isso leva a um resultado final incorreto. Descreva os três passos (leitura, modificação, escrita) e como o escalonador do sistema operacional pode interromper uma thread entre esses passos, causando a inconsistência.

## Questão 17 (Programação Prática - Pthreads e Mutex)

Imagine que você está desenvolvendo um sistema de log concorrente. Múltiplas threads precisam escrever mensagens em um único arquivo de log. O trecho de código abaixo, que representa a função executada por cada thread, é thread-safe? Se não for, identifique a seção crítica e reescreva o código adicionando a sincronização necessária com um pthread mutex t para torná-lo seguro.


```
1 #include <stdio.h>
2 #include <pthread.h>
3
4 // Assuma que ’log_file ’ e ’mutex_log ’ são variáveis globais
5 // FILE* log_file;
6 // pthread_mutex_t mutex_log;
7
8 void* log_message(void* msg_ptr) {
9 char* message = (char*) msg_ptr;
10
11 // ----- INÍCIO DA SEÇÃO CRÍTICA? -----
12 fprintf(log_file , "[Thread %ld] Mensagem: %s\n", pthread_self (), message);
13 fflush(log_file); // Garante que a mensagem seja escrita imediatamente
14 // ----- FIM DA SEÇÃO CRÍTICA? -----
15
16 return NULL;
17 }
18
```

*Listing 2: Função de log (insegura)*

## Questão 18 (Análise de Código - fork())

O que o código a seguir imprime? Analise o fluxo de criação dos processos e o papel do ‘wait(NULL)‘.

```
1 #include <stdio.h>
2 #include <unistd.h>
3 #include <sys/wait.h>
4
5 int main() {
6 for (int i = 0; i < 2; i++) {
7 if (fork() == 0) {
8 printf("[filho] pid %d do pai %d\n", getpid (), getppid ());
9 exit (0);
10 }
11 }
12 for (int i = 0; i < 2; i++) {
13 wait(NULL);
14 }
15 printf("[pai] pid %d terminou\n", getpid ());
16 return 0;
17 }
18
```

*Listing 3: Fluxo de Processos*

## Questão 19 (Raciocínio - Sincronização)

O código da Atividade 3 do Laboratório 04 (‘vector sum fixed.c‘) resolve o problema da condição de corrida fazendo com que cada thread retorne seu resultado parcial para a thread ‘main‘. Compare essa abordagem com a solução que usa um mutex para proteger uma variável global (‘global sum += local sum‘). Qual das duas abordagens você acredita que terá o melhor desempenho? Justifique sua resposta pensando no conceito de contenção de lock.

## Questão 20 (Pesquisa e Conceitual - Deadlock)

Uma condição de corrida não é o único bug que pode ocorrer em programas concorrentes. Um dos mais perigosos é o deadlock. Pesquise sobre as quatro condições de Coffman para a ocorrência de um deadlock. Em seguida, descreva um cenário simples com duas threads e dois mutexes onde um deadlock aconteceria.


## 4 Tópico 4: Tópicos Avançados e de Pesquisa

## Questão 21 (Conceitual - Energia)

As aulas sobre desempenho mencionam a crescente importância da eficiência energética em computação de alto desempenho (HPC). Explique o que é a tecnologia DVFS (Dynamic Voltage and Frequency Scaling) e como ela contribui para a eficiência energética em processadores modernos.

## Questão 22 (Raciocínio - Overhead)

O overhead de paralelização é o “custo” que pagamos para poder executar um programa em paralelo. Liste e descreva pelo menos três fontes diferentes de overhead em um programa paralelo que utiliza Pthreads.

## Questão 23 (Pesquisa - Sincronização)

Mutexes são eficazes, mas podem ser “pesados”. Para situações onde a seção crítica é muito pequena e a contenção é baixa, programadores experientes às vezes usam spinlocks. Pesquise o que é um spinlock, como ele difere de um mutex em termos de implementação (busy-waiting vs. bloqueio no SO) e em que tipo de cenário um spinlock poderia oferecer melhor desempenho.

## Questão 24 (Análise de Problema - False Sharing)

O “falso compartilhamento” é um bug de desempenho sutil e perigoso em sistemas de memória compartilhada. Descreva o que é o falso compartilhamento. Em seguida, imagine um cenário com duas threads, T0 e T1, e um array de inteiros ‘int data[2]‘. Se T0 escreve continuamente em ‘data[0]‘ e T1 escreve continuamente em ‘data[1]‘, como o falso compartilhamento pode degradar severamente o desempenho, mesmo que as threads estejam operando em posições de memória logicamente diferentes? (Dica: pense em como os dados são organizados em linhas de cache).

## Questão 25 (Programação Prática - IPC)

O uso de ‘pipes‘ anônimos para comunicação entre processos, como visto no laboratório, tem uma limitação fundamental: só funciona entre processos com uma relação de ancestralidade (pai/filho). Descreva, em alto nível, qual seria a limitação de usar pipes para um sistema de chat onde processos completamente independentes precisam se comunicar. Que outro mecanismo de IPC (pesquise por “Named Pipes” ou “FIFOs”) poderia resolver este problema no Linux?
