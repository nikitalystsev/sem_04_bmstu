// Пример 13.23. Шаблон any (“безопасный” void) на основе идиомы Type erasure.
#include <iostream>
#include <memory>

using namespace std;

namespace my
{

#pragma region Concepts
    template <typename T>
    struct is_in_place_type : std::false_type
    {
    };

    template <typename T>
    struct is_in_place_type<std::in_place_type_t<T>> : std::true_type
    {
    };

    class any;

    template <typename Type, typename... Args>
    concept Constructible = is_constructible_v<Type, Args...>;

    template <typename Type>
    concept CopyConstructible = is_copy_constructible_v<decay_t<Type>>;

    template <typename Type>
    concept NotAnyCopyConstuctible = CopyConstructible<Type> && !is_same_v<decay_t<Type>, any>;

    template <typename Type>
    concept TypeAnyAble = NotAnyCopyConstuctible<Type> && !is_in_place_type<std::decay_t<Type>>::value;

#pragma endregion

    class any
    {
        template <typename Type>
        friend const Type *any_cast(const any *) noexcept;

        template <typename Type>
        friend Type *any_cast(any *) noexcept;

    public:
        any() = default;
        any(const any &other);
        any(any &&other) noexcept;
        template <TypeAnyAble Type>
        any(Type &&value);
        template <CopyConstructible Type, typename... Args>
        explicit any(in_place_type_t<Type>, Args &&...args)
            requires Constructible<Type, Args...>;

        any &operator=(const any &other);
        any &operator=(any &&other) noexcept;
        template <NotAnyCopyConstuctible Type>
        any &operator=(Type &&value);

        template <CopyConstructible Type, typename... Args>
        decay_t<Type> &emplace(Args &&...args)
            requires Constructible<Type, Args...>;

        bool has_value() const noexcept { return bool(ptr); }
        const type_info &type() const noexcept
        {
            return ptr ? ptr->type() : typeid(void);
        }
        void reset() { ptr.reset(); }
        void swap(any &other) noexcept { ::swap(ptr, other.ptr); }

        template <typename Type>
        operator Type() const;

    private:
        class storage_base;

        unique_ptr<storage_base> ptr;

#pragma region Type erasure
        class storage_base
        {
        public:
            virtual ~storage_base() = default;

            virtual const type_info &type() const noexcept = 0;
            virtual unique_ptr<storage_base> clone() const = 0;
        };

        template <typename Type>
        class storage_impl final : public storage_base
        {
        public:
            template <typename... Args>
            storage_impl(Args &&...args) : value(forward<Args>(args)...) {}

            const type_info &type() const noexcept override { return typeid(Type); }
            unique_ptr<storage_base> clone() const override
            {
                return make_unique<storage_impl<Type>>(value);
            }
            Type get() const { return value; }
            const Type *getptr() const { return &value; }

        private:
            Type value;
        };

#pragma endregion
    };

#pragma region Method
    any::any(const any &other)
    {
        if (other.ptr)
        {
            ptr = other.ptr->clone();
        }
    }

    any::any(any &&other) noexcept : ptr(move(other.ptr)) {}

    template <TypeAnyAble Type>
    any::any(Type &&value)
    {
        emplace<decay_t<Type>>(forward<Type>(value));
    }

    template <CopyConstructible Type, typename... Args>
    any::any(in_place_type_t<Type>, Args &&...args)
        requires Constructible<Type, Args...>
    {
        emplace<decay_t<Type>>(forward<Args>(args)...);
    }

    any &any::operator=(const any &other)
    {
        any(other).swap(*this);

        return *this;
    }

    any &any::operator=(any &&other) noexcept
    {
        any(move(other)).swap(*this);

        return *this;
    }

    template <NotAnyCopyConstuctible Type>
    any &any::operator=(Type &&value)
    {
        any(forward<Type>(value)).swap(*this);

        return *this;
    }

    template <CopyConstructible Type, typename... Args>
    decay_t<Type> &any::emplace(Args &&...args)
        requires Constructible<Type, Args...>
    {
        auto temp = make_unique<storage_impl<Type>>(forward<Args>(args)...);
        auto vl = temp->get();
        ptr = move(temp);

        return vl;
    }

    template <typename Type>
    any::operator Type() const
    {
        storage_impl<Type> &type = dynamic_cast<storage_impl<Type> &>(*ptr);

        return type.get();
    }

#pragma endregion

#pragma region Template functions
    template <CopyConstructible Type, typename... Args>
    any make_any(Args &&...args)
        requires Constructible<Type, Args...>
    {
        return any(in_place_type<Type>, forward<Args>(args)...);
    }

    template <typename Type>
    Type any_cast(const any &thing)
    {
        auto *value = any_cast<Type>(&thing);

        if (!value)
            throw runtime_error("Bad any_cast"); // bad_any_cast();

        return static_cast<Type>(*value);
    }

    template <typename Type>
    const Type *any_cast(const any *other) noexcept
    {
        if (!other)
            return nullptr;

        auto *storage = dynamic_cast<any::storage_impl<Type> *>(other->ptr.get());

        return storage ? storage->getptr() : nullptr;
    }

    template <typename Type>
    Type *any_cast(any *other) noexcept
    {
        return const_cast<Type *>(any_cast<Type>(const_cast<const any *>(other)));
    }

#pragma endregion

}

my::any f()
{
    my::any temp = 7.5;

    return temp;
}

int main()
{
    try
    {
        my::any v1 = 2, v2 = v1, v3 = f(), v4;
        auto v5 = my::make_any<float>(5.5);

        if (v3.has_value())
        {
            cout << v3.type().name() << endl;

            if (v3.type() == typeid(double))
                cout << "v3 = " << double(v3) << endl;
        }

        v4 = f();

        v1.reset();
        int j = 7;
        int &aj = j;
        v1 = j;
        cout << "v1 = " << my::any_cast<int>(v1) << endl;

        cout << "v2 = " << my::any_cast<int>(v2) << endl;
        v2.emplace<float>(5.5f);

        cout << "v2 = " << my::any_cast<float>(v2) << endl;

        int i = v1;
        float d = v2;
        cout << "i = " << i << " f = " << d << endl;
    }
    catch (const std::exception &err)
    {
        cout << err.what() << endl;
    }
}