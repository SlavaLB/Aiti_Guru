# Повторяющиеся поля можно в базовую таблицу, от которой потом наследоваться

categories
----------
id              PK INT                          # Первичный ключ
name            VARCHAR(100)                    # Имя категории макс 100 символов обязательное
parent_id       FK >0- categories.id NULL       # Ссылается на саму себя, без ограничения по вложенности, связь не обязательная
created_at      DATETIME default=now()          # Дата создания по умолчанию current


products
--------
id              PK INT                          # Первичный ключ
name            VARCHAR(100)                    # Имя товара макс 100 символов обязательное
quantity        INTEGER NULL                    # Количество товара на остатке, не обязательное
price           decimal(12,2)                   # Цена товара
category_id     INT FK >0- categories.id NULL   # Связь товара с категорией, не обязательная категория может иметь много товаров
created_at      DATETIME default=now()          # Дата создания по умолчанию current

customers
---------
id              PK                              # Первичный ключ
name            VARCHAR(100)                    # ФИО макс 100 символов обязательное
address         TEXT                            # Адрес доставки
created_at      DATETIME default=now()          # Дата создания по умолчанию current

orders
------
id              PK                              # Первичный ключ
customer_id     FK >- customers.id              # Связь заказ-пользователь, один клиент может иметь много заказов.
created_at      DATETIME default=now()          # Дата создания по умолчанию current


order_items
-----------
id              PK                              # Первичный ключ
order_id        FK >- orders.id NOT NULL        # Связь списка товаров с заказом, список содержит много товаров
product_id      FK >- products.id NOT NULL      # Связь товара со списком товаров, один товар может быть в разных списках
quantity        INT                             # Количество товаров в заказе
price_at_order  decimal(12,2)                   # Цена товара на момент добавления в корзину
