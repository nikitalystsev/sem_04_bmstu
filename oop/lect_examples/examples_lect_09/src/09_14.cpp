// Пример 09.13. Утечка памяти при использовании shared_ptr.
#include <iostream>
#include <string>
#include <memory>

using namespace std;

class Base
{
protected:
    string name;

public:
    Base(const string &nm) : name(nm) {}

    void print(const string &nm)
    {
        cout << name << " now points to " << nm << endl;
    }
};

class BadWidget : public Base
{
private:
    shared_ptr<BadWidget> otherWidget;

public:
    BadWidget(const string &n) : Base(n)
    {
        cout << "BadWidget " << name << endl;
    }
    ~BadWidget() { cout << "~BadWidget " << name << endl; }

    void setOther(const shared_ptr<BadWidget> &x)
    {
        otherWidget = x;
        print(x->name);
    }
};

class GoodWidget : public Base
{
private:
    weak_ptr<GoodWidget> otherWidget;

public:
    GoodWidget(const string &n) : Base(n)
    {
        cout << "GoodWidget " << name << endl;
    }
    ~GoodWidget() { cout << "~GoodWidget " << name << endl; }

    void setOther(const shared_ptr<GoodWidget> &x)
    {
        otherWidget = x;
        print(x->name);
    }
};

int main()
{
    { // В этом примере происходит утечка памяти
        cout << "Example 1" << endl;
        shared_ptr<BadWidget> w1 = make_shared<BadWidget>("1 First");
        shared_ptr<BadWidget> w2 = make_shared<BadWidget>("1 Second");
        w1->setOther(w2);
        w2->setOther(w1);
    }
    { // А в этом примере использован weak_ptr и утечки памяти не происходит
        cout << "Example 2" << endl;
        shared_ptr<GoodWidget> w1 = make_shared<GoodWidget>("2 First");
        shared_ptr<GoodWidget> w2 = make_shared<GoodWidget>("2 Second");
        w1->setOther(w2);
        w2->setOther(w1);
    }
    return 0;
}