// Пример 09.12. Установка deleter для unique_ptr на примере закрытия файла.
#include <iostream>
#include <memory>
#include <stdio.h>

using namespace std;

#define V_1

#ifdef V_1
class Deleter
{
public:
    void operator()(FILE *stream) noexcept
    {
        fclose(stream);
        cout << "file is closed" << endl;
    }
};

#elif defined(V_2)
using Deleter = decltype([](FILE *stream)
                         {
fclose(stream);
cout << "file is closed" << endl; });

#endif

using FilePtr_t = unique_ptr<FILE, Deleter>;

FilePtr_t make_file(const char *filename, const char *mode)
{
    FILE *stream = fopen(filename, mode);

    if (!stream)
        throw runtime_error("File not found!");

    cout << "file is open" << endl;

    return FilePtr_t{stream};
}

int main()
{
    try
    {
        FilePtr_t stream = make_file("test.txt", "r");
    }
    catch (const runtime_error &ex)
    {
        cout << ex.what() << endl;
    }
}
