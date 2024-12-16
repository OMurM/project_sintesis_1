from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, primary_key=True, autoincrement=True, unique=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'phone': self.phone,
            'first_name': self.first_name,
            'last_name': self.last_name
        }

class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), nullable=True)

class Product(db.Model):
    __tablename__ = 'products'
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)  # Ensure this column is defined
    price = db.Column(db.Numeric(10, 2), nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'))
    image_id = db.Column(db.Integer, db.ForeignKey('images.image_id'), nullable=True)
    offer = db.Column(db.Boolean, default=False)

    def serialize(self):
        return {
            'product_id': self.product_id,
            'name': self.name,
            'description': self.description,
            'price': str(self.price),
            'stock': self.stock,
            'category_id': self.category_id,
            'image_id': self.image_id,
            'offer': self.offer
        }
    
class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    order_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Enum('pending', 'shipped', 'delivered', 'canceled'), nullable=False)
    total = db.Column(db.Numeric(10, 2), nullable=False)
    shipping_address = db.Column(db.Text, nullable=True)

class OrderDetail(db.Model):
    __tablename__ = 'order_details'
    detail_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    review_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=True)
    review_date = db.Column(db.DateTime, default=db.func.current_timestamp())

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    supplier_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(100), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    address = db.Column(db.Text, nullable=True)

class Purchase(db.Model):
    __tablename__ = 'purchases'
    purchase_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.supplier_id'))
    product_id = db.Column(db.Integer, db.ForeignKey('products.product_id'))
    quantity = db.Column(db.Integer, nullable=False)
    purchase_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.Enum('pending', 'completed'), nullable=False)

class Payment(db.Model):
    __tablename__ = 'payments'
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.order_id'))
    payment_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    payment_method = db.Column(db.Enum('card', 'paypal', 'transfer'), nullable=False)
    status = db.Column(db.Enum('completed', 'failed'), nullable=False)

class Image(db.Model):
    __tablename__ = 'images'
    image_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    type = db.Column(db.String(100), nullable=True)
    description = db.Column(db.Text, nullable=True)
    creation_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    filename = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(256), nullable=False)

    def serialize(self):
        return {
            'image_id': self.image_id,
            'type': self.type,
            'description': self.description,
            'creation_date': self.creation_date,
            'filename': self.filename,
            'url': self.url
        }