// Пример 11.01. Фабричный метод(Factory Method).Новый объект.
#include <iostream>
#include <memory>

using namespace std;

#pragma region Product
class Product
{
public:
    virtual ~Product() = default;

    virtual void run() = 0;
};

class ConProd1 : public Product
{
public:
    ConProd1() { cout << "Calling the ConProd1 constructor;" << endl; }
    ~ConProd1() override { cout << "Calling the ConProd1 destructor;" << endl; }

    void run() override { cout << "Calling the run method;" << endl; }
};

#pragma endregion

class Creator
{
public:
    virtual ~Creator() = default;

    virtual unique_ptr<Product> createProduct() = 0;
};

template <typename Derived, typename Base>
concept Derivative = is_abstract_v<Base> && is_base_of_v<Base, Derived>;

template <Derivative<Product> Tprod>
class ConCreator : public Creator
{
public:
    unique_ptr<Product> createProduct() override
    {
        return unique_ptr<Product>(new Tprod());
    }
};

class User
{
public:
    void use(shared_ptr<Creator> &cr)
    {
        shared_ptr<Product> ptr = cr->createProduct();

        ptr->run();
    }
};

int main()
{
    shared_ptr<Creator> cr = make_shared<ConCreator<ConProd1>>();

    unique_ptr<User> us = make_unique<User>();

    us->use(cr);
}