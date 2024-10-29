# стратегия

class Strategy:
    def execute(self, data):
        pass

class ConcreteStrategyA(Strategy):
    def execute(self, data):
        return f"Стратегия A: обрабатываем {data}"

class ConcreteStrategyB(Strategy):
    def execute(self, data):
        return f"Стратегия B: обрабатываем {data}"

class Context:
    def __init__(self, strategy: Strategy):
        self._strategy = strategy

    def set_strategy(self, strategy: Strategy):
        self._strategy = strategy

    def do_some_logic(self, data):
        return self._strategy.execute(data)

# Использование
context = Context(ConcreteStrategyA())
print(context.do_some_logic("входные данные"))

context.set_strategy(ConcreteStrategyB())
print(context.do_some_logic("входные данные"))

# цепочка обязоностей

class Handler:
    def set_next(self, handler):
        self._next_handler = handler
        return handler

    def handle(self, request):
        if self._next_handler:
            return self._next_handler.handle(request)
        return None

class ConcreteHandlerA(Handler):
    def handle(self, request):
        if request == "A1":
            return "Обработано A1"
        else:
            return super().handle(request)

class ConcreteHandlerB(Handler):
    def handle(self, request):
        if request == "B2":
            return "Обработано B2"
        else:
            return super().handle(request)

# Использование
handler_a = ConcreteHandlerA()
handler_b = ConcreteHandlerB()

handler_a.set_next(handler_b)

print(handler_a.handle("A1"))
print(handler_a.handle("B2"))

# итератор

class Iterator:
    def __init__(self, collection):
        self._collection = collection
        self._index = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._index < len(self._collection):
            result = self._collection[self._index]
            self._index += 1
            return result
        else:
            raise StopIteration()

class Collection:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def __iter__(self):
        return Iterator(self.items)

# Использование
collection = Collection()
collection.add_item("Первый элемент")
collection.add_item("ВТорой элемент")
collection.add_item("Третий элемент")

for item in collection:
    print(item)