// Пример 03.04. Перегрузка функций.
#include <iostream>

// https://habr.com/ru/articles/487920/ про перегрузку

using namespace std;

void func1(int &x) { cout << "func1(int&)" << endl; }
void func1(const int &x) { cout << "func1(const int&)" << endl; }

void func2(int x) { cout << "func2(int)" << endl; }
void func2(int &x) { cout << "func2(int&)" << endl; }

void func3(const int &x) { cout << "func3(const int&)" << endl; }
void func3(int &&x) { cout << "func3(int&&)" << endl; }

void func4(int &x) { cout << "func4(int&)" << endl; }
void func4(int &&x) { cout << "func4(int&&)" << endl; }

void func5(int x) { cout << "func5(int)" << endl; }
void func5(int &&x) { cout << "func5(int&&)" << endl; }

void func6(int x) {}
void func6(const int &x) {}

int main()
{
    int i = 0;
    const int ci = 0;
    int &lv = i;
    const int &clv = ci;
    int &&rv = i + 1;

    func1(i);     // int&
    func1(ci);    // const int&
    func1(lv);    // int&
    func1(clv);   // const int&
    func1(rv);    // int&
    func1(i + 1); // const int&
    cout << endl;

    // func2(i);// Error!
    func2(ci); // int
    // func2(lv);// Error!
    func2(clv); // int
    // func2(rv);// Error!
    func2(i + 1); // int
    cout << endl;

    func3(i);     // const int&
    func3(ci);    // const int&
    func3(lv);    // const int&
    func3(clv);   // const int&
    func3(rv);    // const int&
    func3(i + 1); // int&&
    cout << endl;

    func4(i); // int&
    // func4(ci);// Error!
    func4(lv); // int&
    // func4(clv);// Error!
    func4(rv);    // int&
    func4(i + 1); // int&&
    cout << endl;

    func5(i);   // int
    func5(ci);  // int
    func5(lv);  // int
    func5(clv); // int
    func5(rv);  // int
    // func5(i + 1);// Error!

    // func6(i);// Error!
    // func6(ci);// Error!
    // func6(lv);// Error!
    // func6(clv);// Error!
    // func6(rv);// Error!
    // func6(i + 1);// Error!
}