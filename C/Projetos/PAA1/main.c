#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "bubble_sort.h"
#include "insertion_sort.h"
#include "selection_sort.h"
#include "recursive_merge_sort.h"
#include "iterative_merge_sort.h"
#include "quicksort_last_pivot.h"
#include "quicksort_random_pivot.h"
#include "quicksort_median_of_three.h"
#include "heapsort.h"

#define ARRAY_SIZE 10000

void fill_array(int *array, int size) {
    for (int i = 0; i < size; i++) {
        array[i] = rand() % 10000;
    }
}

int main() {
    int array[ARRAY_SIZE];
    clock_t start, end;
    double cpu_time_used;

    fill_array(array, ARRAY_SIZE);
    int *copy = malloc(ARRAY_SIZE * sizeof(int));

    // Teste do Bubble Sort
    memcpy(copy, array, ARRAY_SIZE * sizeof(int));
    start = clock();
    bubble_sort(copy, ARRAY_SIZE);
    end = clock();
    cpu_time_used = ((double)(end - start)) / CLOCKS_PER_SEC;
    printf("Bubble Sort Time: %f seconds\n", cpu_time_used);

    // Repita o processo para cada algoritmo de ordenação

    free(copy);
    return 0;
}
