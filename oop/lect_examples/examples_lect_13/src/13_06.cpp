// Пример 13.06. Команда (Command). Объект неизвестен.
#include <iostream>
#include <memory>

using namespace std;

template <typename Reseiver>
class Command
{
public:
    virtual ~Command() = default;
    virtual void execute(shared_ptr<Reseiver>) = 0;
};

template <typename Reseiver>
class SimpleCommand : public Command<Reseiver>
{
    using Action = void (Reseiver::*)();

private:
    Action act;

public:
    SimpleCommand(Action a) : act(a) {}

    virtual void execute(shared_ptr<Reseiver> r) override { ((*r).*act)(); }
};

class Object
{
public:
    virtual void run() = 0;
};

class ConObject : public Object
{
public:
    void run() override { cout << "Run method;" << endl; }
};

int main()
{
    shared_ptr<Command<Object>> command = make_shared<SimpleCommand<Object>>(&Object::run);

    shared_ptr<Object> obj = make_shared<ConObject>();

    command->execute(obj);
}