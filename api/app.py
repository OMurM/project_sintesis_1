from flask import Config, Flask, send_from_directory, jsonify
from models import db, Image
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

IMAGE_DIRECTORY = '/home/2DAM/images'

@app.route('/image/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get(image_id)
    
    if image:
        image_path = os.path.join(IMAGE_DIRECTORY, image.filename)
        
        if os.path.exists(image_path):
            return send_from_directory(IMAGE_DIRECTORY, image.filename)
        else:
            return jsonify({"error": "Image file not found"}), 404
    else:
        return jsonify({"error": "Image not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
