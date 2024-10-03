class GameObject:
    def __init__(self, object_id, name, x, y):
        self.object_id = object_id
        self.name = name
        self.x = x
        self.y = y

    def get_id(self):
        return self.object_id

    def get_name(self):
        return self.name

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y


class Building(GameObject):
    def __init__(self, object_id, name, x, y):
        super().__init__(object_id, name, x, y)
        self.built = False

    def is_built(self):
        return self.built


class Fort(Building):
    def __init__(self, object_id, name, x, y):
        super().__init__(object_id, name, x, y)

    def attack(self, unit):
        damage = 10
        unit.receive_damage(damage)


class MobileHome(Building):
    def __init__(self, object_id, name, x, y):
        super().__init__(object_id, name, x, y)

    def move(self, direction):
        if direction == "north":
            self.y += 1
        elif direction == "south":
            self.y -= 1
        elif direction == "east":
            self.x += 1
        elif direction == "west":
            self.x -= 1
        print(f"{self.name} moved {direction} to ({self.x}, {self.y})")


class Unit(GameObject):
    def __init__(self, object_id, name, x, y, hp):
        super().__init__(object_id, name, x, y)
        self.hp = hp

    def is_alive(self):
        return self.hp > 0

    def get_hp(self):
        return self.hp

    def receive_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0


class Attacker:
    def attack(self, unit):
        raise NotImplementedError("надо переопределить")


class Moveable:
    def move(self, direction):
        raise NotImplementedError("надо переопределить")


class Archer(Unit, Attacker, Moveable):
    def __init__(self, object_id, name, x, y, hp):
        super().__init__(object_id, name, x, y, hp)

    def attack(self, unit):
        damage = 5
        unit.receive_damage(damage)
        print(f"{self.name} attacked {unit.get_name()} for {damage} damage!")


# Примеры
fort = Fort(1, "testFort1", 0, 0)
archer = Archer(2, "testArcher1", 1, 1, 30)

print(f"Fort ID: {fort.get_id()}, Name: {fort.get_name()}, Position: ({fort.get_x()}, {fort.get_y()})")
print(f"Archer ID: {archer.get_id()}, Name: {archer.get_name()}, HP: {archer.get_hp()}")

# Атака
fort.attack(archer)
print(f"Archer's HP after attack: {archer.get_hp()}")

# Движение
mobile_home = MobileHome(3, "horse", 2, 2)
mobile_home.move("south")
