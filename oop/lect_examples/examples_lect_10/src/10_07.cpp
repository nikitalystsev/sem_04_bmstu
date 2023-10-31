// Пример 10.07. Пример итератора (без проверок и обработки исключительных ситуация).
#include <iostream>
#include <memory>
#include <iterator>
#include <initializer_list>

using namespace std;

template <typename Type>
class Iterator;

template <typename Type>
class ConstIterator;

class BaseArray
{
public:
    using size_type = size_t;

    BaseArray(size_t sz = 0) { count = shared_ptr<size_t>(new size_t(sz)); }
    virtual ~BaseArray() = 0;

    size_t size() const noexcept { return bool(count) ? *count : 0; }
    explicit operator bool() const noexcept { return size(); }

protected:
    shared_ptr<size_t> count;
};

BaseArray::~BaseArray() = default;

template <typename Type>
class Array final : public BaseArray
{
public:
    using value_type = Type;
    using iterator = Iterator<Type>;
    using const_iterator = ConstIterator<Type>;

    Array(initializer_list<Type> lt);
    ~Array() override = default;

    iterator begin() const noexcept { return Iterator<Type>(arr, count); }
    iterator end() const noexcept { return Iterator<Type>(arr, count, *count); }

private:
    shared_ptr<Type[]> arr{nullptr};
};

template <typename Type>
class Iterator
{
    friend class Array<Type>;

public:
    using iterator_category = forward_iterator_tag;

    using value_type = Type;
    using difference_type = ptrdiff_t;
    using pointer = Type *;
    using reference = Type &;

public:
    Iterator(const Iterator &it) = default;

    bool operator==(Iterator const &other) const;

    reference operator*();
    const reference operator*() const;
    pointer operator->();
    const pointer operator->() const;
    operator bool() const;

    Iterator &operator++();
    Iterator operator++(int);

private:
    Iterator(const shared_ptr<Type[]> &a, const shared_ptr<size_t> &c, size_t ind = 0)
        : arr(a), count(c), index(ind) {}

private:
    weak_ptr<Type[]> arr;
    weak_ptr<size_t> count;
    size_t index = 0;
};

#pragma region Method Array
template <typename Type>
Array<Type>::Array(initializer_list<Type> lt) : BaseArray(lt.size())
{
    if (!count)
        return;

    arr = make_shared<Type[]>(*count);

    for (size_t i = 0; auto elem : lt)
        arr[i++] = elem;
}

#pragma endregion

#pragma region Methods Iterator
template <typename Type>
bool Iterator<Type>::operator==(Iterator const &other) const
{
    return index == other.index;
}

template <typename Type>
Iterator<Type>::reference Iterator<Type>::operator*()
{
    shared_ptr<Type[]> a(arr);

    return a[index];
}

template <typename Type>
Iterator<Type> &Iterator<Type>::operator++()
{
    shared_ptr<size_t> n(count);
    if (index < *n)
        index++;

    return *this;
}

template <typename Type>
Iterator<Type> Iterator<Type>::operator++(int)
{
    Iterator<Type> it(*this);

    ++(*this);

    return it;
}

#pragma endregion

template <typename Type>
concept Container = requires(Type t) {
    typename Type::value_type;
    typename Type::size_type;
    typename Type::iterator;
    typename Type::const_iterator;

    {
        t.size()
    } noexcept -> same_as<typename Type::size_type>;
    {
        t.end()
    } noexcept -> same_as<typename Type::iterator>;
    {
        t.begin()
    } noexcept -> same_as<typename Type::iterator>;
};

ostream &operator<<(ostream &os, const Container auto &container)
{
    for (auto elem : container)
        cout << elem << " ";

    return os;
}

int main()
{
    Array<int> arr{1, 2, 3, 4, 5};

    cout << "Count = " << distance(arr.begin(), arr.end()) << endl;

    cout << "Array: " << arr << endl;
}