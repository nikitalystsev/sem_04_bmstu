// Пример 11.08. Абстрактная фабрика (Abstract Factory).
#include <iostream>
#include <memory>

using namespace std;

class Image
{
};
class Color
{
};

class BaseGraphics
{
public:
    virtual ~BaseGraphics() = 0;
};
BaseGraphics::~BaseGraphics() {}

class BasePen
{
};
class BaseBrush
{
};

class QtGraphics : public BaseGraphics
{
public:
    QtGraphics(shared_ptr<Image> im) { cout << "Calling the QtGraphics constructor;" << endl; }
    ~QtGraphics() override { cout << "Calling the QtGraphics destructor;" << endl; }
};

class QtPen : public BasePen
{
};
class QtBrush : public BaseBrush
{
};

class AbstractGraphFactory
{
public:
    virtual ~AbstractGraphFactory() = default;

    virtual unique_ptr<BaseGraphics> createGraphics(shared_ptr<Image> im) = 0;
    virtual unique_ptr<BasePen> createPen(shared_ptr<Color> cl) = 0;
    virtual unique_ptr<BaseBrush> createBrush(shared_ptr<Color> cl) = 0;
};

class QtGraphFactory : public AbstractGraphFactory
{
public:
    unique_ptr<BaseGraphics> createGraphics(shared_ptr<Image> im) override
    {
        return make_unique<QtGraphics>(im);
    }

    unique_ptr<BasePen> createPen(shared_ptr<Color> cl) override
    {
        return make_unique<QtPen>();
    }

    unique_ptr<BaseBrush> createBrush(shared_ptr<Color> cl) override
    {
        return make_unique<QtBrush>();
    }
};

int main()
{
    shared_ptr<AbstractGraphFactory> grfactory = make_shared<QtGraphFactory>();

    shared_ptr<Image> image = make_shared<Image>();

    shared_ptr<BaseGraphics> graphics1 = grfactory->createGraphics(image);
}