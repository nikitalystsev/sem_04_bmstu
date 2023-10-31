// Пример 11.14. Прототип (Prototype). «Статический полиморфизм» (CRTP).
#include <iostream>
#include <memory>
#include <concepts>

using namespace std;

struct Base_Obj
{
    virtual ~Base_Obj() = default;

    virtual unique_ptr<Base_Obj> clone() const = 0;
    virtual ostream &print(ostream &os) const = 0;
};

template <typename Type>
concept Abstract = is_abstract_v<Type>;

template <Abstract Base, typename Derived>
struct Clonable : public Base
{
    unique_ptr<Base> clone() const override
    {
        return make_unique<Derived>(static_cast<const Derived &>(*this));
    }
};

class Descendant : public Clonable<Base_Obj, Descendant>
{
private:
    int data;

public:
    Descendant(int d) : data(d) { cout << "Calling the constructor;" << endl; }
    Descendant(const Descendant &obj) : data(obj.data)
    {
        cout << "Calling the Copy constructor;" << endl;
    }
    ~Descendant() override { cout << "Calling the destructor;" << endl; }

    ostream &print(ostream &os) const override
    {
        return os << "data = " << data;
    }
};

// C++23
/*
template <typename Base>
struct Clonable : public Base
{
    template <typename Self>
    unique_ptr<Base> clone(this Selt&& self) const override
    {
        return unique_ptr<Base>(new Self(self));
    }
};

class Descendant : public Clonable<Base_Obj>
{
private:
    int data;

public:
    Descendant(int d) : data(d) {}

    ostream& print(ostream& os) const override
    {
        return os << "data = " << data;

    }
};
*/

ostream &operator<<(ostream &os, const unique_ptr<Base_Obj> &obj)
{
    return obj->print(os);
}

int main()
{
    unique_ptr<Base_Obj> v1 = make_unique<Descendant>(10);
    auto v2 = v1->clone();

    cout << v2 << endl;
}