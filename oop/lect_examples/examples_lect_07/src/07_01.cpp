// Пример 07.01. Обработка исключительных ситуаций.
#include <iostream>
#include <string.h>
#include <exception>

using namespace std;

class ExceptionArray : public std::exception
{
protected:
    static const size_t sizebuff = 128;
    char errormsg[sizebuff]{};

public:
    ExceptionArray() noexcept = default;
    ExceptionArray(const char *msg) noexcept
    {
        strncpy(errormsg, msg, sizebuff);
    }
    ~ExceptionArray() override {}

    const char *what() const noexcept override { return errormsg; }
};

class ErrorIndex : public ExceptionArray
{
private:
    const char *errIndexMsg = "Error Index";
    int ind;

public:
    ErrorIndex(const char *msg, int index) noexcept : ind(index)
    {
        snprintf(errormsg, sizebuff, "%s %s: %4d!", msg, errIndexMsg, ind);
    }
    ~ErrorIndex() override {}

    const char *what() const noexcept override { return errormsg; }
};

int main()
{
    try
    {
        throw(ErrorIndex("Index!!", -1));
    }
    catch (const ExceptionArray &error)
    {
        cout << error.what() << endl;
    }
    catch (std::exception &error)
    {
        cout << error.what() << endl;
    }
    catch (...)
    {
        cout << "All errors!" << endl;
    }

    return 0;
}
