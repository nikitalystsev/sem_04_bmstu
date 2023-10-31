// Пример 07.18. Перегрузка оператора (). Функтор.
#include <iostream>

using namespace std;

class A
{
public:
    int operator()() const { return 0; }
    int operator()(int i) const { return i; }
    int operator()(int i, int j) const { return i + j; }
};

int main()
{
    A obj;

    cout << obj() << ", " << obj(1) << ", " << obj(1, 2) << endl;
}