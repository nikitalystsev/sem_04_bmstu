// Пример 13.21. Шаблон nullptr.
#include <iostream>

using namespace std;

const class nullPtr_t
{
public:
    // Может быть приведен к любому типу нулевого указателя (не на член класса)
    template <typename T>
    inline operator T *() const { return 0; }

    // или любому типу нулевого указателя на член
    template <typename C, typename T>
    inline operator T C::*() const { return 0; }

private:
    void operator&() const = delete;

} nullPtr = {};

int main()
{
    int *i = nullPtr;

    if (i == nullPtr)
        cout << "null ptr;" << endl;
}