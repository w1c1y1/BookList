from PyQt5.QtGui import QPalette, QColor, QBrush, QIcon, QRegularExpressionValidator, QIntValidator, QPixmap
from PyQt5.QtWidgets import QWidget, QFrame, QApplication, QGridLayout, QLabel, QPushButton, QVBoxLayout, \
    QTableWidget, QAbstractItemView, QHBoxLayout, QMessageBox, QTableWidgetItem, QDialog, QGroupBox, QLineEdit, \
    QComboBox
from PyQt5.QtCore import Qt, QSize
import sys
import sqlite3
import csv

class windowAdd(QDialog):
    def __init__(self, parents=None):
        super(windowAdd, self).__init__()
        self.setWindowTitle("Add new book")
        self.setFixedSize(320, 230)
        self.initUI()

    def initUI(self):
        self.information = QGroupBox("", self)
        self.information.setFixedSize(300, 210)
        self.information.move(10, 10)

        labelName = QLabel("Author", self.information)
        labelName.move(15, 15)
        self.lineEditName = QLineEdit(self.information)
        self.lineEditName.setFixedSize(270, 30)
        self.lineEditName.setFocus()
        self.lineEditName.move(15, 30)

        labelNumber = QLabel("Book", self.information)
        labelNumber.move(15, 65)
        self.lineEditBook = QLineEdit(self.information)
        self.lineEditBook.setFixedSize(270, 30)
        self.lineEditBook.setFocus()
        self.lineEditBook.move(15, 80)

        labelUnit = QLabel("Review", self.information)
        labelUnit.move(15, 120)
        self.lineEditReview = QLineEdit(self.information)
        self.lineEditReview.setFixedSize(270, 30)
        self.lineEditReview.move(15, 135)

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
        name = " ".join(self.lineEditName.text().split()).title()
        book = " ".join(self.lineEditBook.text().split()).title()
        review = " ".join(self.lineEditReview.text().split()).title()

        if not name:
            self.lineEditName.setFocus()
        elif not book:
            self.lineEditBook.setFocus()
        elif not review:
            self.lineEditReview.setFocus()
        else:
            con = sqlite3.connect("book.sqlite")
            cur = con.cursor()

            data = [name, book, review]
            sqlRequest = """INSERT INTO names
                            (Author, Book, Review)
                            VALUES
                            (?,?,?)"""
            cur.execute("""CREATE TABLE IF NOT EXISTS names(
                           id INTEGER PRIMARY KEY,
                           Author TEXT,
                           Book TEXT,
                           Review TEXT);""")

            cur.execute(sqlRequest, data)
            con.commit()
            con.close()


            self.lineEditName.clear()
            self.lineEditBook.clear()
            self.lineEditReview.clear()

            self.lineEditName.setFocus()
            self.close()


