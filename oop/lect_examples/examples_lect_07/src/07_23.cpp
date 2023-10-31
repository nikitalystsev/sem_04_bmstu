// Пример 07.23. Оператор “space ship”.
#define _CRT_SECURE_NO_WARNINGS

#include <iostream>
#include <compare>
#include <string.h>

using namespace std;

class MyInt
{
public:
    constexpr MyInt(int val) : value{val} {}
    auto operator<=>(const MyInt &) const = default;

private:
    int value;
};

class MyDouble
{
public:
    constexpr MyDouble(double val) : value{val} {}
    auto operator<=>(const MyDouble &) const = default;

private:
    double value;
};

class MyString
{
public:
    constexpr MyString(const char *val) : value{val} {}
    auto operator<=>(const MyString &) const = default;

private:
    const char *value;
};

int main()
{
    MyInt i1{1}, i2{2};

    cout << (i1 < i2) << endl;

    MyDouble d1{-0.}, d2{0.};

    cout << (d1 != d2) << (1. < d2) << (d1 < 2.) << endl;

    char st[5];
    strcpy(st, "Ok!!");
    MyString s1{"Ok!"}, s2{st};

    cout << (s1 < s2) << ("Ok!!" == s2) << endl; // сравнение адресов
}