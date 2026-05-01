-- V3__add_indexes.sql
-- Adds indexes for common query patterns and a view for reporting

CREATE INDEX idx_products_category ON products (category);
CREATE INDEX idx_products_price    ON products (price);

CREATE VIEW category_summary AS
SELECT
    category,
    COUNT(*)            AS product_count,
    ROUND(AVG(price), 2) AS avg_price,
    MIN(price)          AS min_price,
    MAX(price)          AS max_price
FROM products
GROUP BY category
ORDER BY avg_price DESC;
