# Aula 06, Jean 14.09 
---

### Lei de Gustafson e Escalabilidade parte 2

Na formula de Amdahl o F é a porcentagem não paralelizavel(sequencial)

Para Gustafson o tempo é fixo, ou seja ele busca o maior problema possível de resolver. Amdahl só quer ver qual o speed-up máximo possível.


Ou seja invés de perguntar ```"Quão mais rapido consigo fazer a mesma tarefa?"``` Gustafson pergunta: ```"Quantas tarefas a mais consigo fazer no mesmo tempo?"```


### A fórmula de Gustafson:

``` S`(p) = p + ( 1 - p )f` ```

*P = número de processadores*   *f`= fração serial no programa paralelo* 



### Demonstrando

1 núcleo = 100 imangens em 10s

10 núcleos = 1000 imagens em 10s 

Repare que o tempo é sempre fixo, a parte serial continua a mesma, mas o trabalho útil aumentou em 10x.



___


EX:


Programa rodando em 1 núcleo:

Tempo total = 100s
Parte serial = 10s
Parte paralelizavel = 90s


Em Amdahl pergunta: Quanto tempo leva com 10 núcleos?

Resolve assim

```
Tpar = serial + (paralelizavel/nucleos)

10 + (90/10)  == 19s

Agora realiza o speed-up:

S = 100/19 == 5,26x
```

### Em Gustafson


QUANTO MAIS PROBLEMA RESOLVO NO MESMO TEMPO?

```
Temp_fixo = seria + (n_paralelo/núcleos)


100 = 10 + (Wpar/10)

100 - 10 = Wpar/10

90 = Wpar/10

Wpar = 90 * 10 = 900s

Agora o speed-up:

Total: 10 + 900 = 910


Speed-up escalado:

S` = 910/1000 == 9,1x
```


**Ou seja nesse caso vale mais a pena usar o Gustafson**



Exercicio:

```
1 Núcleo = 200s

Serial = 40 
Paralelo = 60

A Fração Serial é o quanto em porcentagem o serial corresponde, no caso atual é 20%

Amdahl

Com 5 núcleos em Amdahl

S = 1 / 0.2 + 0.8/5 --> 1/0.36 == 2.78x

Em Gustafson:

200 = 40 + (Wpar/5)

160 = Wpar/5

Wpar = 160 * 5 ==  800s

Agora o *speed-up escalado*


Trabalho total == 800 + serial(40)

S` = 840/ 200 == 4,02x

```
**Sempre que for de tamanho fixo usar Amdahl, se for para problemas que crescem com os recuros usar Gustafson.**









