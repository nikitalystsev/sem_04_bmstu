// Пример 16.03. Использование паттерна “Подписчик-издатель” (C++ CLR).
using namespace System;

delegate void Eventhandler(int a);

public
ref class Manager
{
public:
    event Eventhandler ^ onHandler;

    void Method()
    {
        onHandler(10);
    }
};

public
ref class Watcher
{
public:
    Watcher(Manager ^ manager)
    {
        manager->onHandler += gcnew Eventhandler(this, &Watcher::Handler);
    }

    void Handler(int a)
    {
        Console::WriteLine(L"method Handler!");
    }
};

int main()
{
    Manager ^ manager = gcnew Manager();
    Watcher ^ watcher = gcnew Watcher(manager);

    manager->Method();

    return 0;
}
