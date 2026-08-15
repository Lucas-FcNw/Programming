# Aula 01 -- Professor Jean teoria e Mario lab

Um processo por padrão é single-thread. Thread é nada mais do que um fluxo de execução de forma independente mas com memória e processamento compartilhado, como um cluster.

Se criarmos muitas threads teremos overhead, em outros termos, teremos problema de eficiência, as threads rodam em núcleos, comum ver 8 núcleos e 16 threads, se criarmos threads excessivas isso irá quebrar sobrecarregar o núcleo.



---


# Criação de Processos


Para identificar processos só usar um **getpid** e para ver o processo pai que criou o filho só usar **getppid**

| Estado | Descrição |
| :--- | :--- |
| **novo** | Sendo Criado |
| **executando** | Instruções estão sendo processadas |
| **bloqueado** | Esperando por um evento tal como E/S (entrada saída de teclado) |


``` mermaid
stateDiagram-v2
    [*] --> Novo: Criação
    Novo --> Pronto: Admissão
    Pronto --> Executando: Escalonamento
    Executando --> Pronto: Interrupção / Quantum
    Executando --> Bloqueado: E/S Solicitada
    Bloqueado --> Pronto: E/S Examinada
    Executando --> Terminado: Término
    Terminado --> [*]
    Executando --> Terminado: Término
    Terminado --> [*]
```
Podemos examinar os processos em execução e visualizar seus estados utilizando o comando ps -a.

Executando ps -la temos uma saída mais completa com várias informações adicionais sobre os processos.



Campos reportados para as várias opções do comando `ps` na Extensão POSIX:XSI

| cabeçalho | opção | significado |
|---|---|---|
| F | -l | flags (octal e aditivo) associados com o processo |
| S | -l | estado do processo |
| UID | -f,-l | ID de usuário do proprietário do processo |
| PID | (todos) | ID do processo |
| PPID | -f,-l | ID do processo pai |
| C | -f,-l | utilização de processador usada para escalonamento |
| PRI | -l | prioridade do processo |
| NI | -l | valor nice |
| ADDR | -l | endereço de memória do processo |
| SZ | -l | tamanho em blocos da imagem do processo |
| WCHAN | -l | evento no qual o processo está esperando |
| TTY | (todos) | terminal que está controlando |
| TIME | (todos) | tempo de execução cumulativo |
| CMD | (todos) | nome do comando (argumentos com a opção -f) |




# **Criação de processos**

Um processo pode ser criado chamando-se **fork**

O processo chamador se torna **pai** e o processo criado é o **filho**

```
#include <stdio.h>
#include <unistd.h>

int main(void) {
  int x;

  x = 0;
  fork();
  x = 1;

printf("Eu sou um processo %ld e meu X é %d\n", (long)getpid(), x);
  return 0;
}
```

Após executar aparecem 2 saídas. 



---
##### ** Fork de pai e filho**
```
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(void) {
   pid_t childpid;

   childpid = fork();
   if (childpid == -1) {
      perror("Failed to fork");
      return 1;
   }

   if (childpid == 0)      /* child code */
      printf("I am child %ld\n", (long)getpid());
   else                    /* parent code */
      printf("I am parent %ld\n", (long)getpid());
   return 0;
}
```
Comportamento do Processo Filho

O processo filho é gerado através do mecanismo de Copy-on-Write (CoW), duplicando o contexto de execução do pai (tabela de descritores de arquivos, espaço de endereçamento virtual e registradores). Ele se torna uma entidade de execução concorrente independente, gerida pelo escalonador de processos do kernel, iniciando sua execução com childpid = 0.
Distinção de Fluxo (Pai vs. Filho)

A separação de contextos ocorre exclusivamente pela assimetria no valor de retorno da syscall fork():

    Processo Pai: Recebe o PID inteiro positivo do filho recém-criado, direcionando o fluxo para o bloco else.

    Processo Filho: Recebe o valor 0, direcionando o fluxo para o bloco condicional.

Em computação paralela baseada em processos POSIX, esta assimetria é o mecanismo fundamental de bifurcação, permitindo que um único fluxo de instruções (single instruction stream) ramifique-se em múltiplos fluxos concorrentes (multi-processing).


---

Obtendo o process ID


```
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(void) {
   pid_t childpid;
   pid_t mypid:

   mypid = getpid();
   childpid = fork();
   if (childpid == -1) {
      perror("Failed to fork");
      return 1;
   }
   
   if (childpid == )          /* child code */
     printf("I am child %ld, ID = %ld\n", (long)getpid(), (long)mypid);
   else                       /* child code */
     printf("I am parent %ld, ID = %ld\n", (long)getpid(), (long)mypid);
   return 0;
}
```

 #include <stdio.h>#include <unistd.h>#include <sys/types.h>int main(void) { pid_t childpid; pid_t mypid: mypid = getpid(); childpid = fork(); if (childpid == -1) { perror("Failed to fork"); return 1; } if (childpid == ) /* child code */ printf("I am child %ld, ID = %ld\n", (long)getpid(), (long)mypid); else /* child code */ printf("I am parent %ld, ID = %ld\n", (long)getpid(), (long)mypid); return 0;}




O que acontece quando o seguinte programa é executado?

Que valor será printado para a variável mypid?
Execução do Programa

O programa realiza a bifurcação do fluxo de execução através da chamada de sistema fork(), gerando um processo filho concorrente. Devido à replicação do espaço de endereçamento virtual (Copy-on-Write), o contexto e o estado das variáveis locais existentes antes do fork() são herdados pelo filho.
Valor Impresso para a Variável mypid

Para ambos os processos (pai e filho), a variável mypid exibirá o PID do processo pai.
Fundamentação de Sistemas

    Atribuição Pré-Fork: A instrução mypid = getpid() é executada exclusivamente pelo processo pai antes da duplicação.

    Herança de Memória: O processo filho nasce com uma cópia idêntica da pilha de execução e do heap do pai no instante exato da bifurcação. Logo, o filho herda o valor de mypid já preenchido com o PID do pai.

    Resultado Prático:

        O pai imprime seu próprio PID em mypid.

        O filho imprime o PID do seu pai em mypid (embora imprima seu próprio PID real na chamada getpid() inserida diretamente no printf).

---
---


## ** Criando uma cadeia de processos**

Abaixo está o código de um programa que cria uma cadeia de n processos, onde n é um argumento de linha de comando.


```
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main (int argc, char *argv[]) {
   pid_t childpid = 0;
   int i, n;
   if (argc != 2){   /* check for valid number of command-line arguments */
      fprintf(stderr, "Usage: %s processes\n", argv[0]);
      return 1;
   }
   n = atoi(argv[1]);
   for (i = 1; i < n; i++)
      if (childpid = fork())
         break;

   fprintf(stderr, "i:%d process ID:%ld parent ID:%ld child ID:%ld\n",
           i, (long)getpid(), (long)getppid(), (long)childpid);
   return 0;
}
```

PARA RODAR
gcc programa.c -o programa && ./programa 40



```
  GNU nano 8.7.1                                                                         programa.c                                                                   
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    pid_t childpid = 0;
    int i, n;

    if (argc != 2) {   /* check for valid number of command-line arguments */
        fprintf(stderr, "Usage: %s processes\n", argv[0]);
        return 1;
    }
    
    n = atoi(argv[1]);

    for (i = 1; i < n; i++) {
        childpid = fork();

        if (childpid < 0) {
            perror("failed to fork");
            return 1;
        }

        if (childpid == 0) {
            break;
        }
    }

    fprintf(stdout, "i:%d process ID:%ld parent ID:%ld child ID:%ld\n",
            i, (long)getpid(), (long)getppid(), (long)childpid);

    return 0;
}

```



 printf é para gravar arquivo F = file

 prints é para string no buffer


 pesquisar sobre o acima e sobre stderr stdout e stdin, tem algo haver com impressoras e não tela




 ---
 ---
 ---
 ---
 # **Monitoramento de processos filhos**


Caso o processo pai encerre sua execução prematuramente enquanto os processos filhos ainda realizam suas tarefas, estes poderão ser finalizados em cascata. Em termos de hierarquia, a terminação abrupta do processo pai acarreta a interrupção da prole.


Sempre que criamos um processo filho através de um fork: **o processo atual vira o pai e o novo é o filho** 


Processos Órfãos e o Processo init (ou systemd)

    Processo Órfão: Ocorre quando o processo pai termina sua execução antes do processo filho.

    Adoção: O processo filho não fica desamparado. O kernel do sistema operacional reatribui o filho ao processo init (ou ao systemd nas distribuições modernas do Linux, cujo PID é geralmente 1).

    Desse momento em diante, o init assume o papel de "pai adotivo" e será responsável por coletar o status de terminação do filho quando ele finalmente encerrar, liberando seus recursos da tabela de processos.

2. Monitoramento e Sincronização com wait()

    A chamada de sistema wait() (e suas variantes como waitpid()) cumpre dois papéis críticos na programação concorrente:

        Sincronização: Faz o processo pai pausar sua execução até que um de seus filhos termine, permitindo uma coordenação ordenada das tarefas.

        Eliminação de Zumbis: Quando um filho morre, ele se torna um processo zumbi (mantendo seu PID e status na tabela do kernel até que o pai os leia). O uso correto de wait() faz a leitura desse status, permitindo que o kernel remova o zumbi definitivamente e evite o esgotamento de PIDs no sistema.




CHAMA DE WAIT()


Neste exemplo o processo pai não espera pelo filho, o que faz com que o **processo init** vire o novo pai.

```
#include <stdio.h>
#include <unistd.h>  
#include <stdlib.h>   


int main() {
  int pid;
  pid = fork();

  // Processo filho
  if (pid == 0) {
    system("ps -ef");
    sleep(10);
    system("ps -ef");
  } else {
    sleep(3);
  }
  return 0;
}
```



   
