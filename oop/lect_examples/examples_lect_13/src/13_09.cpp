// Пример 13.09. Посредник (Mediator).
#include <iostream>
#include <memory>
#include <list>
#include <vector>

using namespace std;

class Message
{
}; // Request

class Mediator;

class Colleague
{
private:
    weak_ptr<Mediator> mediator;

public:
    virtual ~Colleague() = default;

    void setMediator(shared_ptr<Mediator> mdr) { mediator = mdr; }

    virtual bool send(shared_ptr<Message> msg);
    virtual void receive(shared_ptr<Message> msg) = 0;
};

class ColleagueLeft : public Colleague
{
public:
    void receive(shared_ptr<Message> msg) override { cout << "Right - > Left;" << endl; }
};

class ColleagueRight : public Colleague
{
public:
    void receive(shared_ptr<Message> msg) override { cout << "Left - > Right;" << endl; }
};

class Mediator
{
protected:
    list<shared_ptr<Colleague>> colleagues;

public:
    virtual ~Mediator() = default;

    virtual bool send(const Colleague *coleague, shared_ptr<Message> msg) = 0;

    static bool add(shared_ptr<Mediator> mediator, initializer_list<shared_ptr<Colleague>> list);
};

class ConMediator : public Mediator
{
public:
    bool send(const Colleague *coleague, shared_ptr<Message> msg) override;
};

#pragma region Methods Colleague
bool Colleague::send(shared_ptr<Message> msg)
{
    shared_ptr<Mediator> mdr = mediator.lock();

    return mdr ? mdr->send(this, msg) : false;
}
#pragma endregion

#pragma region Methods Mediator
bool Mediator::add(shared_ptr<Mediator> mediator, initializer_list<shared_ptr<Colleague>> list)
{
    if (!mediator || list.size() == 0)
        return false;

    for (auto elem : list)
    {
        mediator->colleagues.push_back(elem);
        elem->setMediator(mediator);
    }

    return true;
}

bool ConMediator::send(const Colleague *colleague, shared_ptr<Message> msg)
{
    bool flag = false;
    for (auto &&elem : colleagues)
    {
        if (dynamic_cast<const ColleagueLeft *>(colleague) && dynamic_cast<ColleagueRight *>(elem.get()))
        {
            elem->receive(msg);
            flag = true;
        }
        else if (dynamic_cast<const ColleagueRight *>(colleague) && dynamic_cast<ColleagueLeft *>(elem.get()))
        {
            elem->receive(msg);
            flag = true;
        }
    }

    return flag;
}
#pragma endregion

int main()
{
    shared_ptr<Mediator> mediator = make_shared<ConMediator>();

    shared_ptr<Colleague> col1 = make_shared<ColleagueLeft>();
    shared_ptr<Colleague> col2 = make_shared<ColleagueRight>();
    shared_ptr<Colleague> col3 = make_shared<ColleagueLeft>();
    shared_ptr<Colleague> col4 = make_shared<ColleagueLeft>();

    Mediator::add(mediator, {col1, col2, col3, col4});

    shared_ptr<Message> msg = make_shared<Message>();

    col1->send(msg);
    col2->send(msg);
}