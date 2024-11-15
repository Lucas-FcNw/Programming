#include <stdio.h>
#include <stdlib.h>
#include <time.h>

// Prototipos das funções de ordenação
void bubbleSort(int arr[], int n, long *comparisons);
void insertionSort(int arr[], int n, long *comparisons);
void selectionSort(int arr[], int n, long *comparisons);
void mergeSortRec(int arr[], int l, int r, long *comparisons);
void mergeSortIter(int arr[], int n, long *comparisons);
void quickSortLastPivot(int arr[], int low, int high, long *comparisons);
void quickSortRandomPivot(int arr[], int low, int high, long *comparisons);
void heapSort(int arr[], int n, long *comparisons);
void quickSortMedianOfThree(int arr[], int low, int high, long *comparisons);

// Função para copiar a lista
void copyArray(int src[], int dest[], int n)
{
    for (int i = 0; i < n; i++)
    {
        dest[i] = src[i];
    }
}

// Função para medir o tempo de execução e comparações
void runSort(void (*sortFunc)(int[], int, long *), int arr[], int n, const char *sortName)
{
    int *arrCopy = (int *)malloc(n * sizeof(int));
    if (!arrCopy)
    {
        fprintf(stderr, "Erro ao alocar memória.\n");
        return;
    }
    copyArray(arr, arrCopy, n);

    long comparisons = 0;
    clock_t start = clock();

    sortFunc(arrCopy, n, &comparisons);

    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("%s: Tempo de execução: %f segundos, Comparações: %ld\n", sortName, time_taken, comparisons);
    free(arrCopy);
}

// Função para medir o tempo de execução e comparações do quicksort (para pivô específico)
void runQuickSort(void (*sortFunc)(int[], int, int, long *), int arr[], int n, const char *sortName)
{
    int *arrCopy = (int *)malloc(n * sizeof(int));
    if (!arrCopy)
    {
        fprintf(stderr, "Erro ao alocar memória.\n");
        return;
    }
    copyArray(arr, arrCopy, n);

    long comparisons = 0;
    clock_t start = clock();

    sortFunc(arrCopy, 0, n - 1, &comparisons);

    clock_t end = clock();
    double time_taken = ((double)(end - start)) / CLOCKS_PER_SEC;

    printf("%s: Tempo de execução: %f segundos, Comparações: %ld\n", sortName, time_taken, comparisons);
    free(arrCopy);
}

// Função para gerar números aleatórios e salvar no arquivo
void generateRandomData(const char *filename, int n)
{
    FILE *file = fopen(filename, "w");
    if (!file)
    {
        fprintf(stderr, "Erro ao abrir o arquivo.\n");
        return;
    }

    srand(time(NULL));
    for (int i = 0; i < n; i++)
    {
        fprintf(file, "%d\n", rand() % 10000); // Altere o limite conforme desejado
    }

    fclose(file);
}

// Função para carregar dados de um arquivo
int loadData(const char *filename, int arr[], int n)
{
    FILE *file = fopen(filename, "r");
    if (!file)
    {
        fprintf(stderr, "Erro ao abrir o arquivo.\n");
        return 0;
    }

    for (int i = 0; i < n; i++)
    {
        if (fscanf(file, "%d", &arr[i]) != 1)
        {
            fprintf(stderr, "Erro ao ler os dados.\n");
            fclose(file);
            return 0;
        }
    }

    fclose(file);
    return 1;
}

// Implementação dos algoritmos de ordenação
void bubbleSort(int arr[], int n, long *comparisons)
{
    for (int i = 0; i < n - 1; i++)
    {
        for (int j = 0; j < n - i - 1; j++)
        {
            (*comparisons)++;
            if (arr[j] > arr[j + 1])
            {
                int temp = arr[j];
                arr[j] = arr[j + 1];
                arr[j + 1] = temp;
            }
        }
    }
}

void insertionSort(int arr[], int n, long *comparisons)
{
    for (int i = 1; i < n; i++)
    {
        int key = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] > key)
        {
            (*comparisons)++;
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = key;
        if (j >= 0)
            (*comparisons)++; // Comparação final quando o loop é interrompido
    }
}

void selectionSort(int arr[], int n, long *comparisons)
{
    for (int i = 0; i < n - 1; i++)
    {
        int min_idx = i;
        for (int j = i + 1; j < n; j++)
        {
            (*comparisons)++;
            if (arr[j] < arr[min_idx])
            {
                min_idx = j;
            }
        }
        int temp = arr[min_idx];
        arr[min_idx] = arr[i];
        arr[i] = temp;
    }
}

void merge(int arr[], int l, int m, int r, long *comparisons)
{
    int n1 = m - l + 1;
    int n2 = r - m;

    int *L = malloc(n1 * sizeof(int));
    int *R = malloc(n2 * sizeof(int));

    for (int i = 0; i < n1; i++)
        L[i] = arr[l + i];
    for (int j = 0; j < n2; j++)
        R[j] = arr[m + 1 + j];

    int i = 0, j = 0, k = l;

    while (i < n1 && j < n2)
    {
        (*comparisons)++;
        if (L[i] <= R[j])
        {
            arr[k] = L[i];
            i++;
        }
        else
        {
            arr[k] = R[j];
            j++;
        }
        k++;
    }

    while (i < n1)
    {
        arr[k] = L[i];
        i++;
        k++;
    }

    while (j < n2)
    {
        arr[k] = R[j];
        j++;
        k++;
    }

    free(L);
    free(R);
}

void mergeSortRec(int arr[], int l, int r, long *comparisons)
{
    if (l < r)
    {
        int m = l + (r - l) / 2;
        mergeSortRec(arr, l, m, comparisons);
        mergeSortRec(arr, m + 1, r, comparisons);
        merge(arr, l, m, r, comparisons);
    }
}

void mergeSortIter(int arr[], int n, long *comparisons)
{
    for (int curr_size = 1; curr_size <= n - 1; curr_size *= 2)
    {
        for (int left_start = 0; left_start < n - 1; left_start += 2 * curr_size)
        {
            int mid = left_start + curr_size - 1;
            int right_end = (left_start + 2 * curr_size - 1 < n - 1) ? left_start + 2 * curr_size - 1 : n - 1;
            merge(arr, left_start, mid, right_end, comparisons);
        }
    }
}

// Implementação do Quicksort com pivô sendo o último elemento
int partitionLast(int arr[], int low, int high, long *comparisons)
{
    int pivot = arr[high];
    int i = (low - 1);

    for (int j = low; j < high; j++)
    {
        (*comparisons)++;
        if (arr[j] <= pivot)
        {
            i++;
            int temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }
    int temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return (i + 1);
}

void quickSortLastPivot(int arr[], int low, int high, long *comparisons)
{
    if (low < high)
    {
        int pi = partitionLast(arr, low, high, comparisons);
        quickSortLastPivot(arr, low, pi - 1, comparisons);
        quickSortLastPivot(arr, pi + 1, high, comparisons);
    }
}

// Implementação do Quicksort com pivô aleatório
int partitionRandom(int arr[], int low, int high, long *comparisons)
{
    int random_pivot = low + rand() % (high - low);
    int temp = arr[random_pivot];
    arr[random_pivot] = arr[high];
    arr[high] = temp;

    return partitionLast(arr, low, high, comparisons);
}

void quickSortRandomPivot(int arr[], int low, int high, long *comparisons)
{
    if (low < high)
    {
        int pi = partitionRandom(arr, low, high, comparisons);
        quickSortRandomPivot(arr, low, pi - 1, comparisons);
        quickSortRandomPivot(arr, pi + 1, high, comparisons);
    }
}

// Função auxiliar para o Heapsort
void heapify(int arr[], int n, int i, long *comparisons)
{
    int largest = i;
    int left = 2 * i + 1;
    int right = 2 * i + 2;

    if (left < n && arr[left] > arr[largest])
    {
        largest = left;
        (*comparisons)++;
    }

    if (right < n && arr[right] > arr[largest])
    {
        largest = right;
        (*comparisons)++;
    }

    if (largest != i)
    {
        int temp = arr[i];
        arr[i] = arr[largest];
        arr[largest] = temp;
        heapify(arr, n, largest, comparisons);
    }
}

// Implementação do Heapsort
void heapSort(int arr[], int n, long *comparisons)
{
    for (int i = n / 2 - 1; i >= 0; i--)
    {
        heapify(arr, n, i, comparisons);
    }

    for (int i = n - 1; i > 0; i--)
    {
        int temp = arr[0];
        arr[0] = arr[i];
        arr[i] = temp;
        heapify(arr, i, 0, comparisons);
    }
}

// Função auxiliar para encontrar a mediana de três
int medianOfThree(int arr[], int low, int mid, int high)
{
    if ((arr[low] > arr[mid]) != (arr[low] > arr[high]))
        return low;
    else if ((arr[mid] > arr[low]) != (arr[mid] > arr[high]))
        return mid;
    else
        return high;
}

// Função auxiliar para o Quicksort com mediana de três
int partitionMedianOfThree(int arr[], int low, int high, long *comparisons)
{
    int mid = low + (high - low) / 2;
    int medianIndex = medianOfThree(arr, low, mid, high);
    int pivot = arr[medianIndex];
    int temp = arr[medianIndex];
    arr[medianIndex] = arr[high];
    arr[high] = temp;

    int i = low - 1;

    for (int j = low; j <= high - 1; j++)
    {
        if (arr[j] <= pivot)
        {
            i++;
            temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
            (*comparisons)++;
        }
    }
    temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;
    return (i + 1);
}

// Implementação do Quicksort com mediana de três
void quickSortMedianOfThree(int arr[], int low, int high, long *comparisons)
{
    if (low < high)
    {
        int pi = partitionMedianOfThree(arr, low, high, comparisons);
        quickSortMedianOfThree(arr, low, pi - 1, comparisons);
        quickSortMedianOfThree(arr, pi + 1, high, comparisons);
    }
}

int main()
{
    const int sizes[] = {10000, 30000, 50000, 80000, 100000, 300000, 500000, 800000, 1000000, 1100000, 1300000, 1500000, 1800000, 2000000};
    int num_sizes = sizeof(sizes) / sizeof(sizes[0]);

    for (int i = 0; i < num_sizes; i++)
    {
        char filename[100];
        snprintf(filename, sizeof(filename), "data_%d.txt", sizes[i]);

        generateRandomData(filename, sizes[i]);

        int *arr = (int *)malloc(sizes[i] * sizeof(int));
        if (!arr)
        {
            fprintf(stderr, "Erro ao alocar memória para a lista.\n");
            continue;
        }

        if (!loadData(filename, arr, sizes[i]))
        {
            free(arr);
            continue;
        }

        printf("\nTamanho: %d\n", sizes[i]);
        runSort(bubbleSort, arr, sizes[i], "Bubble Sort");
        runSort(insertionSort, arr, sizes[i], "Insertion Sort");
        runSort(selectionSort, arr, sizes[i], "Selection Sort");
        runSort(mergeSortIter, arr, sizes[i], "Mergesort Iterativo");
        runSort((void (*)(int[], int, long *))mergeSortRec, arr, sizes[i], "Mergesort Recursivo");
        runQuickSort(quickSortLastPivot, arr, sizes[i], "Quicksort com pivô último elemento");
        runQuickSort(quickSortRandomPivot, arr, sizes[i], "Quicksort com pivô aleatório");
        runSort(heapSort, arr, sizes[i], "Heapsort");
        runQuickSort(quickSortMedianOfThree, arr, sizes[i], "Quicksort com pivô mediana de três");

        free(arr);
    }

    return 0;
}
