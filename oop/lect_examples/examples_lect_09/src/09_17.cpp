// Пример 09.16. Реализация хранителя unique_ptr.
#include <iostream>

using namespace std;

template <typename Type>
struct DefaultDelete
{
    DefaultDelete() = default;
    DefaultDelete(const DefaultDelete &) = default;

    void operator()(Type *ptr) const { delete ptr; }
};

template <typename Type, typename Deleter = DefaultDelete<Type>>
class UniquePtr
{
public:
    UniquePtr() = default;
    constexpr UniquePtr(nullptr_t) {}
    explicit UniquePtr(Type *p) noexcept : ptr(p) {}
    UniquePtr(UniquePtr &&vright) noexcept;
    ~UniquePtr() { Deleter{}(ptr); }

    UniquePtr &operator=(nullptr_t) noexcept;
    UniquePtr &operator=(UniquePtr &&vright) noexcept;

    Type &operator*() const noexcept { return *ptr; }
    Type *const operator->() const noexcept { return ptr; }
    Type *get() const noexcept { return ptr; }
    explicit operator bool() const noexcept { return ptr != nullptr; }

    Type *release() noexcept;
    void reset(Type *p = nullptr) noexcept;
    void swap(UniquePtr &other) noexcept;

    UniquePtr(const UniquePtr &) = delete;
    UniquePtr &operator=(const UniquePtr &) = delete;

private:
    Type *ptr{nullptr};
};

#pragma region Method UniquePtr
template <typename Type, typename Deleter>
UniquePtr<Type, Deleter>::UniquePtr(UniquePtr &&vright) noexcept : ptr(vright.release())
{
}

template <typename Type, typename Deleter>
UniquePtr<Type, Deleter> &UniquePtr<Type, Deleter>::operator=(nullptr_t) noexcept
{
    reset();

    return *this;
}

template <typename Type, typename Deleter>
UniquePtr<Type, Deleter> &UniquePtr<Type, Deleter>::operator=(UniquePtr &&vright) noexcept
{
    swap(vright);

    return *this;
}

template <typename Type, typename Deleter>
Type *UniquePtr<Type, Deleter>::release() noexcept
{
    Type *p = ptr;
    ptr = nullptr;

    return p;
}

template <typename Type, typename Deleter>
void UniquePtr<Type, Deleter>::reset(Type *p) noexcept
{
    Deleter{}(ptr);
    ptr = p;
}

template <typename Type, typename Deleter>
void UniquePtr<Type, Deleter>::swap(UniquePtr &other) noexcept
{
    ::swap(ptr, other.ptr);
}

template <typename Type, typename... Args>
UniquePtr<Type> makeUnique(Args &&...params)
{
    return UniquePtr<Type>(new Type(forward<Args>(params)...));
}

namespace Unique
{
    template <typename Type>
    UniquePtr<Type> move(const UniquePtr<Type> &unique)
    {
        return UniquePtr<Type>(const_cast<UniquePtr<Type> &>(unique).release());
    }
}

#pragma endregion

class A
{
    int key;

public:
    A(int k) : key(k)
    {
        cout << "Calling the constructor of class A (obj" << key << ");" << endl;
    }
    ~A()
    {
        cout << "Calling a class A destructor (obj" << key << ");" << endl;
    }

    void f() { cout << "Method f;" << endl; }
};

int main()
{
    UniquePtr<A> obj1(new A(1));
    UniquePtr<A> obj2 = makeUnique<A>(2);
    UniquePtr<A> obj3(obj1.release());

    obj2->f();
    (*obj2).f();

    obj1 = Unique::move(obj3);

    if (!obj3)
    {
        obj2.reset(obj1.release());
        obj2->f();
    }

    obj1.swap(obj2);
}