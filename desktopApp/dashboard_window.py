from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QMessageBox, QTableWidget, QTableWidgetItem, QDialog, QLineEdit
)
from api_client import APIClient

class MainWindow(QMainWindow):
    def __init__(self, token):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.setGeometry(100, 100, 600, 400)
        self.api_client = APIClient(token)

        self.init_ui()

    def init_ui(self):
        """Initialize the main UI components."""
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        self.create_greeting_label()
        self.create_users_table()
        self.create_buttons()

    def create_greeting_label(self):
        """Create a greeting label."""
        self.greeting_label = QLabel("Welcome to the Dashboard!")
        self.layout.addWidget(self.greeting_label)

    def create_users_table(self):
        """Create a table to display user data."""
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)  # Email, First Name, Last Name, Phone, Edit
        self.users_table.setHorizontalHeaderLabels(["Email", "First Name", "Last Name", "Phone", "Edit"])
        self.layout.addWidget(self.users_table)

    def create_buttons(self):
        """Create buttons for user interaction."""
        self.fetch_users_button = QPushButton("Fetch Users")
        self.fetch_users_button.clicked.connect(self.fetch_users)
        self.layout.addWidget(self.fetch_users_button)

        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.logout)
        self.layout.addWidget(self.logout_button)

    def fetch_users(self):
        """Fetch users from the API and populate the table."""
        try:
            response = self.api_client.fetch_users()
            if response.status_code == 200:
                users = response.json()
                self.display_users(users)
            else:
                QMessageBox.warning(self, "Error", "Failed to fetch users.")
        except ConnectionError as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_users(self, users):
        """Populate the table with user data."""
        self.users_table.setRowCount(len(users))  # Adjust the row count to the number of users

        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user.get("email", "")))
            self.users_table.setItem(row, 1, QTableWidgetItem(user.get("first_name", "")))
            self.users_table.setItem(row, 2, QTableWidgetItem(user.get("last_name", "")))
            self.users_table.setItem(row, 3, QTableWidgetItem(user.get("phone", "")))

            # Add an "Edit" button
            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda checked, row=row: self.edit_user_data(row))
            self.users_table.setCellWidget(row, 4, edit_button)

    def edit_user_data(self, row):
        """Open a dialog to edit user data."""
        email = self.users_table.item(row, 0).text()
        first_name = self.users_table.item(row, 1).text()
        last_name = self.users_table.item(row, 2).text()
        phone = self.users_table.item(row, 3).text()

        self.edit_window = EditUserWindow(self.api_client, email, first_name, last_name, phone)
        self.edit_window.show()

    def logout(self):
        """Log out the user and close the window."""
        QMessageBox.information(self, "Logged Out", "You have been logged out.")
        self.close()


class EditUserWindow(QDialog):
    def __init__(self, api_client, email, first_name, last_name, phone):
        super().__init__()
        self.setWindowTitle("Edit User Data")
        self.setGeometry(100, 100, 400, 300)

        self.api_client = api_client
        self.email = email

        layout = QVBoxLayout()

        # Editable fields
        self.first_name_label = QLabel("First Name:")
        self.first_name_input = QLineEdit(first_name)
        layout.addWidget(self.first_name_label)
        layout.addWidget(self.first_name_input)

        self.last_name_label = QLabel("Last Name:")
        self.last_name_input = QLineEdit(last_name)
        layout.addWidget(self.last_name_label)
        layout.addWidget(self.last_name_input)

        self.phone_label = QLabel("Phone:")
        self.phone_input = QLineEdit(phone)
        layout.addWidget(self.phone_label)
        layout.addWidget(self.phone_input)

        # Save button
        self.save_button = QPushButton("Save Changes")
        self.save_button.clicked.connect(self.save_changes)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def save_changes(self):
        """Save the edited user data."""
        first_name = self.first_name_input.text()
        last_name = self.last_name_input.text()
        phone = self.phone_input.text()

        if not first_name or not last_name or not phone:
            QMessageBox.warning(self, "Error", "Please fill in all fields!")
            return

        # Call the API to update the user data
        response = self.api_client.update_user(self.email, first_name, last_name, phone)
        if response.status_code == 200:
            QMessageBox.information(self, "Success", "User data updated successfully!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Failed to update user data.")
