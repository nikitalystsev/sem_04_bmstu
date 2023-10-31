// Пример 07.06. Метод с условным оператором noexcept.

#include <iostream>
#include <exception>

using namespace std;

class A
{
private:
    A(int d) // noexcept
    {
        if (d < 0)
            throw std::runtime_error("Error!");
    }

public:
    ~A() noexcept(false) // деструктор по умолчанию noexcept(true)
    {
        throw std::runtime_error("Destructor");
    }

    static A create(int v);
};

/*
В статическом методе A::create(int v) используется ключевое слово noexcept(noexcept(A(v))). 
Здесь используется условный оператор noexcept, который проверяет, 
будет ли генерироваться исключение при создании объекта A(v). 
Если создание объекта A(v) не вызывает исключений (т.е. noexcept(A(v)) возвращает true), 
то метод create также помечается как noexcept(true). 
В противном случае (если noexcept(A(v)) возвращает false), метод create будет помечен как noexcept(false).
*/

// условный оператор тут
A A::create(int v) noexcept(noexcept(A(v)))
{
    return A(v);
}

int main()
{
    try
    {
        A obj = A::create(-5);
    }
    catch (const std::runtime_error &err)
    {
        cout << err.what() << endl;
    }

    return 0;
}
