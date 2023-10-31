// Пример 12.01. Адаптер (Adapter).
# include <iostream>
# include <memory>

using namespace std;

class BaseAdaptee // адаптируемая сущность 
{
public:
	virtual ~BaseAdaptee() = default;

	virtual void specificRequest() = 0;
};

class ConAdaptee : public BaseAdaptee // адаптируемая сущность 
{
public:
	virtual void specificRequest() override { cout << "Method ConAdaptee;" << endl; }
};

class Adapter
{
public:
	virtual ~Adapter() = default;

	virtual void request() = 0;
};

class ConAdapter : public Adapter
{
private:
	shared_ptr<BaseAdaptee>  adaptee;

public:
	ConAdapter(shared_ptr<BaseAdaptee> ad) : adaptee(ad) {}

	virtual void request() override;
};

# pragma region Methods
void ConAdapter::request()
{
	cout << "Adapter: ";

	if (adaptee)
	{
		adaptee->specificRequest();
	}
	else
	{
		cout << "Empty!" << endl;
	}
}

# pragma endregion

int main()
{
	shared_ptr<BaseAdaptee> adaptee = make_shared<ConAdaptee>();
	shared_ptr<Adapter> adapter = make_shared<ConAdapter>(adaptee);

	adapter->request();
}