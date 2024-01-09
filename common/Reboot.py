import sys
import sqlite3
import csv
import windowAdd
import windowSignUp
import windowSettings
import windowLogin


from PyQt5.QtGui import QPalette, QColor, QBrush, QIcon, QRegularExpressionValidator, QIntValidator, QPixmap
from PyQt5.QtWidgets import QWidget, QFrame, QApplication, QGridLayout, QLabel, QPushButton, QVBoxLayout, \
    QTableWidget, QAbstractItemView, QHBoxLayout, QMessageBox, QTableWidgetItem, QDialog, QGroupBox, QLineEdit, \
    QComboBox
from PyQt5.QtCore import Qt, QSize


class Reboot:
        sqlRequest = """SELECT 
            id, 
            Author, 
            Book,
            Review
        FROM
            names
            """

        con = sqlite3.connect("book.sqlite")
        cur = con.cursor()
        cur.execute(sqlRequest)
        returned_data = cur.fetchall()
        con.close()
        self.table.clearContents()
        self.table.setRowCount(0)
        if returned_data:
            row = 0
            for i in returned_data:
                self.table.setRowCount(row + 1)
                self.table.setItem(row, 0, QTableWidgetItem(str(i[0])))
                self.table.setItem(row, 1, QTableWidgetItem(i[1]))
                self.table.setItem(row, 2, QTableWidgetItem(str(i[2])))
                self.table.setItem(row, 3, QTableWidgetItem(str(i[3])))
                row += 1