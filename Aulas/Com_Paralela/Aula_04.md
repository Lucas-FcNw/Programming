# Aula 04 -- Professor Jean: teoria e Mario: lab

---

**JEAN**

Usa o arquivo aula 03

Muita coisa para anotar antes

Seja lá o que veio antes a **LEI DE AMDAH** resolve, algo que envolve overhead(sobrecarga), speed-up, como estamos aproveitando os núcleos.


---

### Qual o speed-up máximo que posso ter com um programa?

Essa lei de Amdah responde isso.

#### Analogia:

Lei de Amdahl: A Reforma da Casa
Analogia
Imagine que você está reformando uma casa e contrata uma equipe de trabalhadores:
Tarefas Paralelizáveis: Pintar as paredes, assentar o piso. Pode colocar 10 pintores
trabalhando ao mesmo tempo e a tarefa terminará 10 vezes mais rápido.
Tarefas Seriais: Instalar o único quadro de disjuntores ou a única porta de entrada. Não
importa se tem 1 ou 100 eletricistas, apenas um pode trabalhar no quadro de cada vez.
Essa tarefa é um gargalo inerentemente sequencia


*O tempo total da reforma será sempre limitado pela duração das tarefas sequenciasi que nao podem ser divididos.*


A lei fornece uma fórmula que me permite calcular o maior speed-up possível:

S<sub>p</sub> = 1 / (f + (1 − f) / p)


Sp : Speedup teórico obtido com p processadores/núcleos
f : Fração do código que é inerentemente serial (não paralelizável) - valor entre 0 e 1
(1 − f ): Fração do código que pode ser paralelizada
p: Número de processadores/núcleos
Quanto menor a fração serial f , maior o speedup potencial!


## Exemplo:

Um programa leva 100 segundos para executar num único núcleo. Após análise:
20 segundos são gastos em tarefas seriais (leitura de configuração, inicialização)
80 segundos são de um cálculo que pode ser perfeitamente paralelizado

<img width="1325" height="442" alt="image" src="https://github.com/user-attachments/assets/79ce33a1-7757-460c-ba1a-0474cdf6481b" />




<img width="1463" height="647" alt="image" src="https://github.com/user-attachments/assets/097d2410-a834-4c6b-9dd6-d78b2e9eb9e6" />




---

Usando o exemplo anterior (Tserial = 100s e f = 0, 2):
Calcule o speedup para p = 2, p = 8, p = 32 e p = ∞ &  Complete a tabela:


| p | S(p) | resultado|
|---|------|----------|
| 2 | ?    | **1.666**|
| 8 | ?    | **3.333**|
| 32 | ?   | **4.444**|
| ∞ | ?    | **5.000**|


O ganho aumenta pouco, no caso satura muito rápido, ou seja adicionar mais nucleos corresponde a beneficios menores





