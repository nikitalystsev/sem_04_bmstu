// Пример 13.07. Цепочка обязанностей (Chain of Responsibility).
#include <iostream>
#include <initializer_list>
#include <memory>

using namespace std;

class AbstractHandler
{
    using PtrAbstractHandler = shared_ptr<AbstractHandler>;

protected:
    PtrAbstractHandler next;

    virtual bool run() = 0;

public:
    using Default = shared_ptr<AbstractHandler>;

    virtual ~AbstractHandler() = default;

    virtual bool handle() = 0;

    void add(PtrAbstractHandler node);
    void add(initializer_list<PtrAbstractHandler> list);
};

class ConHandler : public AbstractHandler
{
private:
    bool condition{false};

protected:
    virtual bool run() override
    {
        cout << "Method run;" << endl;
        return true;
    }

public:
    ConHandler() : ConHandler(false) {}
    ConHandler(bool c) : condition(c) { cout << "Constructor;" << endl; }
    ~ConHandler() override { cout << "Destructor;" << endl; }

    bool handle() override
    {
        if (!condition)
            return next ? next->handle() : false;

        return run();
    }
};

#pragma region Methods
void AbstractHandler::add(PtrAbstractHandler node)
{
    if (next)
        next->add(node);
    else
        next = node;
}

void AbstractHandler::add(initializer_list<PtrAbstractHandler> list)
{
    for (auto elem : list)
        add(elem);
}

#pragma endregion

int main()
{
    shared_ptr<AbstractHandler> chain = make_shared<ConHandler>();

    chain->add(
        {make_shared<ConHandler>(false),
         make_shared<ConHandler>(true),
         make_shared<ConHandler>(true)});

    cout << boolalpha << "Result = " << chain->handle() << ";" << endl;
}