import os
import sys
import time
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile
from PyQt5 import QtWidgets
import json
import xlrd
from datetime import datetime, timedelta
from uuid import uuid4 as uid
import shutil
class FuncMain:
    def __init__(self):
        qfile = QFile("ui/func.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()
        self.ui = QUiLoader().load(qfile)
        self.slot()

    def slot(self):
        self.ui.button_excel.clicked.connect(self.open_excel)
        self.ui.button_excel_ics.clicked.connect(self.read_excel)
        self.ui.button_assignment_ics.clicked.connect(self.make_assignment_ics)
        self.ui.button_save.clicked.connect(self.my_save)
    def open_excel(self):
        # 其中self指向自身，"读取文件夹"为标题名，"./"为打开时候的当前路径
        directory, Ftype = QtWidgets.QFileDialog.getOpenFileName(None,"选取excel","./", "All Files(*)")  # 起始路径
        print(directory)
        self.ui.label_date.setText(directory)
        self.directory = directory
    # 读取文件
    def read_excel(self):
        # 指定信息在 xls 表格内的列数，第一列是第 0 列。
        self.config = dict()
        self.config["ClassName"] = 0
        self.config["StartWeek"] = 1
        self.config["EndWeek"] = 2
        self.config["Weekday"] = 3
        self.config["ClassTime"] = 4
        self.config["Classroom"] = 5
        self.config["WeekStatus"] = 6
        self.config["isClassSerialEnabled"] = [0, 7]
        self.config["isClassTeacherEnabled"] = [1, 8]
        # weekStatus: 0=Disabled 1=odd weeks 单周 2=even weeks 双周
        # 读取 excel 文件
        try:
            self.data = xlrd.open_workbook(self.directory)
            self.ui.label_word.setText("读取excel文件成功\n")
        except FileNotFoundError:
            print("文件不存在，请确认是否将课程信息前的 temp_ 去掉！")
            self.ui.label_word.setText("读取不成功\n")
            sys.exit()
        self.table = self.data.sheets()[0]
        # 基础信息
        self.numOfRow = self.table.nrows  # 获取行数,即课程数
        self.numOfCol = self.table.ncols  # 获取列数,即信息量
        self.ui.label_word.setText(self.ui.label_word.text()+f"行数：{self.numOfRow}\t列数：{self.numOfCol}\n")
        self.classList = list()
        i = 1
        while i < self.numOfRow:
            _i = i - 1
            self.classList.append(dict())
            self.classList[_i].setdefault("ClassName", self.table.cell(i, self.config["ClassName"]).value)
            self.classList[_i].setdefault("StartWeek", self.table.cell(i, self.config["StartWeek"]).value)
            self.classList[_i].setdefault("EndWeek", self.table.cell(i, self.config["EndWeek"]).value)
            self.classList[_i].setdefault("WeekStatus", self.table.cell(i, self.config["WeekStatus"]).value)
            self.classList[_i].setdefault("Weekday", self.table.cell(i, self.config["Weekday"]).value)
            self.classList[_i].setdefault("ClassTimeId", self.table.cell(i, self.config["ClassTime"]).value)
            self.classList[_i].setdefault("Classroom", self.table.cell(i, self.config["Classroom"]).value)
            if self.config["isClassSerialEnabled"][0]:
                try:
                    self.classList[_i].setdefault("ClassSerial",
                                                  str(int(self.table.cell(
                                                      i, self.config["isClassSerialEnabled"][1]).value)))
                except ValueError:
                    self.classList[_i].setdefault("ClassSerial",
                                                  str(self.table.cell(i, self.config["isClassSerialEnabled"][1]).value))
            if self.config["isClassTeacherEnabled"][0]:
                self.classList[_i].setdefault("Teacher",
                                              self.table.cell(i, self.config["isClassTeacherEnabled"][1]).value)
            i += 1
        print(self.classList)
        time.strftime("%Y-%m-%d_%H:%M:%S", time.localtime())
        filename = "data/课表/json/json_%s.json" % (time.strftime("%Y-%m-%d", time.localtime()))
        # if os.path.exists("conf_classInfo.json"):
        #     print("已存在 JSON 文件，使用随机文件名，请手动修改！")
        #     filename = "conf_classInfo_" + str(randint(100, 999)) + ".json"
        # else:
        #     filename = "conf_classInfo.json"
        with open(filename, 'w', encoding='UTF-8') as json_file:
            json_str = json.dumps(self.classList, ensure_ascii=False, indent=4)
            json_file.write(json_str)
            self.ui.label_word.setText(self.ui.label_word.text() + f"json文件存储完成，存储位置及存储名：{filename}\n")
            json_file.close()
            # 定义全局参数
            self.first_week = "20200224"  # 第一周周一的日期
            self.inform_time = 25  # 提前 N 分钟提醒
            self.g_name = self.ui.line_name.text()  # 全局课程表名
            print("g_name = %s" %self.g_name)
            self.g_color = "#ff9500"  # 预览时的颜色（可以在 iOS 设备上修改）
            self.a_trigger = ""

            # 读取文件，返回 dict(class_timetable) 时间表
            try:
                with open("data/课表/conf_classTime.json", 'r', encoding='UTF-8') as f:
                    self.class_timetable = json.loads(f.read())
                    f.close()
            except:
                print("时间配置文件 conf_classTime.json 似乎有点问题")
                sys.exit()
            # 读取文件，返回 dict(class_info) 课程信息
            try:
                with open(filename, 'r', encoding='UTF-8') as f:
                    self.class_info = json.loads(f.read())
                    f.close()
            except:
                print("课程配置文件 conf_classInfo.json 似乎有点问题")
                sys.exit()
        # 2023-01-02
        # 20230102
        _date = self.ui.date_excel.text()
        _date = _date.replace("-", "", 2)
        self.first_week = _date# 第一周周一的日期
        c = 0
        while c == 0:
            self.inform_time = self.ui.line_starttime.text()
            try:
                self.inform_time = int(self.inform_time)  # 提前 N 分钟提醒
                if self.inform_time <= 60:
                    self.a_trigger = f'-P0DT0H{self.inform_time}M0S'
                elif 60 < self.inform_time <= 1440:
                    minutes = self.inform_time % 60
                    hours = self.inform_time // 60
                    self.a_trigger = f'-P0DT{hours}H{minutes}M0S'
                else:
                    minutes = self.inform_time % 60
                    hours = (self.inform_time // 60) - 24
                    days = self.inform_time // 1440
                    self.a_trigger = f'-P{days}DT{hours}H{minutes}M0S'
                c = 1
            except ValueError:
                if self.inform_time in "nN":
                    self.a_trigger = ""
                    c = 1
                else:
                    print("输入数字有误！")
        utc_now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        weekdays = ["MO", "TU", "WE", "TH", "FR", "SA", "SU"]

        # 开始操作，先写入头
        ical_begin_base = f'''BEGIN:VCALENDAR
        VERSION:2.0
        X-WR-CALNAME:{self.g_name}
        X-APPLE-CALENDAR-COLOR:{self.g_color}
        X-WR-TIMEZONE:Asia/Shanghai
        BEGIN:VTIMEZONE
        TZID:Asia/Shanghai
        X-LIC-LOCATION:Asia/Shanghai
        BEGIN:STANDARD
        TZOFFSETFROM:+0800
        TZOFFSETTO:+0800
        TZNAME:CST
        DTSTART:19700101T000000
        END:STANDARD
        END:VTIMEZONE
        '''
        try:
            fileendname = "data/课表/ics/%s.ics" % self.g_name
            with open(fileendname, "w", encoding='UTF-8') as f:  # 追加要a
                f.write(ical_begin_base)
                f.close()
                print("utc_now"+str(utc_now))
        except:
            print("写入失败！可能是没有权限，请重试。")
            sys.exit()
        else:
            print("文件头写入成功！")

        initial_time = datetime.strptime(self.first_week, "%Y%m%d")  # 将开始时间转换为时间对象
        i = 1
        for obj in self.class_info:
            # 计算课程第一次开始的日期 first_time_obj，公式：7*(开始周数-1) （//把第一周减掉） + 周几 - 1 （没有周0，等于把周一减掉）
            try:
                delta_time = 7 * (obj['StartWeek'] - 1) + obj['Weekday'] - 1
            except TypeError:
                print("请检查 Excel 中是否有无用行，并删除 conf_classInfo.json 后重新运行 Excel 读取器及 iCal 生成器！")
                sys.exit()

            if obj['WeekStatus'] == 1:  # 单周
                if obj["StartWeek"] % 2 == 0:  # 若单周就不变，双周加7
                    delta_time += 7
            elif obj['WeekStatus'] == 2:  # 双周
                if obj["StartWeek"] % 2 != 0:  # 若双周就不变，单周加7
                    delta_time += 7
            first_time_obj = initial_time + timedelta(days=delta_time)  # 处理完单双周之后 first_time_obj 就是真正开始的日期
            if obj["WeekStatus"] == 0:  # 处理隔周课程
                extra_status = "1"
            else:
                extra_status = f'2;BYDAY={weekdays[int(obj["Weekday"] - 1)]}'  # BYDAY 是周 N，隔周重复需要带上

            try:  # 尝试处理纯数字的课程序号
                obj["ClassSerial"] = str(int(obj["ClassSerial"]))
                serial = f'课程序号：{obj["ClassSerial"]}'
            except ValueError:
                obj["ClassSerial"] = str(obj["ClassSerial"])
                serial = f'课程序号：{obj["ClassSerial"]}'
            except KeyError:  # 如果没有这个 key，直接略过
                serial = ""

            # 计算课程第一次开始、结束的时间，后面使用RRule重复即可，格式类似 20200225T120000
            final_stime_str = first_time_obj.strftime("%Y%m%d") + "T" + \
                              self.class_timetable[str(int(obj['ClassTimeId']))]["startTime"]
            final_etime_str = first_time_obj.strftime("%Y%m%d") + "T" + \
                              self.class_timetable[str(int(obj['ClassTimeId']))]["endTime"]
            delta_week = 7 * int(obj["EndWeek"] - obj["StartWeek"])
            stop_time_obj = first_time_obj + timedelta(days=delta_week + 1)
            stop_time_str = stop_time_obj.strftime("%Y%m%dT%H%M%SZ")  # 注意是utc时间，直接+1天处理
            # 教师可选，在此做判断
            try:
                teacher = f'教师：{obj["Teacher"]}\t'
            except KeyError:
                teacher = ""

            # 生成此次循环的 event_base
            if self.a_trigger:
                _alarm_base = f'''BEGIN:VALARM\nACTION:DISPLAY\nDESCRIPTION:This is an event reminder
        TRIGGER:{self.a_trigger}\nX-WR-ALARMUID:{uid()}\nUID:{uid()}\nEND:VALARM\n'''
            else:
                _alarm_base = ""
            _ical_base = f'''\nBEGIN:VEVENT
        CREATED:{utc_now}\nDTSTAMP:{utc_now}\nSUMMARY:{obj["ClassName"]}
        DESCRIPTION:{teacher}{serial}\nLOCATION:{obj["Classroom"]}
        TZID:Asia/Shanghai\nSEQUENCE:0\nUID:{uid()}\nRRULE:FREQ=WEEKLY;UNTIL={stop_time_str};INTERVAL={extra_status}
        DTSTART;TZID=Asia/Shanghai:{final_stime_str}\nDTEND;TZID=Asia/Shanghai:{final_etime_str}
        X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\n{_alarm_base}END:VEVENT\n'''

            # 写入文件
            with open(fileendname, "a", encoding='UTF-8') as f:
                f.write(_ical_base)
                print(f"第{i}条课程信息写入成功！")
                i += 1
                f.close()

        # 拼合头尾
        with open(fileendname, "a", encoding='UTF-8') as f:
            f.write("\nEND:VCALENDAR")
            f.close()

        self.ui.label_word.setText(self.ui.label_word.text() + f"ics文件操作完成，文件位置及名称：{fileendname}\n")

    def make_assignment_ics(self):
        utc_now = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
        start_time = self.ui.data_time.text()[0:4]+self.ui.data_time.text()[5:7]+self.ui.data_time.text()[8:10]
        if len(self.ui.data_time.text()[11:self.ui.data_time.text().index(":")]) == 1:
            start_time += "T" + self.ui.data_time.text()[11:self.ui.data_time.text().index(":")] +"0"+ self.ui.data_time.text()[self.ui.data_time.text().index(":")+1:] + "00"
        else:
            start_time += "T" + self.ui.data_time.text()[11:self.ui.data_time.text().index(":")] + self.ui.data_time.text()[self.ui.data_time.text().index(":") + 1:] + "00"

        end_time = self.ui.data_time_2.text()[0:4] + self.ui.data_time_2.text()[5:7] + self.ui.data_time_2.text()[8:10]
        if len(self.ui.data_time_2.text()[11:self.ui.data_time_2.text().index(":")]) == 1:
            end_time += "T" + self.ui.data_time_2.text()[11:self.ui.data_time_2.text().index(":")] + "0" + self.ui.data_time_2.text()[self.ui.data_time_2.text().index(":") + 1:] + "00"
        else:
            end_time += "T" + self.ui.data_time_2.text()[11:self.ui.data_time_2.text().index(":")] + self.ui.data_time_2.text()[self.ui.data_time_2.text().index(":") + 1:] + "00"
        c = 0
        if self.ui.line_starttime2.text() == "":
            self.a_trigger = ""
        else:
            while c == 0:
                self.inform_time = self.ui.line_starttime2.text()
                try:
                    self.inform_time = int(self.inform_time)  # 提前 N 分钟提醒
                    if self.inform_time <= 60:
                        self.a_trigger = f'-P0DT0H{self.inform_time}M0S'
                    elif 60 < self.inform_time <= 1440:
                        minutes = self.inform_time % 60
                        hours = self.inform_time // 60
                        self.a_trigger = f'-P0DT{hours}H{minutes}M0S'
                    else:
                        minutes = self.inform_time % 60
                        hours = (self.inform_time // 60) - 24
                        days = self.inform_time // 1440
                        self.a_trigger = f'-P{days}DT{hours}H{minutes}M0S'
                    c = 1
                except ValueError:
                    if self.inform_time in "nN":
                        self.a_trigger = ""
                        c = 1
                    else:
                        print("输入数字有误！")
        ical_begin_base = f'''BEGIN:VCALENDAR
                VERSION:2.0
                X-WR-CALNAME:{self.ui.line_name_2.text()}
                X-APPLE-CALENDAR-COLOR:#ff9500 
                X-WR-TIMEZONE:Asia/Shanghai
                BEGIN:VTIMEZONE
                TZID:Asia/Shanghai
                X-LIC-LOCATION:Asia/Shanghai
                BEGIN:STANDARD
                TZOFFSETFROM:+0800
                TZOFFSETTO:+0800
                TZNAME:CST
                DTSTART:19700101T000000
                END:STANDARD
                END:VTIMEZONE
                '''
        try:
            fileendname = "data/课表/assignment/%s.ics" % self.ui.line_name_2.text()
            with open(fileendname, "w", encoding='UTF-8') as f:  # 追加要a
                f.write(ical_begin_base)
                f.close()
                print("utc_now"+str(utc_now))
        except:
            print("写入失败！可能是没有权限，请重试。")
            sys.exit()
        else:
            print("文件头写入成功！")


            if self.a_trigger:
                _alarm_base = f'''BEGIN:VALARM\nACTION:DISPLAY\nDESCRIPTION:This is an event reminder
                TRIGGER:{self.a_trigger}\nX-WR-ALARMUID:{uid()}\nUID:{uid()}\nEND:VALARM\n'''
            else:
                _alarm_base = ""

        _ical_base = f'''\nBEGIN:VEVENT
        CREATED:{utc_now}\nDTSTAMP:{utc_now}\nSUMMARY:{self.ui.line_title.text()}
        DESCRIPTION:{self.ui.line_remarks.text()}\nLOCATION:{self.ui.line_place.text()}
        TZID:Asia/Shanghai\nSEQUENCE:0\nUID:{uid()}\n
        DTSTART;TZID=Asia/Shanghai:{start_time}\nDTEND;TZID=Asia/Shanghai:{end_time}
        X-APPLE-TRAVEL-ADVISORY-BEHAVIOR:AUTOMATIC\n{_alarm_base}END:VEVENT\n'''


        with open(fileendname, "a", encoding='UTF-8') as f:
            f.write(_ical_base)
            f.close()

        # 拼合头尾
        with open(fileendname, "a", encoding='UTF-8') as f:
            f.write("\nEND:VCALENDAR")
            f.close()

        self.ui.label_word.setText(self.ui.label_word.text() + f"ics文件操作完成，文件位置及名称：{fileendname}\n")
    def my_save(self):
        self.ui.label_word.setText("")
        self.ui.label_word.setText("这是我自己的备份方案，这里只会备份linux镜像，备份代码，其他的都不会备份，并且这是我自己的备份方法，可能和你的不匹配\n\n这里只会备份到备份库中\n准备开始，你有3s的准备时间，可以立刻退出")
        time.sleep(3)
        self.ui.label_word.setText("开始复制linux")
        now_day = datetime.date.today()
        os.makedirs()
        shutil.copytree(r'F:\OneDrive\娱乐\代码\vm12-linux\centos7_study', rf'E:\备份库\linux\{now_day}~centos7_study')
        self.ui.label_word.setText(self.ui.label_word.text() + f"-----完成\n存储位置：{now_day}~centos7_study")

