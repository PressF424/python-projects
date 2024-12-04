# паттерн Прокси
class RealSubject:
    def request(self):
        return "RealSubject: Handling request."

class Proxy:
    def __init__(self, real_subject):
        self._real_subject = real_subject

    def request(self):
        print("Proxy: Checking access before forwarding the request.")
        result = self._real_subject.request()
        print("Proxy: Logging the request.")
        return result

# запрос клиента
real_subject = RealSubject()
proxy = Proxy(real_subject)
print(proxy.request())

# паттерн Мост
class Implementor:
    def operation_impl(self):
        pass

class ConcreteImplementorA(Implementor):
    def operation_impl(self):
        return "ConcreteImplementorA: Implementation."

class ConcreteImplementorB(Implementor):
    def operation_impl(self):
        return "ConcreteImplementorB: Implementation."

class Abstraction:
    def __init__(self, implementor):
        self._implementor = implementor

    def operation(self):
        return f"Abstraction: Base operation with:\n{self._implementor.operation_impl()}"

# запрос клиента
implementor_a = ConcreteImplementorA()
abstraction_a = Abstraction(implementor_a)
print(abstraction_a.operation())

implementor_b = ConcreteImplementorB()
abstraction_b = Abstraction(implementor_b)
print(abstraction_b.operation())

# паттерн Адаптер
class Target:
    def request(self):
        return "Target: Default behavior."

class Adaptee:
    def specific_request(self):
        return "Adaptee: Specific behavior."

class Adapter(Target):
    def __init__(self, adaptee):
        self._adaptee = adaptee

    def request(self):
        return f"Adapter: Transformed behavior: {self._adaptee.specific_request()}"

# запрос клиента
target = Target()
print(target.request())

adaptee = Adaptee()
adapter = Adapter(adaptee)
print(adapter.request())
