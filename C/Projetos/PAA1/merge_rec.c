#include "recursive_merge_sort.h"
#include <stdlib.h>

void merge(int *array, int left, int mid, int right) {
    int n1 = mid - left + 1;
    int n2 = right - mid;

    int *L = (int *)malloc(n1 * sizeof(int));
    int *R = (int *)malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++) L[i] = array[left + i];
    for (int j = 0; j < n2; j++) R[j] = array[mid + 1 + j];

    int i = 0, j = 0, k = left;
    while (i < n1 && j < n2) {
        if (L[i] <= R[j]) array[k++] = L[i++];
        else array[k++] = R[j++];
    }

    while (i < n1) array[k++] = L[i++];
    while (j < n2) array[k++] = R[j++];

    free(L);
    free(R);
}

void recursive_merge_sort(int *array, int left, int right) {
    if (left < right) {
        int mid = left + (right - left) / 2;
        recursive_merge_sort(array, left, mid);
        recursive_merge_sort(array, mid + 1, right);
        merge(array, left, mid, right);
    }
}
