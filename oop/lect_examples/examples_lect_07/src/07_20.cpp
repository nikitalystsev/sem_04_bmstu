// Пример 07.20. Перегрузка операторов new, delete.
#include <iostream>

using namespace std;

class A
{
public:
    A() { cout << "Calling the constructor" << endl; }
    ~A() { cout << "Calling the destructor" << endl; }
    void *operator new(size_t size)
    {
        cout << "new A" << endl;
        return ::operator new(size);
    }
    void operator delete(void *ptr)
    {
        cout << "delete A" << endl;
        ::operator delete(ptr);
    }
    void *operator new[](std::size_t size)
    {
        cout << "new[] A" << endl;
        return ::operator new[](size);
    }
    void operator delete[](void *ptr)
    {
        cout << "delete[] A" << endl;
        ::operator delete[](ptr);
    }
};

int main()
{
    A *pa = new A;

    delete pa;

    pa = new A[3];

    delete[] pa;
}
