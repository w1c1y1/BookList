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

        btnSignUp = QPushButton(frameMenu)
        btnSignUp.setText("New User")
        btnSignUp.setCursor(Qt.PointingHandCursor)
        btnSignUp.setFixedSize(150, 35)
        btnSignUp.move(0, 150)

        btnSettings = QPushButton(frameMenu)
        btnSettings.setText("Settings")
        btnSettings.setCursor(Qt.PointingHandCursor)
        btnSettings.setFixedSize(150, 35)
        btnSettings.move(0, 185)



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
        windowAdd.windowAdd(self).exec_()




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
        windowSettings.windowSettings(self).exec_()



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
        windowLogin.windowLogin(self).exec_()


    def NewUser(self):
        windowSignUp.windowSignUp(self).exec_()
