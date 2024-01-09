from PyQt5.QtGui import QPalette, QColor, QBrush, QIcon, QRegularExpressionValidator, QIntValidator, QPixmap
from PyQt5.QtWidgets import QWidget, QFrame, QApplication, QGridLayout, QLabel, QPushButton, QVBoxLayout, \
    QTableWidget, QAbstractItemView, QHBoxLayout, QMessageBox, QTableWidgetItem, QDialog, QGroupBox, QLineEdit, \
    QComboBox
from PyQt5.QtCore import Qt, QSize
import sys
import sqlite3
import csv


class windowSettings(QDialog):
    def __init__(self, parents=None):
        super(windowSettings, self).__init__()
        self.setWindowFlag(Qt.FramelessWindowHint)
        self.setFixedSize(500, 500)
        self.initUI()

    def initUI(self):
        pal = self.palette()
        pal.setColor(QPalette.Background, QColor("#FFFFFF"))
        self.setPalette(pal)

        frame = QFrame(self)
        frame.setFrameShape(QFrame.Box)
        frame.setAutoFillBackground(True)
        frame.setFixedSize(500, 500)
        frame.move(0, 0)

        btnImport = QPushButton("Import table", self)
        btnImport.setCursor(Qt.PointingHandCursor)
        btnImport.setFixedSize(247, 444)
        btnImport.move(2, 2)
        btnImport.clicked.connect(self.ImportTable)

        btnExport = QPushButton("Export table", self)
        btnExport.setCursor(Qt.PointingHandCursor)
        btnExport.setFixedSize(247, 444)
        btnExport.move(251, 2)
        btnExport.clicked.connect(self.ExportTable)

        btnClose = QPushButton("Close", self)
        btnClose.setCursor(Qt.PointingHandCursor)
        btnClose.setFixedSize(430, 35)
        btnClose.move(35, 455)
        btnClose.clicked.connect(self.close)

    def ImportTable(self):
        try:
            con = sqlite3.connect("book.sqlite")
            cur = con.cursor()
            sqlRequest = """INSERT INTO names
                                                        (Author, Book, Review)
                                                        VALUES
                                                        (?,?,?)"""
            with open("table.csv", encoding="utf8") as csvfile:
                reader = csv.reader(csvfile)
                cur.execute("DELETE FROM names WHERE id > 0")
                con.commit()
                for index, row in enumerate(reader):
                    t = row[0].split(";")
                    cur.execute(sqlRequest, t)
                con.commit()
                con.close()
                QMessageBox.information(self, "Import table",
                                        "The import was successful.",
                                        QMessageBox.Ok)
        except:
            QMessageBox.critical(self, "Import table",
                                 "The import was not successful. \n"
                                 "Try to check the availability of the table.",
                                 QMessageBox.Ok)


    def ExportTable(self):
        try:
            con = sqlite3.connect("book.sqlite")
            cur = con.cursor()
            sqlRequest = """SELECT Author, Book, Review
                            FROM names"""
            cur.execute(sqlRequest)
            returnedData = cur.fetchall()
            con.close()

            if returnedData:
                csv_file = open("table.csv", "w")
                text = []
                for i in returnedData:
                    t = [str(j) for j in i]
                    st = ";".join(t)
                    text.append(st)
                res = "\n".join(text)
                csv_file.write(res)

                QMessageBox.information(self, "Export table",
                                        "The export was successful.",
                                        QMessageBox.Ok)
            else:
                QMessageBox.critical(self, "Export table",
                                     "There is no data in table.",
                                     QMessageBox.Ok)
        except:
            QMessageBox.critical(self, "Export table",
                                 "The export was not successful.",
                                 QMessageBox.Ok)
