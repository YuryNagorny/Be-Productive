import sys
import traceback
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtWidgets
from sqlBP import *


if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class BeProductive(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('uiBP.ui', self)
        self.session = {}
        self.reg_btn.clicked.connect(self.__reg)
        self.log_btn.clicked.connect(self.__log)
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
        self.Add_Task.clicked.connect(lambda: self.add_task())
        self.Log_Out.clicked.connect(self.__leave_profile)
        self.Del_Profile.clicked.connect(self.__del_profile)
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
            self.Pomo_Start.setText("Начать фокусировку")
            self.pomo_seconds = 0
            self.pomo_flag = True

    def pomodoro_timer_on_off(self):
        if self.pomo_flag:
            self.pomo_seconds = 60 * self.pomo_minutes
            self.pomo_flag = False
        if self.Pomo_Start.text() == "Начать фокусировку" or self.Pomo_Start.text() == "Продолжить фокусировку":
            self.pomo_timer.start()
            self.Pomo_Start.setText("Приостановить")
        elif self.Pomo_Start.text() == "Приостановить":
            self.pomo_timer.stop()
            self.Pomo_Start.setText("Продолжить фокусировку")

    def show_Short(self):
        m, s = divmod(self.short_seconds, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        self.Short_LCD.display(self.min_sec_format)
        self.short_seconds -= 1
        if self.short_seconds < 0:
            self.pomo_timer.stop()
            self.Short_Start.setText("Начать перерыв")
            self.short_seconds = 0
            self.short_flag = True

    def short_timer_on_off(self):
        if self.short_flag:
            self.short_seconds = 60 * self.short_minutes
            self.short_flag = False
        if self.Short_Start.text() == "Начать перерыв" or self.Short_Start.text() == "Продолжить перерыв":
            self.short_timer.start()
            self.Short_Start.setText("Приостановить")
        elif self.Short_Start.text() == "Приостановить":
            self.short_timer.stop()
            self.Short_Start.setText("Продолжить перерыв")

    def show_Long(self):
        m, s = divmod(self.long_seconds, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        self.Long_LCD.display(self.min_sec_format)
        self.long_seconds -= 1
        if self.long_seconds < 0:
            self.pomo_timer.stop()
            self.Long_Start.setText("Начать перерыв")
            self.long_seconds = 0
            self.long_flag = True

    def long_timer_on_off(self):
        if self.long_flag:
            self.long_seconds = 60 * self.long_minutes
            self.long_flag = False
        if self.Long_Start.text() == "Начать перерыв" or self.Long_Start.text() == "Продолжить перерыв":
            self.long_timer.start()
            self.Long_Start.setText("Приостановить")
        elif self.Long_Start.text() == "Приостановить":
            self.long_timer.stop()
            self.Long_Start.setText("Продолжить перерыв")

    def Pomodoro_Reset(self):
        self.pomo_timer.stop()
        self.Pomo_Start.setText("Начать фокусировку")
        self.Pomo_LCD.display(f"{self.pomo_minutes}:00")
        self.pomo_flag = True

    def Short_Reset(self):
        self.short_timer.stop()
        self.Short_Start.setText("Начать перерыв")
        self.Short_LCD.display(f"0{self.short_minutes}:00")
        self.short_flag = True

    def Long_Reset(self):
        self.long_timer.stop()
        self.Long_Start.setText("Начать перерыв")
        self.Long_LCD.display(f"{self.long_minutes}:00")
        self.long_flag = True

    def ref_to_reg(self):
        self.to_reg.clicked.connect(lambda: self.log_cont.hide())
        self.to_reg.clicked.connect(lambda: self.reg_cont.show())

    def ref_to_log(self):
        self.to_log.clicked.connect(lambda: self.reg_cont.hide())
        self.to_log.clicked.connect(lambda: self.log_cont.show())

    def __reg(self):
        login = ui.login_reg.text()
        psw1 = ui.psw_fr_reg.text()
        psw2 = ui.psw_sc_reg.text()
        if len(login) < 3:
            ui.err_msg_reg2.setText("Длина логина должна быть больше 3-ёх")
        else:
            ui.err_msg_reg2.setText("")
        if len(psw1) < 8:
            ui.err_msg_reg3.setText("Длина пароля должна быть больше 8-ми")
        else:
            ui.err_msg_reg3.setText("")
            if psw1 == psw2:
                ui.err_msg_reg4.setText("")
                res = reg(login, psw1)
                if res["status"]:
                    ui.reg_cont.hide()
                    ui.account.show()
                    self.session["id"] = res["id"]
                    msg_box = QtWidgets.QMessageBox(ui)
                    msg_box.setText(res["msg"])
                    msg_box.show()
                else:
                    ui.err_msg_reg1.setText("Такой логин занят!")
            else:
                ui.err_msg_reg4.setText("Пароли должны совпадать")

    def __log(self):
        login = ui.login_log.text()
        psw = ui.psw_log.text()
        res = log(login, psw)
        if res["status"]:
            ui.log_cont.hide()
            ui.account.show()
            self.session["id"] = res["id"]
            msg_box = QtWidgets.QMessageBox(ui)
            msg_box.setText(res["msg"])
            msg_box.show()
        else:
            ui.err_msg_log.setText(res["msg"])

    def __clear_log_reg(self):
        ui.login_log.setText("")
        ui.psw_log.setText("")
        ui.login_reg.setText("")
        ui.psw_fr_reg.setText("")
        ui.psw_sc_reg.setText("")

        ui.err_msg_log.setText("")
        ui.err_msg_reg1.setText("")
        ui.err_msg_reg2.setText("")
        ui.err_msg_reg3.setText("")
        ui.err_msg_reg4.setText("")

    def __leave_profile(self):
        self.__clear_log_reg()
        self.session.pop("id")
        ui.account.hide()
        ui.reg_cont.hide()
        ui.log_cont.show()

    def __del_profile(self):
        psw, ok = QtWidgets.QInputDialog.getText(
            ui,
            "Внимание!",
            "Введите пароль:",
            QtWidgets.QLineEdit.Password
        )
        if ok:
            psw_res = chek_psw(self.session["id"], psw)
            if psw_res["status"]:
                del_res = del_profile(self.session["id"])
                self.__leave_profile()
                msg_box = QtWidgets.QMessageBox(ui)
                msg_box.setWindowTitle("Внимание!")
                msg_box.setText(del_res["msg"])
                msg_box.show()
            else:
                msg_box = QtWidgets.QMessageBox(ui)
                msg_box.setWindowTitle("Внимание!")
                msg_box.setText("Неверный пароль!")
                msg_box.show()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)

if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    ui = BeProductive()
    ui.ref_to_log()
    ui.ref_to_reg()
    ui.show()
    sys.exit(app.exec_())