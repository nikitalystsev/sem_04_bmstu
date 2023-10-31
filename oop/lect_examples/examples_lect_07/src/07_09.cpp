// Пример 07.09. Вызов деструктора в результате прокидывания исключения.
#include <iostream>
#include <exception>

using namespace std;

class A
{
private:
    int count = std::uncaught_exceptions();

public:
    A() = default;
    ~A()
    {
        if (count != std::uncaught_exceptions())
        {
            cout << "Exception -> Destructor!" << endl;
        }
        else
        {
            cout << "Destructor!" << endl;
        }
    }

    void f()
    {
        throw std::runtime_error("Exception in method f!");
    }
};

int main()
{
    try
    {
        A obj;

        obj.f();
    }
    catch (const std::runtime_error &err)
    {
        cout << err.what() << endl;
    }
}