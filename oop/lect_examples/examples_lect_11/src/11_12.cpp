// Пример 11.11. Одиночка (Singleton).
#include <iostream>
#include <memory>

using namespace std;

class Product
{
public:
    static shared_ptr<Product> instance()
    {
        class Proxy : public Product
        {
        };

        static shared_ptr<Product> myInstance = make_shared<Proxy>();

        return myInstance;
    }
    ~Product() { cout << "Calling the destructor;" << endl; }

    void f() { cout << "Method f;" << endl; }

    Product(const Product &) = delete;
    Product &operator=(const Product &) = delete;

private:
    Product() { cout << "Calling the default constructor;" << endl; }
};

int main()
{
    shared_ptr<Product> ptr(Product::instance());

    ptr->f();
}