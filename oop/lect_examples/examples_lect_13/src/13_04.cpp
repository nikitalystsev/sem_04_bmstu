// Пример 13.04. Стратегия (Strategy) на примере сортировки массива.
#include <iostream>
#include <memory>
#include <initializer_list>

using namespace std;

class Strategy;

class Array final
{
public:
    Array(initializer_list<double> list);

    void sort(shared_ptr<Strategy> algorithm);

    const double &operator[](int index) const { return this->arr[index]; }
    unsigned size() const { return count; }

private:
    shared_ptr<double[]> arr;
    unsigned count;
};

class Strategy
{
public:
    virtual void algorithmSort(shared_ptr<double[]> ar, unsigned cnt) = 0;
};

#pragma region Array methods
Array::Array(initializer_list<double> list)
{
    this->count = list.size();
    this->arr = shared_ptr<double[]>(new double[this->count]);

    unsigned i = 0;
    for (auto elem : list)
        arr[i++] = elem;
}

void Array::sort(shared_ptr<Strategy> algorithm)
{
    algorithm->algorithmSort(this->arr, this->count);
}
#pragma endregion

template <typename TComparison>
class BustStrategy : public Strategy
{
public:
    void algorithmSort(shared_ptr<double[]> ar, unsigned cnt) override
    {
        for (int i = 0; i < cnt - 1; i++)
            for (int j = i + 1; j < cnt; j++)
            {
                if (TComparison::compare(ar[i], ar[j]) > 0)
                    swap(ar[i], ar[j]);
            }
    }
};

template <typename Type>
class Comparison
{
public:
    static int compare(const Type &elem1, const Type &elem2) { return elem1 - elem2; }
};

ostream &operator<<(ostream &os, const Array &ar)
{
    for (int i = 0; i < ar.size(); i++)
        os << " " << ar[i];
    return os;
}

int main()
{
    using TStrategy = BustStrategy<Comparison<double>>;
    shared_ptr<Strategy> strategy = make_shared<TStrategy>();

    Array ar{8., 6., 4., 3., 2., 7., 1.};

    ar.sort(strategy);

    cout << ar << endl;
}