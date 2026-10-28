-- SQL Analytics Queries for Customer Shopping Behaviour (SQLite Dialect)
-- Demonstrating: Joins, Aggregations, Group By, Having, CTEs, Window Functions, Subqueries

-- Q1. Total revenue and customer count by gender (JOIN, GROUP BY, SUM)
SELECT 
    c.gender AS Gender,
    COUNT(DISTINCT c.customer_id) AS total_customers,
    ROUND(SUM(o.purchase_amount), 2) AS total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.gender;

-- Q2. Customers who used a discount but still spent above average purchase amount (JOIN, Subquery, WHERE)
SELECT 
    c.customer_id,
    c.age,
    c.gender,
    o.item_purchased,
    o.purchase_amount
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
WHERE o.discount_applied = 'Yes' 
  AND o.purchase_amount >= (SELECT AVG(purchase_amount) FROM orders)
ORDER BY o.purchase_amount DESC;

-- Q3. Top 5 products with highest average review rating (GROUP BY, AVG, ORDER BY, LIMIT)
SELECT 
    item_purchased,
    ROUND(AVG(review_rating), 2) AS average_rating,
    COUNT(*) AS total_reviews
FROM orders
GROUP BY item_purchased
ORDER BY average_rating DESC
LIMIT 5;

-- Q4. Compare average purchase amount and volume between Standard and Express shipping (WHERE IN, GROUP BY, AVG)
SELECT 
    shipping_type,
    COUNT(*) AS order_count,
    ROUND(AVG(purchase_amount), 2) AS average_amount,
    ROUND(SUM(purchase_amount), 2) AS total_amount
FROM orders
WHERE shipping_type IN ('Standard', 'Express')
GROUP BY shipping_type;

-- Q5. Spend comparison between subscribed and non-subscribed customers (JOIN, GROUP BY, COUNT, AVG, SUM)
SELECT 
    c.subscription_status,
    COUNT(c.customer_id) AS total_customers,
    ROUND(AVG(o.purchase_amount), 2) AS average_purchase,
    ROUND(SUM(o.purchase_amount), 2) AS total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.subscription_status
ORDER BY total_revenue DESC;

-- Q6. Products with highest discount rate (Conditional Aggregation with CASE WHEN)
SELECT 
    item_purchased,
    COUNT(*) AS total_orders,
    SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) AS discounted_orders,
    ROUND(100.0 * SUM(CASE WHEN discount_applied = 'Yes' THEN 1 ELSE 0 END) / COUNT(*), 2) AS discount_rate_pct
FROM orders
GROUP BY item_purchased
ORDER BY discount_rate_pct DESC
LIMIT 5;

-- Q7. Customer segmentation by previous purchase history (CTE, CASE WHEN, GROUP BY)
WITH customer_type AS (
    SELECT 
        customer_id,
        previous_purchases,
        CASE 
            WHEN previous_purchases = 1 THEN 'New'
            WHEN previous_purchases BETWEEN 2 AND 10 THEN 'Returning'
            ELSE 'Loyal'
        END AS customer_segment
    FROM customers
)
SELECT 
    customer_segment,
    COUNT(*) AS number_of_customers,
    ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM customer_type), 2) AS percentage_share
FROM customer_type
GROUP BY customer_segment
ORDER BY number_of_customers DESC;

-- Q8. Top 3 most purchased products within each product category (CTE, Window Function: ROW_NUMBER)
WITH item_counts AS (
    SELECT 
        category,
        item_purchased,
        COUNT(*) AS total_orders,
        ROW_NUMBER() OVER (PARTITION BY category ORDER BY COUNT(*) DESC) AS item_rank
    FROM orders
    GROUP BY category, item_purchased
)
SELECT 
    item_rank,
    category,
    item_purchased,
    total_orders
FROM item_counts
WHERE item_rank <= 3
ORDER BY category, item_rank;

-- Q9. Repeat buyers (>5 previous purchases) and subscription distribution (WHERE, GROUP BY)
SELECT 
    subscription_status,
    COUNT(customer_id) AS repeat_buyers,
    ROUND(100.0 * COUNT(customer_id) / (SELECT COUNT(*) FROM customers WHERE previous_purchases > 5), 2) AS percentage_share
FROM customers
WHERE previous_purchases > 5
GROUP BY subscription_status;

-- Q10. Revenue contribution by age group (JOIN, GROUP BY, ORDER BY)
SELECT 
    c.age_group,
    COUNT(o.order_id) AS total_orders,
    ROUND(SUM(o.purchase_amount), 2) AS total_revenue,
    ROUND(AVG(o.purchase_amount), 2) AS avg_order_value
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
GROUP BY c.age_group
ORDER BY total_revenue DESC;

-- Q11. Product categories with high order volume and spend above category average (HAVING clause)
SELECT 
    category,
    COUNT(*) AS total_orders,
    ROUND(AVG(purchase_amount), 2) AS avg_purchase_amount,
    ROUND(SUM(purchase_amount), 2) AS total_category_revenue
FROM orders
GROUP BY category
HAVING COUNT(*) > 500 AND AVG(purchase_amount) > 55.0
ORDER BY total_category_revenue DESC;

