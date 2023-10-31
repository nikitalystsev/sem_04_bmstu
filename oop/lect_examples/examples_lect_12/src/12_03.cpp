// Пример 12.03. Декоратор (Decorator).
#include <iostream>
#include <memory>

using namespace std;

class Component
{
public:
    virtual ~Component() = default;

    virtual void operation() = 0;
};

class ConComponent : public Component
{
public:
    void operation() override { cout << "ConComponent; "; }
};

class Decorator : public Component
{
protected:
    shared_ptr<Component> component;

public:
    Decorator(shared_ptr<Component> comp) : component(comp) {}
};

class ConDecorator : public Decorator
{
public:
    using Decorator::Decorator;

    void operation() override;
};

#pragma region Method
void ConDecorator::operation()
{
    if (component)
    {
        component->operation();

        cout << "ConDecorator; ";
    }
}

#pragma endregion

int main()
{
    shared_ptr<Component> component = make_shared<ConComponent>();
    shared_ptr<Component> decorator1 = make_shared<ConDecorator>(component);

    decorator1->operation();
    cout << endl;

    shared_ptr<Component> decorator2 = make_shared<ConDecorator>(decorator1);

    decorator2->operation();
    cout << endl;
}