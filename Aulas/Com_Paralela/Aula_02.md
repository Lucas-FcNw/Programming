# Aula 02 -- Professor Jean: teoria e Mario: lab

---

JEAN


(DO SLIDE **CRISE 3/3**) Pipeline limita o número de execuções simultâneas; tenho 17 pipelines, posso executar até 17 processos simultâneos.

Tem coisa antes disso, anotar em casa



---

# Mário Lab
---

### Monitorando processos filhos

Sempre que criamos um processo filho a partir de um programa através de `fork`, o seguinte ocorre:
**O processo atual se torna o pai.**
**O processo novo é, obviamente, o filho.**


O pai é o **init**, que é o primeiro a iniciar todas as tarefas.
Para verificar os filhos, usa-se o comando **wait()** ou suas variantes.


### Exemplo 1: Chamada wait()


Neste exemplo, o processo pai não espera pelo processo filho, o que resulta no processo **init** vir a se tornar o novo pai.
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

A saída 
```
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 Aug21 pts/0    00:00:00 /script/cinit
root          83       0  0 Aug21 pts/2    00:00:00 /bin/bash --noediting
runner79     288       1  0 Aug21 ?        00:00:00 [gdb] <defunct>
runner79     294       1  0 Aug21 ?        00:00:00 [a.out] <defunct>
runner79     359       1  0 Aug21 ?        00:00:00 [tinit] <defunct>
runner79     360       1  0 Aug21 ?        00:00:00 [a.out] <defunct>
runner79     879       1  0 00:04 ?        00:00:01 [tinit] <defunct>
runner79     880       1  0 00:04 ?        00:00:00 [a.out] <defunct>
runner79    3075       0  0 Aug21 pts/1    00:00:00 /bin/bash --noediting
runner79    3356    3075  0 Aug21 pts/1    00:00:00 sh -c . /nix/runner-envs/env
runner79    3357    3356  0 Aug21 pts/1    00:00:00 /script/tinit ./a.out
runner79    3358    3357  0 Aug21 pts/3    00:00:00 ./a.out
runner79    3362    3358  0 Aug21 pts/3    00:00:00 ./a.out
runner79    3363    3362  0 Aug21 pts/3    00:00:00 sh -c -- ps -ef
runner79    3364    3363  0 Aug21 pts/3    00:00:00 ps -ef
```

```
1. A árvore de execução do seu programa

Olhando para a parte final da lista, vemos a cadeia exata de processos que levou até o comando ps -ef:

    3357 /script/tinit ./a.out (PPID: 3356): É o processo iniciador/ambiente que executou o seu programa principal.

    3358 ./a.out (PPID: 3357): É o seu processo pai (a função main principal). O PPID (Process Parent ID) mostra que ele foi criado pelo processo 3357.

    3362 ./a.out (PPID: 3358): É o seu processo filho, criado pelo fork(). Note que o PPID dele é 3358, confirmando que o pai é o processo acima.

    3363 sh -c -- ps -ef e 3364 ps -ef: São os processos gerados pela chamada da função system("ps -ef") dentro do código do filho.

2. O significado das colunas principais

    UID: O usuário que está executando o processo (neste caso, runner79).

    PID: O identificador único daquele processo.

    PPID: O PID do processo pai (quem criou este processo).

    CMD: O comando ou programa que está rodando.

3. Outros processos e o fenômeno "defunct" (Zumbis)

Se você reparar mais acima na lista, existem vários processos com o nome entre colchetes seguido de <defunct>, como [a.out] <defunct> e [gdb] <defunct>:

    O que são? São os chamados processos zumbis.

    Por que aparecem? Um processo zumbi ocorre quando um processo filho termina a sua execução, mas o seu processo pai ainda não leu o seu código de saída (geralmente usando a função wait() ou waitpid()). O processo já não faz mais nada e não consome CPU, mas o seu registro ainda permanece na tabela de processos do sistema operacional.

    Quem é o pai deles? Note que o PPID de todos esses zumbis é 1 (/script/cinit). Isso acontece porque o processo pai original deles morreu antes de coletá-los, fazendo com que o processo "Init" (PID 1) adotasse esses órfãos e os limpe periodicamente.

No seu código original, o processo pai apenas dava um sleep(3) e encerrava, sem chamar wait() para o filho, o que ilustra bem o comportamento de gerenciamento de processos no Linux!
```


### **Lembrando: não programamos mais para criar software; tudo aqui é programação em nível de sistema.**
Assim, evita-se programar 500 funções; fazem-se menos funções, mas com processos distintos.




# **PIDD é o PAI**

O **wait()** tem 2 variantes extras.
**waitpid()**
**waitid()**

*A chamada de sistema wait() aguarda o término de um dos processos filhos e retorna seu status de término em um buffer (memória temporária).*
Exemplo:

```
#include <sys/types.h>
#include <sys/wait.h>

pid_t wait(int *status);
```

Em caso de sucesso, essa chamada retorna o código do PID encerrado e `-1` se falhar.

A chamada **wait()** suspende a execução de forma indefinida até que um dos filhos seja encerrado. Ele espera por apenas 1, pois é uma função atômica; o primeiro processo que tiver a execução finalizada pela CPU será o que o `wait()` vai mostrar.





### Segundo exemplo
Nele, o código anterior é modificado para que o PIDD (pai) aguarde o fim do filho.

```
#include <stdio.h>
#include <unistd.h> 
#include <stdlib.h>
#include <sys/wait.h>


int main() {
  int pid;
  int status;
  pid = fork();

  // Processo filho
  if (pid == 0) {
    system("ps -ef");
    sleep(10);
    system("ps -ef");
    return 3;  // Status de saída é 3 do processo filho
  } else {
    sleep(3);
    wait(&status);
    printf("No processo pai: status de saída do filho é decimal %d, hexa %0x\n", status, status);
  }
  return 0;
}
```

A saída é:

```
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 00:09 pts/0    00:00:00 /script/cinit
root         112       0  0 00:10 pts/2    00:00:00 /bin/bash --noediting
runner62     374       1  0 00:16 ?        00:00:00 [a.out] <defunct>
runner62     725       1  0 00:23 ?        00:00:00 [tinit] <defunct>
runner62     726       1  0 00:23 ?        00:00:00 [a.out] <defunct>
runner62     894       1  0 00:30 ?        00:00:00 [tinit] <defunct>
runner62     895       1  0 00:30 ?        00:00:00 [a.out] <defunct>
runner62    3280       0  0 01:16 pts/1    00:00:00 /bin/bash --noediting
runner62    3326       1  0 01:16 pts/1    00:00:00 [tinit] <defunct>
runner62    3327       1  0 01:16 ?        00:00:00 [python3] <defunct>
runner62    3412    3280  0 01:23 pts/1    00:00:00 sh -c . /nix/runner-envs/env
runner62    3413    3412  0 01:23 pts/1    00:00:00 /script/tinit ./a.out
runner62    3414    3413  0 01:23 pts/3    00:00:00 ./a.out
runner62    3418    3414  0 01:23 pts/3    00:00:00 ./a.out
runner62    3419    3418  0 01:23 pts/3    00:00:00 sh -c -- ps -ef
runner62    3420    3419  0 01:23 pts/3    00:00:00 ps -ef
UID          PID    PPID  C STIME TTY          TIME CMD
root           1       0  0 00:09 pts/0    00:00:00 /script/cinit
root         112       0  0 00:10 pts/2    00:00:00 /bin/bash --noediting
runner62     374       1  0 00:16 ?        00:00:00 [a.out] <defunct>
runner62     725       1  0 00:23 ?        00:00:00 [tinit] <defunct>
runner62     726       1  0 00:23 ?        00:00:00 [a.out] <defunct>
runner62     894       1  0 00:30 ?        00:00:00 [tinit] <defunct>
runner62     895       1  0 00:30 ?        00:00:00 [a.out] <defunct>
runner62    3280       0  0 01:16 pts/1    00:00:00 /bin/bash --noediting
runner62    3326       1  0 01:16 pts/1    00:00:00 [tinit] <defunct>
runner62    3327       1  0 01:16 ?        00:00:00 [python3] <defunct>
runner62    3412    3280  0 01:23 pts/1    00:00:00 sh -c . /nix/runner-envs/env
runner62    3413    3412  0 01:23 pts/1    00:00:00 /script/tinit ./a.out
runner62    3414    3413  0 01:23 pts/3    00:00:00 ./a.out
runner62    3418    3414  0 01:23 pts/3    00:00:00 ./a.out
runner62    3421    3418  0 01:24 pts/3    00:00:00 sh -c -- ps -ef
runner62    3422    3421  0 01:24 pts/3    00:00:00 ps -ef
No processo pai: status de saída do filho é decimal 768, hexa 300
```

## Explicação

```
### 1. Duas execuções do `ps -ef`

Note que a listagem aparece **duas vezes** na sua tela. Isso acontece porque o seu código do processo filho faz exatamente isso:

- **Primeiro `ps -ef`:** roda imediatamente quando o filho é criado (no início do programa).
- **Segundo `ps -ef`:** roda após o filho passar por `sleep(10)` (10 segundos depois).

### 2. A hierarquia no momento do `ps -ef`

Olhando para a parte final de qualquer uma das listagens, vemos os PIDs da execução atual:

- **`3414` (`./a.out`):** é o **processo pai**.
- **`3418` (`./a.out`):** é o **processo filho** (criado pelo `3414`).
- **`3421` / `3422` (`ps -ef`):** são os comandos chamados pelo filho através da função `system()`.

### 3. O segredo do status: `decimal 768, hexa 300`

A última linha impressa pelo seu código mostra o resultado do `wait()`:

> `No processo pai: status de saída do filho é decimal 768, hexa 300`

- **Por que deu 768?** O seu filho retornou o número **`3`** (`return 3;`). Porém, a função `wait()` não guarda apenas o número puro; ela empacota o valor deslocando-o em 8 bits para a esquerda (multiplicando por 256, ou seja, $3 \times 256 = 768$).
- Em hexadecimal, `300` indica que o byte de status de saída (`3`) está na posição correta do empacotamento.

Para exibir o número **3** limpo na tela, como vimos anteriormente, seria necessário usar a macro `WEXITSTATUS(status)`.
```


**A terminação normal é a seguinte:  
Byte de Ordem Superior (Bits 8 a 15) | Byte de Ordem Inferior (Bits 0 a 7)  
Status de Saída (0 a 255) | 0**

    A chamada de sistema wait() possui a limitação de só poder esperar pela saída do próximo filho.

    Se precisarmos esperar por um filho específico, não é possível usando wait(); porém, é possível usando a chamada de sistema waitpid().


### A chamada *waitpid()*

Ele é mais objetivo, ou seja, aguarda o fim da execução de um processo específico, o qual deve ser especificado. Após o fim, ele retorna o status do buffer.

```
#include <sys/types.h>
#include <sys/wait.h>

pid_t waitpid(pid_t pid, int *status, int options);
```

A chamada acima serve para retornar o processo filho encerrado, em caso de erro virá -1

A chamada interrompe de forma indefinida até o filho especificado(conforme o valor de pid) termine.


# Tem mais para anotar
