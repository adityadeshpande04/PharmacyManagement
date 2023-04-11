/* stock of medicine X present in the inventory */
SELECT SUM(quantity) AS stock_level
FROM inventory
JOIN medications ON inventory.medication_id = medications.id
WHERE medications.name = 'X';

/* units of the medicine X sold in last 1 month */
SELECT SUM(quantity) AS units_sold
FROM sales_records
JOIN medications ON sales_records.medication_id = medications.id
WHERE medications.name = 'X'
AND date_sold >= DATE_SUB(NOW(), INTERVAL 1 MONTH);

/* sales trends of a medicine X in the last 6 months */
SELECT YEAR(date_sold) AS year, MONTH(date_sold) AS month, SUM(quantity) AS units_sold
FROM sales_records
JOIN medications ON sales_records.medication_id = medications.id
WHERE medications.name = 'X'
AND date_sold >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
GROUP BY YEAR(date_sold), MONTH(date_sold)
ORDER BY year ASC, month ASC;

/* medicines that will expire in the next 30 days */
SELECT name, expiration_date
FROM inventory
JOIN medications ON inventory.medication_id = medications.id
WHERE expiration_date BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)
ORDER BY expiration_date ASC;

/* medication that are currently out of stock */
SELECT name
FROM medications
LEFT JOIN inventory ON medications.id = inventory.medication_id
WHERE quantity IS NULL OR quantity = 0;

/* average monthly sales revenue */
SELECT YEAR(date_sold) AS year, MONTH(date_sold) AS month, SUM(price * quantity) AS monthly_sales_revenue
FROM sales_records
JOIN sales ON sales_records.id = sales.sales_record_id
GROUP BY YEAR(date_sold), MONTH(date_sold);

/* total inventory value */
SELECT SUM(quantity * selling_price) AS total_inventory_value
FROM inventory;

/* medications that are sold most frequently */
SELECT name, SUM(quantity) AS total_quantity_sold
FROM medications
JOIN sales_records ON medications.id = sales_records.medication_id
GROUP BY medication_id
ORDER BY total_quantity_sold DESC;

/* medication that have highest profit margin */
SELECT name, AVG(price - selling_price) AS avg_profit_margin
FROM medications
JOIN sales_records ON medications.id = sales_records.medication_id
JOIN sales ON sales_records.id = sales.sales_record_id
JOIN inventory ON medications.id = inventory.medication_id
WHERE sales_records.date_sold >= DATE_SUB(NOW(), INTERVAL 6 MONTH)
GROUP BY name
ORDER BY avg_profit_margin DESC;

/* medication that have lowest turnover rate */
SELECT name, (SUM(quantity) / DATEDIFF(NOW(), MIN(date_added))) AS turnover_rate
FROM medications
JOIN inventory ON medications.id = inventory.medication_id
GROUP BY medication_id
ORDER BY turnover_rate ASC;





