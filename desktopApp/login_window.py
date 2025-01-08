from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QLineEdit, QPushButton, QVBoxLayout, QWidget, QMessageBox
)
from api_client import APIClient
from main_window import MainWindow

class LoginWindow(QMainWindow):
    
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Page")
        self.setGeometry(100, 100, 400, 300)
        self.api_client = APIClient()

        # Main widget
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        # Layout
        layout = QVBoxLayout()

        # Email field
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        # Password field
        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        # Login button
        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.handle_login)
        layout.addWidget(self.login_button)

        self.central_widget.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text()
        password = self.password_input.text()

        if not email or not password:
            QMessageBox.warning(self, "Error", "Please enter email and password!")
            return

        try:
            response = self.api_client.login(email, password)
            if response.status_code == 200:
                data = response.json()
                token = data.get("access_token")
                QMessageBox.information(self, "Success", "Login successful!")
                self.open_dashboard(token)
            else:
                error_message = response.json().get("message", "Login failed!")
                QMessageBox.warning(self, "Error", error_message)
        except ConnectionError as e:
            QMessageBox.critical(self, "Error", str(e))

    def open_dashboard(self, token):
        self.dashboard = MainWindow(token)
        self.dashboard.show()
        self.close()
