// Пример 13.13. Шаблонный посетитель (Template Visitor) с использованием паттерна CRTP.
#include <iostream>
#include <memory>
#include <initializer_list>
#include <vector>

using namespace std;

template <typename... Types>
class Visitor;

template <typename Type>
class Visitor<Type>
{
public:
    virtual void visit(Type &t) = 0;
};

template <typename Type, typename... Types>
class Visitor<Type, Types...> : public Visitor<Types...>
{
public:
    using Visitor<Types...>::visit;
    virtual void visit(Type &t) = 0;
};

using ShapeVisitor = Visitor<class Figure, class Camera>;

class Point
{
};

class Shape
{
public:
    Shape(const Point &pnt) : point(pnt) {}
    virtual ~Shape() = default;

    const Point &getPoint() const { return point; }
    void setPoint(const Point &pnt) { point = pnt; }

    virtual void accept(shared_ptr<ShapeVisitor> v) = 0;

private:
    Point point;
};

template <typename Derived>
class Visitable : public Shape
{
public:
    using Shape::Shape;

    void accept(shared_ptr<ShapeVisitor> v) override
    {
        v->visit(*static_cast<Derived *>(this));
    }
};

class Figure : public Visitable<Figure>
{
    using Visitable<Figure>::Visitable;
};

class Camera : public Visitable<Camera>
{
    using Visitable<Camera>::Visitable;
};

class Composite : public Shape
{
    using Shapes = vector<shared_ptr<Shape>>;

private:
    Shapes shapes{};

public:
    Composite(initializer_list<shared_ptr<Shape>> list) : Shape(Point{})
    {
        for (auto &&elem : list)
            shapes.emplace_back(elem);
    }

    void accept(shared_ptr<ShapeVisitor> visitor) override
    {
        for (auto &elem : shapes)
            elem->accept(visitor);
    }
};

class DrawVisitor : public ShapeVisitor
{
public:
    void visit(Figure &fig) override { cout << "Draws a figure;" << endl; }
    void visit(Camera &fig) override { cout << "Draws a camera;" << endl; }
};

int main()
{
    Point p;
    shared_ptr<Composite> figure = make_shared<Composite>(
        initializer_list<shared_ptr<Shape>>(
            {make_shared<Figure>(p), make_shared<Camera>(p), make_shared<Figure>(p)}));

    shared_ptr<ShapeVisitor> visitor = make_shared<DrawVisitor>();

    figure->accept(visitor);
}