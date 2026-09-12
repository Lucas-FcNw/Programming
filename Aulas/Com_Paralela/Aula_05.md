# Aula 05; 11.09 Apenas Mário, feriado segunda
---

### Programação de memória compartilhada com Pthreads

Processo é uma instância de um programa que está executando, ou em suspensão.

Threads são análogas à processos "leves"

Ver sobre a ordem, text heap e stack (pilha)

<img width="1037" height="610" alt="image" src="https://github.com/user-attachments/assets/8b8a260f-b93a-456f-83f8-995cbca6cfdf" />

``` 
Explicação passo a passo

    Inclusão das bibliotecas
        stdio.h: funções de entrada e saída, como printf.
        stdlib.h: funções como malloc() e strtol().
        pthread.h: fornece a API POSIX Threads, com tipos e funções para criação e gerenciamento de threads.

    Variável global

    int thread_count;

    Armazena a quantidade de threads que o programa deverá criar. Por ser global, pode ser acessada pelas diferentes threads.

    Função das threads

    void *Hello(void *rank);

    Declara a função que será executada pelas threads. O tipo void * permite receber e retornar um ponteiro genérico, como exigido pela API pthread.

    Declaração no main

    long thread;
    pthread_t *thread_handles;

    thread é utilizado como índice/identificador lógico das threads. Já thread_handles será um vetor de pthread_t, utilizado para armazenar os identificadores das threads criadas.

    Definição da quantidade de threads

    thread_count = strtol(argv[1], NULL, 10);

    argv[1] recebe a quantidade de threads informada pelo usuário na linha de comando. Como argumentos são strings, strtol() converte esse valor para um número inteiro.

    Alocação dinâmica

    thread_handles = malloc(thread_count * sizeof(pthread_t));

    Reserva memória suficiente para armazenar thread_count identificadores do tipo pthread_t. Assim, o programa pode trabalhar com uma quantidade variável de threads em tempo de execução.

```


<img width="1037" height="570" alt="image" src="https://github.com/user-attachments/assets/2071f195-26ac-4344-a4cc-bca6fb495d41" />


```
  Explicação passo a passo

    Criação das threads

    for (thread = 0; thread < thread_count; thread++)
        pthread_create(&thread_handles[thread], NULL,
                       Hello, (void*) thread);

    O for percorre a quantidade de threads definida anteriormente. Para cada iteração, pthread_create() cria uma nova thread.
        &thread_handles[thread]: armazena o identificador da thread.
        NULL: utiliza os atributos padrão.
        Hello: função que a thread executará.
        (void*) thread: passa o índice da thread como argumento.

    Execução da thread principal

    printf("Hello from the main thread\n");

    A thread principal (main) imprime sua mensagem. Como as threads executam concorrentemente, a ordem das mensagens pode variar.

    Sincronização com pthread_join

    for (thread = 0; thread < thread_count; thread++)
        pthread_join(thread_handles[thread], NULL);

    O pthread_join() faz a thread principal esperar cada thread terminar antes de continuar. Isso evita que o programa finalize enquanto ainda existem threads executando.

    Liberação da memória

    free(thread_handles);

    Libera a memória que foi alocada anteriormente com malloc() para armazenar os identificadores das threads.

    Finalização

    return 0;

    Indica que o programa terminou sua execução com sucesso.

Em resumo: o código cria N threads que executam Hello, permite que a thread principal também execute, aguarda todas as threads terminarem com pthread_join(), libera a memória utilizada e finaliza o programa.

```


<img width="1006" height="393" alt="image" src="https://github.com/user-attachments/assets/cee4a876-d9b9-4caf-884d-442353b3ddcd" />


```
Explicação passo a passo

    Definição da função da thread

    void *Hello(void* rank) {

    Define a função que será executada por cada thread. O parâmetro rank recebe o argumento passado pelo pthread_create().

    Identificação da thread

    long my_rank = (long) rank;

    Converte o ponteiro rank de volta para long, recuperando o índice da thread. Assim, cada thread sabe seu próprio identificador (0, 1, 2, ...).

    Impressão da mensagem

    printf("Hello from thread %ld of %d\n", my_rank, thread_count);

    Cada thread imprime seu identificador e o número total de threads. Por exemplo:

    Hello from thread 2 of 4

    Finalização da thread

    return NULL;

    Indica que a função terminou. Como a função retorna void*, NULL é utilizado como valor de retorno.

Em resumo: Hello() é o código executado por cada thread. Ela recebe seu identificador através de rank, converte esse valor para long e imprime qual thread está executando dentre o total criado.

```
## Esses 3 são um código único desmembrado em 3

**OU SEJA**

```
Os três trechos formam um único programa em C utilizando POSIX Threads (pthread). Primeiro, o programa define a quantidade de threads e aloca memória para armazenar seus identificadores. Em seguida, pthread_create() cria as threads, que executam a função Hello() e recebem como argumento seu identificador (rank). Cada thread então informa seu número e o total de threads em execução. Enquanto isso, a thread principal também executa seu código. Por fim, pthread_join() sincroniza a execução, garantindo que todas as threads terminem antes do programa finalizar, e free() libera a memória alocada.

Fluxo:
main → define threads → cria threads → executa Hello() → join() → libera memória → finaliza.
```

 Para passar 2 argumentos para uma função que pode receber apenas 1 se faz:
      -- Usa uma estrutura com parametros e passsa um ponteiro


### *Usa declaração global fora da main para que as threads consigam acessar*


Para executar precissa fazer isso: 
    **gcc −g −Wall −o pth_hello pth_hello . c −lpthread**
Se não usar o LP ele não  liga com a biblioteca




*Inicializando THREADS*
• Processos em MPI são normalmente
inicializados por um script.

• Em Pthreads as threads são incializadas por
um programa executável


### *pthread_t objects*
• Opaco

• Os dados que ele armazena é específico do
sistema.

• Os campos de dados não são acessíveis pelo
código de usuário.

• No entanto, o padrão de Pthreads garante que
um objeto pthread_t object armazena informação
suficiente para idenFficar univocamente a thread
com a qual ela está associada.

### *Função incializada por pthread_create*

• Protótipo:

• void* thread_funcFon ( void* args_p ) ;

• void* pode ser cast para qualquer Fpo de
apontador em C.

• Deste modo, args_p pode apontar para qualquer
lista contendo um ou mais valores necessários à
thread_funcFon.

• Do mesmo modo, o valor de retorno de
thread_funcFon pode apontar para uma lista de um
mais valores



## LAB:

```
TODAS AS THREADS DVEEM EXECUTAR O MESMO CÓDIGO, TEM DE TER TRAVA PARA QUE UMA THREAD EXECUTE POR VEZ
``` 
PARA EM -- MULTIPLICAÇÃO MATRIZ-­‐VETOR
USANDO PTHREADS












