import sys
import time
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PyQt5 import QtCore, QtGui, QtWidgets
from fuzzywuzzy import fuzz
import json
import xlrd
import os
from random import randint
from datetime import datetime, timedelta
from uuid import uuid4 as uid
import socket
class MenuUi:
    def __init__(self):
        qfile = QFile("ui/menu.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)
        self.slot()

    def slot(self):
        self.ui.button_password.clicked.connect(self.input_password)
        self.ui.button_web.clicked.connect(self.input_web)
        self.ui.button_app.clicked.connect(self.input_app)
        self.ui.button_func.clicked.connect(self.input_func)
    def input_password(self):
        if self.ui.line.text() == "030904":
            PassWord_ui.ui.show()
            self.ui.hide()
        else:
            self.ui.label_word.setText("密码错误，请重新输入")

    def input_web(self):
        if self.ui.line.text() == "030904":
            Web_ui.ui.show()
            self.ui.hide()
        else:
            self.ui.label_word.setText("密码错误，请重新输入")

    def input_app(self):
        if self.ui.line.text() == "030904":
            App_ui.ui.show()
            self.ui.hide()
        else:
            self.ui.label_word.setText("密码错误，请重新输入")

    def input_func(self):
        if self.ui.line.text() == "030904":
            Func_ui.ui.show()
            self.ui.hide()
        else:
            self.ui.label_word.setText("密码错误，请重新输入")
class WebMain:
    def __init__(self):
        qfile = QFile("ui/web.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)
        self.ui.widget_add.hide()
        self.ui.widget_del.hide()
        self.ui.scrollArea.hide()
        self.ui.button_end_add.hide()

        self.slot()

    def slot(self):
        self.ui.button_add.clicked.connect(self.add_clicked)
        self.ui.button_del.clicked.connect(self.del_clicked)
        self.ui.button_change.clicked.connect(self.change_clicked)
        self.ui.button_search.clicked.connect(self.search_clicked)

        self.ui.button_add_2.clicked.connect(self.add_end)
        self.ui.button_end_add.clicked.connect(self.add_end2)

        self.ui.button_end_search.clicked.connect(self.search_end)

        self.ui.button_end_change.clicked.connect(self.change_end)
        self.ui.button_end_change_2.clicked.connect(self.change_end2)

        self.ui.button_end_del.clicked.connect(self.del_end)
        self.ui.button_end_del_2.clicked.connect(self.del_end2)

        self.ui.button_exit.clicked.connect(self.exit_end)
    def init(self):
        self.ui.widget_add.hide()
        self.ui.widget_del.hide()
        self.ui.scrollArea.hide()
        self.ui.button_end_change.hide()
        self.ui.button_end_del.hide()
        self.ui.button_end_search.hide()
        self.ui.button_add_2.hide()
        self.ui.button_end_add.hide()
        self.ui.button_end_change_2.hide()
        self.ui.button_end_del_2.hide()
    def add_clicked(self):
        self.init()
        self.ui.widget_add.show()
        self.ui.button_add_2.show()

    def del_clicked(self):
        self.init()
        self.ui.widget_del.show()
        self.ui.button_end_del.show()
        self.ui.label_code.show()
        self.ui.line_code.show()

    def change_clicked(self):
        self.init()
        self.ui.widget_del.show()
        self.ui.button_end_change.show()
        self.ui.label_code.show()
        self.ui.line_code.show()
        self.ui.button_end_change_2.show()
    def search_clicked(self):
        self.init()
        self.ui.widget_del.show()
        self.ui.button_end_search.show()
        self.ui.label_code.hide()
        self.ui.line_code.hide()


    def add_end(self):

        f = open("data/web/web.txt", "r")
        web_list = f.readlines()
        f.close()
        index = 0
        temp = 1
        ss = ""
        while index < len(web_list):
            if fuzz.partial_ratio(self.ui.line_add1.lower(), web_list[index].lower()) >= 60:
                ss += "%d:%s%s%s%s" % (
                    temp, web_list[index], web_list[index + 1], web_list[index + 2], web_list[index + 3])
                temp += 1
            index += 2
        if temp != 1:
            self.ui.scrollArea.show()
            self.ui.label_word.setText(ss + "\n\n上面查询出来的是可能有重复的结果，如果重复就不需要重复添加，如果没有就忽略本文继续添加操作")
            self.ui.button_end_add.show()
            self.ui.button_add_2.hide()
        else:
            self.add_end2()
    def add_end2(self):
        web_list1 = []
        web_list1.append(self.ui.line_add1.text())
        web_list1.append(self.ui.line_add2.text())
        f = open("data/web/web.txt", "a")
        for i in web_list1:
            f.write(i.strip('\n') + '\n')
        f.close()
        self.ui.widget_add.hide()

    def search_end(self):
        self.ui.scrollArea.show()
        f = open("data/web/web.txt", "r")
        web_list = f.readlines()
        f.close()
        name = self.ui.line_end_all.text()
        index = 0
        temp = 1
        ss = ""
        while index < len(web_list):
            if fuzz.partial_ratio(name.lower(), web_list[index].lower()) >= 60:
                ss += "%d:%s%s" % (
                    temp, web_list[index], web_list[index + 1])
                temp += 1
            index += 2
        if temp == 1:
            self.ui.label_word.setText("抱歉没有你想要的值，可能没有这个web")
        else:
            self.ui.label_word.setText(ss)

    def change_end(self):
        self.ui.scrollArea.show()
        f = open("data/web/web.txt", "r")
        self.web_list = f.readlines()
        web_list = self.web_list
        f.close()
        name = self.ui.line_end_all.text()
        index = 0
        temp = 1
        ss = ""
        record_dict = {}
        while index < len(web_list):
            if fuzz.partial_ratio(name.lower(), web_list[index].lower()) >= 60:
                ss += "%d:%s%s" % (temp, web_list[index], web_list[index + 1])
                record_dict[temp] = index
                temp += 1
            index += 2
        if temp == 1:
            self.ui.label_word.setText("抱歉没有你想要的值，可能没有这个web")
        else:
            self.ui.label_word.setText(ss + "\n请在上面的序号中填入你想要的数据，然后在下面填入新的数据进行修改")
            self.record_dict = record_dict
            self.ui.widget_add.show()

    def change_end2(self):
        num = int(self.ui.line_code.text())
        web_list = self.web_list
        record_dict = self.record_dict
        web_list[record_dict[int(num)]] = self.ui.line_add1.text()
        web_list[record_dict[int(num)] + 1] = self.ui.line_add2.text()
        f = open("data/web/web.txt", "w")
        for i in web_list:
            f.write(i.strip('\n') + '\n')
        f.close()
        self.ui.label_word.setText("修改完成")

    def del_end(self):
        self.ui.scrollArea.show()
        self.ui.button_end_del_2.show()
        f = open("data/web/web.txt", "r")
        self.web_list = f.readlines()
        web_list = self.web_list
        f.close()
        name = self.ui.line_end_all.text()
        index = 0
        temp = 1
        ss = ""
        record_dict = {}
        while index < len(web_list):
            if fuzz.partial_ratio(name.lower(), web_list[index].lower()) >= 60:
                ss += "%d:%s%s" % (
                    temp, web_list[index], web_list[index + 1])
                record_dict[temp] = index
                temp += 1
            index += 2
        if temp == 1:
            self.ui.label_word.setText("抱歉没有你想要的值，可能没有这个web")
        else:
            self.ui.label_word.setText(ss + "\n请在上面的序号中填入你想要的数据，然后在下面填入新的数据进行修改")
            self.record_dict = record_dict
    def del_end2(self):
        num = int(self.ui.line_code.text())
        web_list = self.web_list
        record_dict = self.record_dict
        res1 = web_list.pop(record_dict[num])
        res2 = web_list.pop(record_dict[num])
        print(res1, res2)
        f = open("data/web/web.txt", "w")
        for i in web_list:
            f.write(i.strip('\n') + '\n')
        f.close()
        self.ui.label_word.setText("删除完成")

    def exit_end(self):
        self.ui.hide()
        Main0.ui.show()

class PassWordMain:
    def __init__(self):
        qfile = QFile("ui/code.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        self.ui = QUiLoader().load(qfile)
        self.ui.widget_add.hide()
        self.ui.widget_del.hide()
        self.ui.scrollArea.hide()
        self.ui.button_end_add.hide()

        self.slot()

    def slot(self):
        self.ui.button_add.clicked.connect(self.add_clicked)
        self.ui.button_del.clicked.connect(self.del_clicked)
        self.ui.button_change.clicked.connect(self.change_clicked)
        self.ui.button_search.clicked.connect(self.search_clicked)

        self.ui.button_add_2.clicked.connect(self.add_end)
        self.ui.button_end_add.clicked.connect(self.add_end2)

        self.ui.button_end_search.clicked.connect(self.search_end)

        self.ui.button_end_change.clicked.connect(self.change_end)
        self.ui.button_end_change_2.clicked.connect(self.change_end2)

        self.ui.button_end_del.clicked.connect(self.del_end)
        self.ui.button_end_del_2.clicked.connect(self.del_end2)

        self.ui.button_exit.clicked.connect(self.exit_end)
    def init(self):
        self.ui.widget_add.hide()
        self.ui.widget_del.hide()
        self.ui.scrollArea.hide()
        self.ui.button_end_change.hide()
        self.ui.button_end_del.hide()
        self.ui.button_end_search.hide()
        self.ui.button_add_2.hide()
        self.ui.button_end_add.hide()
        self.ui.button_end_change_2.hide()
        self.ui.button_end_del_2.hide()
    def add_clicked(self):
        self.init()
        self.ui.widget_add.show()
        self.ui.button_add_2.show()

    def del_clicked(self):
        self.init()
        self.ui.widget_del.show()
        self.ui.button_end_del.show()
        self.ui.label_code.show()
        self.ui.line_code.show()

    def change_clicked(self):
        self.init()
        self.ui.widget_del.show()
        self.ui.button_end_change.show()
        self.ui.label_code.show()
        self.ui.line_code.show()
        self.ui.button_end_change_2.show()
    def search_clicked(self):
        self.init()
        self.ui.widget_del.show()
        self.ui.button_end_search.show()
        self.ui.label_code.hide()
        self.ui.line_code.hide()


    def add_end(self):

        f = open("data/password/password.txt", "r")
        password_list = f.readlines()
        f.close()
        index = 0
        temp = 1
        ss = ""
        while index < len(password_list):
            if fuzz.partial_ratio(self.ui.line_add1.text().lower(), password_list[index].lower()) >= 60:
                ss += "序号：%d\n名称：%s账户名：%s密码：%s备注：%s" % (temp, password_list[index], password_list[index + 1], password_list[index + 2],password_list[index + 3])
                temp += 1
            index += 4
        if temp != 1:
            print(ss)
            self.ui.scrollArea.show()
            self.ui.label_word.setText(ss + "\n\n上面查询出来的是可能有重复的结果，如果重复就不需要重复添加，如果没有就忽略本文继续添加操作")
            self.ui.button_end_add.show()
            self.ui.button_add_2.hide()
        else:
            self.add_end2()
    def add_end2(self):
        password_list1 = []
        password_list1.append(self.ui.line_add1.text())
        password_list1.append(self.ui.line_add2.text())
        password_list1.append(self.ui.line_add3.text())
        password_list1.append(self.ui.line_add4.text())
        print(password_list1)
        f = open("data/password/password.txt", "a")
        for i in password_list1:
            f.write(i.strip("\n") + "\n")
        f.close()
        self.ui.widget_add.hide()

    def search_end(self):
        self.ui.scrollArea.show()
        f = open("data/password/password.txt", "r")
        password_list = f.readlines()
        f.close()
        name = self.ui.line_end_all.text()
        index = 0
        temp = 1
        ss = ""
        while index < len(password_list):
            if fuzz.partial_ratio(name.lower(), password_list[index].lower()) >= 60:
                ss += "序号：%d:名称：%s账户名：%s密码：%s备注：%s" % (temp, password_list[index], password_list[index + 1], password_list[index + 2],password_list[index + 3])
                temp += 1
            index += 4
        if temp == 1:
            self.ui.label_word.setText("抱歉没有你想要的值，可能没有这个密码")
        else:
            self.ui.label_word.setText(ss)

    def change_end(self):
        self.ui.scrollArea.show()
        f = open("data/password/password.txt", "r")
        self.password_list = f.readlines()
        password_list = self.password_list
        f.close()
        name = self.ui.line_end_all.text()
        index = 0
        temp = 1
        ss = ""
        record_dict = {}
        while index < len(password_list):

            if fuzz.partial_ratio(name.lower(), password_list[index].lower()) >= 60:
                ss += "序号：%d\n名称：%s账户名：%s密码：%s备注：%s" % (
                temp, password_list[index], password_list[index + 1], password_list[index + 2],
                password_list[index + 3])

                record_dict[temp] = index
                temp += 1
            index += 4
        if temp == 1:
            self.ui.label_word.setText("抱歉没有你想要的值，可能没有这个密码")
        else:
            self.ui.label_word.setText(ss + "\n请在上面的序号中填入你想要的数据，然后在下面填入新的数据进行修改")
            self.record_dict = record_dict
            self.ui.widget_add.show()

    def change_end2(self):
        num = int(self.ui.line_code.text())
        password_list = self.password_list
        record_dict = self.record_dict
        password_list[record_dict[int(num)]] = self.ui.line_add1.text()
        password_list[record_dict[int(num)] + 1] = self.ui.line_add2.text()
        password_list[record_dict[int(num)] + 2] = self.ui.line_add3.text()
        password_list[record_dict[int(num)] + 3] = self.ui.line_add4.text()
        f = open("data/password/password.txt", "w")
        for i in password_list:
            f.write(i.strip('\n') + '\n')
        f.close()
        self.ui.label_word.setText("修改完成")

    def del_end(self):
        self.ui.scrollArea.show()
        self.ui.button_end_del_2.show()
        f = open("data/password/password.txt", "r")
        self.password_list = f.readlines()
        password_list = self.password_list
        f.close()
        name = self.ui.line_end_all.text()
        index = 0
        temp = 1
        ss = ""
        record_dict = {}
        while index < len(password_list):

            if fuzz.partial_ratio(name.lower(), password_list[index].lower()) >= 60:
                ss += "序号：%d\n名称：%s账户名：%s密码：%s备注：%s" % (
                    temp, password_list[index], password_list[index + 1], password_list[index + 2],
                    password_list[index + 3])

                record_dict[temp] = index
                temp += 1
            index += 4
        if temp == 1:
            self.ui.label_word.setText("抱歉没有你想要的值，可能没有这个密码")
        else:
            self.ui.label_word.setText(ss + "\n请在上面的序号中填入你想要的数据，然后在下面填入新的数据进行修改")
            self.record_dict = record_dict
    def del_end2(self):
        num = int(self.ui.line_code.text())
        password_list = self.password_list
        record_dict = self.record_dict
        res1 = password_list.pop(record_dict[num])
        res2 = password_list.pop(record_dict[num])
        res3 = password_list.pop(record_dict[num])
        res4 = password_list.pop(record_dict[num])
        print(res1, res2, res3, res4)
        f = open("data/password/password.txt", "w")
        for i in password_list:
            f.write(i.strip('\n') + '\n')
        f.close()
        self.ui.label_word.setText("删除完成")

    def exit_end(self):
        self.ui.hide()
        Main0.ui.show()


class AppMain:
    def __init__(self):
        qfile = QFile("ui/app.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()
        self.ui = QUiLoader().load(qfile)

        self.slot()

    def slot(self):
        self.ui.button_dism.clicked.connect(self.open_dism)
        self.ui.button_ccleaner.clicked.connect(self.open_ccleaner)
        self.ui.button_spacesniffer.clicked.connect(self.open_spacesniffer)
        self.ui.button_exit.clicked.connect(self.exit_end)
        self.ui.button_geek.clicked.connect(self.open_geek)
    def open_dism(self):
        os.startfile(r'F:\OneDrive\工具\app\清理软件\Dism++\Dism++x86.exe')

    def open_ccleaner(self):
        os.startfile(r"F:\OneDrive\工具\app\清理软件\CCleaner\CCleaner_5.75.8238_Professional_Portable\CCleaner64.exe")

    def open_spacesniffer(self):
        os.startfile(r"F:\OneDrive\工具\app\清理软件\spacesniffer\SpaceSniffer.exe")

    def open_geek(self):
        os.startfile(r"F:\OneDrive\工具\geek.exe")
    def exit_end(self):
        self.ui.hide()
        Main0.ui.show()

app = QApplication(sys.argv)
Main0 = MenuUi()
PassWord_ui = PassWordMain()
Web_ui = WebMain()
App_ui = AppMain()

from main_FuncMain import FuncMain
Func_ui = FuncMain()

Main0.ui.show()
sys.exit(app.exec_())