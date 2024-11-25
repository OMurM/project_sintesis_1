CREATE TABLE Purchases (
    purchase_id INT PRIMARY KEY AUTO_INCREMENT UNIQUE,
    supplier_id INT,
    product_id INT,
    quantity INT,
    purchase_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    status ENUM('pending', 'completed'),
    FOREIGN KEY (supplier_id) REFERENCES Suppliers(supplier_id),
    FOREIGN KEY (product_id) REFERENCES Products(product_id)
);