import sys
from numpy import isnan, count_nonzero, dtype
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt, QSize, QRect, QCoreApplication
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLineEdit, QLabel, QRadioButton, QGridLayout, QFrame, QVBoxLayout

import MainCode


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        # The length of the outer list.
        return self._data.shape[0]

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


class ParameterWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ParameterWindow, self).__init__()
        self.setWindowIcon(QIcon("param_table_logo.png"))
        self.setWindowTitle("Таблица со значениями")
        self.central_widget = QtWidgets.QWidget(self)
        self.table = QtWidgets.QTableView(self.central_widget)
        self.resize(800, 600)
        self.data = MainCode.data
        self.grid_layout = QtWidgets.QGridLayout(self.central_widget)
        self.frame1 = QtWidgets.QFrame(self.central_widget)
        self.frame1.setMinimumSize(QSize(0, 25))
        self.push_button1 = QtWidgets.QPushButton(self.frame1)
        self.push_button1.setGeometry(QRect(10, 0, 160, 25))
        self.push_button1.setText(QCoreApplication.translate("", "Проверить данные на Nan'ы", None))
        self.push_button2 = QtWidgets.QPushButton(self.frame1)
        self.push_button2.setGeometry(QRect(170, 0, 120, 25))
        self.push_button2.setText(QCoreApplication.translate("", "Заполнить пропуски", None))
        self.push_button1.clicked.connect(self.is_nan)
        self.push_button2.clicked.connect(self.interpol_settings)

        self.grid_layout.addWidget(self.frame1, 0, 0, 1, 1)

        try:
            self.model = TableModel(self.data)
            self.table.setModel(self.model)
            self.grid_layout.addWidget(self.table, 1, 0, 1, 1)
        except Exception:
            self.no_data = QtWidgets.QLabel()
            self.no_data.setText("No data")
            self.grid_layout.addWidget(self.no_data, 1, 0, 1, 1)
        self.setCentralWidget(self.central_widget)

    def is_nan(self):
        nans = dict()
        for i in self.data.columns[:-1]:
            if dtype(self.data[i]) == object:
                nans.update(({i: "Дичь!"}))
            else:
                nan = isnan(self.data[i])
                if any(nan):
                    nans.update({i: count_nonzero(nan)})
        if nans:
            message = QMessageBox(self)
            message.setWindowTitle("Отчёт                                          ")
            message.setText(f"Параметр: количество пропусков\n{nans}")
            message.show()
        elif not nans:
            message1 = QMessageBox(self)
            message1.setWindowTitle("Отчёт                                          ")
            message1.setText("Пропусков нет!")
            message1.show()

    def fill_nans(self):
        self.method = "linear"
        self.degree = 0
        if self.radio_button_1.isChecked():
            self.method = "nearest"
        elif self.radio_button_2.isChecked():
            self.method = "linear"
        elif self.radio_button_3.isChecked():
            self.method = "polynomial"
            self.degree = int(self.line_edit.text())
        if self.degree:
            try:
                MainCode.data.interpolate(method="polynomial", limit_direction="both", inplace=True, order=self.degree)
                success = QMessageBox(self)
                success.setWindowTitle("Отчёт                                                ")
                success.setWindowIcon(QIcon("success_logo.png"))
                success.setText("Успешно!")
                success.show()
            except Exception:
                error = QMessageBox(self)
                error.setWindowTitle("Отчёт                                                 ")
                error.setWindowIcon(QIcon("error_logo.png"))
                error.setText("Упс! Что-то не получилось!\nПопробуйте заново.")
                error.show()
        else:
            try:
                MainCode.data.interpolate(method=self.method, limit_direction="both", inplace=True)
                success = QMessageBox(self)
                success.setWindowTitle("Отчёт                                                ")
                success.setWindowIcon(QIcon("success_logo.png"))
                success.setText("Успешно!")
                success.show()
            except Exception:
                error = QMessageBox(self)
                error.setWindowTitle("Отчёт                                                 ")
                error.setWindowIcon(QIcon("error_logo.png"))
                error.setText("Упс! Что-то не получилось!\nПопробуйте заново.")
                error.show()

    def interpol_settings(self):
        self.diag = QtWidgets.QDialog()
        self.vertical_layout = QVBoxLayout(self.diag)
        self.vertical_layout.setObjectName(u"verticalLayout")
        self.frame = QFrame(self.diag)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.grid_layout = QGridLayout(self.frame)
        self.grid_layout.setObjectName(u"gridLayout")
        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")
        self.label.setMinimumSize(QSize(200, 20))
        self.label.setMaximumSize(QSize(200, 20))

        self.grid_layout.addWidget(self.label, 0, 0, 1, 1)

        self.radio_button_1 = QRadioButton(self.frame)
        self.radio_button_1.setObjectName(u"radioButton")

        self.grid_layout.addWidget(self.radio_button_1, 2, 0, 1, 1)

        self.radio_button_2 = QRadioButton(self.frame)
        self.radio_button_2.setObjectName(u"radioButton_3")

        self.grid_layout.addWidget(self.radio_button_2, 3, 0, 1, 1)

        self.radio_button_3 = QRadioButton(self.frame)
        self.radio_button_3.setObjectName(u"radioButton_4")

        self.grid_layout.addWidget(self.radio_button_3, 4, 0, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setMinimumSize(QSize(200, 20))
        self.label_2.setMaximumSize(QSize(200, 20))

        self.grid_layout.addWidget(self.label_2, 5, 0, 1, 1)

        self.line_edit = QLineEdit(self.frame)
        self.line_edit.setObjectName(u"lineEdit")

        self.grid_layout.addWidget(self.line_edit, 6, 0, 1, 1)

        self.vertical_layout.addWidget(self.frame)

        self.push_button = QPushButton(self.diag)
        self.push_button.setObjectName(u"pushButton")

        self.vertical_layout.addWidget(self.push_button)


        self.push_button.clicked.connect(self.fill_nans)

        self.diag.setWindowTitle(QCoreApplication.translate("", "Интерполяция", None))
        self.label.setText(QCoreApplication.translate("", "Выберите метод интерполяции:", None))
        self.radio_button_1.setText(QCoreApplication.translate("", "Заполнить ближайшими значениями", None))
        self.radio_button_2.setText(QCoreApplication.translate("", "Линейная", None))
        self.radio_button_3.setText(QCoreApplication.translate("", "Полиномиальная (указать степень)", None))
        self.label_2.setText(QCoreApplication.translate("", "Степень полинома (для полиномиальной)", None))
        self.push_button.setText(QCoreApplication.translate("", "Интерполировать", None))

        self.diag.show()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = ParameterWindow()
    window.show()
    app.exec()
