#include "quicksort_random_pivot.h"
#include <stdlib.h>

int partition_random(int *array, int low, int high) {
    int random = low + rand() % (high - low);
    int temp = array[random];
    array[random] = array[high];
    array[high] = temp;
    return partition(array, low, high);
}

void quicksort_random_pivot(int *array, int low, int high) {
    if (low < high) {
        int pi = partition_random(array, low, high);
        quicksort_random_pivot(array, low, pi - 1);
        quicksort_random_pivot(array, pi + 1, high);
    }
}
