// Пример 13.01. Стратегия (Strategy).
#include <iostream>
#include <memory>

using namespace std;

class Strategy
{
public:
    virtual ~Strategy() = default;

    virtual void algorithm() = 0;
};

class ConStrategy1 : public Strategy
{
public:
    void algorithm() override { cout << "Algorithm 1;" << endl; }
};

class ConStrategy2 : public Strategy
{
public:
    void algorithm() override { cout << "Algorithm 2;" << endl; }
};

class Context
{
protected:
    unique_ptr<Strategy> strategy;

public:
    explicit Context(unique_ptr<Strategy> ptr = make_unique<ConStrategy1>())
        : strategy(move(ptr)) {}
    virtual ~Context() = default;

    virtual void algorithmStrategy() = 0;
};

class Client1 : public Context
{
public:
    using Context::Context;

    void algorithmStrategy() override { strategy->algorithm(); }
};

int main()
{
    shared_ptr<Context> obj = make_shared<Client1>(make_unique<ConStrategy2>());

    obj->algorithmStrategy();
}