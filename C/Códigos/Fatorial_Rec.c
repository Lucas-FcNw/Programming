#include <stdio.h>

int fatorial(int n) {
    if (n == 0) {
        return 1;
    } else {
        return n * fatorial(n - 1);
    }
}

int main() {
    int num;
    printf("Digite um número: ");
    scanf("%d", &num);
    printf("Fatorial de %d é %d\n", num, fatorial(num));
    return 0;
}