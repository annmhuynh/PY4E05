USE Olist

-- Câu 1 — Dễ
-- Đếm số đơn hàng theo từng bang (state) của khách hàng
-- Gợi ý: JOIN orders với customers, GROUP BY customer_state
/*
SELECT cust.customer_state AS State, COUNT(order_id) AS TotalOrders
FROM olist_orders_dataset ors
JOIN olist_customers_dataset cust ON ors.customer_id = cust.customer_id
GROUP BY cust.customer_state
*/

-- Câu 2 — Dễ-Trung
-- Tổng doanh thu theo từng danh mục sản phẩm (product_category_name)
-- Gợi ý: JOIN order_items → products, GROUP BY product_category_name, SUM price
/*
SELECT PD.product_category_name AS Category_name, ROUND(SUM(PMT.payment_value),2) AS Amount
FROM olist_orders_dataset O
JOIN olist_order_items_dataset PDI ON O.order_id = PDI.order_id
JOIN olist_products_dataset PD ON PD.product_id = PDI.product_id
JOIN olist_order_payments_dataset PMT ON O.order_id = PMT.order_id
WHERE O.order_status NOT IN ('cancelled', 'unavailable')
GROUP BY PD.product_category_name
*/
-- Câu 3 — Trung
-- Top 10 seller có tổng doanh thu cao nhất, kèm theo số đơn hàng của mỗi seller
-- Gợi ý: JOIN order_items với sellers, GROUP BY seller_id, dùng SUM và COUNT, ORDER BY + LIMIT
/*
WITH T10S AS (
    SELECT OI.seller_id
    FROM olist_order_items_dataset OI
    JOIN olist_order_payments_dataset PMT ON OI.order_id = PMT.order_id
    GROUP BY OI.seller_id
    ORDER BY SUM(PMT.payment_value) DESC
    LIMIT 10
),
MOPS AS (
    SELECT OI.seller_id,
           OI.order_id,
           SUM(PMT.payment_value) AS OrderAmount
    FROM olist_order_items_dataset OI
    JOIN olist_order_payments_dataset PMT ON OI.order_id = PMT.order_id
    GROUP BY OI.seller_id, OI.order_id
)
SELECT T10S.seller_id AS Seller,
       MOPS.order_id AS MaxSellerOrder
FROM T10S
JOIN MOPS ON T10S.seller_id = MOPS.seller_id
WHERE MOPS.OrderAmount = (
    SELECT MAX(OrderAmount)
    FROM MOPS M
    WHERE M.seller_id = T10S.seller_id
);
*/
-- Câu 4 — Trung-Khó
-- Số lượng đơn hàng và điểm review trung bình theo từng tháng trong năm 2018
-- Gợi ý: JOIN orders với order_reviews, GROUP BY tháng (dùng YEAR + MONTH hoặc DATE_FORMAT), lọc năm 2018
/*
SELECT DATE_FORMAT(O.order_purchase_timestamp, '%Y-%m') AS SalesMonth, COUNT(O.order_id) AS TotalOrder, AVG(R.review_score) AS AvgReviewScore
FROM olist_orders_dataset O
JOIN olist_order_reviews_dataset R ON O.order_id = R.order_id
WHERE YEAR(order_purchase_timestamp) = 2018
GROUP BY SalesMonth
ORDER BY SalesMonth
*/

-- Câu 5 — Khó
-- Danh sách các danh mục sản phẩm có điểm review trung bình dưới 3.5 và có ít nhất 100 đơn hàng
/*
SELECT PD.product_category_name AS product, AVG(R.review_score) AS AvgReviewScore, COUNT(O.order_id) AS TotalOrder
FROM olist_order_reviews_dataset R
JOIN olist_orders_dataset O ON R.order_id = O.order_id
JOIN olist_order_items_dataset OI ON OI.order_id = O.order_id
JOIN olist_products_dataset PD ON PD.product_id = OI.product_id
GROUP BY product
HAVING AvgReviewScore < 3.5 AND TotalOrder >= 100
*/

-- Câu 6 — Trung
-- Mỗi phương thức thanh toán (payment_type) có bao nhiêu đơn hàng và giá trị thanh toán trung bình là bao nhiêu?
-- Gợi ý: JOIN orders với order_payments, GROUP BY payment_type, dùng COUNT và AVG
/*
SELECT DISTINCT PMT.payment_type AS PaymentMethod, COUNT(O.order_id) AS TotalOrders, ROUND(AVG(PMT.payment_value),2) AS AvgPayment
FROM olist_order_payments_dataset PMT
JOIN olist_orders_dataset O ON PMT.order_id = O.order_id
GROUP BY PMT.payment_type
*/
-- Câu 7 — Trung
-- Thời gian giao hàng trung bình (tính bằng ngày) theo từng bang của seller
-- Gợi ý: JOIN orders với order_items → sellers, tính DATEDIFF giữa order_delivered_customer_date và order_purchase_timestamp, GROUP BY seller_state
/*
SELECT DISTINCT S.seller_state AS SelleerState, AVG(DATEDIFF(O.order_purchase_timestamp,O.order_delivered_customer_date)) AS AvgDeliveryLeadtime
FROM olist_orders_dataset O
JOIN olist_order_items_dataset OIT ON O.order_id = OIT.order_id
JOIN olist_sellers_dataset S ON OIT.seller_id = S.seller_id
GROUP BY S.seller_state
*/

-- Câu 8 — Trung-Khó
-- Top 5 khách hàng mua nhiều đơn hàng nhất, hiển thị customer_city, customer_state và tổng số đơn
-- Gợi ý: JOIN orders với customers, GROUP BY customer_unique_id, ORDER BY COUNT DESC, LIMIT 5

-- Câu 9 — Khó
-- Số seller hoạt động (có ít nhất 1 đơn hàng) theo từng tháng trong năm 2017
-- Gợi ý: JOIN order_items với orders, lọc năm 2017, GROUP BY tháng, dùng COUNT(DISTINCT seller_id)

-- Câu 10 — Khó
-- So sánh doanh thu trung bình mỗi đơn hàng giữa các bang của khách hàng — chỉ lấy những bang có trên 500 đơn hàng, sắp xếp doanh thu trung bình giảm dần
-- Gợi ý: JOIN orders → order_items → customers, GROUP BY customer_state, HAVING COUNT > 500, tính AVG của tổng price mỗi đơn, ORDER BY DESC