// Пример 13.18. “Статический полиморфизм”.Паттерн CRTP(Curiously Recurring Template Pattern).
#include <iostream>
#include <memory>

using namespace std;

template <typename Implementation>
class Product
{
public:
    virtual ~Product() { cout << "Destructor Product;" << endl; }

    void run() { impl()->method(); }

private:
    Implementation *impl()
    {
        return static_cast<Implementation *>(this);
    }
    void method() { cout << "Method Product;" << endl; }
};

class ConProd1 : public Product<ConProd1>
{
public:
    ~ConProd1() override { cout << "Destructor Conprod1;" << endl; }

private:
    friend class Product<ConProd1>;
    void method() { cout << "Method ConProd1;" << endl; }
};

class ConProd2 : public Product<ConProd2>
{
public:
    ~ConProd2() override { cout << "Destructor Conprod2;" << endl; }
};

int main()
{
    unique_ptr<Product<ConProd1>> prod1 = make_unique<ConProd1>();

    prod1->run();

    unique_ptr<Product<ConProd2>> prod2 = make_unique<ConProd2>();

    prod2->run();
}