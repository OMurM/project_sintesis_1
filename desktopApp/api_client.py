import requests

API_URL = "http://localhost:5000"

class APIClient:
    def __init__(self, token=None):
        self.token = token

    def login(self, email, password):
        """Login method to authenticate a user and get access token."""
        try:
            response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def register_user(self, email, password, first_name, last_name, phone=None):
        """Register a new user."""
        try:
            response = requests.post(f"{API_URL}/register", json={
                "email": email,
                "password": password,
                "first_name": first_name,
                "last_name": last_name,
                "phone": phone
            })
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def fetch_users(self):
        """Fetch a list of users."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(f"{API_URL}/users", headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def get_user_by_email_or_id(self, email=None, user_id=None):
        """Fetch a specific user by email or user ID."""
        params = {}
        if email:
            params['email'] = email
        if user_id:
            params['id'] = user_id

        try:
            response = requests.get(f"{API_URL}/users/find", params=params)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def update_user(self, email, user_data):
        """Send a PUT request to update user details."""
        url = f"{API_URL}/users/{email}"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.put(url, json=user_data, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def delete_user(self, email):
        """Delete a user by email."""
        url = f"{API_URL}/users/{email}"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.delete(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    # Product Management
    def fetch_products(self):
        """Fetch all products along with their images."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(f"{API_URL}/images/all_products", headers=headers)
            if response.status_code == 200:
                return response.json()  # Return the parsed JSON data (a list of products)
            else:
                return []  # If the response code is not 200, return an empty list
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def get_product_by_name(self, product_name):
        """Fetch a product by its name."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.get(f"{API_URL}/products/{product_name}", headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def create_product(self, product_data):
        """Send a POST request to create a new product."""
        url = f"{API_URL}/products"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.post(url, json=product_data, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def update_product(self, product_name, product_data):
        """Send a PUT request to update product details."""
        url = f"{API_URL}/products/{product_name}"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.put(url, json=product_data, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def delete_product(self, product_name):
        """Delete a product by its name."""
        url = f"{API_URL}/products/{product_name}"
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.delete(url, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    # Token management
    def refresh_token(self):
        """Refresh the JWT token."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.post(f"{API_URL}/refresh", headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")
