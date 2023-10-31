// Пример 11.13. Пул объектов (Object Pool).
#include <iostream>
#include <memory>
#include <iterator>
#include <vector>

using namespace std;

template <typename T>
concept PoolObject = requires(T t) {
    t.clear();
};

class Product
{
private:
    static size_t count;

public:
    Product() { cout << "Constructor(" << ++count << ");" << endl; }
    ~Product() { cout << "Destructor(" << count-- << ");" << endl; }

    void clear() { cout << "Method clear: 0x" << this << endl; }
};

size_t Product::count = 0;

template <PoolObject Type>
class Pool
{
public:
    static shared_ptr<Pool<Type>> instance();

    shared_ptr<Type> getObject();
    bool releaseObject(shared_ptr<Type> &obj);
    size_t count() const { return pool.size(); }

    Pool(const Pool &) = delete;
    Pool &operator=(const Pool &) = delete;

private:
    vector<pair<bool, shared_ptr<Type>>> pool;

    Pool() {}

    pair<bool, shared_ptr<Type>> create();

    template <typename Type2>
    friend ostream &operator<<(ostream &os, const Pool<Type2> &pl);
};

#pragma region ObjectPool class Methods
template <PoolObject Type>
shared_ptr<Pool<Type>> Pool<Type>::instance()
{
    static shared_ptr<Pool<Type>> myInstance(new Pool<Type>());

    return myInstance;
}

template <PoolObject Type>
shared_ptr<Type> Pool<Type>::getObject()
{
    size_t i;
    for (i = 0; i < pool.size() && pool[i].first; ++i)
        ;

    if (i < pool.size())
    {
        pool[i].first = true;
    }
    else
    {
        pool.push_back(create());
    }

    return pool[i].second;
}

template <PoolObject Type>
bool Pool<Type>::releaseObject(shared_ptr<Type> &obj)
{
    size_t i;
    for (i = 0; pool[i].second != obj && i < pool.size(); ++i)
        ;

    if (i == pool.size())
        return false;

    obj.reset();
    pool[i].first = false;
    pool[i].second->clear();

    return true;
}

template <PoolObject Type>
pair<bool, shared_ptr<Type>> Pool<Type>::create()
{
    return {true, make_shared<Type>()};
}

#pragma endregion

template <typename Type>
ostream &operator<<(ostream &os, const Pool<Type> &pl)
{
    for (auto elem : pl.pool)
        os << "{" << elem.first << ", 0x" << elem.second << "} ";

    return os;
}

int main()
{
    shared_ptr<Pool<Product>> pool = Pool<Product>::instance();

    vector<shared_ptr<Product>> vec(4);

    for (auto &elem : vec)
        elem = pool->getObject();

    pool->releaseObject(vec[1]);

    cout << *pool << endl;

    shared_ptr<Product> ptr = pool->getObject();
    vec[1] = pool->getObject();

    cout << *pool << endl;
}