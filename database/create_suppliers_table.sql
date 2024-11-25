CREATE TABLE Suppliers (
    supplier_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    name VARCHAR(100),
    contact VARCHAR(100) NULL,
    phone VARCHAR(20) NULL,
    email VARCHAR(100) NULL,
    address TEXT NULL
);