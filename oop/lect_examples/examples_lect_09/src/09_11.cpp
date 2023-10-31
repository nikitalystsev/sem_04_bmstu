// Пример 09.10. Шаблон Holder.
#include <iostream>

using namespace std;

template <typename Type>
class Holder
{
private:
    Type *ptr{nullptr};

public:
    Holder() = default;
    explicit Holder(Type *p) : ptr(p) {}
    Holder(Holder &&other) noexcept
    {
        ptr = other.ptr;
        other.ptr = nullptr;
    }
    ~Holder() { delete ptr; }

    Type *operator->() noexcept { return ptr; }
    Type &operator*() noexcept { return *ptr; }
    operator bool() noexcept { return ptr != nullptr; }

    Type *release() noexcept
    {
        Type *work = ptr;
        ptr = nullptr;

        return work;
    }

    Holder(const Holder &) = delete;
    Holder &operator=(const Holder &) = delete;
};

class A
{
public:
    void f() { cout << "Function f of class A is called" << endl; }
};

int main()
{
    Holder<A> obj(new A{});

    obj->f();
}