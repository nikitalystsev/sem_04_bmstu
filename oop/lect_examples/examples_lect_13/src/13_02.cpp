// Пример 13.02. Стратегия (Strategy).
#include <iostream>
#include <memory>
#include <vector>

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
public:
    virtual void algorithmStrategy(shared_ptr<Strategy> strategy) = 0;
};

class Client1 : public Context
{
public:
    void algorithmStrategy(shared_ptr<Strategy> strategy = make_shared<ConStrategy1>()) override
    {
        strategy->algorithm();
    }
};

int main()
{
    shared_ptr<Context> obj = make_shared<Client1>();
    shared_ptr<Strategy> strategy = make_shared<ConStrategy2>();

    obj->algorithmStrategy(strategy);
}