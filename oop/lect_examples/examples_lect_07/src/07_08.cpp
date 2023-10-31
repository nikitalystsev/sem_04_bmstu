// Пример 07.08. Обертывание исключения в exception_ptr.
#include <iostream>
#include <exception>

using namespace std;

void do_raise()
{
    throw std::runtime_error("Exception!");
}

exception_ptr get_excption()
{
    try
    {
        do_raise();
    }
    catch (...)
    {
        return current_exception();
    }

    return nullptr;
}

int main()
{
    try
    {
        exception_ptr ex = get_excption();

        rethrow_exception(ex);
    }
    catch (const std::runtime_error &err)
    {
        cout << err.what() << endl;
    }
}
