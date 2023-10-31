// Пример 13.17. Свойство (Property). Специализация для ReadOnly и WriteOnly.
#include <iostream>

using namespace std;

struct ReadOnly_tag
{
};
struct WriteOnly_tag
{
};
struct ReadWrite_tag
{
};

template <typename Owner, typename Type, typename Access = ReadWrite_tag>
class Property
{
    using Getter = Type (Owner::*)() const;
    using Setter = void (Owner::*)(const Type &);

private:
    Owner *owner;
    Getter methodGet;
    Setter methodSet;

public:
    Property() = default;
    Property(Owner *const owr, Getter getmethod, Setter setmethod) : owner(owr), methodGet(getmethod), methodSet(setmethod) {}

    void init(Owner *const owr, Getter getmethod, Setter setmethod)
    {
        owner = owr;
        methodGet = getmethod;
        methodSet = setmethod;
    }

    operator Type() { return (owner->*methodGet)(); }               // Getter
    void operator=(const Type &data) { (owner->*methodSet)(data); } // Setter
};

template <typename Owner, typename Type>
class Property<typename Owner, typename Type, ReadOnly_tag>
{
    using Getter = Type (Owner::*)() const;

private:
    Owner *owner;
    Getter methodGet;

public:
    Property() = default;
    Property(Owner *const owr, Getter getmethod) : owner(owr), methodGet(getmethod) {}

    void init(Owner *const owr, Getter getmethod)
    {
        owner = owr;
        methodGet = getmethod;
    }

    operator Type() { return (owner->*methodGet)(); } // Getter
};

template <typename Owner, typename Type>
class Property<typename Owner, typename Type, WriteOnly_tag>
{
    using Setter = void (Owner::*)(const Type &);

private:
    Owner *owner;
    Setter methodSet;

public:
    Property() = default;
    Property(Owner *const owr, Setter setmethod) : owner(owr), methodSet(setmethod) {}

    void init(Owner *const owr, Setter setmethod)
    {
        owner = owr;
        methodSet = setmethod;
    }

    void operator=(const Type &data) { (owner->*methodSet)(data); } // Setter
};

class Object
{
public:
    Object(double vRW = 0., double vRO = 0., double vWO = 0.)
        : valueRW(vRW), valueRO(vRO), valueWO(vWO)
    {
        ValueRW.init(this, &Object::getValueRW, &Object::setValueRW);
        ValueRO.init(this, &Object::getValueRO);
        ValueWO.init(this, &Object::setValueWO);
    }

private:
    double valueRW;

public:
    Property<Object, double> ValueRW;

    double getValueRW() const { return valueRW; }
    void setValueRW(const double &v) { valueRW = v; }

private:
    double valueRO;

public:
    Property<Object, double, ReadOnly_tag> ValueRO;

    double getValueRO() const { return valueRO; }

private:
    double valueWO;

public:
    Property<Object, double, WriteOnly_tag> ValueWO;

    void setValueWO(const double &v) { valueWO = v; }
};

int main()
{
    Object obj(5., 15., 25.);

    obj.ValueRW = 10.;
    cout << "value = " << obj.ValueRW << endl;

    //	obj.ValueRO = 10.;							// Error! (ReadOnly)
    cout << "value = " << obj.ValueRO << endl;

    obj.ValueWO = 10.;
    //	cout << "value = " << obj.ValueWO << endl;	// Error! (WriteOnly)
}