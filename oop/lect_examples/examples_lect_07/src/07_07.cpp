// Пример 07.07. Код небезопасный относительно исключений.
#include <iostream>
#include <exception>

using namespace std;

class A
{
public:
    void operator=(const A &obj)
    {
        throw std::runtime_error("Copy error!");
    }
};

class Array
{
private:
    A *arr;
    int count;

public:
    explicit Array(int cnt)
    try : count(cnt), arr(new A[cnt]{})
    {
    }
    catch (const std::bad_alloc &err)
    {
        throw;
    }
    explicit Array(const Array &a);
    ~Array();
};

Array::~Array()
{
    cout << "Destructor!" << endl;
    delete[] arr;
}

Array::Array(const Array &a) : count(a.count)
{
    arr = new A[count]{};

    for (int i = 0; i < count; ++i)
    {
        cout << "это роняет" << endl;
        arr[i] = a.arr[i];
    }
}

int main()
{
    try
    {
        Array a1(10);
        Array a2{a1};
    }
    catch (const std::runtime_error &err)
    {
        cout << err.what() << endl;
    }
    catch (const std::bad_alloc &err)
    {
        cout << err.what() << endl;
    }

    return 0;
}