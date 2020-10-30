#
#
#
#
#   PyQT5 Window class module for EncryptX v1.1
#
#
APP_VERSION = "Pre Alpha v1.1"
import requests
import PyPDF2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from encryption import *
from lib import *

class Ui_Main_Window(object):
    def setupUi(self, Main_Window):
        #INITIALIZATION OF VARIABLES
        self.pctype = sysCheck()
        self.file = ""
        self.filename = ""
        self.path_to_file = ""
        Main_Window.setObjectName("Main_Window")
        Main_Window.resize(664, 600)
        self.centralwidget = QtWidgets.QWidget(Main_Window)
        self.centralwidget.setObjectName("centralwidget")

        #browse button widget
        self.browse_button = QtWidgets.QPushButton(self.centralwidget)
        self.browse_button.setGeometry(QtCore.QRect(510, 130, 111, 31))
        self.browse_button.setObjectName("browse_button")

        #encrypt button widget
        self.encrypt_button = QtWidgets.QPushButton(self.centralwidget)
        self.encrypt_button.setGeometry(QtCore.QRect(70, 390, 231, 71))
        self.encrypt_button.setObjectName("encrypt_button")

        #decrypt button widget
        self.decrypt_button = QtWidgets.QPushButton(self.centralwidget)
        self.decrypt_button.setGeometry(QtCore.QRect(70, 470, 231, 71))
        self.decrypt_button.setObjectName("decrypt_button")

        #path of target file widget
        self.path_label = QtWidgets.QLabel(self.centralwidget)
        self.path_label.setGeometry(QtCore.QRect(60, 130, 441, 31))
        self.path_label.setText("")
        self.path_label.setObjectName("path_label")

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(60, 260, 551, 31))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")

        #PASSWORD INPU FIELD LINE EDIT
        self.lineEdit = QtWidgets.QLineEdit(self.horizontalLayoutWidget)
        self.lineEdit.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.lineEdit)

        #clear pass widget
        self.clearpass_button = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.clearpass_button.setObjectName("clearpass_button")
        self.horizontalLayout.addWidget(self.clearpass_button)

        #password label widget
        self.password_label = QtWidgets.QLabel(self.centralwidget)
        self.password_label.setGeometry(QtCore.QRect(270, 220, 131, 31))
        font = QtGui.QFont()
        font.setFamily("Segoe MDL2 Assets")
        self.password_label.setFont(font)
        self.password_label.setObjectName("password_label")

        #EncryptX logo widget
        self.title_label = QtWidgets.QLabel(self.centralwidget)
        self.title_label.setGeometry(QtCore.QRect(130, 0, 401, 101))
        self.title_label.setText("")
        self.title_label.setPixmap(QtGui.QPixmap("encryptx2.png"))
        self.title_label.setObjectName("title_label")

        #output browser widget
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setGeometry(QtCore.QRect(360, 390, 256, 151))
        self.textBrowser.setObjectName("textBrowser")
        Main_Window.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(Main_Window)
        self.statusbar.setObjectName("statusbar")
        Main_Window.setStatusBar(self.statusbar)

        self.retranslateUi(Main_Window)
        QtCore.QMetaObject.connectSlotsByName(Main_Window)

    def retranslateUi(self, Main_Window):   #attach commands to all buttons and labels and input fields
        _translate = QtCore.QCoreApplication.translate
        Main_Window.setWindowTitle(_translate("Main_Window", "EncryptX "+self.pctype+" Edition "+APP_VERSION))
        self.browse_button.setText(_translate("Main_Window", "Browse Files"))
        self.browse_button.clicked.connect(self.browse_handler)
        self.encrypt_button.setText(_translate("Main_Window", "ENCRYPT"))
        self.encrypt_button.clicked.connect(self.encrypt_handler)
        self.decrypt_button.setText(_translate("Main_Window", "DECRYPT"))
        self.decrypt_button.clicked.connect(self.decrypt_handler)
        self.clearpass_button.setText(_translate("Main_Window", "Clear"))
        self.clearpass_button.clicked.connect(self.passclear_handler)
        self.password_label.setText(_translate("Main_Window", "Encryption Password"))
        
    def browse_handler(self):   #handler function for when the browse file button is pressed
        #print("Browse pressed")
        self.open_dialog_box()

    def passclear_handler(self):    #handler function for when the passclear button is pressed
        #print("Clear pressed")
        self.lineEdit.clear()   #clear whatever is in the password field

    def encrypt_handler(self):  #handler function for when the encrypt button is pressed
        #print("Encrypt pressed")
        passw = self.lineEdit.text()
        pcheck = passwCheck(passw)
        if pcheck is True:
            pw = encode_passw(passw)
            kdf = make_kdf()
            key = generateKey(pw, kdf)
            encryption_return = encryptFile(self.filename, self.path_to_file, self.file, key)
            if encryption_return == 0:
                self.output_handle(f"    Succesfully encrypted {self.filename}\n"+
                                   "    With our secret password and created\n"+
                                   f"    encrypted_{self.filename} at path\n    {self.path_to_file}/encrypted_{self.filename}")
            else:
                self.output_handle("\n\n    Error in encryption either file selected is a\n"+
                                    "   directory or non-existant")
        else:
            self.output_handle("\n\n    Error invalid or blank password")

    def decrypt_handler(self):  #handler function for when the decrypt button is pressed
        #print("Decrypt pressed")
        passw = self.lineEdit.text()
        pcheck = passwCheck(passw)
        if pcheck is True:
            pw = encode_passw(passw)
            kdf = make_kdf()
            key = generateKey(pw, kdf)
            decryption_return = decryptFile(self.filename, self.path_to_file, self.file, key)
            if decryption_return == 0:
                self.output_handle(f"    Succesfully decrypted {self.filename}\n"+
                                   "    With our secret password and created\n"+
                                   f"    decrypted_{self.filename} at path\n    {self.path_to_file}/decrypted_{self.filename}")
            else:
                self.output_handle("\n\n    Error in decryption either file selected is a\n"+
                                    "   directory or non-existant")
        else:
            self.output_handle("\n\n    Error invalid or blank password")

    def open_dialog_box(self):  #open a browse file dialog box and change the target path to the file selected
        filename = QFileDialog.getOpenFileName()
        split_path = splitPath(filename[0])
        self.file = filename[0]
        self.filename = split_path[1]
        self.path_to_file = split_path[0]
        self.path_label.setText(self.file)

    def output_handle(self, output_string):     #change the output textbrowser string to output_string
        self.textBrowser.setText(output_string)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    Main_Window = QtWidgets.QMainWindow()
    ui = Ui_Main_Window()
    ui.setupUi(Main_Window)
    Main_Window.show()
    sys.exit(app.exec_())
