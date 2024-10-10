import sys
from PyQt5.QtWidgets import QApplication
from model import *

app = QApplication(sys.argv)
main_frame = Frame()
main_frame.show()
app.exec_()
