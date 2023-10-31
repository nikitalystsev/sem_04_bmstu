// Пример 11.04. Фабричный метод (Factory Method). Без повторного создания.
#include <iostream>
#include <memory>

using namespace std;

class Product;

class Creator
{
public:
	virtual ~Creator() = default;

	shared_ptr<Product> getProduct();

protected:
	virtual shared_ptr<Product> createProduct() = 0;

private:
	shared_ptr<Product> product;
};

template <derived_from<Product> Tprod>
class ConCreator : public Creator
{
protected:
	shared_ptr<Product> createProduct() override
	{
		return make_shared<Tprod>();
	}
};

#pragma region Method Creator
shared_ptr<Product> Creator::getProduct()
{
	if (!product)
	{
		product = createProduct();
	}

	return product;
}

#pragma endregion

#pragma region Product
class Product
{
public:
	virtual ~Product() = default;

	virtual void run() = 0;
};

class ConProd1 : public Product
{
public:
	ConProd1() { cout << "Calling the ConProd1 constructor;" << endl; }
	~ConProd1() override { cout << "Calling the ConProd1 destructor;" << endl; }

	void run() override { cout << "Calling the run method;" << endl; }
};

#pragma endregion

int main()
{
	shared_ptr<Creator> cr = make_shared<ConCreator<ConProd1>>();
	shared_ptr<Product> ptr1 = cr->getProduct();
	shared_ptr<Product> ptr2 = cr->getProduct();

	cout << "use count = " << ptr1.use_count() << endl;
	ptr1->run();
}