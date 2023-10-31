// Пример 10.06. Концепты итераторов и реализация distance, advance с их использованием.
#include <iostream>
#include <iterator>
#include <vector>
#include <list>

using namespace std;

template <typename I>
concept Iterator = requires() {
    typename I::value_type;
    typename I::difference_type;
    typename I::pointer;
    typename I::reference;
};

template <typename T, typename U>
concept DerivedFrom = is_base_of<U, T>::value;

#pragma region Input_Iterator
template <typename T>
concept EqualityComparable = requires(T a, T b) {
    {
        a == b
    } -> same_as<bool>;
    {
        a != b
    } -> same_as<bool>;
};

template <typename I>
concept InputIterator = Iterator<I> &&
                        requires { typename I::iterator_category; } &&
                        EqualityComparable<I> &&
                        DerivedFrom<typename I::iterator_category, input_iterator_tag>;

#pragma endregion

#pragma region Forward_Iterator
template <typename I>
concept Incrementable = requires(I it) {
    {
        ++it
    } -> same_as<I &>;
    {
        it++
    } -> same_as<I>;
};

template <typename I>
concept ForwardIterator = InputIterator<I> &&
                          Incrementable<I> &&
                          DerivedFrom<typename I::iterator_category, forward_iterator_tag>;

#pragma endregion

#pragma region Bidirectional_Iterator
template <typename I>
concept Decrementable = requires(I it) {
    {
        --it
    } -> same_as<I &>;
    {
        it--
    } -> same_as<I>;
};

template <typename I>
concept BidirectionalIterator = ForwardIterator<I> &&
                                Decrementable<I> &&
                                DerivedFrom<typename I::iterator_category, bidirectional_iterator_tag>;

#pragma endregion

#pragma region Random_Access_Iterator
template <typename I>
concept RandomAccess = requires(I it, typename I::difference_type n) {
    {
        it + n
    } -> same_as<I>;
    {
        it - n
    } -> same_as<I>;
    {
        it += n
    } -> same_as<I &>;
    {
        it -= n
    } -> same_as<I &>;
    {
        it[n]
    } -> same_as<typename I::reference>;
};

template <typename I>
concept Distance = requires(I it1, I it2) {
    {
        it2 - it1
    } -> convertible_to<typename I::difference_type>;
};

template <typename I>
concept RandomAccessIterator = BidirectionalIterator<I> &&
                               RandomAccess<I> && Distance<I> &&
                               DerivedFrom<typename I::iterator_category, random_access_iterator_tag>;

#pragma endregion

namespace my
{
#define V_4

#ifdef V_1
    template <InputIterator Iter>
    typename Iter::difference_type distance(Iter first, Iter last)
    {
        typename Iter::difference_type count = 0;
        for (Iter current = first; current != last; ++current, ++count)
            ;

        return count;
    }

    template <RandomAccessIterator Iter>
    typename Iter::difference_type distance(Iter first, Iter last)
    {
        return last - first;
    }

#elif defined(V_2)
    template <InputIterator Iter>
    auto distance(Iter first, Iter last)
    {
        typename Iter::difference_type count = 0;
        for (Iter current = first; current != last; ++current, ++count)
            ;

        return count;
    }

    template <RandomAccessIterator Iter>
    auto distance(Iter first, Iter last)
    {
        return last - first;
    }

#elif defined(V_3)
    template <InputIterator Iter>
    constexpr auto distance(Iter first, Iter last)
    {
        if constexpr (RandomAccessIterator<Iter>)
        {
            return last - first;
        }
        else
        {
            iter_difference_t<Iter> count{};
            for (auto current = first; current != last; ++current, ++count)
                ;

            return count;
        }
    }

#elif defined(V_4)
    constexpr auto distance(InputIterator auto first, InputIterator auto last)
    {
        if constexpr (is_same_v<decltype(first), decltype(last)>)
        {
            iter_difference_t<decltype(first)> count{};
            for (auto current = first; current != last; ++current, ++count)
                ;

            return count;
        }
    }

    constexpr auto distance(RandomAccessIterator auto first, RandomAccessIterator auto last)
    {
        if constexpr (is_same_v<decltype(first), decltype(last)>)
        {
            return last - first;
        }
    }

#endif

    template <InputIterator Iter, typename Dist>
    void advance(Iter &it, Dist n)
    {
        for (auto dist = typename Iter::difference_type(n); dist > 0; --dist, ++it)
            ;
    }

    template <BidirectionalIterator Iter, typename Dist>
    void advance(Iter &it, Dist n)
    {
        auto dist = typename Iter::difference_type(n);

        typename Iter::difference_type step{dist > 0 ? 1 : -1};

        for (; step * dist > 0; (dist > 0 ? ++it : --it), dist -= step)
            ;
    }

    template <RandomAccessIterator Iter, typename Dist>
    void advance(Iter &it, Dist n)
    {
        auto dist = typename Iter::difference_type(n);

        it += dist;
    }
}

int main()
{
    vector<double> v(100);
    auto iv = v.begin();

    my::advance(iv, 3);
    cout << my::distance(iv, v.end()) << endl;

    list<double> l(10);
    auto il = l.begin();

    my::advance(il, 3);
    cout << my::distance(il, l.end()) << endl;
}
