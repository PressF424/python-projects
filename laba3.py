# одиночка

class Singleton:
    _instance = None

    def __new__(clss):
        if clss._instance is None:
            clss._instance = super(Singleton, clss).__new__(clss)
        return clss._instance

# Вызов
s1 = Singleton()
s2 = Singleton()
print(s1 is s2)

# фабричный
class Transport:
    def create_transport(self):
        raise NotImplementedError()

class Vehicle(Transport):
    def create_transport(self):
        return "Создание машины"

class Bike(Transport):
    def create_transport(self):
        return "Создание велосипеда"

# Фабрика
class TransportFactory:
    @staticmethod
    def create_transport(transport_type):
        if transport_type == "car":
            return Vehicle().create_transport()
        else:
            return Bike().create_transport()

# Использование
print(TransportFactory.create_transport("vehicle"))
print(TransportFactory.create_transport("bike"))

# абстрактная фабрика

class CarFactory:
    def create_engine(self):
        raise NotImplementedError()
    def create_wheels(self):
        raise NotImplementedError()

class DefaultCarFac(CarFactory):
    def create_engine(self):
        return "Обычный двигатель"

    def create_wheels(self):
        return "Обычные колёса"

class OffRoadCarFac(CarFactory):
    def create_engine(self):
        return "Внедорожный двигатель"

    def create_wheels(self):
        return "Внедорожные колёса"

def create_car(factory: CarFactory):
    engine = factory.create_engine()
    wheels = factory.create_wheels()
    return f'В автомобиле установлены {engine} и {wheels}'

default_car = create_car(DefaultCarFac())
offroad_car = create_car(OffRoadCarFac())

print(default_car)
print(offroad_car)

# строитель

class House:
    def __init__(self):
        self.parts = []

    def add_part(self, part):
        self.parts.append(part)

class HouseBuilder:
    def __init__(self):
        self.house = House()

    def build_roof(self):
        self.house.add_part("Крыша")
        return self

    def build_walls(self):
        self.house.add_part("Стены")
        return self

    def build_foundation(self):
        self.house.add_part("Фундамент")
        return self

    def build(self):
        return self.house

# Использование
builder = HouseBuilder()
house = builder.build_foundation().build_walls().build_roof().build()
print(house.parts)
