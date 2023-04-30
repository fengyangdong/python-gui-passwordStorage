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
import sys
from test import FuncMain
app = QApplication(sys.argv)
ui = FuncMain()
ui.ui.show()
sys.exit(app.exec_())