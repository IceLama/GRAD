from numpy import isnan, count_nonzero, dtype
from PyQt5.QtCore import Qt, QSize, QRect, QCoreApplication, QAbstractTableModel
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QPushButton, QLineEdit, QLabel, QRadioButton, QGridLayout, QFrame, \
    QVBoxLayout, QWidget, QTableView, QMainWindow, QDialog
import MainCode


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index,  role):
        if role == Qt.DisplayRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


# noinspection PyBroadException
class ParameterWindow(QMainWindow):
    dialog: QDialog
    vertical_layout: QVBoxLayout
    frame: QFrame
    label: QLabel
    radio_button_1: QRadioButton
    radio_button_2: QRadioButton
    radio_button_3: QRadioButton
    label_2: QLabel
    line_edit: QLineEdit
    push_button: QPushButton
    message_1: QMessageBox
    message_2: QMessageBox
    success: QMessageBox
    error_1: QMessageBox
    error_2: QMessageBox

    def __init__(self):
        super(ParameterWindow, self).__init__()
        self.setWindowIcon(QIcon("logos/param_table_logo.png"))
        self.setWindowTitle("Таблица со значениями")
        self.central_widget = QWidget(self)
        self.table = QTableView(self.central_widget)
        self.resize(800, 600)
        self.data = MainCode.data
        self.grid_layout = QGridLayout(self.central_widget)
        self.frame1 = QFrame(self.central_widget)
        self.frame1.setMinimumSize(QSize(0, 25))
        self.push_button_1 = QPushButton(self.frame1)
        self.push_button_1.setGeometry(QRect(0, 0, 180, 25))
        self.push_button_1.setText(QCoreApplication.translate("", "Проверить данные на пропуски", None))
        self.push_button_1.setWhatsThis(
            QCoreApplication.translate("", "Проверка данных на пропущенные значения. Если таковые есть, то они "
                                           "обозначены как NaN. Если в значениях параметра разные типы данных или все "
                                           "значения None - выдаст, что 'Параметр такой-то': 'Дичь!'"
                                           "\nВнимание! Во избежание несчастных случаев крайне не рекомендуется "
                                           "добавлять новые параметры, когда открыто это окно."))
        self.push_button_2 = QPushButton(self.frame1)
        self.push_button_2.setGeometry(QRect(180, 0, 120, 25))
        self.push_button_2.setText(QCoreApplication.translate("", "Заполнить пропуски", None))
        self.push_button_1.clicked.connect(self.is_nan)
        self.push_button_2.clicked.connect(self.interpol_settings)

        self.grid_layout.addWidget(self.frame1, 0, 0, 1, 1)

        try:
            self.model = TableModel(self.data)
            self.table.setModel(self.model)
            self.grid_layout.addWidget(self.table, 1, 0, 1, 1)
        except Exception:
            self.no_data = QLabel()
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
            self.message_1 = QMessageBox()
            self.message_1.setWindowIcon(QIcon("logos/error_logo.png"))
            self.message_1.setWindowTitle("Отчёт                                                                ")
            self.message_1.setText(f"Параметр - количество пропусков:\n{[f'{i} - {nans.get(i)}' for i in nans]}")
            self.message_1.show()
        elif not nans:
            self.message_2 = QMessageBox()
            self.message_2.setWindowIcon(QIcon("logos/success_logo.png"))
            self.message_2.setWindowTitle("Отчёт                                                              ")
            self.message_2.setText("Пропусков нет!")
            self.message_2.show()

    #
    def fill_nans(self):
        method = ""
        degree = 0
        if self.radio_button_1.isChecked():
            method = "nearest"
        elif self.radio_button_2.isChecked():
            method = "linear"
        elif self.radio_button_3.isChecked():
            method = "polynomial"
            degree = int(self.line_edit.text())
        if method:
            try:
                MainCode.data.interpolate(method=method, limit_direction="both", inplace=True, order=degree)
                self.success = QMessageBox()
                self.success.setWindowTitle("Отчёт                                                ")
                self.success.setWindowIcon(QIcon("logos/success_logo.png"))
                self.success.setText("Успешно!")
                self.success.show()
            except Exception:
                self.error_1 = QMessageBox()
                self.error_1.setWindowTitle("Отчёт                                                 ")
                self.error_1.setWindowIcon(QIcon("logos/error_logo.png"))
                self.error_1.setText("Упс! Что-то не получилось!\nПопробуйте заново.")
                self.error_1.show()
        else:
            self.error_2 = QMessageBox(self)
            self.error_2.setWindowTitle("Что-то не так!                                            ")
            self.error_2.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_2.setText("Выберите метод для интерполяции")
            self.error_2.show()

    def interpol_settings(self):
        self.dialog = QDialog()
        self.vertical_layout = QVBoxLayout(self.dialog)
        self.frame = QFrame(self.dialog)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.grid_layout = QGridLayout(self.frame)
        self.label = QLabel(self.frame)
        self.label.setMinimumSize(QSize(200, 20))
        self.label.setMaximumSize(QSize(200, 20))

        self.grid_layout.addWidget(self.label, 0, 0, 1, 1)

        self.radio_button_1 = QRadioButton(self.frame)

        self.grid_layout.addWidget(self.radio_button_1, 2, 0, 1, 1)

        self.radio_button_2 = QRadioButton(self.frame)

        self.grid_layout.addWidget(self.radio_button_2, 3, 0, 1, 1)

        self.radio_button_3 = QRadioButton(self.frame)

        self.grid_layout.addWidget(self.radio_button_3, 4, 0, 1, 1)

        self.label_2 = QLabel(self.frame)
        self.label_2.setMinimumSize(QSize(230, 20))
        self.label_2.setMaximumSize(QSize(230, 20))

        self.grid_layout.addWidget(self.label_2, 5, 0, 1, 1)

        self.line_edit = QLineEdit(self.frame)
        self.line_edit.setText("1")

        self.grid_layout.addWidget(self.line_edit, 6, 0, 1, 1)

        self.vertical_layout.addWidget(self.frame)

        self.push_button = QPushButton(self.dialog)

        self.vertical_layout.addWidget(self.push_button)
        self.push_button.clicked.connect(self.fill_nans)

        self.dialog.setWindowTitle(QCoreApplication.translate("", "Интерполяция", None))
        self.label.setText(QCoreApplication.translate("", "Выберите метод интерполяции:", None))
        self.radio_button_1.setText(QCoreApplication.translate("", "Заполнить ближайшими значениями", None))
        self.radio_button_2.setText(QCoreApplication.translate("", "Линейная", None))
        self.radio_button_3.setText(QCoreApplication.translate("", "Полиномиальная (указать степень)", None))
        self.label_2.setText(QCoreApplication.translate("", "Степень полинома (для полиномиальной)", None))
        self.push_button.setText(QCoreApplication.translate("", "Интерполировать", None))

        self.dialog.show()
