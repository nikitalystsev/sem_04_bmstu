// Пример 13.11. Посетитель (Visitor). Приведение типа между базовыми классами.
#include <iostream>
#include <vector>
#include <memory>

using namespace std;

class AbstractVisitor
{
public:
    virtual ~AbstractVisitor() = default;
};

template <typename T>
class Visitor
{
public:
    virtual ~Visitor() = default;

    virtual void visit(const T &) const = 0;
};

class Shape
{
public:
    Shape() = default;
    virtual ~Shape() = default;

    virtual void accept(const AbstractVisitor &) const = 0;
};

class Circle : public Shape
{
private:
    double radius;

public:
    Circle(double radius) : radius(radius) {}

    void accept(const AbstractVisitor &v) const override
    {
        auto cv = dynamic_cast<const Visitor<Circle> *>(&v);

        if (cv)
        {
            cv->visit(*this);
        }
    }
};

class Square : public Shape
{
private:
    double side;

public:
    Square(double side) : side(side) {}

    void accept(const AbstractVisitor &v) const override
    {
        auto cv = dynamic_cast<const Visitor<Square> *>(&v);

        if (cv)
        {
            cv->visit(*this);
        }
    }
};

class DrawCircle : public Visitor<Circle>
{
    void visit(const Circle &circle) const override
    {
        cout << "Circle" << endl;
    }
};

class DrawSquare : public Visitor<Square>
{
    void visit(const Square &circle) const override
    {
        cout << "Square" << endl;
    }
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

    void accept(const AbstractVisitor &visitor) const override
    {
        for (auto &elem : shapes)
            elem->accept(visitor);
    }
};

class Draw : public AbstractVisitor, public DrawCircle, public DrawSquare
{
};

int main()
{
    shared_ptr<Shape> figure = make_shared<Figure>(
        initializer_list<shared_ptr<Shape>>({make_shared<Circle>(1), make_shared<Square>(2)}));

    figure->accept(Draw{});
}