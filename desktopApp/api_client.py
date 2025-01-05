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

    def update_user(self, user_id, email=None, password=None, first_name=None, last_name=None, phone=None):
        """Update a user's details."""
        headers = {"Authorization": f"Bearer {self.token}"}
        data = {}
        if email:
            data['email'] = email
        if password:
            data['password'] = password
        if first_name:
            data['first_name'] = first_name
        if last_name:
            data['last_name'] = last_name
        if phone:
            data['phone'] = phone
        
        try:
            response = requests.put(f"{API_URL}/users/{user_id}", json=data, headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")

    def refresh_token(self):
        """Refresh the JWT token."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response = requests.post(f"{API_URL}/refresh", headers=headers)
            return response
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"API connection error: {e}")
