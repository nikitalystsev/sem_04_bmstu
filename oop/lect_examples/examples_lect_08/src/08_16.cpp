// Пример 08.15. Параметры шаблона класса по умолчанию.
#include <iostream>
#include <exception>

using namespace std;

template <typename T>
class Default_delete
{
public:
    void operator()(T *ptr) { delete ptr; }
};

template <typename Type, typename Deleter = Default_delete<Type>>
class Holder
{
private:
    Type *ptr;
    Deleter del;

public:
    Holder(Type *p = nullptr, Deleter d = Deleter{}) noexcept : ptr(p), del(d) {}
    ~Holder() { del(ptr); }

    Type *get() const { return ptr; }
};

class File_close
{
public:
    void operator()(FILE *stream) { fclose(stream); }
};

Holder<FILE, File_close> make_file(const char *filename, const char *mode)
{
    FILE *stream = fopen(filename, mode);

    if (!stream)
        throw std::runtime_error("file opening error");

    return {stream};
}

auto main() -> int
{
    try
    {
        Holder<FILE, File_close> stream = make_file("test.txt", "w");

        fputs("Ok!!!", stream.get());
    }
    catch (const runtime_error &e)
    {
        cout << e.what() << endl;
    }
}