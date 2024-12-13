import configparser
import logging
import os
import subprocess
import sys

from config import logs_file, file_exe_path

from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QHBoxLayout

logging.basicConfig(filename=logs_file,
                    level=logging.INFO,  # Log events with level INFO and higher
                    format='%(asctime)s - %(levelname)s - %(message)s')

class ResultWindow(QWidget):
    def __init__(self, message, result):
        super().__init__()

        # Set window properties
        self.setWindowTitle("Результат Аутентификации")
        self.setGeometry(100, 100, 300, 100)

        # Layout for the result window
        layout = QVBoxLayout()

        # Label for showing result message
        self.result_label = QLabel(message)
        if (result == False):
            self.result_label.setStyleSheet('color:red')
        else:
            self.result_label.setStyleSheet('color:green')
        layout.addWidget(self.result_label)

        # Close button
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)
        layout.addWidget(self.close_button)

        # Set layout for the window
        self.setLayout(layout)

        if (result == True):
            self.open_external_program()

    def open_external_program(self):
        try:
            # Path to the external executable file (change this to your executable file's path)
            exe_path = file_exe_path
            QTimer.singleShot(500, self.close)
            # Start the external .exe file
            subprocess.Popen([exe_path])

            # Log the event of opening the external program
            logging.info(f"External program started: {exe_path}")


        except Exception as e:
            # Log any error that occurs
            logging.error(f"Failed to start the external program: {e}")




class LoginWindow(QWidget):
    def __init__(self, isPreviosPassed):
        super().__init__()

        if (isPreviosPassed):
            # Set window properties
            self.setWindowTitle("User Login")
            self.setGeometry(100, 100, 300, 150)

            # Define layout
            layout = QVBoxLayout()

            # Username label and input
            self.username_label = QLabel("Username:")
            self.username_input = QLineEdit()
            self.username_input.setPlaceholderText("Enter your username")

            # Password label and input
            self.password_label = QLabel("Password:")
            self.password_input = QLineEdit()
            self.password_input.setPlaceholderText("Enter your password")
            self.password_input.setEchoMode(QLineEdit.Password)  # Hide password text

            # Login button
            self.login_button = QPushButton("Login")
            self.login_button.clicked.connect(self.authenticate_user)

            # Add widgets to layout
            layout.addWidget(self.username_label)
            layout.addWidget(self.username_input)
            layout.addWidget(self.password_label)
            layout.addWidget(self.password_input)
            layout.addWidget(self.login_button)

            # Set layout to the window
            self.setLayout(layout)
        else:
            self.setWindowTitle("Auth Failed")
            self.setGeometry(100, 100, 300, 150)

            layout = QVBoxLayout()
            self.label = QLabel("Не пройдена проверка")
            self.label.setStyleSheet('color:red')
            layout.addWidget(self.label)
            self.setLayout(layout)

    def authenticate_user(self):
        # Get entered data
        entered_username = self.username_input.text()
        entered_password = self.password_input.text()

        users_and_passwords = self.read_users_and_passwords_from_ini_file()

        # Check if entered credentials are correct
        if entered_username in users_and_passwords and users_and_passwords[entered_username] == entered_password:
            message = "Login Successful!"
            logging.info(f"Login attempt by username: {entered_username}")

            result = True
        else:
            message = "Invalid credentials. Try again."
            logging.warning(f"Login failed for username: {entered_username}")
            result = False

        # Show the result window
        self.result_window = ResultWindow(message, result)
        self.result_window.show()

        # Optionally, you can close the login window after showing the result
        self.close()

    def get_ini_path(self):
        # Get the path to the .ini file in the same directory as the script/exe
        if getattr(sys, 'frozen', False):  # If running from a bundled .exe
            return os.path.join(sys._MEIPASS, 'passwords.ini')
        else:  # If running as a script
            return os.path.join(os.path.dirname(__file__), 'passwords.ini')

    def read_users_and_passwords_from_ini_file(self):
        # Create a ConfigParser object
        config = configparser.ConfigParser()
        ini_file = self.get_ini_path()
        try:
            # Read the INI file
            config.read(ini_file)

            users_and_passwords = {}

            # Loop through each section (which is the username)
            for section in config.sections():
                # Read the password for each section
                users_and_passwords[section] = config.get(section, 'password')

            return users_and_passwords

        except FileNotFoundError:
            print("INI file not found.")
            return {}


app = QApplication(sys.argv)