CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    email VARCHAR(100) UNIQUE,
    password_hash VARCHAR(255),
    phone VARCHAR(20) NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100)
);