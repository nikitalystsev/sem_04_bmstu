// Пример 03.02. rvalue ссылки.
#include <iostream>

using namespace std;

int main()
{
    int i = 0;
    int &&rv1 = i + 0;
    int &&rv2 = move(i);
    int &&rv3 = (int)i;

    // ++i;
    ++rv3;
    cout << "i = " << i << endl;

    int &&rv4 = 5;
    ++rv4;

    cout << "rv1 = " << rv1 << "; rv2 = " << rv2 << "; rv3 = " << rv3 << endl;
    cout << "rv4 = " << rv4 << endl;
}
