// Пример 11.02. Фабричный метод (Factory Method). Шаблонный creator.
#include <iostream>
#include <memory>

using namespace std;

class Product;

template <typename Type>
concept NotAbstract = !is_abstract_v<Type>;

template <NotAbstract Tprod>
    requires derived_from<Tprod, Product>
class Creator
{
public:
    unique_ptr<Product> createProduct()
    {
        return make_unique<Tprod>();
    }
};

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

class User
{
public:
    template <NotAbstract Tprod>
    void use(shared_ptr<Creator<Tprod>> cr);
};

template <NotAbstract Tprod>
void User::use(shared_ptr<Creator<Tprod>> cr)
{
    shared_ptr<Product> ptr = cr->createProduct();

    ptr->run();
}

int main()
{
    shared_ptr<Creator<ConProd1>> cr(new Creator<ConProd1>());

    unique_ptr<User> us = make_unique<User>();

    us->use(cr);
}