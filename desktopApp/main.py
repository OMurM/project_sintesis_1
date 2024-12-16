import sys
import requests
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QLineEdit, QLabel, QTableWidget, QTableWidgetItem

API_URL = "http://localhost:5000"

class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        # Set up the window
        self.setWindowTitle('PyQt5 with API')
        self.resize(400, 300)

        # Create UI elements
        self.email_input = QLineEdit(self)
        self.password_input = QLineEdit(self)
        self.name_input = QLineEdit(self)
        self.first_name_input = QLineEdit(self)
        self.last_name_input = QLineEdit(self)
        self.phone_input = QLineEdit(self)
        self.add_button = QPushButton('Register', self)
        self.login_button = QPushButton('Login', self)
        self.load_button = QPushButton('Load Users', self)
        self.table = QTableWidget(self)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Email:'))
        layout.addWidget(self.email_input)
        layout.addWidget(QLabel('Password:'))
        layout.addWidget(self.password_input)
        layout.addWidget(QLabel('First Name:'))
        layout.addWidget(self.first_name_input)
        layout.addWidget(QLabel('Last Name:'))
        layout.addWidget(self.last_name_input)
        layout.addWidget(QLabel('Phone:'))
        layout.addWidget(self.phone_input)
        layout.addWidget(self.add_button)
        layout.addWidget(self.login_button)
        layout.addWidget(self.load_button)
        layout.addWidget(self.table)

        self.setLayout(layout)

        # Connect buttons to functions
        self.add_button.clicked.connect(self.register_user)
        self.login_button.clicked.connect(self.login_user)
        self.load_button.clicked.connect(self.load_users)

    def api_request(self, method, endpoint, data=None, headers=None):
        url = f"{API_URL}/{endpoint}"
        if method == 'POST':
            response = requests.post(url, json=data, headers=headers)
        elif method == 'GET':
            response = requests.get(url, headers=headers)
        elif method == 'PUT':
            response = requests.put(url, json=data, headers=headers)
        elif method == 'DELETE':
            response = requests.delete(url, headers=headers)
        return response

    def register_user(self):
        data = {
            'email': self.email_input.text(),
            'password': self.password_input.text(),
            'first_name': self.first_name_input.text(),
            'last_name': self.last_name_input.text(),
            'phone': self.phone_input.text()
        }

        response = self.api_request('POST', 'register', data)
        if response.status_code == 201:
            print(f"User registered: {data['email']}")
        else:
            print(f"Error: {response.json()['message']}")

    def login_user(self):
        data = {
            'email': self.email_input.text(),
            'password': self.password_input.text()
        }

        response = self.api_request('POST', 'login', data)
        if response.status_code == 200:
            print(f"Login successful: {response.json()['user']['email']}")
            # Store the access token for further requests
            access_token = response.json()['access_token']
            print(f"Access Token: {access_token}")
            headers = {'Authorization': f'Bearer {access_token}'}
            # Perform further actions like loading user info, etc.
        else:
            print(f"Error: {response.json()['message']}")

    def load_users(self):
        response = self.api_request('GET', 'users')
        if response.status_code == 200:
            users = response.json()
            self.table.setRowCount(0)
            self.table.setColumnCount(3)
            self.table.setHorizontalHeaderLabels(['ID', 'Name', 'Email'])

            for row_num, user in enumerate(users):
                self.table.insertRow(row_num)
                self.table.setItem(row_num, 0, QTableWidgetItem(str(user['user_id'])))
                self.table.setItem(row_num, 1, QTableWidgetItem(user['first_name'] + ' ' + user['last_name']))
                self.table.setItem(row_num, 2, QTableWidgetItem(user['email']))
        else:
            print(f"Error: {response.status_code}")

def main():
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
