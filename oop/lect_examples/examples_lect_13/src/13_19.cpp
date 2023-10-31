// Пример 13.19. “Статический полиморфизм”. Идиома MixIn.
#include <iostream>

using namespace std;

template <typename Derived>
struct Increment
{
    Derived &operator++()
    {
        auto &self = static_cast<Derived &>(*this);
        self.setValue(self.getValue() + 1);

        return self;
    }

    Derived operator++(int)
    {
        auto &self = static_cast<Derived &>(*this);
        Derived temp = self;
        self.setValue(self.getValue() + 1);

        return temp;
    }
};

// C++23
/*
struct Increment
{
    auto& operator ++(this auto& self)
    {
        self.setValue(self.getValue() + 1);

        return self;
    }

    auto operator ++(this auto& self, int)
    {
        auto tmp = self;
        self.setValue(self.getValue() + 1);

        return tmp;
    }
};
*/

class Age : public Increment<Age>
{
private:
    unsigned short age;

public:
    Age(unsigned short value) : age(value) {}

    unsigned short getValue() const { return age; }
    void setValue(unsigned short value) { age = value; }
};

int main()
{
    Age a{18};

    a++;

    cout << "age = " << a.getValue() << endl;
}