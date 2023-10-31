// Пример 10.09. Реализация zip и zip итератора.
#include <iostream>
#include <vector>
#include <list>

using namespace std;

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

template <input_iterator KIter, input_iterator VIter>
class ZipIterator
{
private:
    using keys_type = typename iterator_traits<KIter>::value_type;
    using values_type = typename iterator_traits<VIter>::value_type;
    using keys_reference = typename iterator_traits<KIter>::reference;
    using values_reference = typename iterator_traits<VIter>::reference;

    template <typename Reference>
    struct Proxy
    {
        Reference r;
        Reference *operator->() { return &r; }
    };

public:
    using iterator_category = forward_iterator_tag;

    using value_type = pair<keys_type, values_type>;
    using difference_type = ptrdiff_t;
    using reference = pair<keys_reference, values_reference>;
    using pointer = Proxy<reference>;

private:
    KIter kiter;
    VIter viter;

public:
    ZipIterator(KIter kit, VIter vit) : kiter(kit), viter(vit) {}

    ZipIterator &operator++()
    {
        ++kiter;
        ++viter;
        return *this;
    }
    ZipIterator operator++(int)
    {
        ZipIterator temp(kiter, viter);
        ++kiter;
        ++viter;
        return temp;
    }

    pointer operator->() { return pointer{{*kiter, *viter}}; }
    reference operator*() { return {*kiter, *viter}; }

    bool operator==(const ZipIterator &other) const
    {
        return kiter == other.kiter && viter == other.viter;
    }
};

template <Container Keys, Container Values>
    requires requires(Keys k, Values v) { k.size() == v.size(); }
class Zip
{
private:
    using keys_iterator = typename remove_reference_t<Keys>::iterator;
    using values_iterator = typename remove_reference_t<Values>::iterator;
    using keys_const_iterator = typename remove_reference_t<Keys>::const_iterator;
    using values_const_iterator = typename remove_reference_t<Values>::const_iterator;

public:
    using value_type = pair<typename Keys::value_type, typename Values::value_type>;
    using size_type = Keys::size_type;
    using iterator = ZipIterator<keys_iterator, values_iterator>;
    using const_iterator = ZipIterator<keys_const_iterator, values_const_iterator>;

private:
    Keys &keys;
    Values &values;

public:
    Zip(Keys &ks, Values &vs) : keys(ks), values(vs) {}

    iterator begin() noexcept { return iterator(keys.begin(), values.begin()); }
    iterator end() noexcept { return iterator(keys.end(), values.end()); }
    const_iterator begin() const noexcept
    {
        return const_iterator(keys.cbegin(), values.cbegin());
    }
    const_iterator end() const noexcept
    {
        return const_iterator(keys.cend(), values.cend());
    }

    size_type size() const noexcept { return keys.size(); }
};

template <typename First, typename Second>
ostream &operator<<(ostream &os, const pair<First, Second> &pr)
{
    return os << "(" << pr.first << ", " << pr.second << ")";
}

ostream &operator<<(ostream &os, const Container auto &container)
{
    for (auto &&elem : container)
        cout << elem << " ";

    return os;
}

int main()
{
    vector v{1, 2, 3, 4, 5};
    list l{7.2, 1.3, 4.4, 8.1, 5.6};

    Zip zip(v, l);

    cout << "count = " << distance(zip.begin(), zip.end()) << endl;
    cout << "zip: " << zip << endl;
}