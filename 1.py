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
import datetime
from uuid import uuid4 as uid
import socket

print(datetime.date.today())