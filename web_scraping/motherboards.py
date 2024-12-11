import csv
import mysql.connector

# Conexión a MySQL
conn = mysql.connector.connect(
    host="192.168.1.41",
    user="oscar",
    password="My5q1!p@ss2024#",
    database="sintesis_project"
)

cursor = conn.cursor()

with open('motherboards.csv', 'r', encoding='latin-1') as file:
    csv_reader = csv.DictReader(file, delimiter=';')
    print(f"Encabezados detectados: {csv_reader.fieldnames}")

    for row in csv_reader:
        if not any(row.values()):
            continue

        category_name = row['Category'].strip()
        cursor.execute("SELECT category_id FROM categories WHERE name = %s", (category_name,))
        category = cursor.fetchone()

        if not category:
            cursor.execute("INSERT INTO categories (name) VALUES (%s)", (category_name,))
            conn.commit()
            category_id = cursor.lastrowid
            print(f"Insertada nueva categoría: {category_name} con ID {category_id}")
        else:
            category_id = category[0]
            print(f"Categoría existente: {category_name} con ID {category_id}")

        image_url = row['Image'].strip()
        cursor.execute("SELECT image_id FROM images WHERE url = %s", (image_url,))
        image = cursor.fetchone()

        if not image:
            filename = image_url.split('/')[-1]
            description = row['Product'].strip()
            cursor.execute(""" 
                INSERT INTO images (type, description, filename, url) 
                VALUES ('product', %s, %s, %s)
            """, (description, filename, image_url))
            conn.commit()
            image_id = cursor.lastrowid
            print(f"Insertada nueva imagen: {filename} con ID {image_id}")
        else:
            image_id = image[0]
            print(f"Imagen existente: {image_url} con ID {image_id}")

        product_name = row['Product'].strip()
        discounted_price_str = row['Discounted Price'].replace('€', '').replace(',', '.').strip() if row['Discounted Price'] else None
        original_price_str = row['Original Price'].replace('€', '').replace(',', '.').strip() if row['Original Price'] else None

        try:
            if discounted_price_str:
                discounted_price = float(discounted_price_str)
            if original_price_str:
                original_price = float(original_price_str)
        except ValueError:
            print(f"Error al convertir precios para el producto {product_name}. Saltando...")
            continue

        # Asignar el precio dependiendo de si hay descuento o no
        price = discounted_price if discounted_price_str else original_price

        description = f"Precio original: {original_price}€, Precio descontado: {discounted_price}€" if discounted_price_str else f"Precio: {original_price}€"
        stock = 100  # Puedes ajustar esto según tus necesidades

        cursor.execute("SELECT product_id FROM products WHERE name = %s AND category_id = %s", (product_name, category_id))
        existing_product = cursor.fetchone()

        if not existing_product:
            cursor.execute(""" 
                INSERT INTO products (name, description, price, stock, category_id, image_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (product_name, description, price, stock, category_id, image_id))
            conn.commit()
            product_id = cursor.lastrowid
            print(f"Insertado producto: {product_name} con ID {product_id}")
        else:
            print(f"Producto existente: {product_name} con ID {existing_product[0]}")

conn.close()
print("Importación completada exitosamente.")
