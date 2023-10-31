// Пример 13.12. Посетитель (Visitor) с использованием шаблона variant (“безопасный” union).
# include <iostream>
# include <vector>
# include <variant>

using namespace std;

class Circle {};
class Square {};

using Shape = std::variant<Circle, Square>;

class Formation
{
public:
	static vector<Shape> initialization(initializer_list<Shape> list)
	{
		vector<Shape> vec;

		for (auto&& elem : list)
			vec.emplace_back(elem);

		return vec;
	}
};

class Draw
{
public:
    void operator ()(const Circle&) const { cout << "Circle" << endl; }
    void operator ()(const Square&) const { cout << "Square" << endl; }
};

int main()
{
    using Shapes = vector<Shape>;

	Shapes fiqure = Formation::initialization({ Circle{}, Square{} });

	for (const auto& elem : fiqure)
		std::visit(Draw{}, elem);
}