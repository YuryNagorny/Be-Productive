import sys
import traceback
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QColor

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class BeProductive(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uiBP.ui', self)
        self.setWindowTitle('Be Productive')
        self.Short_Start.clicked.connect(self.short_timer_on_off)
        self.Long_Start.clicked.connect(self.long_timer_on_off)
        self.time = QtCore.QTime(0, 0)
        self.Short_LCD.display(self.time.toString("mm:ss"))
        self.Long_LCD.display(self.time.toString("mm:ss"))
        self.Pomo_Slider.setMinimum(20)
        self.Pomo_Slider.setMaximum(30)
        self.Pomo_Start.clicked.connect(self.pomodoro_timer_on_off)
        self.Pomo_LCD.display(self.time.toString("mm:ss"))
        self.Pomo_LCD_Set.display(25)
        self.Pomo_Slider.setValue(25)
        self.pomo_minutes = 25
        self.Pomo_LCD.display(f"{self.pomo_minutes}:00")
        self.Pomo_Slider.valueChanged.connect(self.Pomo_LCD_Set.display)
        self.Short_LCD_Set.display(5)
        self.Long_LCD_Set.display(20)
        self.Short_Slider.setMinimum(3)
        self.Short_Slider.setMaximum(9)
        self.Short_Slider.setValue(5)
        self.Short_Slider.valueChanged.connect(self.Short_LCD_Set.display)
        self.short_minutes = 5
        self.Short_LCD.display(f"0{self.short_minutes}:00")
        self.Long_Slider.setMinimum(10)
        self.Long_Slider.setMaximum(40)
        self.Long_Slider.setValue(20)
        self.Long_Slider.valueChanged.connect(self.Long_LCD_Set.display)
        self.long_minutes = 20
        self.Long_LCD.display(f"{self.long_minutes}:00")
        self.Save_Changes.clicked.connect(lambda: self.save_changes())
        self.pomo_timer = QTimer(self)
        self.pomo_timer.timeout.connect(self.show_Pomo)
        self.pomo_timer.setInterval(1000)
        self.pomo_flag = True
        self.short_timer = QTimer(self)
        self.short_timer.timeout.connect(self.show_Short)
        self.short_timer.setInterval(1000)
        self.short_flag = True
        self.long_timer = QTimer(self)
        self.long_timer.timeout.connect(self.show_Long)
        self.long_timer.setInterval(1000)
        self.long_flag = True
        self.Reset_Pomo.clicked.connect(lambda: self.Pomodoro_Reset())
        self.Reset_Short.clicked.connect(lambda: self.Short_Reset())
        self.Reset_Long.clicked.connect(lambda: self.Long_Reset())
        #####################################################################
        self.Add_Task.clicked.connect(lambda: self.add_task())
        self.account.hide()
        self.reg_cont.hide()

    def add_task(self):
        if self.Enter_Task != "":
            self.List_Task.addItem(self.Enter_Task.text())

    def save_changes(self):
        self.pomo_minutes = int(self.Pomo_Slider.value())
        self.Pomo_LCD.display(f"{self.pomo_minutes}:00")
        self.short_minutes = int(self.Short_Slider.value())
        self.Short_LCD.display(f"0{self.short_minutes}:00")
        self.long_minutes = int(self.Long_Slider.value())
        self.Long_LCD.display(f"{self.long_minutes}:00")
        self.pomo_flag = True
        self.short_flag = True
        self.long_flag = True

    def show_Pomo(self):
        m, s = divmod(self.pomo_seconds, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        self.Pomo_LCD.display(self.min_sec_format)
        self.pomo_seconds -= 1
        if self.pomo_seconds < 0:
            self.pomo_timer.stop()
            self.Pomo_Start.setText("???????????? ??????????????????????")
            self.pomo_seconds = 0
            self.pomo_flag = True

    def pomodoro_timer_on_off(self):
        if self.pomo_flag:
            self.pomo_seconds = 60 * self.pomo_minutes
            self.pomo_flag = False
        if self.Pomo_Start.text() == "???????????? ??????????????????????" or self.Pomo_Start.text() == "???????????????????? ??????????????????????":
            self.pomo_timer.start()
            self.Pomo_Start.setText("??????????????????????????")
        elif self.Pomo_Start.text() == "??????????????????????????":
            self.pomo_timer.stop()
            self.Pomo_Start.setText("???????????????????? ??????????????????????")

    def show_Short(self):
        m, s = divmod(self.short_seconds, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        self.Short_LCD.display(self.min_sec_format)
        self.short_seconds -= 1
        if self.short_seconds < 0:
            self.pomo_timer.stop()
            self.Short_Start.setText("???????????? ??????????????")
            self.short_seconds = 0
            self.short_flag = True

    def short_timer_on_off(self):
        if self.short_flag:
            self.short_seconds = 60 * self.short_minutes
            self.short_flag = False
        if self.Short_Start.text() == "???????????? ??????????????" or self.Short_Start.text() == "???????????????????? ??????????????":
            self.short_timer.start()
            self.Short_Start.setText("??????????????????????????")
        elif self.Short_Start.text() == "??????????????????????????":
            self.short_timer.stop()
            self.Short_Start.setText("???????????????????? ??????????????")

    def show_Long(self):
        m, s = divmod(self.long_seconds, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        self.Long_LCD.display(self.min_sec_format)
        self.long_seconds -= 1
        if self.long_seconds < 0:
            self.pomo_timer.stop()
            self.Long_Start.setText("???????????? ??????????????")
            self.long_seconds = 0
            self.long_flag = True

    def long_timer_on_off(self):
        if self.long_flag:
            self.long_seconds = 60 * self.long_minutes
            self.long_flag = False
        if self.Long_Start.text() == "???????????? ??????????????" or self.Long_Start.text() == "???????????????????? ??????????????":
            self.long_timer.start()
            self.Long_Start.setText("??????????????????????????")
        elif self.Long_Start.text() == "??????????????????????????":
            self.long_timer.stop()
            self.Long_Start.setText("???????????????????? ??????????????")

    def Pomodoro_Reset(self):
        self.pomo_timer.stop()
        self.Pomo_Start.setText("???????????? ??????????????????????")
        self.Pomo_LCD.display(f"{self.pomo_minutes}:00")
        self.pomo_flag = True

    def Short_Reset(self):
        self.short_timer.stop()
        self.Short_Start.setText("???????????? ??????????????")
        self.Short_LCD.display(f"0{self.short_minutes}:00")
        self.short_flag = True

    def Long_Reset(self):
        self.long_timer.stop()
        self.Long_Start.setText("???????????? ??????????????")
        self.Long_LCD.display(f"{self.long_minutes}:00")
        self.long_flag = True

    def ref_to_reg(self):
        self.to_reg.clicked.connect(lambda: self.log_cont.hide())
        self.to_reg.clicked.connect(lambda: self.reg_cont.show())

    def ref_to_log(self):
        self.to_log.clicked.connect(lambda: self.reg_cont.hide())
        self.to_log.clicked.connect(lambda: self.log_cont.show())

    def enter_to_account(self):
        self.log_btn.clicked.connect(lambda: self.account.show())
        self.log_btn.clicked.connect(lambda: self.log_cont.hide())
        self.log_btn.clicked.connect(lambda: self.reg_cont.hide())

    # def customize(self):
    #    self.setAttribute(Qt.WA_StyledBackground, True)
    #    self.setStyleSheet(f'background-color: {backplan_color}')
    #    self.start.setStyleSheet(f"background-color: {button_color}; color: {button_font_color}")
    #    self.number.setStyleSheet(f'background-color: {input_color}')
    #    self.token.setStyleSheet(f'background-color: {input_color}')
    #    self.label.setStyleSheet(f'color: {font_color}')
    #    self.label_2.setStyleSheet(f'color: {font_color}')


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("O?????????????????? ???????????? !:", tb)

if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ex = BeProductive()
    ex.ref_to_log()
    ex.ref_to_reg()
    ex.enter_to_account()
    ex.show()
    sys.exit(app.exec_())