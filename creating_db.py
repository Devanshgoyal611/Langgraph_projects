import os
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

Base = declarative_base()  # base class for all ORM (Object Relational Mapping) models


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    age = Column(Integer)
    email = Column(String, unique=True, index=True)

    orders = relationship("Order", back_populates="user")


class Food(Base):
    __tablename__ = "food"

    food_id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    price = Column(Float)

    orders = relationship("Order", back_populates="food")


class Order(Base):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    food_id = Column(Integer, ForeignKey("food.food_id"))
    user_id = Column(Integer, ForeignKey("users.user_id"))

    user = relationship("User", back_populates="orders")
    food = relationship("Food", back_populates="orders")
    
"""
Q: Why add relationships to the tables and not just foreign keys

Ans: A Foreign Key (ForeignKey("users.id") or ForeignKey("food.id")) is enough to establish a connection at the database level, 
but it does not automatically allow easy access to related objects in Python.

if we queried an Order, we'll only get food_id and user_id, not the actual Food or User object.

order = session.query(Order).first()
print(order.user)  # ❌ This would not work without `relationship()`
print(order.user_id)  # ✅ This would work but only gives the user ID, not the full user details

The relationship() function creates an automatic link between related objects in Python, making it easier to access related data.

order = session.query(Order).first()
print(order.user.name)  # ✅ Automatically fetches the associated User object
print(order.food.name)  # ✅ Automatically fetches the associated Food object
"""


DATABASE_URL = "sqlite:///example.db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def init_db():
    Base.metadata.create_all(bind=engine)

    session = SessionLocal()

    users = [
        User(name="Alice", age=30, email="alice@example.com"),
        User(name="Bob", age=25, email="bob@example.com"),
        User(name="Charlie", age=35, email="charlie@example.com"),
    ]
    session.add_all(users)
    session.commit()

    foods = [
        Food(name="Pizza Margherita", price=12.5),
        Food(name="Spaghetti Carbonara", price=15.0),
        Food(name="Lasagne", price=14.0),
    ]
    session.add_all(foods)
    session.commit()

    orders = [
        Order(food_id=1, user_id=1),
        Order(food_id=2, user_id=1),
        Order(food_id=3, user_id=3),
    ]
    session.add_all(orders)
    session.commit()

    session.close()
    print("Database has been successfully filled with sample data.")


if __name__ == "__main__":
    if not os.path.exists("example.db"):
        init_db()
    else:
        print("Database already exists, skipping creation.")