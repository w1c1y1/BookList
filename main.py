import sys
import sqlite3
import csv

from PyQt5.QtGui import QPalette, QColor, QBrush, QIcon, QRegularExpressionValidator, QIntValidator, QPixmap
from PyQt5.QtWidgets import QWidget, QFrame, QApplication, QGridLayout, QLabel, QPushButton, QVBoxLayout, \
    QTableWidget, QAbstractItemView, QHBoxLayout, QMessageBox, QTableWidgetItem, QDialog, QGroupBox, QLineEdit, \
    QComboBox
from PyQt5.QtCore import Qt, QSize


class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowTitle("BookList")
        self.resize(1920, 1080)
        self.initUI()

    def initUI(self):
        # frame with menu

        palMenu = self.palette()
        palMenu.setColor(QPalette.Background, QColor("#CCFFFF"))

        frameMenu = QFrame()
        frameMenu.setFrameStyle(QFrame.NoFrame)
        frameMenu.setAutoFillBackground(True)
        frameMenu.setPalette(palMenu)
        frameMenu.setFixedWidth(150)

        # header for menu

        palHeader = self.palette()
        palHeader.setBrush(QPalette.Background, QBrush(QColor("#00CCCC"), Qt.SolidPattern))
        palHeader.setColor(QPalette.Foreground, QColor("#000000"))

        headerForMenu_font = self.font()
        headerForMenu_font.setFamily("SansSerif")
        headerForMenu_font.setPixelSize(12)

        headerForMenu = QLabel("Menu", frameMenu)
        headerForMenu.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        headerForMenu.setAutoFillBackground(True)
        headerForMenu.setPalette(palHeader)
        headerForMenu.setFont(headerForMenu_font)
        headerForMenu.setFixedSize(150, 45)
        headerForMenu.move(0, 0)

        # buttons for menu

        btnAdd = QPushButton(frameMenu)
        btnAdd.setText("Add book")
        btnAdd.setCursor(Qt.PointingHandCursor)
        btnAdd.setFixedSize(150, 35)
        btnAdd.move(0, 45)


        btnDelete = QPushButton(frameMenu)
        btnDelete.setText("Delete book")
        btnDelete.setCursor(Qt.PointingHandCursor)
        btnDelete.setFixedSize(150, 35)
        btnDelete.move(0, 80)

        btnLogin = QPushButton(frameMenu)
        btnLogin.setText("Login")
        btnLogin.setCursor(Qt.PointingHandCursor)
        btnLogin.setFixedSize(150, 35)
        btnLogin.move(0, 115)

        btnSettings = QPushButton(frameMenu)
        btnSettings.setText("Settings")
        btnSettings.setCursor(Qt.PointingHandCursor)
        btnSettings.setFixedSize(150, 35)
        btnSettings.move(0, 150)



        # title

        palTitle = self.palette()
        palTitle.setColor(QPalette.Background, QColor("FFCC99"))

        headerTitle = QFrame()
        headerTitle.setFrameStyle(QFrame.NoFrame)
        headerTitle.setAutoFillBackground(True)
        headerTitle.setPalette(palTitle)
        headerTitle.setFixedHeight(45)

        palText = self.palette()
        palText.setColor(QPalette.Foreground, QColor("#FFCC99"))

        titleText_font = self.font()
        titleText_font.setFamily("SansSerif")
        titleText_font.setBold(True)
        titleText_font.setPixelSize(12)

        titleText = QLabel("BookList")
        titleText.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        titleText.setFont(titleText_font)
        titleText.setPalette(palText)

        btnReboot = QPushButton()
        btnReboot.setIcon(QIcon("reboot_icon.png"))
        btnReboot.setIconSize(QSize(30, 30))
        btnReboot.setCursor(Qt.PointingHandCursor)
        btnReboot.setFixedWidth(40)

        titleFrame = QHBoxLayout()
        titleFrame.addWidget(titleText, Qt.AlignCenter)
        titleFrame.addStretch()
        titleFrame.addWidget(btnReboot)
        titleFrame.setContentsMargins(0, 0, 5, 0)
        headerTitle.setLayout(titleFrame)

        # Columns

        NAMES_FOR_COLUMNS = ["Student Name", "Author", "Book", "Review"]

        # table

        self.table = QTableWidget()
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setSortingEnabled(True)

        self.table.setColumnCount(4)
        self.table.setRowCount(0)

        self.table.verticalHeader().setVisible(False)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setDefaultSectionSize(35)
        self.table.setHorizontalHeaderLabels(NAMES_FOR_COLUMNS)

        for i, width in enumerate((300, 325, 325, 1000), start=0):
            self.table.setColumnWidth(i, width)

        tableLayout = QVBoxLayout()
        tableLayout.addWidget(self.table)
        tableLayout.setSpacing(10)
        tableLayout.setContentsMargins(10, 10, 10, 0)

        # config

        rightColumn = QVBoxLayout()
        rightColumn.addWidget(headerTitle)
        rightColumn.addLayout(tableLayout)
        rightColumn.setContentsMargins(0, 0, 0, 0)

        finalLayout = QGridLayout()
        finalLayout.addWidget(frameMenu, 0, 0)
        finalLayout.addLayout(rightColumn, 0, 1)
        finalLayout.setSpacing(0)
        finalLayout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(finalLayout)

        # --------------------------------------------
        # ---------------CONNECTS---------------------
        # --------------------------------------------

        btnAdd.clicked.connect(self.Add)
        btnDelete.clicked.connect(self.Delete)
        btnSettings.clicked.connect(self.Settings)
        btnReboot.clicked.connect(self.Reboot)
        btnLogin.clicked.connect(self.Login)

    # ------------------------------------------------
    # ----------------FUNCTIONS-----------------------
    # ------------------------------------------------

    def Add(self):
        windowAdd(self).exec_()




    def Delete(self):
        selected_string = self.table.selectedItems()
        if selected_string:
            id = selected_string[0].row()
            id_for_db = self.table.item(id, 0).text()
            con = sqlite3.connect("book.sqlite")
            cur = con.cursor()
            cur.execute("DELETE FROM names WHERE id = ?", (id_for_db,))
            con.commit()
            con.close()
            self.table.removeRow(id)
            self.table.clearSelection()
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
        else:
            QMessageBox.critical(self, "Delete book", "Select a row", QMessageBox.Ok)

    def Settings(self):
        windowSettings(self).exec_()



    def Reboot(self):
        # sqlRequest = "SELECT * FROM names"
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
        else:
            QMessageBox.critical(self, "Reboot", "There is no data in db", QMessageBox.Ok)


    def Login(self):
        windowLogin(self).exec_()


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
                           Review TEXT);
                        """)

            cur.execute(sqlRequest, data)
            con.commit()
            con.close()

            self.lineEditName.clear()
            self.lineEditBook.clear()
            self.lineEditReview.clear()

            self.lineEditName.setFocus()
            self.close()




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


class windowLogin(QDialog):
    def __init__(self, parents=None):
        super(windowLogin, self).__init__()
        self.setWindowTitle("Log In")
        self.setFixedSize(320, 230)
        self.initUI()

    def initUI(self):
        btnTeacher = QPushButton("As Teacher", self)
        btnTeacher.setCursor(Qt.PointingHandCursor)
        btnTeacher.move(30, 90)
        btnTeacher.clicked.connect(self.LogInAsTeacher)

        btnStudent = QPushButton("As Student", self)
        btnStudent.setCursor(Qt.PointingHandCursor)
        btnStudent.move(185, 90)
        btnStudent.clicked.connect(self.LogInAsStudent)


    def LogInAsTeacher(self):
        TeacherLogin(self).exec_()

    def LogInAsStudent(self):
        StudentLogin(self).exec_()


class TeacherLogin(QDialog):
    def __init__(self, parents=None):
        super(TeacherLogin, self).__init__()
        self.setWindowTitle("Log In")
        self.setFixedSize(320, 230)
        self.initUI()

    def initUI(self):
        labelName = QLabel("Login", self.information)
        labelName.move(15, 15)
        self.lineEditName = QLineEdit(self.information)
        self.lineEditName.setFixedSize(270, 30)
        self.lineEditName.setFocus()
        self.lineEditName.move(15, 30)

        labelNumber = QLabel("Password", self.information)
        labelNumber.move(15, 65)
        self.lineEditBook = QLineEdit(self.information)
        self.lineEditBook.setFixedSize(270, 30)
        self.lineEditBook.setFocus()
        self.lineEditBook.move(15, 80)

        btnAccept = QPushButton("Accept", self)
        btnAccept.setCursor(Qt.PointingHandCursor)
        btnAccept.move(30, 180)
        btnAccept.clicked.connect(self.Accept)

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
                           Review TEXT);
                        """)

            cur.execute(sqlRequest, data)
            con.commit()
            con.close()

            self.lineEditName.clear()
            self.lineEditBook.clear()
            self.lineEditReview.clear()

            self.lineEditName.setFocus()
            self.close()


class StudentLogin(QDialog):
    pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    sys.excepthook = except_hook
    sys.exit(app.exec())
