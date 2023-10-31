// Пример 10.12. Использование dynamic_cast для приведения типа между родительскими классами при
// множественном наследовании.
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

class Draw : public AbstractVisitor, public DrawCircle, public DrawSquare
{
};

class DrawAll
{
public:
    void operator()(const vector<unique_ptr<Shape>> &shapes)
    {
        for (const auto &s : shapes)
        {
            s->accept(Draw{});
        }
    }
};

int main()
{
    using Shapes = vector<unique_ptr<Shape>>;

    Shapes shapes;

    shapes.emplace_back(make_unique<Circle>(1.));
    shapes.emplace_back(make_unique<Square>(2.));

    DrawAll{}(shapes);
}