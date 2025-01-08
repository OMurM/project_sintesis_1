from PyQt5.QtWidgets import QDialog, QLabel, QLineEdit, QPushButton, QVBoxLayout, QMessageBox

class CreateUserWindow(QDialog):
    def __init__(self, api_client):
        super().__init__()
        self.setWindowTitle("Create New User")
        self.setGeometry(100, 100, 400, 300)

        self.api_client = api_client

        layout = QVBoxLayout()

        # Fields
        self.email_label = QLabel("Email:")
        self.email_input = QLineEdit()
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)

        self.first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit()
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_input)

        self.last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit()
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_input)

        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit()
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        self.password_label = QLabel("Password:")
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)

        self.save_button = QPushButton("Save New User")
        self.save_button.clicked.connect(self.save_new_user)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_new_user(self):
        email = self.email_input.text()
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone = self.phone_input.text()
        password = self.password_input.text()

        if not email or not first_name or not last_name or not password:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        response = self.api_client.register_user(email, password, first_name, last_name, phone)
        if response.status_code == 201:
            QMessageBox.information(self, "Success", "User created successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Failed to create user.")
