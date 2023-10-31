// Пример 08.02. Правило вызова функций и шаблонов функций.
#include <iostream>

template <typename Type>
void swap(Type &val1, Type &val2)
{   
    std::cout << "Вызываю шаблонную первую функцию!" << std::endl;
    Type temp = std::move(val1);
    val1 = std::move(val2);
    val2 = std::move(temp);
}

template <>
void swap<float>(float &val1, float &val2)
{
    std::cout << "Вызываю специализацию шаблона для float!" << std::endl;
    float temp = val1;
    val1 = val2;
    val2 = temp;
}

void swap(float &val1, float &val2)
{
    std::cout << "Вызываю нешаблонную функцию для float!" << std::endl;
    float temp = val1;
    val1 = val2;
    val2 = temp;
}

void swap(int &val1, int &val2)
{
    std::cout << "Вызываю нешаблонную функцию для int!" << std::endl;
    int temp = val1;
    val1 = val2;
    val2 = temp;
}

class A
{
public:
    A() = default;
    A(A &&) noexcept { std::cout << "Move constuctor!" << std::endl; }
    A &operator=(A &&) noexcept
    {
        std::cout << "Move assignment operator!" << std::endl;
        return *this;
    }
};

int main()
{
    const int N = 2;
    int a1[N];
    float a2[N];
    double a3[N];
    A a4[N]{};

    swap(a1[0], a1[1]);        // swap(int&, int&)
    swap<int>(a1[0], a1[1]);   // swap<int>(int&, int&)
    swap(a2[0], a2[1]);        // swap(float&, float&)
    swap<float>(a2[0], a2[1]); // swap<>(float&, float&)
    swap(a3[0], a3[1]);        // swap<double>(double&, double&)
    swap(a4[0], a4[1]);        // swap<A>(A&, A&)
}