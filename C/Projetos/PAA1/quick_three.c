#include "quicksort_median_of_three.h"

int median_of_three(int *array, int low, int high) {
    int mid = low + (high - low) / 2;
    if (array[low] > array[mid]) {
        int temp = array[low];
        array[low] = array[mid];
        array[mid] = temp;
    }
    if (array[low] > array[high]) {
        int temp = array[low];
        array[low] = array[high];
        array[high] = temp;
    }
    if (array[mid] > array[high]) {
        int temp = array[mid];
        array[mid] = array[high];
        array[high] = temp;
    }
    return mid;
}

void quicksort_median_of_three(int *array, int low, int high) {
    if (low < high) {
        int pi = median_of_three(array, low, high);
        quicksort_median_of_three(array, low, pi - 1);
        quicksort_median_of_three(array, pi + 1, high);
    }
}
