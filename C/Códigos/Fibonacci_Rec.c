#include <stdio.h>
#include <time.h>

int fibonacci_recursivo(int n) {
  if (n == 0 || n == 1) {
    return n;
  } else {
    return fibonacci_recursivo(n - 1) + fibonacci_recursivo(n - 2);
  }
}

int main() {
  int n;
  clock_t inicio, fim;
  double tempo_execucao;

  printf("Digite o n-ésimo número de Fibonacci: ");
  scanf("%d", &n);

  inicio = clock();

  int resultado = fibonacci_recursivo(n);

  fim = clock();
  tempo_execucao = (double)(fim - inicio) / CLOCKS_PER_SEC;

  printf("O n-ésimo número de Fibonacci é: %d\n", resultado);
  printf("Tempo de execução: %lf segundos\n", tempo_execucao);

  return 0;
}
