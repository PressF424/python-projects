from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship, declarative_base

DATABASE_URL = "sqlite:///store.db"  # я использовал  SQLite
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

#  базовый класс всех моделей
Base = declarative_base()


#  модель Category
class Category(Base):
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    products = relationship("Product", back_populates="category", cascade="all, delete-orphan")


#  модель Product
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('categories.id'))

    category = relationship("Category", back_populates="products")


# создание таблицы в БД
Base.metadata.create_all(engine)


# CRUD
def create_category(name):
    session = Session()
    new_category = Category(name=name)
    session.add(new_category)
    session.commit()
    session.close()


def create_product(name, price, category_id):
    session = Session()
    new_product = Product(name=name, price=price, category_id=category_id)
    session.add(new_product)
    session.commit()
    session.close()


def read_products_by_category(category_id):
    session = Session()
    products = session.query(Product).filter(Product.category_id == category_id).all()
    session.close()
    return products


def update_product_category(product_id, new_category_id):
    session = Session()
    product = session.query(Product).filter(Product.id == product_id).first()
    if product:
        product.category_id = new_category_id
        session.commit()
    session.close()


def delete_category(category_id):
    session = Session()
    category = session.query(Category).filter(Category.id == category_id).first()
    if category:
        session.delete(category)
        session.commit()
    session.close()


#  использование
if __name__ == "__main__":
    #  категории
    create_category("Electronics")
    create_category("Clothing")

    #  продукты
    create_product("Laptop", 1000, 1)
    create_product("Smartphone", 500, 1)
    create_product("T-shirt", 20, 2)

    # Чтение продуктов по категории
    products = read_products_by_category(1)  
    for product in products:
        print(f"Product: {product.name}, Price: {product.price}")

    update_product_category(1, 2)  # перемещение продукт с ID-1 в ID-2

    # Удаление категории и все продукты в ней
    delete_category(2)
