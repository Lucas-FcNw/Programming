#include "iterative_merge_sort.h"
#include <stdlib.h>

void merge(int *array, int left, int mid, int right);

void iterative_merge_sort(int *array, int size) {
    for (int width = 1; width < size; width = 2 * width) {
        for (int i = 0; i < size; i = i + 2 * width) {
            int mid = i + width - 1;
            int right = i + 2 * width - 1 < size ? i + 2 * width - 1 : size - 1;
            if (mid < right) merge(array, i, mid, right);
        }
    }
}
