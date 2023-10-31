// Пример 09.08. Перегрузка шаблонов методов класса.
#include <iostream>

using namespace std;

class A
{
public:
    template <typename Type>
        requires is_floating_point<Type>::value
    A(Type t)
    {
        cout << "Creating float object" << endl;
    }
    template <typename Type>
        requires is_integral<Type>::value
    A(Type t)
    {
        cout << "Creating integer object" << endl;
    }
};

int main()
{
    A obj(1.);
}
