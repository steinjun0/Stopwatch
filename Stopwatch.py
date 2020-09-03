# 참고한 코드 https://www.inflearn.com/questions/23977

import sys
from PyQt5.QtWidgets import*
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import *
import threading
import datetime

def generate_lcd(color_code):
    lcd = QLCDNumber()#시계디자인 위젯
    lcd.setSegmentStyle(QLCDNumber.Flat)#글자평평하게
    lcd.setDigitCount(8)#글자 총 8개까지 보여줌(hh:mm:ss)
    lcd.setFrameStyle(QFrame.NoFrame)#박스없앰
    lcd.setStyleSheet("color: "+color_code+";"
                            "border-width: 2px;"
                            "border-color: #7FFFD4;"
                            "border-radius: 3px")
    return lcd

class MyClock(QWidget):
    def __init__(self):
        super().__init__()
        
        self.red_watch_start_time = 0
        self.delta = datetime.timedelta(0,1)
        self.mouseClick = False
        self.setWindowTitle("Timer")
        self.initWidgets()
        self.resize(300,200)
        self.show()
        

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        
        elif e.key() == Qt.Key_C:
            self.switchWatch()

        elif e.key() == Qt.Key_X:
            self.timer.stop()
            self.stop = True
        
    
    def initWidgets(self):
        self.flag = 'ready'

        self.layout = QVBoxLayout(self)

        self.lbl_red = QLabel('Study')
        self.lbl_red.setStyleSheet("color: #EB2200;"
                                   "border-width: 0.5px;")
        self.lbl_red.setAlignment(Qt.AlignHCenter)

        self.lbl_blue = QLabel('Rest')
        self.lbl_blue.setStyleSheet("color: #2A4AEB;")
        self.lbl_blue.setAlignment(Qt.AlignHCenter)
                        


        self.button_layout = QHBoxLayout(self)
        self.btn_start = QPushButton("Start", self)
        self.btn_switch = QPushButton("Switch", self)
        self.btn_finish = QPushButton("Finish", self)

        self.button_layout.addWidget(self.btn_start)
        self.button_layout.addWidget(self.btn_switch)
        self.button_layout.addWidget(self.btn_finish)

        self.lcd_red = generate_lcd('#EB2200')
        self.lcd_blue = generate_lcd('#2A4AEB')
        


        self.timer = QTimer()
        self.timer.timeout.connect(self.showWatch)
        
        self.resetWatch()
        self.layout.addWidget(self.lbl_red)
        self.layout.addWidget(self.lcd_red,2)
        self.layout.addLayout(self.button_layout)
        self.layout.addWidget(self.lcd_blue,2)
        self.layout.addWidget(self.lbl_blue)
        self.setLayout(self.layout)

        self.pause_duation = 0

        self.btn_start.clicked.connect(self.startWatch)
        self.btn_switch.clicked.connect(self.switchWatch)
        self.btn_finish.clicked.connect(self.resetWatch)


    def show_time(self):
        time = QTime.currentTime()
        self.currentTime = time.toString("hh:mm:ss")
        self.lcd_red.display(self.currentTime)
        self.lcd_blue.display(self.currentTime)

    def startWatch(self):
 
        if self.flag == 'finish':
            self.red_watch_start_time = datetime.datetime.now()
            self.blue_watch_start_time = datetime.datetime.now()
            self.blue_watch_pause_time = datetime.datetime.now()
            self.flag = 'red_start'
            self.timer.start(100)

        elif self.flag == 'red_start' or self.flag == 'blue_start':
            pass

    def switchWatch(self):
        if self.flag == 'red_start': 
            self.flag = 'blue_start'
            self.red_watch_pause_time = datetime.datetime.now()

            self.blue_watch_start_time += self.pause_duration
            self.timer.start(100)
        
        elif self.flag == 'blue_start':
            self.flag = 'red_start'
            self.blue_watch_pause_time = datetime.datetime.now()

            self.red_watch_start_time += self.pause_duration
            self.timer.start(100)


    def resetWatch(self):
        if self.btn_finish.text() == 'Reset':
            text = "00:00:00"
            self.lcd_red.display(text)
            self.lcd_blue.display(text)
            self.timer.stop()
            self.flag = 'finish'
            self.btn_finish.setText('Finish')

        elif self.flag == 'red_start' or self.flag == 'blue_start':
            self.timer.stop()
            self.btn_finish.setText('Reset')
        
        elif self.flag == 'ready':
            text = "00:00:00"
            self.lcd_red.display(text)
            self.lcd_blue.display(text)
            self.timer.stop()
            self.flag = 'finish'            
            


    def showWatch(self):

        if self.flag == 'red_start':
            self.pause_duration = datetime.datetime.now() - self.blue_watch_pause_time

            red_elapsed_seconds = (datetime.datetime.now() - self.red_watch_start_time).total_seconds()
            hour = int(red_elapsed_seconds // 3600)
            minute = int(red_elapsed_seconds % 3600 // 60)
            second = int(red_elapsed_seconds % 60)
            # 시:분:초 형태로 문자열 포맷팅을 합니다.
            text = '{:02d}:{:02d}:{:02d}'.format(hour, minute, second)
            # 출력
            self.lcd_red.display(text)


        elif self.flag == 'blue_start':
            #self.red_watch_start_time += self.delta
            #print(self.red_watch_start_time)
            self.pause_duration = datetime.datetime.now() - self.red_watch_pause_time

            blue_elapsed_seconds = (datetime.datetime.now() - self.blue_watch_start_time).total_seconds()
            hour = int(blue_elapsed_seconds // 3600)
            minute = int(blue_elapsed_seconds % 3600 // 60)
            second = int(blue_elapsed_seconds % 60)
            # 시:분:초 형태로 문자열 포맷팅을 합니다.
            text = '{:02d}:{:02d}:{:02d}'.format(hour, minute, second)
            # 출력
            self.lcd_blue.display(text)



    
app = QApplication([])
win = MyClock()
app.exec_()