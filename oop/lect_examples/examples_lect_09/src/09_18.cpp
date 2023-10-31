// Пример 09.17. Реализация shared_ptr и weak_ptr.
#include <iostream>

using namespace std;

template <typename Type>
class UniquePtr;

template <typename Type>
class SharedPtr;

template <typename Type>
class WeakPtr;

struct Count
{
    long countS{0};
    long countW{0};

    Count(long cS = 1, long cW = 0) noexcept : countS(cS), countW(cW) {}
};

template <typename Type>
class Pointers
{
public:
    long use_count() const noexcept { return rep ? rep->countS : 0; }

    Pointers(const Pointers &) = delete;
    Pointers &operator=(const Pointers &) = delete;

protected:
    Pointers() = default;

    Type *get() const noexcept { return ptr; }
    void set(Type *p, Count *r) noexcept
    {
        ptr = p;
        rep = r;
    }

    void delShared() noexcept;
    void delWeak() noexcept;
    void delCount() noexcept;

    bool _compare(const Pointers &right) const noexcept { return ptr == right.ptr; }
    void _swap(Pointers &right) noexcept
    {
        std::swap(ptr, right.ptr);
        std::swap(rep, right.rep);
    }
    void _copyShared(const Pointers &right) noexcept;
    void _copyWeak(const Pointers &right) noexcept;
    void _move(Pointers &right) noexcept;

private:
    Type *ptr{nullptr};
    Count *rep{nullptr};
};

#pragma region Method Pointers

template <typename Type>
void Pointers<Type>::delShared() noexcept
{
    if (!ptr)
        return;

    (rep->countS)--;

    if (!rep->countS)
    {
        delete ptr;
        ptr = nullptr;
        delCount();
    }
}

template <typename Type>
void Pointers<Type>::delWeak() noexcept
{
    if (rep)
    {
        (rep->countW)--;
        delCount();
    }
}

template <typename Type>
void Pointers<Type>::delCount() noexcept
{
    if (!rep->countS && !rep->countW)
    {
        delete rep;
        rep = nullptr;
    }
}

template <typename Type>
void Pointers<Type>::_copyShared(const Pointers<Type> &right) noexcept
{
    if (right.ptr)
        (right.rep->countS)++;

    ptr = right.ptr;
    rep = right.rep;
}

template <typename Type>
void Pointers<Type>::_copyWeak(const Pointers<Type> &right) noexcept
{
    if (right.rep)
        (right.rep->countW)++;

    ptr = right.ptr;
    rep = right.rep;
}

template <typename Type>
void Pointers<Type>::_move(Pointers<Type> &right) noexcept
{
    ptr = right.ptr;
    rep = right.rep;

    right.ptr = nullptr;
    right.rep = nullptr;
}

#pragma endregion

template <typename Type>
class SharedPtr : public Pointers<Type>
{
public:
    SharedPtr() = default;
    explicit SharedPtr(Type *p);
    constexpr SharedPtr(nullptr_t) noexcept {}
    SharedPtr(const SharedPtr &other) noexcept;
    explicit SharedPtr(const WeakPtr<Type> &other) noexcept;
    SharedPtr(SharedPtr &&right) noexcept;
    SharedPtr(UniquePtr<Type> &&right);
    ~SharedPtr();

    SharedPtr &operator=(const SharedPtr &vright) noexcept;
    SharedPtr &operator=(SharedPtr &&vright) noexcept;
    SharedPtr &operator=(UniquePtr<Type> &&vright);

    Type &operator*() const noexcept { return *this->get(); }
    Type *operator->() const noexcept { return this->get(); }
    explicit operator bool() const noexcept { return this->get() != nullptr; }
    bool unique() const noexcept { return this->use_count() == 1; }

    void swap(SharedPtr<Type> &right) noexcept { this->_swap(right); }
    void reset(Type *p = nullptr) noexcept { (p ? SharedPtr(p) : SharedPtr()).swap(*this); }
};

#pragma region Methods SharedPtr

template <typename Type>
SharedPtr<Type>::SharedPtr(Type *p)
{
    this->set(p, new Count());
}

template <typename Type>
SharedPtr<Type>::SharedPtr(const SharedPtr<Type> &other) noexcept
{
    this->_copyShared(other);
}

template <typename Type>
SharedPtr<Type>::SharedPtr(const WeakPtr<Type> &other) noexcept
{
    this->_copyShared(other);
}

template <typename Type>
SharedPtr<Type>::SharedPtr(SharedPtr<Type> &&right) noexcept
{
    this->_move(right);
}

template <typename Type>
SharedPtr<Type>::SharedPtr(UniquePtr<Type> &&vright)
{
    Type *p = vright.release();

    if (p)
        this->set(p, new Count());
}

template <typename Type>
SharedPtr<Type>::~SharedPtr()
{
    this->delShared();
}

template <typename Type>
SharedPtr<Type> &SharedPtr<Type>::operator=(const SharedPtr<Type> &vright) noexcept
{
    if (this->_compare(vright))
        return *this;

    this->delShared();

    this->_copyShared(vright);

    return *this;
}

template <typename Type>
SharedPtr<Type> &SharedPtr<Type>::operator=(SharedPtr<Type> &&vright) noexcept
{
    if (this->_compare(vright))
        return *this;

    this->delShared();

    this->_move(vright);

    return *this;
}

template <typename Type>
SharedPtr<Type> &SharedPtr<Type>::operator=(UniquePtr<Type> &&vright)
{
    this->delShared();

    Type *p = vright.release();

    this->set(p, p ? new Count() : nullptr);

    return *this;
}

#pragma endregion

template <typename Type>
class WeakPtr : public Pointers<Type>
{
public:
    WeakPtr() = default;
    WeakPtr(const WeakPtr &other) noexcept;
    WeakPtr(const SharedPtr<Type> &other) noexcept;
    WeakPtr(WeakPtr &&other) noexcept;
    ~WeakPtr();

    WeakPtr &operator=(const WeakPtr &vright) noexcept;
    WeakPtr &operator=(const SharedPtr<Type> &vright) noexcept;
    WeakPtr &operator=(WeakPtr &&vright) noexcept;

    void reset() noexcept { WeakPtr().swap(*this); }
    void swap(WeakPtr &other) noexcept { this->_swap(other); }
    bool expired() const noexcept { return this->use_count() == 0; }

    SharedPtr<Type> lock() const noexcept { return SharedPtr<Type>(*this); }
};

#pragma region Methods WeakPtr

template <typename Type>
WeakPtr<Type>::WeakPtr(const WeakPtr<Type> &other) noexcept
{
    this->_copyWeak(other);
}

template <typename Type>
WeakPtr<Type>::WeakPtr(const SharedPtr<Type> &other) noexcept
{
    this->_copyWeak(other);
}

template <typename Type>
WeakPtr<Type>::WeakPtr(WeakPtr<Type> &&other) noexcept
{
    this->_move(other);
}

template <typename Type>
WeakPtr<Type>::~WeakPtr()
{
    this->delWeak();
}

template <typename Type>
WeakPtr<Type> &WeakPtr<Type>::operator=(const WeakPtr<Type> &vright) noexcept
{
    if (this->_compare(vright))
        return *this;

    this->delWeak();
    this->_copyWeak(vright);

    return *this;
}

template <typename Type>
WeakPtr<Type> &WeakPtr<Type>::operator=(const SharedPtr<Type> &vright) noexcept
{

    if (this->_compare(vright))
        return *this;

    this->delWeak();
    this->_copyWeak(vright);

    return *this;
}

template <typename Type>
WeakPtr<Type> &WeakPtr<Type>::operator=(WeakPtr<Type> &&vright) noexcept
{
    if (this->_compare(vright))
        return *this;

    this->delWeak();
    this->_move(vright);

    return *this;
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
    ~A() { cout << "Calling a class A destructor (obj" << key << ");" << endl; }

    void f() { cout << "Method f;" << endl; }
};

int main()
{
    SharedPtr<A> obj1(new A(1));

    obj1->f();

    SharedPtr<A> s1, s2(obj1), s3;

    s2->f();

    cout << s2.use_count() << endl;

    WeakPtr<A> w1 = s2;

    s1 = w1.lock();

    SharedPtr<A> s4(w1);

    cout << s2.use_count() << endl;

    WeakPtr<A> w2;
    {
        SharedPtr<A> obj2(new A(2));
        w2 = obj2;

        if (!w2.expired())
            (w2.lock())->f();
    }
    if (!w2.expired())
        (w2.lock())->f();

    s2.reset();
    s3 = s1;
}
