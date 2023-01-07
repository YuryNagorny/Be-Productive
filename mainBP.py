import sys
import traceback
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QInputDialog, QMessageBox, QLineEdit
from PyQt5.QtCore import QTimer
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import *
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
        self.Log_Out.clicked.connect(self.__leave_profile)
        self.Del_Profile.clicked.connect(self.__del_profile)
        self.account.hide()
        self.reg_window.hide()
        self.log_flag = False
        self.Frame_color.clicked.connect(self.frame_color)
        self.App_color.clicked.connect(self.app_color)
        self.Text_color.clicked.connect(self.text_color)
        self.palette = self.palette()
        self.palette.setColor(QPalette.Window, QColor(186, 73, 73))
        self.palette.setColor(QPalette.Button, QColor(186, 73, 73))
        self.palette.setColor(QPalette.WindowText, QColor(186, 73, 73))
        self.setPalette(self.palette)
        self.color_dialog = QtWidgets.QColorDialog(self)
        self.color_dialog.currentColorChanged.connect(self.on_currentColorChanged)
        self.color = QColor(186, 73, 73)
        self.Add_Task.clicked.connect(self.add_task)
        self.Edit_Task.clicked.connect(self.edit_task)
        self.Del_Cur_Task.clicked.connect(self.remove_task)
        self.Clear_List.clicked.connect(lambda: self.clear_list())
        self.Make_Up.clicked.connect(lambda: self.up_task())
        self.Make_Down.clicked.connect(lambda: self.down_task())

    def add_task(self):
        currentIndex = self.List_Task.currentRow()
        text, ok = QInputDialog.getText(self, "Новая задача", "Напишите название задачи:")
        if ok and text is not None:
            self.List_Task.insertItem(currentIndex, text)

    def edit_task(self):
        currentIndex = self.List_Task.currentRow()
        item = self.List_Task.item(currentIndex)
        if item is not None:
            text, ok = QInputDialog.getText(self, "Edit Student", "Student Name", QLineEdit.Normal, item.text())
            if text and ok is not None:
                item.setText(text)

    def remove_task(self):
        currentIndex = self.List_Task.currentRow()
        item = self.List_Task.item(currentIndex)
        if item is None:
            return

        question = QMessageBox.question(self, "Удаление задачи",
                                        "Вы точно хотите удалить задачу?" + item.text(),
                                        QMessageBox.Yes | QMessageBox.No)

        if question == QMessageBox.Yes:
            item = self.List_Task.takeItem(currentIndex)
            del item

    def up_task(self):
        index = self.List_Task.currentRow()
        if index >= 1:
            item = self.List_Task.takeItem(index)
            self.List_Task.insertItem(index - 1, item)
            self.List_Task.setCurrentItem(item)

    def down_task(self):
        index = self.List_Task.currentRow()
        if index < self.List_Task.count() - 1:
            item = self.List_Task.takeItem(index)
            self.List_Task.insertItem(index + 1, item)
            self.List_Task.setCurrentItem(item)

    def clear_list(self): #очистка списка задач
        self.List_Task.clear()

    def frame_color(self): #изменение цвета рамки приложения
        self.color_dialog.exec_()
        self.palette.setColor(QPalette.Window, self.color)
        self.setPalette(self.palette)

    def app_color(self): #изменение цвета темы
        self.color_dialog.exec_()
        self.palette.setColor(QPalette.Button, self.color)
        self.setPalette(self.palette)

    def text_color(self): #изменение цвета текста
        self.color_dialog.exec_()
        self.palette.setColor(QPalette.WindowText, self.color)
        self.palette.setColor(QPalette.ButtonText, self.color)
        self.setPalette(self.palette)

    @QtCore.pyqtSlot(QColor)
    def on_currentColorChanged(self, color):
        self.color = color

    def save_changes(self): #сохранение изменений
        self.pomo_minutes = int(self.Pomo_Slider.value())
        self.Pomo_LCD.display(f"{self.pomo_minutes}:00")
        self.short_minutes = int(self.Short_Slider.value())
        self.Short_LCD.display(f"0{self.short_minutes}:00")
        self.long_minutes = int(self.Long_Slider.value())
        self.Long_LCD.display(f"{self.long_minutes}:00")
        self.pomo_flag = True
        self.short_flag = True
        self.long_flag = True

    def show_Pomo(self): #таймер Pomodoro
        m, s = divmod(self.pomo_seconds, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        self.Pomo_LCD.display(self.min_sec_format)
        self.pomo_seconds -= 1
        if self.log_flag:
            count_seconds(self.session["id"])
            place_res = return_place(self.session["id"])
            sec_res = return_seconds(self.session["id"])
            self.Num_place.setText(str(place_res["place"]))
            self.Num_total.setText(str(round(sec_res["seconds"] / 3600, 2)))
        if self.pomo_seconds < 0:
            self.pomo_timer.stop()
            self.Pomo_Start.setText("Начать фокусировку")
            self.pomo_seconds = 0
            self.pomo_flag = True

    def pomodoro_timer_on_off(self): #обработка остановки / повторного запуска таймера Pomodoro
        if self.pomo_flag:
            self.pomo_seconds = 60 * self.pomo_minutes
            self.pomo_flag = False
        if self.Pomo_Start.text() == "Начать фокусировку" or self.Pomo_Start.text() == "Продолжить фокусировку":
            self.pomo_timer.start()
            self.Pomo_Start.setText("Приостановить")
        elif self.Pomo_Start.text() == "Приостановить":
            self.pomo_timer.stop()
            self.Pomo_Start.setText("Продолжить фокусировку")

    def show_Short(self): #таймер короткого перерыва
        m, s = divmod(self.short_seconds, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        self.Short_LCD.display(self.min_sec_format)
        self.short_seconds -= 1
        if self.short_seconds < 0:
            self.pomo_timer.stop()
            self.Short_Start.setText("Начать перерыв")
            self.short_seconds = 0
            self.short_flag = True

    def short_timer_on_off(self): #обработка остановки / повторного запуска таймера короткого перерыва
        if self.short_flag:
            self.short_seconds = 60 * self.short_minutes
            self.short_flag = False
        if self.Short_Start.text() == "Начать перерыв" or self.Short_Start.text() == "Продолжить перерыв":
            self.short_timer.start()
            self.Short_Start.setText("Приостановить")
        elif self.Short_Start.text() == "Приостановить":
            self.short_timer.stop()
            self.Short_Start.setText("Продолжить перерыв")

    def show_Long(self): #таймер длинного перерыва
        m, s = divmod(self.long_seconds, 60)
        self.min_sec_format = '{:02d}:{:02d}'.format(m, s)
        self.Long_LCD.display(self.min_sec_format)
        self.long_seconds -= 1
        if self.long_seconds < 0:
            self.pomo_timer.stop()
            self.Long_Start.setText("Начать перерыв")
            self.long_seconds = 0
            self.long_flag = True

    def long_timer_on_off(self): #обработка остановки / повторного запуска таймера длинного перерыва
        if self.long_flag:
            self.long_seconds = 60 * self.long_minutes
            self.long_flag = False
        if self.Long_Start.text() == "Начать перерыв" or self.Long_Start.text() == "Продолжить перерыв":
            self.long_timer.start()
            self.Long_Start.setText("Приостановить")
        elif self.Long_Start.text() == "Приостановить":
            self.long_timer.stop()
            self.Long_Start.setText("Продолжить перерыв")

    def Pomodoro_Reset(self): #обработка сброса таймера Pomodoro
        self.pomo_timer.stop()
        self.Pomo_Start.setText("Начать фокусировку")
        self.Pomo_LCD.display(f"{self.pomo_minutes}:00")
        self.pomo_flag = True

    def Short_Reset(self): #обработка сброса таймера короткого перерыва
        self.short_timer.stop()
        self.Short_Start.setText("Начать перерыв")
        self.Short_LCD.display(f"0{self.short_minutes}:00")
        self.short_flag = True

    def Long_Reset(self): #обработка сброса таймера длинного перерыва
        self.long_timer.stop()
        self.Long_Start.setText("Начать перерыв")
        self.Long_LCD.display(f"{self.long_minutes}:00")
        self.long_flag = True

    def reset_all_timers(self): #сброс всех таймеров
        self.Pomodoro_Reset()
        self.Short_Reset()
        self.Long_Reset()

    def log_to_reg(self): #переключение между окнами входа и регистрации
        self.to_reg_btn.clicked.connect(lambda: self.log_window.hide())
        self.to_reg_btn.clicked.connect(lambda: self.reg_window.show())

    def reg_to_log(self): #переключение между окнами регистрации и входа
        self.to_log_btn.clicked.connect(lambda: self.reg_window.hide())
        self.to_log_btn.clicked.connect(lambda: self.log_window.show())

    def __reg(self): #регистрация пользователя
        login = ex.login_reg.text()
        password1 = ex.password1.text()
        password2 = ex.password2.text()
        if len(login) < 3:
            ex.error_reg2.setText("Длина логина должна быть больше 3-ёх")
        else:
            ex.error_reg2.setText("")
        if len(password1) < 8:
            ex.error_reg3.setText("Длина пароля должна быть больше 8-ми")
        else:
            ex.error_reg3.setText("")
            if password1 == password2:
                ex.error_reg4.setText("")
                res = reg(login, password1)
                if res["status"]:
                    ex.reg_window.hide()
                    ex.account.show()
                    self.session["id"] = res["id"]
                    msg_box = QMessageBox(ex)
                    msg_box.setText(res["msg"])
                    msg_box.show()
                    self.log_flag = True
                else:
                    ex.error_reg1.setText("Такой логин занят!")
            else:
                ex.error_reg4.setText("Пароли должны совпадать!")

    def __log(self): #вход пользователя в свой профиль
        login = ex.login_log.text()
        password = ex.password_log.text()
        res = log(login, password)
        if res["status"]:
            self.session["id"] = res["id"]
            ex.log_window.hide()
            ex.account.show()
            msg_box = QMessageBox(ex)
            msg_box.setText(res["msg"])
            msg_box.show()
            self.log_flag = True
            place_res = return_place(self.session["id"])
            sec_res = return_seconds(self.session["id"])
            self.Num_place.setText(str(place_res["place"]))
            self.Num_total.setText(str(round(sec_res["seconds"] / 3600, 2)))
        else:
            ex.err_msg_log.setText(res["msg"])

    def __clear_log_and_reg(self): #очистка окон регистрации и входа
        ex.login_log.setText("")
        ex.password_log.setText("")
        ex.login_reg.setText("")
        ex.password_reg1.setText("")
        ex.password_reg1.setText("")
        ex.error_log.setText("")
        ex.error_reg1.setText("")
        ex.error_reg2.setText("")
        ex.error_reg3.setText("")
        ex.error_reg4.setText("")

    def __leave_profile(self): #обработка выхода пользователя из профиля
        self.__clear_log_and_reg()
        self.session.pop("id")
        self.reset_all_timers()
        ex.account.hide()
        ex.reg_window.hide()
        ex.log_window.show()
        self.log_flag = False

    def __del_profile(self): #обработка удаления пользователем своего профиля
        password, ok = QInputDialog.getText(
            ex,
            "Внимание!",
            "Введите пароль:",
            QLineEdit.Password
        )
        if ok:
            password_res = check_password(self.session["id"], password)
            if password_res["status"]:
                del_res = del_profile(self.session["id"])
                self.__leave_profile()
                msg_box = QtWidgets.QMessageBox(ex)
                msg_box.setWindowTitle("Внимание!")
                msg_box.setText(del_res["msg"])
                msg_box.show()
                self.reset_all_timers()
                self.log_flag = False
            else:
                msg_box = QMessageBox(ex)
                msg_box.setWindowTitle("Внимание!")
                msg_box.setText("Неверный пароль!")
                msg_box.show()


def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    print("Oбнаружена ошибка !:", tb)


if __name__ == '__main__':
    sys.excepthook = excepthook
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    ex = BeProductive()
    ex.reg_to_log()
    ex.log_to_reg()
    ex.show()
    sys.exit(app.exec_())