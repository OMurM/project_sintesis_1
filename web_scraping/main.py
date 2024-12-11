import requests
import pandas as pd
from bs4 import BeautifulSoup

# Función para obtener los productos de la página web
def obtener_productos(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        productos = soup.find_all('div', class_='product')  # Asegúrate de que el selector es correcto
        return productos
    else:
        print(f"Error al acceder a la página: {url}")
        return []

# Función para extraer la información del producto
def extraer_datos_producto(producto):
    try:
        nombre = producto.find('h2', class_='product-title').text.strip()
        precio_descuento = producto.find('span', class_='discount-price').text.strip()
        precio_original = producto.find('span', class_='original-price').text.strip()
        imagen_url = producto.find('img')['src']
        return {
            'Nombre': nombre,
            'Precio Descuento': precio_descuento,
            'Precio Original': precio_original,
            'Imagen URL': imagen_url
        }
    except Exception as e:
        print(f"Error al extraer datos de un producto: {e}")
        return None

# URL de PC Componentes (ajusta según lo necesario)
url = 'https://www.pccomponentes.com/tarjetas-graficas'
productos = obtener_productos(url)

# Extraer los datos de los productos y almacenarlos en una lista
productos_data = []
for producto in productos:
    datos = extraer_datos_producto(producto)
    if datos:
        productos_data.append(datos)

# Guardar los datos en un archivo Excel
df = pd.DataFrame(productos_data)
df.to_excel('productos_pc_componentes.xlsx', index=False)
