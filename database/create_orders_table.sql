CREATE TABLE Orders (
    order_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    user_id INT,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'shipped', 'delivered', 'canceled'),
    total DECIMAL(10, 2),
    shipping_address TEXT NULL,
    FOREIGN KEY (user_id) REFERENCES Users(user_id)
);