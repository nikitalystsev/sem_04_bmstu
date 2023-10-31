// Пример 11.05. Фабричный метод (Factory Method). Разделение обязанностей.
#include <iostream>
#include <initializer_list>
#include <memory>
#include <map>

using namespace std;

class Product;

class Creator
{
public:
    virtual ~Creator() = default;

    virtual unique_ptr<Product> createProduct() = 0;
};

template <derived_from<Product> Tprod>
class ConCreator : public Creator
{
public:
    unique_ptr<Product> createProduct() override
    {
        return make_unique<Tprod>();
    }
};

#pragma region Product
class Product
{
public:
    virtual ~Product() = default;

    virtual void run() = 0;
};

class ConProd1 : public Product
{
public:
    ConProd1() { cout << "Calling the ConProd1 constructor;" << endl; }
    ~ConProd1() override { cout << "Calling the ConProd1 destructor;" << endl; }

    void run() override { cout << "Calling the run method ConProd1;" << endl; }
};

class ConProd2 : public Product
{
public:
    ConProd2() { cout << "Calling the ConProd2 constructor;" << endl; }
    ~ConProd2() override { cout << "Calling the ConProd2 destructor;" << endl; }

    void run() override { cout << "Calling the run method ConProd2;" << endl; }
};
#pragma endregion

class CrCreator
{
public:
    template <typename Tprod>
    static unique_ptr<Creator> createConCreator()
    {
        return make_unique<ConCreator<Tprod>>();
    }
};

class Solution
{
    using CreateCreator = unique_ptr<Creator> (&)();
    using CallBackMap = map<size_t, CreateCreator>;

public:
    Solution() = default;
    Solution(initializer_list<pair<size_t, CreateCreator>> list);

    bool registration(size_t id, CreateCreator createfun);
    bool check(size_t id) { return callbacks.erase(id) == 1; }

    unique_ptr<Creator> create(size_t id);

private:
    CallBackMap callbacks;
};

#pragma region Solution
Solution::Solution(initializer_list<pair<size_t, CreateCreator>> list)
{
    for (auto &&elem : list)
        this->registration(elem.first, elem.second);
}

bool Solution::registration(size_t id, CreateCreator createfun)
{
    return callbacks.insert(CallBackMap::value_type(id, createfun)).second;
}

unique_ptr<Creator> Solution::create(size_t id)
{
    CallBackMap::const_iterator it = callbacks.find(id);

    if (it == callbacks.end())
    {
        //			throw IdError();
    }

    return unique_ptr<Creator>(it->second());
}

#pragma endregion

int main()
{
    shared_ptr<Solution> solution(new Solution({{1, CrCreator::createConCreator<ConProd1>}}));

    if (!solution->registration(2, CrCreator::createConCreator<ConProd2>))
    {
        cout << "Error registration!" << endl;
        // throw ...
    }
    else
    {
        solution->registration(2, CrCreator::createConCreator<ConProd2>);

        shared_ptr<Creator> cr(solution->create(2));
        shared_ptr<Product> ptr = cr->createProduct();

        ptr->run();
    }
}