CREATE TABLE Products (
    product_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    name VARCHAR(100),
    description TEXT NULL,
    price DECIMAL(10, 2),
    stock INT,
    category_id INT,
    image_url VARCHAR(255) NULL,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES Categories(category_id)
);