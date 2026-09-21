## Lista de Exerc´ıcios Preparat´orios para a Avalia¸c˜ao 1

Computa¸c˜ ao Paralela

Dr. Jean M. Laine

## Resumo

Esta lista de exerc´ıcios foi elaborada com base no conte´udo das Aulas 01 a 04 e dos Laborat´orios 01 a 05. O objetivo ´e fornecer um guia de estudos completo, com quest˜oes te´oricas e pr´aticas de n´ıvel semelhante ao que ser´a cobrado na avalia¸c˜ ao. As quest˜oes foram projetadas para exigir racioc´ınio, interpreta¸c˜ ao e a aplica¸c˜ ao dos conceitos aprendidos.

## Sum´ario


## 1 T´opico 1: Fundamentos e Motiva¸c˜ oes

## Quest˜ao 1 (Conceitual)

Explique, com suas pr´oprias palavras, o que foi o fenˆomeno conhecido como ”O Fim do Almo¸co Gr´atis”na ind´ustria de software. Quais foram os trˆes ”muros”(barreiras f´ısicas) que levaram a esse ponto de inflex˜ao e como a ind´ustria de hardware respondeu a esse desafio?

## Quest˜ao 2 (Racioc´ınio)

Um colega seu, de outro curso, afirma: ”Meu computador tem um processador de 8 n´ucleos, ent˜ ao ele ´e 8 vezes mais r´ apido que um computador antigo de 1 n´ucleo”. Vocˆe, como estudante de Computa¸c˜ ao Paralela, sabe que essa afirma¸c˜ ao ´e simplista e geralmente incorreta. Elabore uma resposta para seu colega explicando por que um programa serial tradicional n˜ao se bene- ficia do hardware multicore e qual ´e a principal mudan¸ca de paradigma necess´aria para extrair desempenho de processadores modernos. Use a ”Analogia da Cozinha Paralela”para ilustrar sua explica¸c˜ ao.

## Quest˜ao 3 (Pesquisa)

A Lei de Moore, embora ainda v´alida em termos de densidade de transistores, n˜ao se traduz mais em desempenho de single-thread. Pesquise sobre o conceito de Dark Silicon. O que ´e, e como ele se relaciona diretamente com o fim da Escala de Dennard e a ascens˜ao das arquiteturas multicore e de aceleradores especializados (como GPUs e TPUs)?

## Quest˜ao 4 (Conceitual)

Diferencie os conceitos de Paralelismo e Concorrˆencia. Um programa pode ser concorrente sem ser paralelo? E pode ser paralelo sem ser concorrente? Dˆe um exemplo pr´atico para ilustrar sua resposta (pense em um sistema com um ´unico n´ucleo vs. m´ultiplos n´ucleos).

## Quest˜ao 5 (Racioc´ınio)

Discuta os dois grandes objetivos da programa¸c˜ ao paralela: resolver um problema mais r´ apido (strong scaling) e resolver um problema maior (weak scaling). Para cada um dos cen´arios abaixo, identifique qual objetivo ´e o principal:

- 1. Uma empresa de efeitos visuais precisa renderizar o pr´oximo filme da Pixar, que tem o dobro de complexidade do anterior, mas o prazo de entrega continua o mesmo.

- 2. Um jogador de e-sports quer que seu jogo de tiro em primeira pessoa rode com a maior taxa de quadros (FPS) poss´ıvel para ter o menor tempo de resposta.

## 2 T´opico 2: Arquiteturas e M´etricas de Desempenho

## Quest˜ao 6 (C´alculo e An´alise - Lei de Amdahl)

Vocˆe est´a trabalhando em um sistema de simula¸c˜ ao de part´ıculas que leva 500 segundos para executar. Uma an´alise de desempenho (profiling) revelou a seguinte distribui¸c˜ ao de tempo:

-  Carregamento de dados iniciais (serial): 40 segundos

-  C´alculo de intera¸c˜ oes entre part´ıculas (paraleliz´avel): 450 segundos

-  Consolida¸c˜ ao e grava¸c˜ ao dos resultados (serial): 10 segundos


Responda:

- 1. Qual a fra¸c˜ ao paraleliz´avel (F) do programa?

- 2. Qual ´e o speedup m´aximo te´orico que pode ser alcan¸cado, segundo a Lei de Amdahl?

- 3. Qual o speedup esperado ao executar a simula¸c˜ ao em um sistema com 32 n´ucleos?

## Quest˜ao 7 (Conceitual e Comparativa)

Explique a principal diferen¸ca filos´ofica entre a Lei de Amdahl e a Lei de Gustafson-Barsis. Descreva os conceitos de Escalabilidade Forte e Escalabilidade Fraca, associando cada um a` lei correspondente e explicando em que tipo de problema cada perspectiva ´e mais relevante.

## Quest˜ao 8 (Classifica¸c˜ao e Justificativa)

Com base na Taxonomia de Flynn, classifique as seguintes arquiteturas e justifique sua resposta, descrevendo o fluxo de instru¸c˜ oes e dados:

- 1. Um processador Intel Core i9 moderno.

- 2. Uma GPU NVIDIA RTX 4090 executando um shader para renderizar sombras.

- 3. O supercomputador ”Frontier”, que ´e um cluster de n´os de computa¸c˜ ao.

## Quest˜ao 9 (An´alise de Arquitetura)

Discuta a principal diferen¸ca entre sistemas de mem´oria compartilhada (UMA/NUMA) e siste- mas de mem´oria distribu´ıda. Compare os dois modelos em termos de:

-  Modelo de programa¸c˜ ao (como os programadores interagem com a mem´oria).

-  Mecanismo de comunica¸c˜ ao entre unidades de processamento.

-  Vantagens e desvantagens em rela¸c˜ ao `a escalabilidade e complexidade de programa¸c˜ ao.

## Quest˜ao 10 (Racioc´ınio - Arquitetura)

Em uma arquitetura NUMA, um programador descuidado implementou um algoritmo de soma de vetor onde a thread executando no N´ucleo 0 processa a metade final do vetor (que est´a na mem´oria local do N´ucleo 1), enquanto a thread no N´ucleo 1 processa a metade inicial (que est´a na mem´oria local do N´ucleo 0). Qual ser´a o impacto dessa decis˜ao no desempenho do programa? Justifique sua resposta.

## Quest˜ao 11 (C´alculo e An´alise - M´etricas)

Um programa serial executa em 120 segundos. A tabela abaixo mostra o tempo de execu¸c˜ ao da sua vers˜ao paralela com diferentes n´umeros de processadores. Complete a tabela calculando o Speedup e a Eficiˆencia para cada caso. A partir de quantos processadores a adi¸c˜ ao de mais hardware come¸ca a se tornar ineficiente?

## Quest˜ao 12 (Pesquisa)

Explique o que ´e um protocolo de coerˆencia de cache do tipo snooping (como o MESI). Por que ele ´e eficaz em sistemas com poucos n´ucleos, mas n˜ao escala bem para sistemas com dezenas ou centenas de n´ucleos?


|   | Processadores (p) Tempo Paralelo (s) Speedup (S) Eficiˆencia (E) |   |   |
| --- | --- | --- | --- |
| 1 | 120.0 | ? | ? |
| 2 | 65.0 | ? | ? |
| 4 | 35.0 | ? | ? |
| 8 | 20.0 | ? | ? |
| 16 | 15.0 | ? | ? |

## 3 T´opico 3: Processos, IPC e Threads

## Quest˜ao 13 (An´alise de C´odigo - fork())

Analise o trecho de c´ odigo C abaixo. Supondo que a chamada ‘fork()‘ nunca falhe, quantas vezes a mensagem ”Computacao Paralela”ser´a impressa na tela? Justifique sua resposta desenhando a ´arvore de processos criada.

```
1 #include <stdio.h>
2 #include <unistd.h>
3
4 int main() {
5 fork();
6 fork();
7 printf("Computacao Paralela\n");
8 return 0;
9 }
10
```

*Listing 1: An´alise de fork()*

## Quest˜ao 14 (Conceitual - Processos vs. Threads)

Descreva as diferen¸cas fundamentais entre um processo e uma thread em um sistema operacional POSIX. Foque sua resposta na forma como eles gerenciam a mem´oria (o que ´e compartilhado e o que ´e privado) e no custo computacional associado `a cria¸c˜ ao e troca de contexto de cada um.

## Quest˜ao 15 (Programa¸c˜ao Pr´atica - IPC com pipe())

Vocˆe precisa modificar um programa paralelo que usa fork() para encontrar o menor valor em um grande vetor de inteiros. Cada processo filho analisa uma fatia do vetor e encontra o m´ınimo local. Descreva, em alto n´ıvel (sem precisar escrever o c´ odigo completo), como vocˆe usaria pipes para que o processo pai colete o m´ınimo local de cada filho e determine o m´ınimo global. Quantos pipes seriam necess´arios? Quem escreveria e quem leria em cada pipe?

## Quest˜ao 16 (An´alise de Problema - Condi¸c˜ao de Corrida)

No Guia do Laborat´orio 04, o primeiro exemplo (‘race condition.c‘) demonstra uma condi¸c˜ ao de corrida ao incrementar um contador global. Explique detalhadamente por que a opera¸c˜ ao ‘counter++‘ n˜ao ´e atˆomica e como isso leva a um resultado final incorreto. Descreva os trˆes pas- sos (leitura, modifica¸c˜ ao, escrita) e como o escalonador do sistema operacional pode interromper uma thread entre esses passos, causando a inconsistˆencia.

## Quest˜ao 17 (Programa¸c˜ao Pr´atica - Pthreads e Mutex)

Imagine que vocˆe est´a desenvolvendo um sistema de log concorrente. M´ultiplas threads precisam escrever mensagens em um ´unico arquivo de log. O trecho de c´ odigo abaixo, que representa a fun¸c˜ao executada por cada thread, ´e thread-safe? Se n˜ao for, identifique a se¸c˜ ao cr´ıtica e reescreva o c´ odigo adicionando a sincroniza¸c˜ ao necess´aria com um pthread mutex t para torn´a-lo seguro.


```
1 #include <stdio.h>
2 #include <pthread.h>
3
4 // Assuma que ’log_file ’ e ’mutex_log ’ sao variaveis globais
5 // FILE* log_file;
6 // pthread_mutex_t mutex_log;
7
8 void* log_message(void* msg_ptr) {
9 char* message = (char*) msg_ptr;
10
11 // ----- INICIO DA SECAO CRITICA? -----
12 fprintf(log_file , "[Thread %ld] Mensagem: %s\n", pthread_self (), message);
13 fflush(log_file); // Garante que a mensagem seja escrita imediatamente
14 // ----- FIM DA SECAO CRITICA? -----
15
16 return NULL;
17 }
18
```

*Listing 2: Fun¸c˜ ao de log (insegura)*

## Quest˜ao 18 (An´alise de C´odigo - fork())

O que o c´ odigo a seguir imprime? Analise o fluxo de cria¸c˜ ao dos processos e o papel do ‘wait(NULL)‘.

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

## Quest˜ao 19 (Racioc´ınio - Sincroniza¸c˜ao)

O c´ odigo da Atividade 3 do Laborat´orio 04 (‘vector sum fixed.c‘) resolve o problema da condi¸c˜ ao de corrida fazendo com que cada thread retorne seu resultado parcial para a thread ‘main‘. Compare essa abordagem com a solu¸c˜ ao que usa um mutex para proteger uma vari´avel glo- bal (‘global sum += local sum‘). Qual das duas abordagens vocˆe acredita que ter´a o melhor desempenho? Justifique sua resposta pensando no conceito de conten¸c˜ao de lock.

## Quest˜ao 20 (Pesquisa e Conceitual - Deadlock)

Uma condi¸c˜ ao de corrida n˜ao ´e o ´unico bug que pode ocorrer em programas concorrentes. Um dos mais perigosos ´e o deadlock. Pesquise sobre as quatro condi¸c˜ oes de Coffman para a ocorrˆencia de um deadlock. Em seguida, descreva um cen´ario simples com duas threads e dois mutexes onde um deadlock aconteceria.


## 4 T´opico 4: T´opicos Avan¸cados e de Pesquisa

## Quest˜ao 21 (Conceitual - Energia)

As aulas sobre desempenho mencionam a crescente importˆancia da eficiˆencia energ´etica em com- puta¸c˜ ao de alto desempenho (HPC). Explique o que ´e a tecnologia DVFS (Dynamic Voltage and Frequency Scaling) e como ela contribui para a eficiˆencia energ´etica em processadores modernos.

## Quest˜ao 22 (Racioc´ınio - Overhead)

O overhead de paraleliza¸c˜ ao ´e o ”custo”que pagamos para poder executar um programa em paralelo. Liste e descreva pelo menos trˆes fontes diferentes de overhead em um programa paralelo que utiliza Pthreads.

## Quest˜ao 23 (Pesquisa - Sincroniza¸c˜ao)

Mutexes s˜ ao eficazes, mas podem ser ”pesados”. Para situa¸c˜ oes onde a se¸c˜ao cr´ıtica ´e muito pequena e a conten¸c˜ ao ´e baixa, programadores experientes `as vezes usam spinlocks. Pesquise o que ´e um spinlock, como ele difere de um mutex em termos de implementa¸c˜ ao (busy-waiting vs. bloqueio no SO) e em que tipo de cen´ario um spinlock poderia oferecer melhor desempenho.

## Quest˜ao 24 (An´alise de Problema - False Sharing)

O ”falso compartilhamento”´e um bug de desempenho sutil e perigoso em sistemas de mem´oria compartilhada. Descreva o que ´e o falso compartilhamento. Em seguida, imagine um cen´ario com duas threads, T0 e T1, e um array de inteiros ‘int data[2]‘. Se T0 escreve continuamente em ‘data[0]‘ e T1 escreve continuamente em ‘data[1]‘, como o falso compartilhamento pode degradar severamente o desempenho, mesmo que as threads estejam operando em posi¸c˜ oes de mem´oria logicamente diferentes? (Dica: pense em como os dados s˜ ao organizados em linhas de cache).

## Quest˜ao 25 (Programa¸c˜ao Pr´atica - IPC)

O uso de ‘pipes‘ anˆonimos para comunica¸c˜ ao entre processos, como visto no laborat´orio, tem uma limita¸c˜ ao fundamental: s´o funciona entre processos com uma rela¸c˜ ao de ancestralidade (pai/filho). Descreva, em alto n´ıvel, qual seria a limita¸c˜ ao de usar pipes para um sistema de chat onde processos completamente independentes precisam se comunicar. Que outro mecanismo de IPC (pesquise por ”Named Pipes”ou ”FIFOs”) poderia resolver este problema no Linux?
