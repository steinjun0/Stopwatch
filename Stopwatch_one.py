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
        self.resize(300,130)
        self.show()
    
    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        
    
    def initWidgets(self):
        self.layout = QVBoxLayout(self)

        self.button_layout = QHBoxLayout(self)
        self.btn_start = QPushButton("Start", self)
        self.btn_pause = QPushButton("Pause", self)
        self.btn_finish = QPushButton("Finish", self)

        self.button_layout.addWidget(self.btn_start)
        self.button_layout.addWidget(self.btn_pause)
        self.button_layout.addWidget(self.btn_finish)

        self.lcd_red = generate_lcd('#202020')
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.showWatch)
        
        self.resetWatch()
        self.layout.addWidget(self.lcd_red)
        self.layout.addLayout(self.button_layout)
        self.setLayout(self.layout)

        self.pause_time = 0

        self.btn_start.clicked.connect(self.startWatch)
        self.btn_pause.clicked.connect(self.pauseWatch)
        self.btn_finish.clicked.connect(self.resetWatch)


    def show_time(self):
        time = QTime.currentTime()
        self.currentTime = time.toString("hh:mm:ss")
        self.lcd_red.display(self.currentTime)
        
    def startWatch(self):
        if self.flag == 'pause':
            self.red_watch_start_time += self.pause_time
            self.flag = 'start'
            self.timer.start(100)

        elif self.flag != 'start':
            self.red_watch_start_time = datetime.datetime.now()
            self.flag = 'start'
            self.timer.start(100)

    def pauseWatch(self):
        if self.flag != 'pause': 
            self.flag = 'pause'
            self.red_watch_pause_time = datetime.datetime.now()
            

    def resetWatch(self):
        text = "00:00:00"
        self.lcd_red.display(text)
        
        self.timer.stop()
        self.flag = 'finish'


    def showWatch(self):
        if self.flag == 'pause':
            #self.red_watch_start_time += self.delta
            #print(self.red_watch_start_time)
            self.pause_time = datetime.datetime.now() - self.red_watch_pause_time


        else:

            red_elapsed_seconds = (datetime.datetime.now() - self.red_watch_start_time).total_seconds()
            hour = int(red_elapsed_seconds // 3600)
            minute = int(red_elapsed_seconds % 3600 // 60)
            second = int(red_elapsed_seconds % 60)
            # 시:분:초 형태로 문자열 포맷팅을 합니다.
            text = '{:02d}:{:02d}:{:02d}'.format(hour, minute, second)
            # 출력
            self.lcd_red.display(text)

    
app = QApplication([])
win = MyClock()
app.exec_()