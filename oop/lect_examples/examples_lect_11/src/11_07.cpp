// Пример 11.07. Использование паттерна «фабричный метод» для паттерна Command.
#include <iostream>
#include <functional>
#include <memory>

using namespace std;

class Command;

class BaseCommandCreator
{
public:
    ~BaseCommandCreator() = default;

    virtual shared_ptr<Command> create_command() const = 0;
};

template <typename Tder, typename Tbase = Command>
concept Derived = is_base_of_v<Tbase, Tder>;

template <Derived<Command> Type>
class CommandCreator : public BaseCommandCreator
{
public:
    template <typename... Args>
    CommandCreator(Args... args)
    {
        create_func = [args...]()
        { return make_shared<Type>(args...); };
    }
    ~CommandCreator() = default;

    shared_ptr<Command> create_command() const override
    {
        return create_func();
    }

private:
    function<shared_ptr<Command>()> create_func;
};

#pragma region Member_Function_Pointer
namespace MFP
{
    template <typename T>
    struct is_member_function_pointer_helper : std::false_type
    {
    };

    template <typename T, typename U>
    struct is_member_function_pointer_helper<T U::*> : std::is_function<T>
    {
    };

    template <typename T>
    struct is_member_function_pointer
        : is_member_function_pointer_helper<typename std::remove_cv<T>::type>
    {
    };

    template <typename T>
    inline constexpr bool is_member_function_pointer_v = is_member_function_pointer<T>::value;
}

#pragma endregion

#pragma region Command
class Command
{
public:
    virtual ~Command() = default;

    virtual void execute() = 0;
};

template <typename Reseiver>
    requires is_class_v<Reseiver> && MFP::is_member_function_pointer_v<void (Reseiver::*)()>
class SimpleCommand : public Command
{
    using Action = void (Reseiver::*)();
    using Pair = pair<shared_ptr<Reseiver>, Action>;

private:
    Pair call;

public:
    SimpleCommand(shared_ptr<Reseiver> r, Action a) : call(r, a) {}

    void execute() override { ((*call.first).*call.second)(); }
};

#pragma endregion

class Object
{
public:
    void operation() { cout << "Run method;" << endl; }
};

class Invoker
{
public:
    void run(shared_ptr<Command> com) { com->execute(); }
};

template <typename Type>
using SimpleComCreator = CommandCreator<SimpleCommand<Type>>;

int main()
{
    shared_ptr<Invoker> inv = make_shared<Invoker>();
    shared_ptr<Object> obj = make_shared<Object>();

    shared_ptr<BaseCommandCreator> cr = make_shared<SimpleComCreator<Object>>(obj, &Object::operation);

    shared_ptr<Command> com = cr->create_command();

    inv->run(com);
}
