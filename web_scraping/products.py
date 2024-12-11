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
        discounted_price_str = row['Price'].replace('€', '').replace(',', '.').strip()

        try:
            discounted_price = float(discounted_price_str)
            if discounted_price <= 0:
                print(f"Precio no válido para el producto {product_name}. Saltando...")
                continue
        except ValueError:
            print(f"Error al convertir precios para el producto {product_name}. Saltando...")
            continue

        description = f"Precio: {discounted_price}€"
        stock = 100  # Ajusta este valor según lo necesites

        cursor.execute("SELECT product_id FROM products WHERE name = %s AND category_id = %s", (product_name, category_id))
        existing_product = cursor.fetchone()

        if not existing_product:
            cursor.execute(""" 
                INSERT INTO products (name, price, stock, category_id, image_id)
                VALUES (%s, %s, %s, %s, %s)
            """, (product_name, discounted_price, stock, category_id, image_id))
            conn.commit()
            product_id = cursor.lastrowid
            print(f"Insertado producto: {product_name} con ID {product_id}")
        else:
            print(f"Producto existente: {product_name} con ID {existing_product[0]}")

conn.close()
print("Importación completada exitosamente.")
