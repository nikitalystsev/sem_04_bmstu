// Пример 13.24. Шаблон variant (“безопасный” union).
#include <iostream>
#include <exception>

using namespace std;

class bad_variant_access : public exception
{
public:
    bad_variant_access() : exception("Bad variant access!") {}
};

template <typename... Types>
class Variant
{
private:
    template <typename... Ts>
    union UnionStorage
    {
    };

    template <typename Head>
    union UnionStorage<Head>
    {
    private:
        Head head;

    public:
        UnionStorage() {}
        ~UnionStorage() {}

        void destroy(int index)
        {
            if (index != 0)
                throw bad_variant_access();

            head.Head::~Head();
        }

        template <typename Type>
        int put(const Type &value, size_t index)
        {
            if (!std::is_same_v<Head, Type>)
                throw bad_variant_access();

            new (&head) Type(value);

            return index;
        }

        template <typename Type>
        Type get(int index) const
        {
            if (index != 0 || !std::is_same_v<Head, Type>)
                throw bad_variant_access();

            return *reinterpret_cast<const Type *>(&head);
        }

        int copy(const UnionStorage<Head> &stg, size_t index)
        {
            if (index != 0)
                throw bad_variant_access();

            new (&head) Head(stg.head);

            return index;
        }
    };

    template <typename Head, typename... Tail>
    union UnionStorage<Head, Tail...>
    {
    private:
        Head head;
        UnionStorage<Tail...> tail;

    public:
        UnionStorage() {}
        ~UnionStorage() {}

        void destroy(int index)
        {
            if (index == 0)
                head.Head::~Head();
            else
                tail.destroy(index - 1);
        }

        template <typename Type>
        int put(const Type &value, size_t index = 0)
        {
            if (!std::is_same_v<Head, Type>)
                return tail.put(value, index + 1);

            new (&head) Type(value);

            return index;
        }

        template <typename Type>
        Type get(int index) const
        {
            if (index == 0 && is_same_v<Head, Type>)
                return *reinterpret_cast<const Type *>(&head);

            return tail.get<Type>(index - 1);
        }

        int copy(const UnionStorage<Head, Tail...> &stg, size_t index)
        {
            if (index != 0)
                return tail.copy(stg.tail, index - 1);

            new (&head) Head(stg.head);

            return index;
        }
    };

public:
    Variant() = default;
    Variant(Variant<Types...> &const vr);
    Variant(Variant<Types...> &&vr) noexcept;
    template <typename Type>
    explicit Variant(Type &&value) { which = storage.put(value); }

    ~Variant() { destroy(); }

    Variant &operator=(Variant<Types...> &const vr);
    Variant &operator=(Variant<Types...> &&vr) noexcept;
    template <typename Type>
    Variant &operator=(Type &&value);

    int index() const noexcept { return which; }
    bool valueless_by_exception() const noexcept { return which == -1; }

    template <typename Type>
    Type get() const { return storage.get<Type>(which); }

private:
    int which{-1};
    UnionStorage<Types...> storage;

    void destroy()
    {
        if (which != -1)
            storage.destroy(which);
    }
};

#pragma region Variant methods
template <typename... Types>
Variant<Types...>::Variant(Variant<Types...> &const vr)
{
    which = vr.which;
    storage.copy(vr.storage, vr.which);
}

template <typename... Types>
Variant<Types...>::Variant(Variant &&vr) noexcept
{
    which = vr.which;
    storage = vr.storege;

    vr.which = -1;
}

template <typename... Types>
Variant<Types...> &Variant<Types...>::operator=(Variant<Types...> &const vr)
{
    destroy();

    which = vr.which;
    storage.copy(vr.storage, vr.which);

    return *this;
}

template <typename... Types>
Variant<Types...> &Variant<Types...>::operator=(Variant &&vr) noexcept
{
    destroy();

    which = vr.which;
    storage = vr.storege;

    vr.which = -1;

    return *this;
}

template <typename... Types>
template <typename Type>
Variant<Types...> &Variant<Types...>::operator=(Type &&value)
{
    destroy();
    which = storage.put(value);

    return *this;
}

#pragma endregion

class Object
{
private:
    int num = 10;

public:
    Object() { cout << "Calling the default constructor!" << endl; }
    Object(const Object &obj) { cout << "Calling the copy constructor!" << endl; }
    ~Object() { cout << "Calling the destructor!" << endl; }

    int getNum() { return num; }
};

int main()
{
    try
    {
        Variant<double, Object, int> var(5);

        cout << var.get<int>() << endl;

        var = 7.1;
        cout << var.get<double>() << endl;

        Object obj;

        var = obj;

        cout << var.get<Object>().getNum() << endl;

        Variant<double, Object, int> var2(var);
        var2 = var;
    }
    catch (bad_variant_access &err)
    {
        cout << err.what() << endl;
    }
}