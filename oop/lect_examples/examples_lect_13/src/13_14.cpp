// Пример 13.14. Опекун (Memento).
#include <iostream>
#include <memory>
#include <list>

using namespace std;

class Memento;

class Caretaker
{
public:
    unique_ptr<Memento> getMemento();
    void setMemento(unique_ptr<Memento> memento);

private:
    list<unique_ptr<Memento>> mementos;
};

class Originator
{
public:
    Originator(int s) : state(s) {}

    const int getState() const { return state; }
    void setState(int s) { state = s; }

    std::unique_ptr<Memento> createMemento() { return make_unique<Memento>(*this); }
    void restoreMemento(std::unique_ptr<Memento> memento);

private:
    int state;
};

class Memento
{
    friend class Originator;

public:
    Memento(Originator o) : originator(o) {}

private:
    void setOriginator(Originator o) { originator = o; }
    Originator getOriginator() { return originator; }

private:
    Originator originator;
};

#pragma region Methods Caretaker
void Caretaker::setMemento(unique_ptr<Memento> memento)
{
    mementos.push_back(move(memento));
}

unique_ptr<Memento> Caretaker::getMemento()
{

    unique_ptr<Memento> last = move(mementos.back());

    mementos.pop_back();

    return last;
}
#pragma endregion

#pragma region Method Originator
void Originator::restoreMemento(std::unique_ptr<Memento> memento)
{
    *this = memento->getOriginator();
}
#pragma endregion

int main()
{
    auto originator = make_unique<Originator>(1);
    auto caretaker = make_unique<Caretaker>();

    cout << "State = " << originator->getState() << endl;
    caretaker->setMemento(originator->createMemento());

    originator->setState(2);
    cout << "State = " << originator->getState() << endl;
    caretaker->setMemento(originator->createMemento());
    originator->setState(3);
    cout << "State = " << originator->getState() << endl;
    caretaker->setMemento(originator->createMemento());

    originator->restoreMemento(caretaker->getMemento());
    cout << "State = " << originator->getState() << endl;
    originator->restoreMemento(caretaker->getMemento());
    cout << "State = " << originator->getState() << std::endl;
    originator->restoreMemento(caretaker->getMemento());
    cout << "State = " << originator->getState() << std::endl;
}