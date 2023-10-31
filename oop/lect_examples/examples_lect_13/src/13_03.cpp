// Пример 13.03. Стратегия (Strategy). Стратегия на шаблоне.
#include <iostream>
#include <memory>
#include <vector>

using namespace std;

class Strategy1
{
public:
    void algorithm() { cout << "Algorithm 1;" << endl; }
};

class Strategy2
{
public:
    void algorithm() { cout << "Algorithm 2;" << endl; }
};

template <typename TStrategy = Strategy1>
class Context
{
private:
    unique_ptr<TStrategy> strategy;

public:
    Context() : strategy(make_unique<TStrategy>()) {}

    void algorithmStrategy() { strategy->algorithm(); }
};

int main()
{
    using Client = Context<Strategy2>;

    shared_ptr<Client> obj = make_shared<Client>();

    obj->algorithmStrategy();
}