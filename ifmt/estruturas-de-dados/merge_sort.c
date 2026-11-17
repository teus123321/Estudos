#include <stdio.h>
#include <stdlib.h>

void printArr(const int a[], int n) {
    for (int i = 0; i < n; i++) printf("%d ", a[i]);
    printf("\n");
}

void merge(int a[], int lo, int mid, int hi) {
    int* tmp = malloc((hi - lo + 1) * sizeof(int));
    int i = lo, j = mid + 1, k = 0;
    while (i <= mid && j <= hi) {
        if (a[i] <= a[j]) tmp[k++] = a[i++];
        else tmp[k++] = a[j++];
    }
    while (i <= mid) tmp[k++] = a[i++];
    while (j <= hi) tmp[k++] = a[j++];
    for (k = 0; k <= hi - lo; k++) a[lo + k] = tmp[k];
    free(tmp);
}

void mergeSort(int a[], int lo, int hi) {
    if (lo >= hi) return;
    int mid = lo + (hi - lo) / 2;
    mergeSort(a, lo, mid);      // sort the left half
    mergeSort(a, mid + 1, hi);  // sort the right half
    merge(a, lo, mid, hi);      // merge the sorted halves
}

int main(void) {
    int data[] = {38, 27, 43, 3, 9, 82, 10};
    int n = sizeof(data) / sizeof(data[0]);
    printf("Before: ");
    printArr(data, n);
    mergeSort(data, 0, n - 1);
    printf("After:  ");
    printArr(data, n);
    return 0;
}
