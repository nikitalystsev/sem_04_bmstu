// Пример 11.06. Фабричный метод (Factory Method). «Статический полиморфизм» (CRTP).
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

template <typename Tcrt>
class Creator
{
public:
    auto create() const
    {
        return static_cast<const Tcrt *>(this)->create_impl();
    }
};

template <typename Tprod>
class ProductCreator : public Creator<ProductCreator<Tprod>>
{
public:
    unique_ptr<Product> create_impl() const
    {
        return make_unique<Tprod>();

        //		return unique_ptr<Product>(new Tprod());
    }
};

template <typename Type>
concept Creatable = requires(Type t) {
    t.create();
};

class Work
{
public:
    template <Creatable Type>
    auto create(const Type &crt)
    {
        return crt.create();
    }
};

int main()
{
    Creator<ProductCreator<ConProd1>> cr;

    auto product = Work{}.create(cr);

    product->run();
}