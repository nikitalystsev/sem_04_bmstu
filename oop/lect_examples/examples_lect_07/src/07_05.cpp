// Пример 07.05. Цикл for с блоком try.

#include <iostream>
#include <exception>

using namespace std;

class ErrorBase : public std::exception
{
public:
    const char *what() const noexcept override
    {
        return "Error in the Base";
    }
};

#pragma region Errors with the array
class ErrorArray : public std::exception
{
public:
    const char *what() const noexcept override
    {
        return "Error in the Array";
    }
};

class ErrorArraySize : public ErrorArray
{
public:
    const char *what() const noexcept override
    {
        return "Array size error";
    }
};

class ErrorArrayIndex : public ErrorArray
{
public:
    const char *what() const noexcept override
    {
        return "Array index error";
    }
};
#pragma endregion

class Base
{
public:
    Base(int size)
    {
        cout << "Contructor Base" << endl;
        if (size < 0)
            throw ErrorBase();
    }
    ~Base()
    {
        cout << "Destructor Base" << endl;
    }
};

class Array : public Base
{
private:
    double *ar;
    int count;

public:
    Array(int n)
    try : Base(n), count(n)
    {
        cout << "Contructor Array" << endl;
        if (this->count <= 0)
            throw ErrorArraySize();

        this->ar = new double[this->count];
    }
    catch (const ErrorBase &err)
    {
        cout << "перехват базы: " << err.what() << endl;
        throw ErrorArray();
    }
    ~Array()
    {
        cout << "Destructor Array" << endl;
        delete[] ar;
    }

    double &operator[](int index)
    {
        if (index < 0 || index >= this->count)
            throw ErrorArrayIndex();

        return this->ar[index];
    }
};

int main()
{
    for (int i = -1; i < 3; i++)
        try
        {
            cout << i + 1 << endl;
            Array ar(i);

            ar[i - 2];
        }
        catch (const ErrorArray &err)
        {
            cout << "массив: " << err.what() << endl;
        }
        catch (const ErrorBase &err)
        {
            cout << "база: " << err.what() << endl;
        }

    return 0;
}
