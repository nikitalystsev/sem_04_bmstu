// Пример 09.14. Возврат shared_ptr на себя.
#include <iostream>
#include <memory>

using namespace std;

class A : public enable_shared_from_this<A>
{
public:
    A() { cout << "Constructor" << endl; }
    ~A() { cout << "Destructor" << endl; }
    shared_ptr<A> getptr()
    {
        return shared_from_this();
    }
};

int main()
{
    try
    {
        shared_ptr<A> obj1 = make_shared<A>();
        shared_ptr<A> obj2 = obj1->getptr();
        cout << "good1.use_count() = " << obj1.use_count() << endl;

        A obj;
        shared_ptr<A> gp = obj.getptr();
    }
    catch (const bad_weak_ptr &e)
    {
        cout << e.what() << endl;
    }
}