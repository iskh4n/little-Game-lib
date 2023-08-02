import sys
import os
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QWidget, QLabel
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5 import QtGui, QtCore

import sqlite3


class loginscreen(QDialog):
    def __init__(self):
        super(loginscreen, self).__init__()
        loadUi("login.ui", self)
        self.login.clicked.connect(self.golog)
        self.signup.clicked.connect(self.gosignup)
        pixmap=QPixmap('logbg3.jpg')
        self.background.setPixmap(pixmap)
        # login== ui login pushbutton obj name   #

    def golog(self):
        login = Loginscreen1()
        widget.addWidget(login)
        widget.setCurrentIndex(widget.currentIndex() + 1)

    def gosignup(self):
        signup = Signupscreen()
        widget.addWidget(signup)
        widget.setCurrentIndex(widget.currentIndex() + 1)




class Loginscreen1(QDialog):
    def __init__(self):
        super(Loginscreen1, self).__init__()
        loadUi("login1.ui", self)
        self.passbox.setEchoMode(QtWidgets.QLineEdit.Password)
        self.login1.clicked.connect(self.logkontrol)
        pixmap=QPixmap('logbg3.jpg')
        self.background.setPixmap(pixmap)
        self.exitbutton.clicked.connect(self.login_screen)



    def logkontrol(self):
        username=self.emailbox.text()
        password=self.passbox.text()

        if len(username)==0 or len(password)==0:
            self.error.setText("Please fill the empty fields") #error== login1.ui label#
        else:
            conn=sqlite3.connect("logindata.db")
            #curs=conn.cursor()
           # komut='SELECT password FROM login WHERE username=\''+username+"\'"
            komut=conn.execute('SELECT * from login WHERE username=? AND password=?',(username,password))
            #curs.execute(komut)
            if(len(komut.fetchall())>0):
                print("successfully logged")
                self.error.setText("")
                welcomelib = Welcomlibscreen()
                widget.addWidget(welcomelib)
                widget.setCurrentIndex(widget.currentIndex() + 1)


            else:
                self.error.setText("Invalid username or password")
            '''      result_pass=curs.fetchone()[0] 
           if result_pass==password:
                print("successfully logged")
                self.error.setText("")
            else:
                self.error.setText("Invalid username or password") '''


    def login_screen(self):
        login_screen = loginscreen()
        widget.addWidget(login_screen)
        widget.setCurrentIndex(widget.currentIndex() +1)


class Welcomlibscreen(QDialog):
    def __init__(self):
        super(Welcomlibscreen, self).__init__()
        loadUi("welcomelib.ui",self)
        pixmap=QPixmap('logbg3.jpg')
        self.background.setPixmap(pixmap)
        self.space.clicked.connect(self.spaceinvaders)
        self.space.setStyleSheet("background-image: url(logbg4.png);color:white;")
        self.pong.clicked.connect(self.ponggame)
        self.pong.setStyleSheet("background-image: url(bg3.png);color:white;")
        self.ded.clicked.connect(self.deneme_deneme)
        self.ded.setStyleSheet("background-image: url(bg.png);color:white;")

        self.alien.setStyleSheet("background-image: url(bg4.png);color:white;")
        self.alien.clicked.connect(self.flappy)
        self.exitbutton.clicked.connect(self.login_screen)
    def spaceinvaders(self):
        os.system('python main.py')
    def ponggame(self):
        os.system('python deneme2.py')
    def deneme_deneme(self):
        os.system('python deneme.py')
    def flappy(self):
        os.system('python flapp/flappdeneme.py')
    def login_screen(self):
        login_screen = Loginscreen1()
        widget.addWidget(login_screen)
        widget.setCurrentIndex(widget.currentIndex() +1)
class Signupscreen(QDialog):
    def __init__(self):
        super(Signupscreen, self).__init__()
        loadUi("signup.ui",self)
        self.passbox1.setEchoMode(QtWidgets.QLineEdit.Password)
        self.passbox1_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.signupbutton.clicked.connect(self.Signupfunction)
        pixmap=QPixmap('logbg3.jpg')
        self.background.setPixmap(pixmap)
        self.exitbutton.clicked.connect(self.login_screen)


    def login_screen(self):
        login_screen = Loginscreen1()
        widget.addWidget(login_screen)
        widget.setCurrentIndex(widget.currentIndex() +1)

    def Signupfunction(self):
        user1=self.userbox.text()
        password1=self.passbox1.text()
        confirm1=self.passbox1_2.text()
        if len(user1)==0 or len(password1)==0 or len(confirm1)==0:
          self.error.setText("Please fill all inputs")

        elif password1!=confirm1:
            self.error.setText("Passwords do not match, please try again")
        else:
            conn=sqlite3.connect("logindata.db")
            #userinfo=[user1,password1]
            conn.execute('''INSERT INTO login(username,password) VALUES(?,?)''',(user1,password1))
            conn.commit()
            conn.close()
            print('successfully added')
            welcomelib1 = Welcomlibscreen()
            widget.addWidget(welcomelib1)
            widget.setCurrentIndex(widget.currentIndex() + 1)




# logsayfa

app = QApplication(sys.argv)
log = loginscreen()
widget = QtWidgets.QStackedWidget()
widget.addWidget(log)
widget.setFixedHeight(640)
widget.setFixedWidth(800)
widget.show()
try:
    sys.exit(app.exec())
except:
    print("exit")
