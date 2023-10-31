// Пример 08.01. Шаблоны функций.
#include <iostream>

using namespace std;

template <typename Type>
Type *initArray(int count);

template <typename Type>
void freeArray(Type *arr);

template <typename Type>
Type *inputArray(Type *arr, int cnt);

template <typename Type>
void outputArray(Type *arr, int cnt);

template <typename Type>
using Tfunc = int (*)(const Type &, const Type &);

template <typename Type>
void sort(Type *arr, int cnt, Tfunc<Type> cmp);

int compare(const double &d1, const double &d2)
{
    return d1 - d2;
}

void main()
{
    const int N = 10;
    double *arr = initArray<double>(N);

    cout << "Enter array: ";
    inputArray(arr, N);

    sort(arr, N, compare);

    cout << "Resulting array: ";
    outputArray(arr, N);

    freeArray(arr);
}

template <typename Type>
Type *initArray(int count)
{
    return new Type[count];
}

template <typename Type>
void freeArray(Type *arr)
{
    delete[] arr;
}

template <typename Type>
Type *inputArray(Type *arr, int cnt)
{
    for (int i = 0; i < cnt; i++)
        cin >> arr[i];

    return arr;
}

template <typename Type>
void outputArray(Type *arr, int cnt)
{
    for (int i = 0; i < cnt; i++)
        cout << arr[i] << " ";
    cout << endl;
}

template <typename Type>
void sort(Type *arr, int cnt, Tfunc<Type> cmp)
{
    for (int i = 0; i < cnt - 1; i++)
        for (int j = i + 1; j < cnt; j++)
            if (cmp(arr[i], arr[j]) > 0)
                std::swap(arr[i], arr[j]);
}