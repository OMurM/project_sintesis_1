import logging
from flask import request, jsonify
from . import main
from models import db, Image, Product

# Set up logging configuration
logging.basicConfig(level=logging.DEBUG)

# Endpoint to fetch the images on offer
@main.route('/images/on_offer', methods=['GET'])
def get_images_on_offer():
    # Join Product and Image tables
    products_on_offer = db.session.query(Product, Image).join(Image, Product.image_id == Image.image_id).filter(Product.offer == True).all()

    # Serialize the images
    images = []
    for product, image in products_on_offer:
        image_data = image.serialize()
        images.append(image_data)
        
    return jsonify(images), 200

# Endpoint to fetch all products and their images
@main.route('/images/all_products', methods=['GET'])
def get_all_products():
    # Join Product and Image tables without filtering by offer
    all_products = db.session.query(Product, Image).join(Image, Product.image_id == Image.image_id).all()

    # Serialize the products and their associated images
    products_with_images = []
    for product, image in all_products:
        product_data = product.serialize()
        image_data = image.serialize()
        
        product_data['image'] = image_data
        products_with_images.append(product_data)

    return jsonify(products_with_images), 200
