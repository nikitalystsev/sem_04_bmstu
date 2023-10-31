// Пример 13.25. Шаблон function.
#include <iostream>
#include <memory>

using namespace std;

template <typename TypeUnused>
class Function;

template <typename TypeReturn, typename... Args>
class Function<TypeReturn(Args...)>
{
    class Function_holder_base;
    using invoker_t = unique_ptr<Function_holder_base>;

private:
    invoker_t mInvoker;

public:
    Function() = default;
    Function(const Function &other) : mInvoker(other.mInvoker->clone()) {}
    template <typename TFunction>
    Function(TFunction func)
        : mInvoker(make_unique<Function_holder<TFunction>>(func)) {}
    template <typename TypeFunction, typename TypeClass>
    Function(TypeFunction TypeClass::*method)
        : mInvoker(make_unique<Method_holder<TypeFunction, Args...>>(method)) {}

    Function &operator=(const Function &other)
    {
        mInvoker = other.mInvoker->clone();

        return *this;
    }

    TypeReturn operator()(Args... args) { return mInvoker->invoke(args...); }

private:
    class Function_holder_base
    {
    public:
        virtual ~Function_holder_base() = default;

        virtual TypeReturn invoke(Args... args) = 0;
        virtual invoker_t clone() const = 0;
    };

    template <typename TFunction>
    class Function_holder : public Function_holder_base
    {
        using self_t = Function_holder<TFunction>;

    private:
        TFunction mFunction;

    public:
        Function_holder(TFunction func) : mFunction(func) {}

        TypeReturn invoke(Args... args) override { return mFunction(args...); }
        invoker_t clone() const override
        {
            return invoker_t(make_unique<self_t>(mFunction));
        }
    };

    template <typename TypeFunction, typename TypeClass, typename... RestArgs>
    class Method_holder : public Function_holder_base
    {
        using TMethod = TypeFunction TypeClass::*;

    private:
        TMethod mFunction;

    public:
        Method_holder(TMethod method) : mFunction(method) {}

        TypeReturn invoke(TypeClass obj, RestArgs... restArgs) override
        {
            return (obj.*mFunction)(restArgs...);
        }

        invoker_t clone() const override
        {
            return invoker_t(new Method_holder(mFunction));
        }
    };
};

struct Foo1
{
    double smth(int x) { return x / 2.; }
};

struct Foo2
{
    double smth(int x) { return x / 3.; }
};

class Test
{
    int elem = 5;

public:
    template <typename Tobj>
    double result(Tobj &obj, Function<double(Tobj, int)> func)
    {
        return func(obj, this->elem);
    }
};

int main()
{
    Function<double(Foo1, int)> f1 = &Foo1::smth, f2;

    Foo1 foo;
    f2 = f1;
    cout << "calling member function: " << f2(foo, 5) << endl;

    Test ts;

    cout << "calling member function: " << ts.result(foo, f2) << endl;
}
