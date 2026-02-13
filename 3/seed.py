import asyncio
from app.core.db import AsyncSessionLocal
from app.models import Category, Product, Customer, Order, OrderItem


async def seed():
    async with AsyncSessionLocal() as session:
        async with session.begin():

            electronics = Category(name="Электроника")
            clothing = Category(name="Одежда")

            session.add_all([electronics, clothing])
            await session.flush()

            smartphones = Category(
                name="Смартфоны",
                parent_id=electronics.id,
                root_category_id=electronics.id
            )

            laptops = Category(
                name="Ноутбуки",
                parent_id=electronics.id,
                root_category_id=electronics.id
            )

            android = Category(
                name="Android",
                parent_id=smartphones.id,
                root_category_id=electronics.id
            )

            iphone = Category(
                name="iPhone",
                parent_id=smartphones.id,
                root_category_id=electronics.id
            )

            session.add_all([smartphones, laptops, android, iphone])
            await session.flush()

            products = [
                Product(
                    name="Samsung Galaxy S24",
                    price=1000,
                    quantity=5,
                    category_id=android.id,
                    root_category_id=electronics.id
                ),
                Product(
                    name="iPhone 15",
                    price=1500,
                    quantity=3,
                    category_id=iphone.id,
                    root_category_id=electronics.id
                ),
                Product(
                    name="MacBook Pro",
                    price=2500,
                    quantity=2,
                    category_id=laptops.id,
                    root_category_id=electronics.id
                ),
            ]

            session.add_all(products)
            await session.flush()

            customers = [
                Customer(name="Иван Иванов", address="Москва"),
                Customer(name="Петр Петров", address="СПб"),
            ]

            session.add_all(customers)
            await session.flush()

            orders = [
                Order(customer_id=customers[0].id),
                Order(customer_id=customers[1].id),
            ]

            session.add_all(orders)
            await session.flush()

            order_items = [
                OrderItem(
                    order_id=orders[0].id,
                    product_id=products[0].id,
                    quantity=1,
                    price_at_order=products[0].price
                ),
                OrderItem(
                    order_id=orders[0].id,
                    product_id=products[1].id,
                    quantity=1,
                    price_at_order=products[1].price
                ),
                OrderItem(
                    order_id=orders[1].id,
                    product_id=products[2].id,
                    quantity=1,
                    price_at_order=products[2].price
                ),
            ]

            session.add_all(order_items)

if __name__ == "__main__":
    asyncio.run(seed())
    print("Database seeded successfully 🚀")
