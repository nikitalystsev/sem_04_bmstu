//  Пример 03.03. Перегрузка функций с параметром lvalue и rvalue.
#include <iostream>

using namespace std;

int func(int &ref)
{
    cout << "lvalue - " << ref << endl;
    return ++ref;
}
int func(int &&ref)
{
    cout << "rvalue - " << ref << endl;
    return ++ref;
}

int main()
{
    int i = 0;

    func(i);
    func(move(i));
    func(i + 1);
    func(func(i));

    cout << "i = " << i << endl;
}
