from PyQt5.QtGui import QPalette, QColor, QBrush, QIcon, QRegularExpressionValidator, QIntValidator, QPixmap
from PyQt5.QtWidgets import QWidget, QFrame, QApplication, QGridLayout, QLabel, QPushButton, QVBoxLayout, \
    QTableWidget, QAbstractItemView, QHBoxLayout, QMessageBox, QTableWidgetItem, QDialog, QGroupBox, QLineEdit, \
    QComboBox
from PyQt5.QtCore import Qt, QSize
import sys
import sqlite3
import csv



class windowSignUp(QDialog):
    def __init__(self, parents=None):
        super(windowSignUp, self).__init__()
        self.setWindowTitle("New User Registration")
        self.setFixedSize(320, 230)
        self.initUI()

    def initUI(self):
        self.information = QGroupBox("", self)
        self.information.setFixedSize(300, 210)
        self.information.move(10, 10)

        labelName = QLabel("Login", self.information)
        labelName.move(15, 15)
        self.lineEditLogin = QLineEdit(self.information)
        self.lineEditLogin.setFixedSize(270, 30)
        self.lineEditLogin.setFocus()
        self.lineEditLogin.move(15, 30)

        labelNumber = QLabel("Password", self.information)
        labelNumber.move(15, 65)
        self.lineEditPassword = QLineEdit(self.information)
        self.lineEditPassword.setFixedSize(270, 30)
        self.lineEditPassword.setFocus()
        self.lineEditPassword.move(15, 80)

        labelUnit = QLabel("Repeat password", self.information)
        labelUnit.move(15, 120)
        self.lineEditRepeatedPassword = QLineEdit(self.information)
        self.lineEditRepeatedPassword.setFixedSize(270, 30)
        self.lineEditRepiatedPassword.move(15, 135)

        btnAccept = QPushButton("Accept", self)
        btnAccept.setCursor(Qt.PointingHandCursor)
        btnAccept.move(30, 180)
        btnAccept.clicked.connect(self.Accept)

        btnCancel = QPushButton("Cancel", self)
        btnCancel.setCursor(Qt.PointingHandCursor)
        btnCancel.move(185, 180)
        btnCancel.clicked.connect(self.close)

    def Accept(self):
        Login = " ".join(self.lineEditLogin.text().split()).title()
        Password = " ".join(self.lineEditPassword.text().split()).title()
        RepeatedPassword = " ".join(self.lineEditRepeatedPassword.text().split()).title()

        con = sqlite3.connect("users_db.sqlite")
        cur = con.cursor()
        check_data = [Login]

        def check(Login: str, Password: str):
            cur.execute("SELECT * FROM users WHERE Login=Login AND Password=Password")
            return cur.fetchone()

        if not Login:
            self.lineEditLogin.setFocus()
            QMessageBox.critical(self, "Введите логин", QMessageBox.Ok)
        elif not Password:
            self.lineEditPassword.setFocus()
            QMessageBox.critical(self, "Введите пароль", QMessageBox.Ok)
        elif not RepeatedPassword:
            self.lineRepeatedPassword.setFocus()
            QMessageBox.critical(self, "Подтвердите пароль", QMessageBox.Ok)
        elif Password != RepeatedPassword:
            self.lineEditRepeatedPassword()
            QMessageBox.critical(self, "Пароли не совпадают", QMessageBox.Ok)
        elif check(check_data):
            self.lineEditLogin.setFocus()
            QMessageBox.critical(self, "Такой логин уже существует", QMessageBox.Ok)
        else:

            data = [Login, Password]
            sqlRequest = """INSERT INTO users
                            (Login, Password)
                            VALUES
                            (?,?)"""
            cur.execute("""CREATE TABLE IF NOT EXISTS names(
                           Login TEXT UNIQUE,
                           Password TEXT,);
                        """)

            cur.execute(sqlRequest, data)
            con.commit()
            con.close()

            self.lineEditLogin.clear()
            self.lineEditPassword.clear()
            self.lineEditRepeatedPassword.clear()

            self.lineEditLogin.setFocus()
            self.close()
