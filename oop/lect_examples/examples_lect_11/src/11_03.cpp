// Пример 11.03. Фабричный метод (Factory Method). Шаблонный базовый класс creator.
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
private:
    int count;
    double price;

public:
    ConProd1(int c, double p) : count(c), price(p)
    {
        cout << "Calling the ConProd1 constructor;" << endl;
    }
    ~ConProd1() override { cout << "Calling the ConProd1 destructor;" << endl; }

    void run() override { cout << "Count = " << count << "; Price = " << price << endl; }
};

class ConProd2 // : public Product
{
public:
    ConProd2(int c, double p)
    {
        cout << "Calling the ConProd2 constructor;" << endl;
    }
    virtual ~ConProd2() { cout << "Calling the ConProd2 destructor;" << endl; }
    virtual void run() { cout << "Calling the run method ConProd2;" << endl; }
};

#pragma endregion

template <typename Type>
concept Abstract = is_abstract_v<Type>;

template <typename Type>
concept NotAbstract = !is_abstract_v<Type>;

template <typename Derived, typename Base>
concept Derivative = is_abstract_v<Base> && is_base_of_v<Base, Derived>;

#pragma region Variants of the concept Constructible
#define V_1

#ifdef V_1
template <typename Type, typename... Args>
concept Constructible = requires(Args... args) {
    Type{args...};
};

#elif defined(V_2)
template <typename Type, typename... Args>
concept Constructible = requires {
    Type{declval<Args>()...};
};

#elif defined(V_3)
template <typename Type, typename... Args>
concept Constructible = is_constructible_v<Type, Args...>;

#endif

#pragma endregion

template <Abstract Tbase, typename... Args>
class BaseCreator
{
public:
    virtual ~BaseCreator() = default;

    virtual unique_ptr<Tbase> create(Args &&...args) = 0;
};

template <typename Tbase, typename Tprod, typename... Args>
    requires NotAbstract<Tprod> && Derivative<Tprod, Tbase> && Constructible<Tprod, Args...>
class Creator : public BaseCreator<Tbase, Args...>
{
public:
    unique_ptr<Tbase> create(Args &&...args) override
    {
        return make_unique<Tprod>(forward<Args>(args)...);
    }
};

using BaseCreator_t = BaseCreator<Product, int, double>;

class User
{
public:
    void use(shared_ptr<BaseCreator_t> &cr)
    {
        shared_ptr<Product> ptr = cr->create(1, 100.);

        ptr->run();
    }
};

int main()
{
    shared_ptr<BaseCreator_t> cr = make_shared<Creator<Product, ConProd1, int, double>>();

    unique_ptr<User> us = make_unique<User>();

    us->use(cr);
}