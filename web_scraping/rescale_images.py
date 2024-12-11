import mysql.connector
import os
import requests
from PIL import Image
from io import BytesIO
from datetime import datetime

# MySQL database connection setup
conn = mysql.connector.connect(
    host="192.168.1.41",
    user="oscar",
    password="My5q1!p@ss2024#",
    database="sintesis_project"
)

cursor = conn.cursor()

# Directory where images will be saved
IMAGE_DIRECTORY = '/home/2DAM/images'
if not os.path.exists(IMAGE_DIRECTORY):
    os.makedirs(IMAGE_DIRECTORY)

# Fetch all images from the database (Image ID and URL)
cursor.execute("SELECT image_id, url FROM images")
images = cursor.fetchall()

# Function to resize images
def resize_image(image_data, output_path, size=(150, 150)):
    img = Image.open(BytesIO(image_data))
    img = img.resize(size, Image.ANTIALIAS)  # Resize the image
    img.save(output_path)

# Process each image
for image_id, url in images:
    try:
        # Fetch the image from the URL
        response = requests.get(url)
        if response.status_code == 200:
            image_data = response.content
            # Create a filename for the resized image
            filename = f"{image_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            file_path = os.path.join(IMAGE_DIRECTORY, filename)
            
            # Resize and save the image
            resize_image(image_data, file_path)
            
            # Update the image URL in the database (new path on the server)
            new_url = f"http://your-server-ip/images/{filename}"  # The new URL
            cursor.execute("UPDATE images SET url = %s WHERE image_id = %s", (new_url, image_id))
            conn.commit()
            print(f"Image {image_id} resized and URL updated to {new_url}")
        else:
            print(f"Failed to download image {image_id} from {url}")
    except Exception as e:
        print(f"Error processing image {image_id}: {e}")

conn.close()

print("Image resizing and URL updating complete.")
