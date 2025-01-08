from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QPushButton, QTableWidget, QTableWidgetItem,
    QLabel, QWidget, QMessageBox, QDialog, QLineEdit, QFormLayout, QInputDialog
)
from api_client import APIClient
from create_user_window import CreateUserWindow
import requests


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
        self.create_buttons()

    def create_greeting_label(self):
        """Create a greeting label."""
        self.greeting_label = QLabel("Welcome to the Dashboard!")
        self.layout.addWidget(self.greeting_label)

    def create_buttons(self):
        """Create buttons for user interaction."""
        self.fetch_users_button = QPushButton("Fetch Users")
        self.fetch_users_button.clicked.connect(self.fetch_users)
        self.layout.addWidget(self.fetch_users_button)

        self.create_user_button = QPushButton("Create New User")
        self.create_user_button.clicked.connect(self.create_new_user)
        self.layout.addWidget(self.create_user_button)

        self.fetch_products_button = QPushButton("Fetch Products")
        self.fetch_products_button.clicked.connect(self.fetch_products)
        self.layout.addWidget(self.fetch_products_button)

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
        except requests.ConnectionError as e:
            QMessageBox.critical(self, "Error", str(e))

    def fetch_products(self):
        """Fetch products from the API and display them."""
        try:
            response = self.api_client.fetch_products()
            if response:
                self.display_products(response)
            else:
                QMessageBox.warning(self, "Error", "Failed to fetch products.")
        except requests.ConnectionError as e:
            QMessageBox.critical(self, "Error", str(e))

    def display_users(self, users):
        """Populate the table with user data."""
        self.clear_tables()  # Hide any existing table

        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)  # Email, First Name, Last Name, Phone, Edit
        self.users_table.setHorizontalHeaderLabels(["Email", "First Name", "Last Name", "Phone", "Edit"])
        self.layout.addWidget(self.users_table)

        self.users_table.setRowCount(len(users))  # Adjust the row count to the number of users

        for row, user in enumerate(users):
            self.users_table.setItem(row, 0, QTableWidgetItem(user.get("email", "")))
            self.users_table.setItem(row, 1, QTableWidgetItem(user.get("first_name", "")))
            self.users_table.setItem(row, 2, QTableWidgetItem(user.get("last_name", "")))
            self.users_table.setItem(row, 3, QTableWidgetItem(user.get("phone", "")))

            edit_button = QPushButton("Edit")
            edit_button.clicked.connect(lambda checked, row=row: self.edit_user_data(row))
            self.users_table.setCellWidget(row, 4, edit_button)

    def display_products(self, products):
        """Populate the table with product data."""
        self.clear_tables()  # Hide any existing table

        self.products_table = QTableWidget()
        self.products_table.setColumnCount(3)  # Product Name, Description, Price
        self.products_table.setHorizontalHeaderLabels(["Product Name", "Description", "Price"])
        self.layout.addWidget(self.products_table)

        self.products_table.setRowCount(len(products))  # Adjust the row count to the number of products

        for row, product in enumerate(products):
            self.products_table.setItem(row, 0, QTableWidgetItem(product.get("name", "")))
            self.products_table.setItem(row, 1, QTableWidgetItem(product.get("description", "")))
            self.products_table.setItem(row, 2, QTableWidgetItem(str(product.get("price", ""))))

    def clear_tables(self):
        """Clear any existing tables from the layout."""
        for table_attr in ["users_table", "products_table"]:
            table = getattr(self, table_attr, None)
            if table:
                self.layout.removeWidget(table)
                table.deleteLater()
                setattr(self, table_attr, None)

    def edit_user_data(self, row):
        """Edit the user data in the specified row."""
        try:
            user = {
                "email": self.users_table.item(row, 0).text(),
                "first_name": self.users_table.item(row, 1).text(),
                "last_name": self.users_table.item(row, 2).text(),
                "phone": self.users_table.item(row, 3).text(),
            }

            self.edit_user_dialog = EditUserDialog(user)
            if self.edit_user_dialog.exec_():
                updated_user = self.edit_user_dialog.get_user_data()
                response = self.api_client.update_user(user["email"], updated_user)
                if response.status_code == 200:
                    QMessageBox.information(self, "Success", "User updated successfully.")
                    self.fetch_users()
                else:
                    QMessageBox.warning(self, "Error", f"Failed to update user: {response.text}")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")

    def create_new_user(self):
        """Open the Create User dialog."""
        self.create_user_window = CreateUserWindow(self.api_client)
        self.create_user_window.show()

    def logout(self):
        """Log out the user and close the window."""
        QMessageBox.information(self, "Logged Out", "You have been logged out.")
        self.close()


class EditUserDialog(QDialog):
    def __init__(self, user):
        super().__init__()
        self.setWindowTitle("Edit User")
        self.setGeometry(100, 100, 300, 200)
        self.user = user
        self.init_ui()

    def init_ui(self):
        """Initialize the edit user dialog components."""
        layout = QFormLayout()
        self.email_label = QLabel(self.user.get("email", ""))
        self.first_name_edit = QLineEdit(self.user.get("first_name", ""))
        self.last_name_edit = QLineEdit(self.user.get("last_name", ""))
        self.phone_edit = QLineEdit(self.user.get("phone", ""))

        layout.addRow("Email:", self.email_label)
        layout.addRow("First Name:", self.first_name_edit)
        layout.addRow("Last Name:", self.last_name_edit)
        layout.addRow("Phone:", self.phone_edit)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_user)
        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_user(self):
        """Save the updated user data."""
        self.user.update(
            first_name=self.first_name_edit.text(),
            last_name=self.last_name_edit.text(),
            phone=self.phone_edit.text(),
        )
        self.accept()

    def get_user_data(self):
        """Return the updated user data."""
        return self.user


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = MainWindow(token="your_api_token_here")
    window.show()
    sys.exit(app.exec_())
