from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Windows.MainWindow import Ui_MainWindow
import json

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)
        self.users = self.load_credentials()
        self.Register_but.clicked.connect(self.switch_to_reg_page)
        self.BackToLogin_but.clicked.connect(self.return_to_login)
        self.LogIn_but.clicked.connect(self.check_login)
        self.RegisterPage_but.clicked.connect(self.register_new_account)

    def load_credentials(self):
        try:
            with open("users.json", "r") as file:
                users = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            users = {}

        return users
    
    def switch_to_reg_page(self):
        self.stackedWidget.setCurrentIndex(1)

    def return_to_login(self):
        self.stackedWidget.setCurrentIndex(0)

    def switch_to_main_page(self, username):
        self.stackedWidget.setCurrentIndex(2)
        self.label.setText(f"Welcome back {username}")

    def check_login(self):
        username = self.Username_LineEdit.text()
        password = self.Password_LineEdit.text()

        if username in self.users and self.users[username]["password"] == password:
            self.switch_to_main_page(username)
        else:
            self.Error_lbl.setText("Wrong username or password")
    def register_new_account(self):
        username = self.Username_LineEdit_2.text()
        password_1 = self.Password_LineEdit_2.text()
        password_2 = self.Password_LineEdit_3.text()

        if username in self.users:
            self.ErrorPassword_lbl.setText("This Username already exist")
        elif password_1 != password_2:
            self.ErrorPassword_lbl.setText("Passwords do not match. \n"
                " Please enter matching passwords.")
        else:
            self.users[username] = {"password": password_1}
            self.save_users()
            self.switch_to_main_page(username)

    def save_users(self):
        with open("users.json", "w") as file:
            json.dump(self.users, file)