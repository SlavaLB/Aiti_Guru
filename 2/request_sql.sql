# Сумма заказов по каждому клиенту

SELECT
    c.name AS customer_name,
    COALESCE(SUM(oi.quantity * oi.price_at_order), 0) AS total_amount
FROM customers c
LEFT JOIN orders o
    ON o.customer_id = c.id
LEFT JOIN order_items oi
    ON oi.order_id = o.id
GROUP BY c.id, c.name
ORDER BY total_amount DESC;

# Количество дочерних элементов первого уровня
SELECT
    root.id,
    root.name,
    COUNT(child.id) AS first_level_children_count
FROM categories root
LEFT JOIN categories child
    ON child.parent_id = root.id
WHERE root.parent_id IS NULL
GROUP BY root.id, root.name
ORDER BY root.name;



# Топ-5 самых покупаемых товаров за последний месяц
CREATE OR REPLACE VIEW top_5_products_last_month AS
WITH RECURSIVE category_tree AS (
    SELECT
        id,
        name,
        parent_id,
        id AS root_id,
        name AS root_name
    FROM categories
    WHERE parent_id IS NULL

    UNION ALL

    SELECT
        c.id,
        c.name,
        c.parent_id,
        ct.root_id,
        ct.root_name
    FROM categories c
    JOIN category_tree ct
        ON c.parent_id = ct.id
)

SELECT
    p.name AS product_name,
    ct.root_name AS first_level_category,
    SUM(oi.quantity) AS total_sold
FROM order_items oi
JOIN orders o
    ON o.id = oi.order_id
JOIN products p
    ON p.id = oi.product_id
LEFT JOIN category_tree ct
    ON ct.id = p.category_id
WHERE o.created_at >= date_trunc('month', CURRENT_DATE - INTERVAL '1 month')
GROUP BY p.id, p.name, ct.root_name
ORDER BY total_sold DESC
LIMIT 5;

Оптимизация
- растет кол заказов в день, order_items, много товаров
Добавление индексов таблицу, чтобы получать поля по хэшу, проводить очистку мертвых строк(Postgres это делает, но нужно донастроить под задачи)
CREATE INDEX idx_orders_created_at ON orders(created_at);
CREATE INDEX idx_orders_customer_id ON orders(customer_id);
CREATE INDEX idx_order_items_order_id ON order_items(order_id);
CREATE INDEX idx_order_items_product_id ON order_items(product_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_categories_parent_id ON categories(parent_id);

+ в продукте хранить id корневой директории, тогда не придется рекурсивно искать корневую директорию
поиск сведется к простой строчке
JOIN categories root_cat
  ON root_cat.id = p.root_category_id