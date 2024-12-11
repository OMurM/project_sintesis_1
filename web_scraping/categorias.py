import csv
import mysql.connector

conn = mysql.connector.connect(
    host="192.168.1.41",
    user="oscar",
    password="My5q1!p@ss2024#",
    database="sintesis_project"
)

cursor = conn.cursor()

# Leer el archivo CSV con delimitador ";"
with open('productos.csv', 'r', encoding='latin-1') as file:
    csv_reader = csv.DictReader(file, delimiter=';')  # Especifica el delimitador correcto
    print(f"Encabezados detectados: {csv_reader.fieldnames}")  # Debug: Verifica los encabezados

    for row in csv_reader:
        category_name = row['Category']  # Ahora debería funcionar

        cursor.execute("SELECT category_id FROM categories WHERE name = %s", (category_name,))
        category = cursor.fetchone()

        if not category:
            cursor.execute("""
                INSERT INTO categories (name)
                VALUES (%s)
            """, (category_name,))
            conn.commit()

conn.close()
