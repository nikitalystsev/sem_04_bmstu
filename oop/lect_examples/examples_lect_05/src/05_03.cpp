// Пример 05.03. Конструкторы копирования и переноса.
#include <iostream>

using namespace std;

class Array
{
private:
    double *arr;
    int count;

public:
    Array() = default;
    Array(int cnt) : count(cnt)
    {
        cout << "создание" << endl;
        arr = new double[count]{};
    }
    Array(const Array &ar);
    Array(Array &&ar) noexcept;
    ~Array();

    bool equals(Array ar);

    static Array minus(const Array &ar);
};

Array::Array(const Array &ar) : count(ar.count)
{
    cout << "копирование" << endl;
    arr = new double[count];

    for (int i = 0; i < count; ++i)
        arr[i] = ar.arr[i];
}

Array::Array(Array &&ar) noexcept : count(ar.count)
{
    cout << "перенос" << endl;
    arr = ar.arr;

    ar.arr = nullptr;
}

Array::~Array()
{
    cout << "деструктор" << endl;
    delete[] arr;
}

bool Array::equals(Array ar)
{
    cout << "сравнение" << endl;
    if (count != ar.count)
        return false;

    int i;
    for (i = 0; i < count && arr[i] == ar.arr[i]; ++i)
        ;

    return i == count;
}

Array Array::minus(const Array &ar)
{
    cout << "минус" << endl;
    Array temp(ar);

    for (int i = 0; i < temp.count; ++i)
        temp.arr[i] *= -1;

    return temp;
}

int main()
{
    Array mas{10};
    // Array mas2 = Array::minus(mas);
    
    if (mas.equals(Array::minus(mas)))
    {
        cout << "true" << endl;
    }
    else
    {
        cout << "false" << endl;
    }
}