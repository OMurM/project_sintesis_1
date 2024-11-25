CREATE TABLE Categories (
    category_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    name VARCHAR(100),
    description TEXT NULL,
    creation_date DATETIME DEFAULT CURRENT_TIMESTAMP
);