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
        self.lineEditRepeatedPassword.move(15, 135)

        btnAccept = QPushButton("Accept", self)
        btnAccept.setCursor(Qt.PointingHandCursor)
        btnAccept.move(30, 180)
        btnAccept.clicked.connect(self.Accept)
        btnAccept.clicked.connect(self.close)

        btnCancel = QPushButton("Cancel", self)
        btnCancel.setCursor(Qt.PointingHandCursor)
        btnCancel.move(185, 180)
        btnCancel.clicked.connect(self.close)

    def Accept(self):
        Login = " ".join(self.lineEditLogin.text().split()).title()
        Password = " ".join(self.lineEditPassword.text().split()).title()
        RepeatedPassword = " ".join(self.lineEditRepeatedPassword.text().split()).title()

        data = [Login]

        con = sqlite3.connect("users.sqlite")
        cur = con.cursor()
        info = cur.execute('SELECT * FROM users WHERE Login = ?', (data[0],))


        if not Login:
            self.lineEditLogin.setFocus()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Ошибка регистрации")
            msgBox.setWindowTitle("Вы не ввели логин")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msgBox.exec()
        elif not Password:
            self.lineEditPassword.setFocus()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Ошибка регистрации")
            msgBox.setWindowTitle("Вы не ввели пароль")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msgBox.exec()
        elif not RepeatedPassword:
            self.lineEditRepeatedPassword.setFocus()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Ошибка регистарции")
            msgBox.setWindowTitle("Вы не ввели пароль повторно")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msgBox.exec()
        elif Password != RepeatedPassword:
            self.lineEditRepeatedPassword.setFocus()
            msgBox = QMessageBox()
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setText("Ошибка регистрации")
            msgBox.setWindowTitle("Введенные пароли не совпадают")
            msgBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)

            msgBox.exec()
        else:

            con = sqlite3.connect("users.sqlite")
            cur = con.cursor()
            data = [Login, Password]
            cur.execute("""CREATE TABLE IF NOT EXISTS users(
                                       Login TEXT,
                                       Password TEXT)""")
            sqlRequest = """INSERT INTO users
                            (Login, Password)
                            VALUES
                            (?, ?)"""


            cur.execute(sqlRequest, data)
            con.commit()
            con.close()

            self.lineEditLogin.clear()
            self.lineEditPassword.clear()
            self.lineEditRepeatedPassword.clear()

            self.lineEditLogin.setFocus()
            self.close()
