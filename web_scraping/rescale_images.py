import mysql.connector
import requests
from PIL import Image
from io import BytesIO

# Conexión a la base de datos MySQL
conn = mysql.connector.connect(
    host="192.168.1.41",
    user="oscar",
    password="My5q1!p@ss2024#",
    database="sintesis_project"
)
cursor = conn.cursor()

# Obtener todas las imágenes de la base de datos
cursor.execute("SELECT image_id, url FROM images WHERE type = 'product'")
images = cursor.fetchall()

print(f"Imágenes encontradas: {len(images)}")

# Función para reescalar la imagen
def upscale_image(image_url):
    response = requests.get(image_url)
    img = Image.open(BytesIO(response.content))

    # Reescalar la imagen (por ejemplo, duplicando el tamaño)
    img_upscaled = img.resize((img.width * 2, img.height * 2))
    return img_upscaled

# Procesar cada imagen
for image_id, image_url in images:
    print(f"Procesando imagen: {image_url}")

    # Reescalar la imagen
    upscaled_img = upscale_image(image_url)

    # Guardar la imagen reescalada en un archivo temporal
    temp_image_path = f"temp_{image_id}.png"
    upscaled_img.save(temp_image_path)

    # Convertir la imagen reescalada a formato binario para actualizar en la base de datos
    with open(temp_image_path, 'rb') as f:
        img_data = f.read()

    # Actualizar la imagen en la base de datos
    cursor.execute("UPDATE images SET image_data = %s WHERE image_id = %s", (img_data, image_id))
    conn.commit()

    print(f"Imagen con ID {image_id} actualizada en la base de datos.")

# Cerrar la conexión
conn.close()
print("Proceso de actualización completado.")
