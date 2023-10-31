// Пример 09.15. Возврат shared_ptr на член данное объекта.
#include <iostream>
#include <memory>

using namespace std;

template <typename Type>
class Node : public enable_shared_from_this<Node<Type>>
{
private:
    shared_ptr<Node> nt;
    Type data;

    Node(shared_ptr<Node> nxt, Type d) : nt(nxt), data(d) {}

public:
    Node(const Node &) = delete;
    Node(Node &&) = delete;

    template <typename... Args>
    static shared_ptr<Node> create(Args &&...params);
    shared_ptr<Node> next();
    shared_ptr<Type> get();
};

#pragma region Method
template <typename Type>
template <typename... Args>
shared_ptr<Node<Type>> Node<Type>::create(Args &&...params)
{
    struct Enable_make_shared : public Node<Type>
    {
        Enable_make_shared(Args &&...params) : Node<Type>(forward<Args>(params)...) {}
    };

    return make_shared<Enable_make_shared>(forward<Args>(params)...);
}

template <typename Type>
shared_ptr<Node<Type>> Node<Type>::next()
{
    return nt;
}

template <typename Type>
shared_ptr<Type> Node<Type>::get()
{
    shared_ptr<Node> work = this->shared_from_this();

    return {work, &work->data};
}

#pragma endregion

int main()
{
    shared_ptr<double> value;

    {
        auto nd = Node<double>::create(nullptr, 10.);

        value = nd->get();
    }

    if (value.use_count() == 0)
        cout << "empty" << endl;
    else
        cout << "value = " << *value << endl;
}