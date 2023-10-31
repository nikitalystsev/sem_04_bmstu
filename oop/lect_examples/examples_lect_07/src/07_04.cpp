// Пример 07.04. Блок try для раздела инициализации конструктора.

#include <iostream>
#include <exception>

using namespace std;

class ErrorArrayAlloc : public std::exception
{
public:
    const char *what() const noexcept override
    {
        return "Errors in allocating memory for an Array!";
    }
};

class Array
{
private:
    double *mas;
    int cnt;

public:
    Array(int q);
    ~Array() { delete[] mas; }
};

Array::Array(int q)
try : mas(new double[q]), cnt(q)
{
}
catch (const std::bad_alloc &exc)
{
    cout << exc.what() << endl;

    throw ErrorArrayAlloc();
}

int main()
{
    try
    {
        Array a(-1);
    }
    catch (const ErrorArrayAlloc &err)
    {
        cout << err.what() << endl;
    }
    catch (const std::bad_alloc &exc)
    {
        cout << exc.what() << endl;
    }

    return 0;
}
