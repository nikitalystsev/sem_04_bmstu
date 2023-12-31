// Пример 13.15. Шаблонный метод (Template Method).
#include <iostream>

using namespace std;

class AbstractClass
{
public:
    void templateMethod()
    {
        primitiveOperation();
        concreteOperation();
        hook();
    }
    virtual ~AbstractClass() = default;

protected:
    virtual void primitiveOperation() = 0;
    void concreteOperation() { cout << "concreteOperation;" << endl; }
    virtual void hook() { cout << "hook Base;" << endl; }
};

class ConClassA : public AbstractClass
{
protected:
    void primitiveOperation() override { cout << "primitiveOperation A;" << endl; }
};

class ConClassB : public AbstractClass
{
protected:
    void primitiveOperation() override { cout << "primitiveOperation B;" << endl; }
    void hook() override { cout << "hook B;" << endl; }
};

int main()
{
    ConClassA ca;
    ConClassB cb;

    ca.templateMethod();
    cb.templateMethod();
}