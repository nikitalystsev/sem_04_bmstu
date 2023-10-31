// Пример 13.05. Команда (Command). Объект известен.
# include <iostream>
# include <memory>
# include <vector>
# include <initializer_list>

using namespace std;

class Command
{
public:
	virtual ~Command() = default;

	virtual void execute() = 0;
};

template <typename Reseiver>
class SimpleCommand : public Command
{
	using Action = void(Reseiver::*)();
	using Pair = pair<shared_ptr<Reseiver>, Action>;

private:
	Pair call;

public:
	SimpleCommand(shared_ptr<Reseiver> r, Action a) : call(r, a) {}

	void execute() override { ((*call.first).*call.second)(); }
};

class CompoundCommand : public Command
{
	using VectorCommand = vector<shared_ptr<Command>>;

private:
	VectorCommand vec;

public:
	CompoundCommand(initializer_list<shared_ptr<Command>> lt);

	virtual void execute() override;
};

# pragma region Methods
CompoundCommand::CompoundCommand(initializer_list<shared_ptr<Command>> lt)
{
	for (auto&& elem : lt)
		vec.push_back(elem);
}

void CompoundCommand::execute()
{
	for (auto com : vec)
		com->execute();
}

# pragma endregion

class Object
{
public:
	void run() { cout << "Run method;" << endl; }
};

int main()
{
	shared_ptr<Object> obj = make_shared<Object>();
	shared_ptr<Command> command = make_shared<SimpleCommand<Object>>(obj, &Object::run);

	command->execute();

	shared_ptr<Command> complex(new CompoundCommand
		{
			make_shared<SimpleCommand<Object>>(obj, &Object::run),
			make_shared<SimpleCommand<Object>>(obj, &Object::run)
		});

	complex->execute();
}