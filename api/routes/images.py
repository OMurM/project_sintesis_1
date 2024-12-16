from flask import request, jsonify
from . import main
from models import db, Image, Product

# Endpoint to featch the images
@main.route('/images/on_offer', methods=['GET'])
def get_images_on_offer():
    # Join Porduct and Image tables
    products_on_offer = db.session.query(Product, Image).join(Image, Product.image_id == Image.image_id).filter(Product.offer == True).all()

    # Serialize the images
    images = []
    for product, image in products_on_offer:
        images.append(image.serialize())
    
    return jsonify(images), 200