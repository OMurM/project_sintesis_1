CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    order_id INT,
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    amount DECIMAL(10, 2),
    payment_method ENUM('card', 'paypal', 'transfer'),
    status ENUM('completed', 'failed'),
    FOREIGN KEY (order_id) REFERENCES Orders(order_id)
);
