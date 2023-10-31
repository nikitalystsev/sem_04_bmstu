// Пример 11.12. Шаблон одиночка (Singleton).
#include <iostream>
#include <memory>

using namespace std;

template <typename T>
concept NotAbstractClass = is_class_v<T> && !is_abstract_v<T>;

template <typename T>
concept CopyConstructible = requires(T t) {
    T(t);
};

template <typename T>
concept Assignable = requires(T t1, T t2) {
    t1 = t2;
};

template <typename T>
concept OnlyObject = NotAbstractClass<T> && !CopyConstructible<T> && !Assignable<T>;

template <OnlyObject Type>
class Singleton
{
private:
    static unique_ptr<Type> inst;

public:
    template <typename... Args>
    static Type &instance(Args... args)
    {
        struct Proxy : public Type
        {
            Proxy(Args &&...args) : Type(forward<Args>(args)...) {}
        };

        if (!inst)
            inst = make_unique<Proxy>(forward<Args>(args)...);

        return *inst;
    }

    Singleton() = delete;
    Singleton(const Singleton &) = delete;
    Singleton &operator=(const Singleton &) = delete;
};

template <OnlyObject Type>
unique_ptr<Type> Singleton<Type>::inst{};

class Product
{
private:
    int num;
    double data;

protected:
    Product() = default;
    Product(int n, double d) : num(n), data(d)
    {
        cout << "Calling the constructor;" << endl;
    }

public:
    ~Product() { cout << "Calling the destructor;" << endl; }

    void f() { cout << "num = " << num << "; data = " << data << endl; }

    Product(const Product &) = delete;
    Product &operator=(const Product &) = delete;
};

int main()
{
    decltype(auto) d1 = Singleton<Product>::instance(1, 2.);
    decltype(auto) d2 = Singleton<Product>::instance();

    d2.f();
}