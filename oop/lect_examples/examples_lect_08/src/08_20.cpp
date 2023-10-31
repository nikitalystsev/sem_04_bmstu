// Пример 08.19. Шаблон функции с переменным числом параметров.
#include <iostream>

using namespace std;

template <typename Type>
Type sum(Type value)
{
    return value;
}

template <typename Type, typename... Args>
Type sum(Type value, Args... params)
{
    cout << "call two param sum" << endl;
    
    return value + sum(params...);
}

int main()
{
    cout << sum(1, 2, 3, 4, 5) << endl;
}