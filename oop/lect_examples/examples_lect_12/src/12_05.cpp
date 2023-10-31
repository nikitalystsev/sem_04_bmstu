// Пример 12.06. Мост (Bridge).
#include <iostream>
#include <memory>

using namespace std;

class Implementor
{
public:
    virtual ~Implementor() = default;

    virtual void operationImp() = 0;
};

class Abstraction
{
protected:
    shared_ptr<Implementor> implementor;

public:
    Abstraction(shared_ptr<Implementor> imp) : implementor(imp) {}
    virtual ~Abstraction() = default;

    virtual void operation() = 0;
};

class ConImplementor : public Implementor
{
public:
    virtual void operationImp() override { cout << "Implementor;" << endl; }
};

class Entity : public Abstraction
{
public:
    using Abstraction::Abstraction;

    virtual void operation() override
    {
        cout << "Entity: ";
        implementor->operationImp();
    }
};

int main()
{
    shared_ptr<Implementor> implementor = make_shared<ConImplementor>();
    shared_ptr<Abstraction> abstraction = make_shared<Entity>(implementor);

    abstraction->operation();
}