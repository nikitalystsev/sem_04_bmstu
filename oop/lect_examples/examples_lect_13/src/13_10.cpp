// Пример 13.10. Посетитель (Visitor).
#include <iostream>
#include <memory>
#include <vector>

using namespace std;

class Circle;
class Rectangle;

class Visitor
{
public:
    virtual ~Visitor() = default;

    virtual void visit(Circle &ref) = 0;
    virtual void visit(Rectangle &ref) = 0;
};

class Shape
{
public:
    virtual ~Shape() = default;

    virtual void accept(shared_ptr<Visitor> visitor) = 0;
};

class Circle : public Shape
{
public:
    void accept(shared_ptr<Visitor> visitor) override { visitor->visit(*this); }
};

class Rectangle : public Shape
{
public:
    void accept(shared_ptr<Visitor> visitor) override { visitor->visit(*this); }
};

class ConVisitor : public Visitor
{
public:
    void visit(Circle &ref) override { cout << "Circle;" << endl; }
    void visit(Rectangle &ref) override { cout << "Rectangle;" << endl; }
};

class Figure : public Shape
{
    using Shapes = vector<shared_ptr<Shape>>;

private:
    Shapes shapes;

public:
    Figure(initializer_list<shared_ptr<Shape>> list)
    {
        for (auto &&elem : list)
            shapes.emplace_back(elem);
    }

    void accept(shared_ptr<Visitor> visitor) override
    {
        for (auto &elem : shapes)
            elem->accept(visitor);
    }
};

int main()
{
    shared_ptr<Shape> figure = make_shared<Figure>(
        initializer_list<shared_ptr<Shape>>(
            {make_shared<Circle>(), make_shared<Rectangle>(), make_shared<Circle>()}));

    shared_ptr<Visitor> visitor = make_shared<ConVisitor>();

    figure->accept(visitor);
}