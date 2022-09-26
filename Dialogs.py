from PyQt5.QtCore import QSize, QMetaObject, QCoreApplication, QStringListModel, Qt, QAbstractTableModel, QRect
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QAbstractItemView, QDialogButtonBox, QVBoxLayout, \
    QWidget, QListView, QHBoxLayout, QPushButton, QRadioButton, QLabel, QInputDialog, \
    QApplication, QGridLayout, QSizePolicy, QFrame, QFileDialog, QMessageBox, QSpacerItem, QSpinBox, QDialog, \
    QPlainTextEdit, QTableView, QCheckBox, QLineEdit
from pandas import DataFrame

import MainCode
from MainCode import Files, Methods, Parameters
import GraphicsMatplotlib


class ParameterUiDialog(QWidget):
    def __init__(self):
        super(ParameterUiDialog, self).__init__()

    def setup_ui(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName("Dialog")
        dialog.resize(700, 800)
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        dialog.setWindowIcon(QIcon("formulas_logo.png"))
        self.grid_layout = QGridLayout(dialog)
        self.frame = QFrame(dialog)
        self.frame.setObjectName(u"widget")
        self.frame.setMinimumSize(QSize(100, 30))
        self.vertical_layout = QVBoxLayout(self.frame)
        self.vertical_layout.setObjectName(u"verticalLayout_2")
        self.widget_1 = QWidget(self.frame)
        self.horizontalLayout_1 = QHBoxLayout(self.widget_1)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout")

        self.label_1 = QLabel(self.frame)
        self.label_1.setText("Будьте бдительны, 'Ctrl Z' здесь не работает!")
        self.vertical_layout.addWidget(self.label_1)
        self.pushButton_1 = QPushButton(self.widget_1)
        self.pushButton_1.setObjectName(u"pushButton")

        self.horizontalLayout_1.addWidget(self.pushButton_1)

        self.pushButton_2 = QPushButton(self.widget_1)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout_1.addWidget(self.pushButton_2)

        self.pushButton_4 = QPushButton(self.widget_1)
        self.pushButton_4.setObjectName("pushButton_4")

        self.horizontalLayout_1.addWidget(self.pushButton_4)

        self.pushButton_3 = QPushButton(self.widget_1)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout_1.addWidget(self.pushButton_3)

        self.pushButton_5 = QPushButton(self.widget_1)
        self.pushButton_5.setObjectName("pushButton_5")

        self.horizontalLayout_1.addWidget(self.pushButton_5)

        self.vertical_layout.addWidget(self.widget_1)

        self.widget_2 = QWidget(self.frame)
        self.horizontalLayout_2 = QHBoxLayout(self.widget_2)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout")

        self.pushButton_6 = QPushButton(self.widget_2)
        self.pushButton_6.setObjectName(u"pushButton_6")

        self.horizontalLayout_2.addWidget(self.pushButton_6)

        self.pushButton_7 = QPushButton(self.widget_2)
        self.pushButton_7.setObjectName(u"pushButton_7")

        self.horizontalLayout_2.addWidget(self.pushButton_7)

        self.pushButton_8 = QPushButton(self.widget_2)
        self.pushButton_8.setObjectName(u"pushButton_8")

        self.horizontalLayout_2.addWidget(self.pushButton_8)

        self.pushButton_9 = QPushButton(self.widget_2)
        self.pushButton_9.setObjectName(u"pushButton_9")

        self.horizontalLayout_2.addWidget(self.pushButton_9)

        self.pushButton_10 = QPushButton(self.widget_2)
        self.pushButton_10.setObjectName(u"pushButton_10")

        self.horizontalLayout_2.addWidget(self.pushButton_10)


        self.vertical_layout.addWidget(self.widget_2)

        self.grid_layout.addWidget(self.frame, 1, 0, 1, 1)

        self.table_view = QTableView(dialog)
        self.table_view.setEditTriggers(QAbstractItemView.CurrentChanged | QAbstractItemView.EditKeyPressed)
        self.label_err = QLabel("Нет данных")
        try:
            data_to_show = MainCode.data.columns[:-1:]
            self.rows_count = len(data_to_show)
            self.formulas = MainCode.data["__Формулы__"][:self.rows_count:]
            self.rows_names = data_to_show
            data_b = {"Параметры": self.rows_names, "Формула": self.formulas}
            self.data = DataFrame(data_b)
            self.model = TableModel(self.data)
            self.table_view.setModel(self.model)
        except Exception:
            self.vertical_layout.addWidget(self.label_err)

        self.grid_layout.addWidget(self.table_view, 4, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.grid_layout.addWidget(self.buttonBox, 5, 0, 1, 1)

        self.retranslate_ui(dialog)

        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)

        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.pushButton_1.clicked.connect(self.add_parameter_pd)
        self.pushButton_2.clicked.connect(self.delete_parameter_pd)
        self.pushButton_3.clicked.connect(self.add_formula_pd)
        self.pushButton_4.clicked.connect(self.rename_parameter_pd)
        self.pushButton_5.clicked.connect(self.copy_parameters_pd)
        self.pushButton_6.clicked.connect(self.add_zero_parameters_pd)
        self.pushButton_7.clicked.connect(self.add_h_parameters_pd)
        self.pushButton_8.clicked.connect(self.key_c_pressed)
        self.table_view.doubleClicked.connect(self.db_edit)
        dialog.accepted.connect(self.accepted_event)
        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Параметры", None))
        self.pushButton_1.setText(QCoreApplication.translate("Dialog", "Добавить параметр", None))
        self.pushButton_1.setShortcut(QCoreApplication.translate("dialog", "insert"))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", "Удалить параметр", None))
        self.pushButton_2.setShortcut(QCoreApplication.translate("dialog", "delete"))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", "Добавить формулу", None))
        self.pushButton_4.setText(QCoreApplication.translate("dialog", "Переименовать", None))
        self.pushButton_5.setText(QCoreApplication.translate("dialog", "Создать копию", None))
        self.pushButton_6.setText(QCoreApplication.translate("dialog", "Создать копию с _0", None))
        self.pushButton_7.setText(QCoreApplication.translate("dialog", "Создать копию с _h", None))
        self.pushButton_8.setText(QCoreApplication.translate("dialog", "Копировать в буфер", None))
        self.pushButton_8.setShortcut(QCoreApplication.translate("Dialog", "ctrl+c"))
        self.pushButton_9.setText(QCoreApplication.translate("dialog", "Заглушка 2", None))
        self.pushButton_10.setText(QCoreApplication.translate("dialog", "Заглушка 3", None))


    def update_data(self):
        data_to_show = MainCode.data.columns[:-1:]
        self.rows_count = len(data_to_show)
        self.formulas = MainCode.data["__Формулы__"][:self.rows_count:]
        self.rows_names = data_to_show
        data_b = {"Параметры": self.rows_names, "Формула": self.formulas}
        self.data = DataFrame(data_b)
        self.model = TableModel(self.data)
        self.table_view.setModel(self.model)

    def db_edit(self):
        item = self.table_view.currentIndex()
        col = item.column()
        if col == 0:
            self.rename_parameter_pd()
        elif col == 1:
            self.add_formula_pd()

    def add_parameter_pd(self):
        parameter_name, ok = QInputDialog.getText(QWidget(), "Новый параметр",
                                                  "Введите название параметра:                                        ")
        if ok and parameter_name:
            if parameter_name in MainCode.data.columns:
                message = QMessageBox(self)
                message.setWindowTitle("Новый параметр")
                message.setFocusPolicy(Qt.StrongFocus)
                message.setText("Параметр с таким названием уже существует!")
                message.show()
            elif parameter_name == "Time":
                freq, f = QInputDialog.getInt(QWidget(), "Частота", "Введите частоту: ")
                Parameters.add_parameter(input_name=parameter_name, freq=freq)
            else:
                Parameters.add_parameter(parameter_name)
        elif not ok:
            pass
        else:
            message = QMessageBox(self)
            message.setWindowTitle("Новый параметр")
            message.setFocusPolicy(Qt.StrongFocus)
            message.setText("Введите название параметра!")
            message.show()
        self.update_data()

    def add_formula_pd(self):
        item = self.table_view.currentIndex()
        index = item.row()
        parameter_name = self.table_view.model().index(index, 0).data(0)
        if parameter_name:
            f = QDialog(self)
            f.ui = AddFormulaDialog(parameter_name=parameter_name, index=index)
            f.ui.setup_ui(f)
            f.show()
            if f.exec():
                if f.ui.accept():
                    self.update_data()
                else:
                    message = QMessageBox(self)
                    message.setWindowTitle("Упс! Что-то пошло не так.")
                    message.setFocusPolicy(Qt.StrongFocus)
                    message.setText("Проверьте формулу и введите её заново!")
                    message.show()
                    self.update_data()
        else:
            pass

    def delete_parameter_pd(self):
        items = self.table_view.selectedIndexes()
        indexes = set([i.row() for i in items])
        parameters_names = []
        for index in indexes:
            parameters_names.append(self.table_view.model().index(index, 0).data(0))
        quest = QMessageBox()
        ok = quest.question(self, "", f"Удалить выбранные параметры?", quest.Yes | quest.No)
        if ok == quest.Yes:
            Parameters.delete_parameters(parameters_names=parameters_names, indexes=indexes)
        self.update_data()

    def rename_parameter_pd(self):
        item = self.table_view.currentIndex()
        index = item.row()
        name = self.table_view.model().index(index, 0).data(0)
        new_name, ok = QInputDialog.getText(QWidget(), f"Переименовываем параметр: {name}",
                                            "Новое название параметра:                                                 "
                                            "                                                                         ",
                                            text=f"{name}")
        if ok and new_name:
            if new_name in MainCode.data.columns:
                message = QMessageBox(self)
                message.setWindowTitle("Новое название")
                message.setFocusPolicy(Qt.StrongFocus)
                message.setText("Параметр с таким названием уже существует!")
                message.show()
            else:
                Parameters.rename_parameter(name, new_name)
                self.update_data()
        elif not ok:
            pass
        else:
            message = QMessageBox(self)
            message.setWindowTitle("Новое название")
            message.setFocusPolicy(Qt.StrongFocus)
            message.setText("Введите новое название параметра!")
            message.show()

    def copy_parameters_pd(self):
        items = self.table_view.selectedIndexes()
        indexes = set([i.row() for i in items])
        parameters_names = []
        for index in indexes:
            parameters_names.append(self.table_view.model().index(index, 0).data(0))
        ok = Parameters.copy_parameters(parameters_names)
        if ok:
            self.update_data()
        else:
            self.error1 = QMessageBox()
            self.error1.setWindowTitle("Ошибка!")
            self.error1.setWindowIcon(QIcon("error_logo.png"))
            self.error1.setText("Что-то не получилось! Возможно такие параметры уже есть!")
            self.error1.show()

    def add_zero_parameters_pd(self):
        items = self.table_view.selectedIndexes()
        indexes = set([i.row() for i in items])
        parameters_names = []
        for index in indexes:
            parameters_names.append(self.table_view.model().index(index, 0).data(0))
        ok = Parameters.add_zero_parameters(parameters_names)
        if ok:
            self.update_data()
        else:
            self.error2 = QMessageBox()
            self.error2.setWindowTitle("Ошибка!")
            self.error2.setWindowIcon(QIcon("error_logo.png"))
            self.error2.setText("Что-то не получилось! Возможно такие параметры уже есть!")
            self.error2.show()

    def add_h_parameters_pd(self):
        items = self.table_view.selectedIndexes()
        indexes = set([i.row() for i in items])
        parameters_names = []
        for index in indexes:
            parameters_names.append(self.table_view.model().index(index, 0).data(0))
        ok = Parameters.add_h_parameters(parameters_names)
        if ok:
            self.update_data()
        else:
            self.error3 = QMessageBox()
            self.error3.setWindowTitle("Ошибка!")
            self.error3.setWindowIcon(QIcon("error_logo.png"))
            self.error3.setText("Что-то не получилось! Возможно такие параметры уже есть!")
            self.error3.show()

    def key_c_pressed(self):
        copied_cells = self.table_view.selectedIndexes()
        copy_text = ""
        if copied_cells:
            max_column = copied_cells[-1].column()
            for c in copied_cells:
                copy_text += self.table_view.model().index(c.row(), c.column()).data(0)
                if c.column() == max_column:
                    copy_text += '\n'
                else:
                    copy_text += '\t'

            QApplication.clipboard().setText(copy_text)
        else:
            pass

    def accepted_event(self):
        ok, err_req = MainCode.Parameters.accept_formulas()
        if ok:
            pass
        else:
            self.error4 = QMessageBox()
            self.error4.setWindowTitle("Ошибки в формулах!                                       ")
            self.error4.setWindowIcon(QIcon("error_logo.png"))
            self.error4.setText(f"Ошибка в формуле параметра: {err_req}")
            self.error4.show()


################################################################################


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
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

    def setData(self, index, value, role):
        if role == Qt.EditRole:
            self._data.iloc[index.row(), index.column()] = value
            return True
        return False

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if role == Qt.ItemDataRole.DisplayRole:
            if orientation == Qt.Horizontal:
                return str(self._data.columns[section])

            if orientation == Qt.Vertical:
                return str(self._data.index[section])


################################################################################


class AddFormulaDialog(object):
    def __init__(self, parameter_name: str, index: str):
        self.parameter_name = parameter_name
        self.index = index
        self.text = MainCode.data["__Формулы__"][self.index]

    def setup_ui(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(1100, 400)
        Dialog.setMinimumSize(QSize(0, 0))
        Dialog.setWindowIcon(QIcon("formulas_logo.png"))
        self.vertical_layout = QVBoxLayout(Dialog)
        self.vertical_layout.setObjectName(u"verticalLayout")
        self.frame = QFrame(Dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontal_layout = QHBoxLayout(self.frame)
        self.horizontal_layout.setObjectName(u"horizontalLayout")
        self.text_edit = QPlainTextEdit(self.frame)
        self.text_edit.setObjectName(u"textEdit")
        self.text_edit.setMinimumSize(QSize(550, 0))
        if self.text == "no formula":
            self.text_edit.insertPlainText("")
        else:
            self.text_edit.insertPlainText(self.text)
        font = QFont()
        font.setFamily("Calibri")
        font.setPointSize(12)
        self.text_edit.setFont(font)

        self.horizontal_layout.addWidget(self.text_edit)

        self.vertical_spacer = QSpacerItem(10, 309, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.horizontal_layout.addItem(self.vertical_spacer)

        self.list_view = QListView(self.frame)
        self.list_view.setObjectName(u"listView")
        self.list_view.setMinimumSize(QSize(200, 0))
        self.list_view.setMaximumSize(QSize(200, 16777215))
        self.list_view.setAlternatingRowColors(True)
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_text = MainCode.data.columns[:-1]
        self.model = QStringListModel(self.list_text)
        self.list_view.setModel(self.model)

        self.horizontal_layout.addWidget(self.list_view)

        self.vertical_layout.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout.addWidget(self.buttonBox)

        self.check_box = QCheckBox(Dialog)
        self.check_box.setObjectName("check_box")
        self.vertical_layout.addWidget(self.check_box)
        self.check_box.toggled.connect(self.checked)


        self.retranslate_ui(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.list_view.doubleClicked.connect(self.add_param)
        Dialog.accepted.connect(self.accept)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("Dialog",
                                                         f"Ввод формулы для параметра: {self.parameter_name}",
                                                         None))
        self.check_box.setText(QCoreApplication.translate("Dialog", "Логику?", None))

    def add_param(self):
        item = self.list_view.currentIndex().data()
        self.text_edit.insertPlainText(item)

    def checked(self):
        self.text = \
            f"data.loc[:, '{self.parameter_name}'] = np.where((data['Time'] > 0) & (data['Time'] <= data['t1']), " \
            f"значение, data['{self.parameter_name}']);\n" \
            f"data.loc[:, '{self.parameter_name}'] = np.where((data['Time'] > data['t1']) & " \
            f"(data['Time'] <= data['t2']), значение, data['{self.parameter_name}']);"
        self.text_edit.clear()
        self.text_edit.insertPlainText(self.text)

    def accept(self):
        formula = self.text_edit.toPlainText()
        ok = Parameters.add_formula(parameter_name=self.parameter_name,
                                    formula=formula)
        return ok


################################################################################
################################################################################


class GraphicByTimeUiDialog(object):
    def setup_ui(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(500, 600)
        Dialog.setWindowIcon(QIcon("graphic_sharex_logo.png"))
        self.item_list_2 = [i for i in MainCode.data.columns[:-1:]]
        self.file_name = MainCode.file_name_g
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.listView_1 = QListView(self.widget_4)
        self.listView_1.setObjectName(u"listView")
        self.item_list_1 = []
        self.model_1 = QStringListModel(self.widget)
        self.model_1.setStringList(self.item_list_1)
        self.listView_1.setModel(self.model_1)

        self.horizontalLayout_3.addWidget(self.listView_1)

        self.listView_2 = QListView(self.widget_4)
        self.listView_2.setObjectName(u"listView_2")
        self.model_2 = QStringListModel(self.widget)
        self.model_2.setStringList(self.item_list_2)
        self.listView_2.setModel(self.model_2)
        self.listView_2.setEditTriggers(
            QAbstractItemView.AnyKeyPressed | QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)
        self.listView_2.setTabKeyNavigation(True)
        self.listView_2.setSelectionMode(QAbstractItemView.MultiSelection)

        self.horizontalLayout_3.addWidget(self.listView_2)

        self.verticalLayout.addWidget(self.widget_4)

        self.pushButton_1 = QPushButton(self.widget)
        self.pushButton_1.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton_1)

        self.pushButton_4 = QPushButton(self.widget)
        self.pushButton_4.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_4)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(100, 35))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.radioButton_1 = QRadioButton(self.widget_3)
        self.radioButton_1.setObjectName(u"radioButton")

        self.horizontalLayout_2.addWidget(self.radioButton_1)

        self.radioButton_2 = QRadioButton(self.widget_3)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.horizontalLayout_2.addWidget(self.radioButton_2)

        self.verticalLayout.addWidget(self.widget_3)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(100, 50))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.pushButton_3 = QPushButton(self.widget_2)
        self.pushButton_3.setObjectName(u"pushButton_3")

        self.horizontalLayout.addWidget(self.pushButton_3)

        self.verticalLayout.addWidget(self.widget_2)

        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout_2.addWidget(self.widget)

        self.retranslate_ui(Dialog)
        self.buttonBox.accepted.connect(self.draw_pdf_sharex)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.radioButton_1.pressed.connect(self.listView_2.selectAll)
        self.radioButton_2.pressed.connect(self.listView_2.reset)
        self.listView_2.doubleClicked.connect(self.update_by_doubleclick)
        self.listView_1.doubleClicked.connect(self.delete_by_doubleclick)
        self.pushButton_1.clicked.connect(self.update_by_button)
        self.pushButton_2.clicked.connect(self.draw_pdf_sharex)
        self.pushButton_3.clicked.connect(self.draw_pdf_oney)
        self.pushButton_4.clicked.connect(self.delete_by_button)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslate_ui(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "График по времени. "
                                                                   "Выбор параметров для графика", None))
        self.pushButton_1.setText(QCoreApplication.translate("Dialog", "Добавить выбранные параметры", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", "Графики с разными осями Y", None))
        self.pushButton_3.setText(QCoreApplication.translate("Dialog", "График с одной осью Y", None))
        self.pushButton_4.setText(QCoreApplication.translate("dialog", "Очистить выбор", None))
        self.radioButton_1.setText(QCoreApplication.translate("Dialog", "Выбрать все", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", "Снять все", None))
        self.label.setText(QCoreApplication.translate("Dialog", "Выберите параметры (минимум 2) \n"
                                                                "Для графика с разными осями max рекомендуется  10",
                                                      None))

    def update_by_doubleclick(self):
        self.item_list_1.append(self.listView_2.currentIndex().data())
        self.model_1.setStringList(self.item_list_1)

    def delete_by_doubleclick(self):
        self.item_list_1.remove(self.listView_1.currentIndex().data())
        self.model_1.setStringList(self.item_list_1)

    def update_by_button(self):
        items = self.listView_2.selectedIndexes()
        self.item_list_1 = [s.data() for s in items]
        self.model_1.setStringList(self.item_list_1)

    def delete_by_button(self):
        self.item_list_1.clear()
        self.model_1.setStringList(self.item_list_1)

    def draw_pdf_oney(self):
        args = self.item_list_1
        if "Time" in MainCode.data.columns:
            if len(args) == 2:
                graph_title, ok = QInputDialog.getText(QWidget(), "Название", "Название графика(по желанию):")
                if ok:
                    GraphicsMatplotlib.GraphicOneY(args=args, file_name=self.file_name, graph_title=graph_title)
            else:
                self.error = QMessageBox()
                self.error.setWindowTitle("Ошибка!")
                self.error.setText("Выберите данные для графика!")
                self.error.setFocusPolicy(Qt.StrongFocus)
                self.error.show()
        else:
            self.error1 = QMessageBox()
            self.error1.setWindowTitle("Ошибка!")
            self.error1.setWindowIcon(QIcon("error_logo.png"))
            self.error1.setFocusPolicy(Qt.StrongFocus)
            self.error1.setText("В данных нет времени!")
            self.error1.show()

    def draw_pdf_sharex(self):
        args = self.item_list_1
        if "Time" in MainCode.data.columns:
            if len(args) > 1:
                graph_title, ok = QInputDialog.getText(QWidget(), "Название", "Название графика(по желанию):")
                if ok:
                    GraphicsMatplotlib.GraphicShareX(args=args, file_name=self.file_name, graph_title=graph_title)
            else:
                self.error = QMessageBox()
                self.error.setWindowTitle("Ошибка!")
                self.error.setWindowIcon(QIcon("error_logo.png"))
                self.error.setFocusPolicy(Qt.StrongFocus)
                self.error.setText("Выберите данные для графика!")
                self.error.show()
        else:
            self.error1 = QMessageBox()
            self.error1.setWindowTitle("Ошибка!")
            self.error1.setWindowIcon(QIcon("error_logo.png"))
            self.error1.setFocusPolicy(Qt.StrongFocus)
            self.error1.setText("В данных нет времени!")
            self.error1.show()


################################################################################
################################################################################

class GraphicByParameterUiDialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName("Dialog")
        dialog.resize(600, 400)
        dialog.setWindowIcon(QIcon("graphic_param_logo.png"))
        self.item_list = [i for i in MainCode.data.columns[:-1:]]
        self.file_name = MainCode.file_name_g
        self.verticalLayout = QVBoxLayout(dialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_1 = QLabel(dialog)
        self.label_1.setObjectName("label_1")

        self.verticalLayout.addWidget(self.label_1)

        self.widget = QWidget(dialog)
        self.widget.setObjectName("widget")
        self.horizontalLayout = QHBoxLayout(self.widget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName("label")
        self.label_2.setSizeIncrement(QSize(10, 10))

        self.horizontalLayout.addWidget(self.label_2)

        self.listView_1 = QListView(self.widget)
        self.listView_1.setObjectName("listView")
        self.model_1 = QStringListModel(self.widget)
        self.model_1.setStringList(self.item_list)
        self.listView_1.setModel(self.model_1)
        self.listView_1.setEditTriggers(
            QAbstractItemView.AnyKeyPressed | QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)

        self.horizontalLayout.addWidget(self.listView_1)

        self.listView_2 = QListView(self.widget)
        self.listView_2.setObjectName("listView_2")
        self.model_2 = QStringListModel(self.widget)
        self.model_2.setStringList(self.item_list)
        self.listView_2.setModel(self.model_2)
        self.listView_2.setEditTriggers(
            QAbstractItemView.AnyKeyPressed | QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)

        self.horizontalLayout.addWidget(self.listView_2)

        self.label_3 = QLabel(self.widget)
        self.label_3.setObjectName("label_3")

        self.horizontalLayout.addWidget(self.label_3)

        self.verticalLayout.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(self.draw_pdf_by_param)
        self.buttonBox.rejected.connect(dialog.reject)

        QMetaObject.connectSlotsByName(dialog)

    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("Dialog", "График ПП", None))
        self.label_1.setText(QCoreApplication.translate("Dialog", "График параметр по параметру", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "X(параметр)", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "Y(аргумент)", None))

    # retranslateUi

    def draw_pdf_by_param(self):
        x = self.listView_1.currentIndex().data()
        y = self.listView_2.currentIndex().data()

        if x and y:
            graph_title, ok = QInputDialog.getText(QWidget(), "Название", "Название графика(по желанию):")
            args = [x, y]
            if ok:
                GraphicsMatplotlib.GraphicParamByParam(args=args, file_name=self.file_name, graph_title=graph_title)
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!")
            self.error.setWindowIcon(QIcon("error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Не хватает данных!")
            self.error.show()


################################################################################
################################################################################


class LinalgUiDialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 600)
        Dialog.setMinimumSize(QSize(300, 500))
        Dialog.setWindowIcon(QIcon("regression_logo.png"))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.item_list = [i for i in MainCode.data.columns[:-1:]]
        self.label_1 = QLabel(Dialog)
        self.label_1.setObjectName(u"label_1")

        self.verticalLayout.addWidget(self.label_1)

        self.widget_1 = QWidget(Dialog)
        self.widget_1.setObjectName(u"widget_1")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.widget_1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setSizeIncrement(QSize(10, 10))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.widget_1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.verticalLayout.addWidget(self.widget_1)

        self.widget_2 = QWidget(Dialog)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listView_1 = QListView(self.widget_2)
        self.listView_1.setObjectName(u"listView_1")
        self.listView_1.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.model_1 = QStringListModel(self.widget_2)
        self.model_1.setStringList(self.item_list)
        self.listView_1.setModel(self.model_1)
        self.listView_1.setSelectionRectVisible(False)

        self.horizontalLayout.addWidget(self.listView_1)

        self.listView_2 = QListView(self.widget_2)
        self.listView_2.setObjectName(u"listView_2")
        self.listView_2.setModel(self.model_1)

        self.horizontalLayout.addWidget(self.listView_2)

        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(Dialog)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"horizontalLayout_2")

        self.label_5 = QLabel(self.widget_3)
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QLabel(self.widget_3)
        self.verticalLayout_2.addWidget(self.label_6)

        self.line_edit_1 = QLineEdit(self.widget_3)
        self.line_edit_1.insert("0")

        self.line_edit_2 = QLineEdit(self.widget_3)
        self.line_edit_2.insert(f"{len(MainCode.data)}")

        self.verticalLayout_2.addWidget(self.line_edit_1)
        self.label_7 = QLabel(self.widget_3)
        self.verticalLayout_2.addWidget(self.label_7)
        self.verticalLayout_2.addWidget(self.line_edit_2)
        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")

        self.verticalLayout_2.addWidget(self.label_4)

        self.verticalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(Dialog)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(100, 50))
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.listView_3 = QListView(self.widget_4)
        self.listView_3.setObjectName(u"listView_3")
        self.listView_3.setMinimumSize(QSize(0, 30))

        self.verticalLayout_3.addWidget(self.listView_3)

        self.pushButton = QPushButton(self.widget_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 20))

        self.verticalLayout_3.addWidget(self.pushButton)

        self.verticalLayout.addWidget(self.widget_4)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslate_ui(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.pushButton.clicked.connect(self.linalg)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslate_ui(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Регрессия", None))
        self.label_1.setText(QCoreApplication.translate("Dialog", "Линейная регрессия", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "Y|функция|\n  |рассчитанный момент|", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "X|тензо-параметр|\n  |независимая переменная|", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", "Уравнение", None))
        self.label_5.setText(QCoreApplication.translate("Dialogs", "Отрезок для анализа", None))
        self.label_6.setText(QCoreApplication.translate("", "От:", None))
        self.label_7.setText(QCoreApplication.translate("", "До:", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", "Расcчитать", None))

    # retranslateUi

    def linalg(self):
        f_parameter = self.listView_1.currentIndex().data()
        tenzo_parameter = self.listView_2.currentIndex().data()
        t0 = int(self.line_edit_1.text())
        t1 = int(self.line_edit_2.text())
        if tenzo_parameter and f_parameter:
            ok, ans = Methods.linear_regression(tenzo_parameter=tenzo_parameter, f_parameter=f_parameter, t0=t0, t1=t1)
            if ok:
                k, c = ans
                self.item_list_3 = [f"{f_parameter} = {round(k, 5)} * {tenzo_parameter} + {round(c, 5)}"]
                self.model_3 = QStringListModel(self.widget_4)
                self.model_3.setStringList(self.item_list_3)
                self.listView_3.setModel(self.model_3)
            else:
                self.error1 = QMessageBox()
                self.error1.setWindowTitle("Ошибка!                             ")
                self.error1.setWindowIcon(QIcon("error_logo.png"))
                self.error1.setFocusPolicy(Qt.StrongFocus)
                self.error1.setText("Что-то не получилось! Проверьте данные!")
                self.error1.show()
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!                                  ")
            self.error.setWindowIcon(QIcon("error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Выберите данные!")
            self.error.show()


################################################################################
################################################################################

class MultiLinalgUiDialog(object):
    def setup_ui(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"Dialog")
        Dialog.resize(500, 700)
        Dialog.setMinimumSize(QSize(400, 500))
        Dialog.setWindowIcon(QIcon("regression_logo.png"))
        self.verticalLayout = QVBoxLayout(Dialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.item_list = [i for i in MainCode.data.columns[:-1:]]
        self.label_1 = QLabel(Dialog)
        self.label_1.setObjectName(u"label_1")

        self.verticalLayout.addWidget(self.label_1)

        self.widget_1 = QWidget(Dialog)
        self.widget_1.setObjectName(u"widget_1")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_1)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.label_2 = QLabel(self.widget_1)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setSizeIncrement(QSize(10, 10))

        self.horizontalLayout_3.addWidget(self.label_2)

        self.label_3 = QLabel(self.widget_1)
        self.label_3.setObjectName(u"label_3")

        self.horizontalLayout_3.addWidget(self.label_3)

        self.verticalLayout.addWidget(self.widget_1)

        self.widget_2 = QWidget(Dialog)
        self.widget_2.setObjectName(u"widget_2")
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.listView_1 = QListView(self.widget_2)
        self.listView_1.setObjectName(u"listView_1")
        self.listView_1.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.model_1 = QStringListModel(self.widget_2)
        self.model_1.setStringList(self.item_list)
        self.listView_1.setModel(self.model_1)
        self.listView_1.setMinimumSize(200, 250)
        self.listView_1.setSelectionRectVisible(False)

        self.horizontalLayout.addWidget(self.listView_1)

        self.listView_2 = QListView(self.widget_2)
        self.listView_2.setObjectName(u"listView_2")
        self.listView_2.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.listView_2.setSelectionMode(QAbstractItemView.MultiSelection)
        self.listView_2.setMinimumSize(200, 250)
        self.listView_2.setModel(self.model_1)

        self.horizontalLayout.addWidget(self.listView_2)

        self.verticalLayout.addWidget(self.widget_2)

        self.widget_3 = QWidget(Dialog)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label_4 = QLabel(self.widget_3)
        self.label_4.setObjectName(u"label_4")

        self.label_5 = QLabel(self.widget_3)
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QLabel(self.widget_3)
        self.verticalLayout_2.addWidget(self.label_6)

        self.line_edit_1 = QLineEdit(self.widget_3)
        self.line_edit_1.insert("0")

        self.line_edit_2 = QLineEdit(self.widget_3)
        self.line_edit_2.insert(f"{len(MainCode.data)}")

        self.verticalLayout_2.addWidget(self.line_edit_1)
        self.label_7 = QLabel(self.widget_3)
        self.verticalLayout_2.addWidget(self.label_7)
        self.verticalLayout_2.addWidget(self.line_edit_2)

        self.verticalLayout_2.addWidget(self.label_4)


        self.verticalLayout.addWidget(self.widget_3)

        self.widget_4 = QWidget(Dialog)
        self.widget_4.setObjectName(u"widget_4")
        self.widget_4.setMinimumSize(QSize(100, 50))
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.listView_3 = QListView(self.widget_4)
        self.listView_3.setObjectName(u"listView_3")
        self.listView_3.setMinimumSize(QSize(0, 30))

        self.verticalLayout_3.addWidget(self.listView_3)

        self.pushButton = QPushButton(self.widget_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setMinimumSize(QSize(0, 20))

        self.verticalLayout_3.addWidget(self.pushButton)

        self.verticalLayout.addWidget(self.widget_4)

        self.buttonBox = QDialogButtonBox(Dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslate_ui(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.pushButton.clicked.connect(self.multi_reg)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslate_ui(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Регрессия", None))
        self.label_1.setText(QCoreApplication.translate("Dialog", "Множественная регрессия", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "Y|функция|\n  |рассчитанный момент|", None))
        self.label_3.setText(QCoreApplication.translate("Dialog", "X|тензо-параметры|\n  |независимые переменные|", None))
        self.label_4.setText(QCoreApplication.translate("Dialog", "Коэффициенты", None))
        self.label_5.setText(QCoreApplication.translate("", "Отрезок для анализа", None))
        self.label_6.setText(QCoreApplication.translate("", "От:", None))
        self.label_7.setText(QCoreApplication.translate("", "До:", None))
        self.pushButton.setText(QCoreApplication.translate("Dialog", "Расcчитать", None))

    # retranslateUi

    def multi_reg(self):
        f_parameter = self.listView_1.currentIndex().data()
        items = self.listView_2.selectedIndexes()
        t0 = int(self.line_edit_1.text())
        t1 = int(self.line_edit_2.text())
        self.item_list_1 = [s.data() for s in items]
        tenzo_parameters = self.item_list_1
        if len(tenzo_parameters) > 1 and f_parameter:
            ok, multi_reg = Methods.multi_regression(f_parameter=f_parameter, tenzo_parameters=tenzo_parameters,
                                                     t0=t0, t1=t1)
            answer = list()
            if ok:
                answer.append(f"константа = {round(multi_reg.pop(-1), 5)}")
                for i, k in enumerate(multi_reg):
                    answer.append(f"{tenzo_parameters[i]} = {round(k, 5)}")
                self.item_list_3 = answer
                self.model_3 = QStringListModel(self.widget_4)
                self.model_3.setStringList(self.item_list_3)
                self.listView_3.setModel(self.model_3)
            else:
                self.error1 = QMessageBox()
                self.error1.setWindowTitle("Ошибка!")
                self.error1.setWindowIcon(QIcon("error_logo.png"))
                self.error1.setFocusPolicy(Qt.StrongFocus)
                self.error1.setText("Что-то не получилось! Проверьте данные!")
                self.error1.show()
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!")
            self.error.setWindowIcon(QIcon("error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Выберите данные!")
            self.error.show()


################################################################################
################################################################################

class ImportUiDialog(object):
    def setupUi(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(600, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        dialog.setMinimumSize(QSize(600, 500))
        dialog.setMaximumSize(QSize(600, 500))
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_1")
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.frame = QFrame(dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_1 = QGridLayout(self.frame)
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.listView_1 = QListView(self.frame)
        self.listView_1.setObjectName(u"listView_1")
        self.listView_1.setMaximumSize(QSize(16777215, 40))
        self.list1_txt = []
        self.model_1 = QStringListModel(self.frame)
        self.model_1.setStringList(self.list1_txt)
        self.listView_1.setModel(self.model_1)

        self.gridLayout_1.addWidget(self.listView_1, 2, 0, 1, 1)

        self.pushButton_1 = QPushButton(self.frame)
        self.pushButton_1.setObjectName(u"pushButton_1")

        self.gridLayout_1.addWidget(self.pushButton_1, 1, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_4")

        self.gridLayout_1.addWidget(self.pushButton_2, 5, 0, 1, 1)

        self.widget_1 = QWidget(self.frame)
        self.widget_1.setObjectName(u"widget_1")
        self.widget_1.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout_1 = QHBoxLayout(self.widget_1)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_2")
        self.widget_2 = QWidget(self.widget_1)
        self.widget_2.setObjectName(u"widget_8")
        self.verticalLayout_1 = QVBoxLayout(self.widget_2)
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_1.addWidget(self.label_2)

        self.radioButton_1 = QRadioButton(self.widget_2)
        self.radioButton_1.setObjectName(u"radioButton_1")

        self.verticalLayout_1.addWidget(self.radioButton_1)

        self.radioButton_2 = QRadioButton(self.widget_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_1.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.widget_2)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout_1.addWidget(self.radioButton_3)

        self.horizontalLayout_1.addWidget(self.widget_2)

        self.line_1 = QFrame(self.widget_1)
        self.line_1.setObjectName(u"line_3")
        self.line_1.setFrameShape(QFrame.VLine)
        self.line_1.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_1.addWidget(self.line_1)

        self.widget_3 = QWidget(self.widget_1)
        self.widget_3.setObjectName(u"widget_9")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.radioButton_4 = QRadioButton(self.widget_3)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.verticalLayout_2.addWidget(self.radioButton_4)

        self.radioButton_5 = QRadioButton(self.widget_3)
        self.radioButton_5.setObjectName(u"radioButton_21")

        self.verticalLayout_2.addWidget(self.radioButton_5)

        self.radioButton_6 = QRadioButton(self.widget_3)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.verticalLayout_2.addWidget(self.radioButton_6)

        self.horizontalLayout_1.addWidget(self.widget_3)

        self.gridLayout_1.addWidget(self.widget_1, 0, 0, 1, 1)

        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.pushButton_1.clicked.connect(self.chose_file)
        self.pushButton_2.clicked.connect(self.import_iw)

        QMetaObject.connectSlotsByName(dialog)

    # setupUi

    def retranslateUi(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Импорт", None))
        self.pushButton_1.setText(QCoreApplication.translate("dialog", u"Выбрать файл для импорта", None))
        self.pushButton_2.setText(QCoreApplication.translate("dialog", u"Импортировать", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Разделитель", None))
        self.radioButton_1.setText(QCoreApplication.translate("dialog", u"Пробел", None))
        self.radioButton_2.setText(QCoreApplication.translate("dialog", u"Точка с запятой: ';'", None))
        self.radioButton_3.setText(QCoreApplication.translate("dialog", u"Запятая: ','", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Кодировка", None))
        self.radioButton_4.setText(QCoreApplication.translate("dialog", u"UTF-8", None))
        self.radioButton_5.setText(QCoreApplication.translate("dialog", u"CP1250", None))
        self.radioButton_6.setText(QCoreApplication.translate("dialog", u"CP1251", None))

    def chose_file(self):
        file = QFileDialog.getOpenFileName(parent=None, filter="*.csv *.txt")
        self.list1_txt.append(file[0])
        self.model_1.setStringList(self.list1_txt)

    def import_iw(self):
        file = self.listView_1.currentIndex().data()
        if not file:
            importing = False
        elif file:
            full_path = QFileDialog.getSaveFileName(filter="*.grad")
            name = full_path[0].split("/")[-1]
            if self.radioButton_1.isChecked() and self.radioButton_4.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="utf-8", sep=True)
            elif self.radioButton_1.isChecked() and self.radioButton_5.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1250", sep=True)
            elif self.radioButton_1.isChecked() and self.radioButton_6.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1251", sep=True)
            elif self.radioButton_2.isChecked() and self.radioButton_4.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="utf-8", sep=False, delimiter=";")
            elif self.radioButton_2.isChecked() and self.radioButton_5.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1250", sep=False, delimiter=";")
            elif self.radioButton_2.isChecked() and self.radioButton_6.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1251", sep=False, delimiter=";")
            elif self.radioButton_3.isChecked() and self.radioButton_4.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="utf-8", sep=False, delimiter=",")
            elif self.radioButton_3.isChecked() and self.radioButton_5.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1250", sep=False, delimiter=",")
            elif self.radioButton_3.isChecked() and self.radioButton_6.isChecked():
                importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1251", sep=False, delimiter=",")
        if importing:
            self.successful = QMessageBox()
            self.successful.setWindowTitle("Успех!")
            self.successful.setWindowIcon(QIcon("success_logo.png"))
            self.successful.setFocusPolicy(Qt.StrongFocus)
            self.successful.setText("Импорт данных завершен!")
            self.successful.show()
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!")
            self.error.setWindowIcon(QIcon("error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Что-то не получилось. Импорт не произведен!")
            self.error.show()


################################################################################
################################################################################

class UniteDataUiDialog(object):
    def setup_ui(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"dialog")
        dialog.resize(600, 500)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(sizePolicy)
        dialog.setMinimumSize(QSize(600, 500))
        dialog.setMaximumSize(QSize(600, 500))
        self.gridLayout_2 = QGridLayout(dialog)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.gridLayout_2.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.frame = QFrame(dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.gridLayout_1 = QGridLayout(self.frame)
        self.gridLayout_1.setObjectName(u"gridLayout_1")
        self.listView_1 = QListView(self.frame)
        self.listView_1.setObjectName(u"listView_1")

        self.list1_txt = []
        self.model_1 = QStringListModel(self.frame)
        self.model_1.setStringList(self.list1_txt)
        self.listView_1.setModel(self.model_1)
        self.listView_1.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.listView_1.setSelectionMode(QAbstractItemView.MultiSelection)

        self.gridLayout_1.addWidget(self.listView_1, 2, 0, 1, 1)

        self.pushButton_1 = QPushButton(self.frame)
        self.pushButton_1.setObjectName(u"pushButton_1")

        self.gridLayout_1.addWidget(self.pushButton_1, 1, 0, 1, 1)

        self.pushButton_2 = QPushButton(self.frame)
        self.pushButton_2.setObjectName(u"pushButton_4")

        self.gridLayout_1.addWidget(self.pushButton_2, 5, 0, 1, 1)

        self.widget_1 = QWidget(self.frame)
        self.widget_1.setObjectName(u"widget_1")
        self.widget_1.setMaximumSize(QSize(16777215, 120))
        self.horizontalLayout_1 = QHBoxLayout(self.widget_1)
        self.horizontalLayout_1.setObjectName(u"horizontalLayout_2")
        self.widget_2 = QWidget(self.widget_1)
        self.widget_2.setObjectName(u"widget_8")
        self.verticalLayout_1 = QVBoxLayout(self.widget_2)
        self.verticalLayout_1.setObjectName(u"verticalLayout_1")
        self.label_2 = QLabel(self.widget_2)
        self.label_2.setObjectName(u"label_2")

        self.verticalLayout_1.addWidget(self.label_2)

        self.radioButton_1 = QRadioButton(self.widget_2)
        self.radioButton_1.setObjectName(u"radioButton_1")

        self.verticalLayout_1.addWidget(self.radioButton_1)

        self.radioButton_2 = QRadioButton(self.widget_2)
        self.radioButton_2.setObjectName(u"radioButton_2")

        self.verticalLayout_1.addWidget(self.radioButton_2)

        self.radioButton_3 = QRadioButton(self.widget_2)
        self.radioButton_3.setObjectName(u"radioButton_3")

        self.verticalLayout_1.addWidget(self.radioButton_3)

        self.horizontalLayout_1.addWidget(self.widget_2)

        self.line_1 = QFrame(self.widget_1)
        self.line_1.setObjectName(u"line_3")
        self.line_1.setFrameShape(QFrame.VLine)
        self.line_1.setFrameShadow(QFrame.Sunken)

        self.horizontalLayout_1.addWidget(self.line_1)

        self.widget_3 = QWidget(self.widget_1)
        self.widget_3.setObjectName(u"widget_3")
        self.verticalLayout_2 = QVBoxLayout(self.widget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_3 = QLabel(self.widget_3)
        self.label_3.setObjectName(u"label_3")

        self.verticalLayout_2.addWidget(self.label_3)

        self.radioButton_4 = QRadioButton(self.widget_3)
        self.radioButton_4.setObjectName(u"radioButton_4")

        self.verticalLayout_2.addWidget(self.radioButton_4)

        self.radioButton_5 = QRadioButton(self.widget_3)
        self.radioButton_5.setObjectName(u"radioButton_21")

        self.verticalLayout_2.addWidget(self.radioButton_5)

        self.radioButton_6 = QRadioButton(self.widget_3)
        self.radioButton_6.setObjectName(u"radioButton_6")

        self.verticalLayout_2.addWidget(self.radioButton_6)

        self.horizontalLayout_1.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_1)
        self.widget_4.setObjectName("widget_4")
        self.verticalLayout_3 = QVBoxLayout(self.widget_4)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_4 = QLabel(self.widget_4)
        self.label_4.setObjectName("label_4")

        self.verticalLayout_3.addWidget(self.label_4)

        self.radioButton_7 = QRadioButton(self.widget_4)
        self.radioButton_7.setObjectName("radioButton_7")
        self.verticalLayout_3.addWidget(self.radioButton_7)

        self.radioButton_8 = QRadioButton(self.widget_4)
        self.radioButton_8.setObjectName("radioButton_8")
        self.verticalLayout_3.addWidget(self.radioButton_8)

        self.radioButton_9 = QRadioButton(self.widget_4)
        self.radioButton_9.setObjectName("radioButton_9")
        self.verticalLayout_3.addWidget(self.radioButton_9)

        self.horizontalLayout_1.addWidget(self.widget_4)

        self.gridLayout_1.addWidget(self.widget_1, 0, 0, 1, 1)

        self.gridLayout_2.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslate_ui(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.pushButton_1.clicked.connect(self.choose_file)
        self.pushButton_2.clicked.connect(self.unite_data_iw)

        QMetaObject.connectSlotsByName(dialog)

    # setupUi

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", u"Склеивание", None))
        self.pushButton_1.setText(QCoreApplication.translate("dialog", u"Выбрать файлы для склейки", None))
        self.pushButton_2.setText(QCoreApplication.translate("dialog", u"Собрать воедино", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Разделитель", None))
        self.radioButton_1.setText(QCoreApplication.translate("dialog", u"Пробел", None))
        self.radioButton_2.setText(QCoreApplication.translate("dialog", u"Точка с запятой: ';'", None))
        self.radioButton_3.setText(QCoreApplication.translate("dialog", u"Запятая: ','", None))
        self.label_3.setText(QCoreApplication.translate("dialog", u"Кодировка", None))
        self.radioButton_4.setText(QCoreApplication.translate("dialog", u"UTF-8", None))
        self.radioButton_5.setText(QCoreApplication.translate("dialog", u"CP1250", None))
        self.radioButton_6.setText(QCoreApplication.translate("dialog", u"CP1251", None))
        self.label_4.setText(QCoreApplication.translate("dialog", "Как склеиваем?"))
        self.radioButton_7.setText(QCoreApplication.translate("dialog", u"Последовательно", None))
        self.radioButton_8.setText(QCoreApplication.translate("dialog", u"Параллельно (max = 2 файла)", None))
        self.radioButton_9.setText(QCoreApplication.translate("dialog", "Одиночные", None))

    def choose_file(self):
        files = QFileDialog.getOpenFileNames(filter="*.txt \n *.csv \n *.grad\n *AllFiles()")
        if self.listView_1:
            self.list1_txt.clear()
            self.list1_txt.extend(files[0])
            self.model_1.setStringList(self.list1_txt)
        else:
            self.list1_txt.extend(files[0])
            self.model_1.setStringList(self.list1_txt)

    def unite_data_iw(self):
        items = self.listView_1.selectedIndexes()
        files = [s.data() for s in items]
        if not files:
            uniting = False
        else:
            path, ok = QFileDialog.getSaveFileName(filter="*.txt\n*.csv\n*.grad")
            how = "Параллельно"
            uniting = False
            if ok:
                name = path.split("/")[-1]
                if self.radioButton_7.isChecked():
                    how = "Последовательно"
                elif self.radioButton_8.isChecked():
                    how = "Параллельно"
                elif self.radioButton_9.isChecked():
                    how = "Одиночные"
                    uniting = Files.concat_txt_data(files, ex_file_name=name, how=how)
                if self.radioButton_1.isChecked() and self.radioButton_4.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="utf-8", sep=True, how=how)
                elif self.radioButton_1.isChecked() and self.radioButton_5.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="cp1250", sep=True, how=how)
                elif self.radioButton_1.isChecked() and self.radioButton_6.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="cp1251", sep=True, how=how)
                elif self.radioButton_2.isChecked() and self.radioButton_4.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="utf-8",
                                                    sep=False, delimiter=";", how=how)
                elif self.radioButton_2.isChecked() and self.radioButton_5.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="cp1250",
                                                    sep=False, delimiter=";", how=how)
                elif self.radioButton_2.isChecked() and self.radioButton_6.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="cp1251",
                                                    sep=False, delimiter=";", how=how)
                elif self.radioButton_3.isChecked() and self.radioButton_4.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="utf-8",
                                                    sep=False, delimiter=",", how=how)
                elif self.radioButton_3.isChecked() and self.radioButton_5.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="cp1250",
                                                    sep=False, delimiter=",", how=how)
                elif self.radioButton_3.isChecked() and self.radioButton_6.isChecked():
                    uniting = Files.concat_txt_data(files, ex_file_name=name, coding="cp1251",
                                                    sep=False, delimiter=",", how=how)
        if uniting:
            self.successful = QMessageBox()
            self.successful.setWindowTitle("Успех!")
            self.successful.setWindowIcon(QIcon("success_logo.png"))
            self.successful.setFocusPolicy(Qt.StrongFocus)
            self.successful.setText("Склеивание данных завершено!")
            self.successful.show()
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!")
            self.error.setWindowIcon(QIcon("error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Что-то не получилось. Склеивание не произведено!")
            self.error.show()

################################################################################
################################################################################


class ShiftParameters(object):
    def setup_ui(self, dialog):
        if not dialog.objectName():
            dialog.setObjectName(u"Dialog")
        dialog.resize(440, 500)
        dialog.setMinimumSize(QSize(300, 500))
        dialog.setFocusPolicy(Qt.StrongFocus)
        self.vertical_layout = QVBoxLayout(dialog)
        self.vertical_layout.setObjectName(u"verticalLayout")
        self.frame = QFrame(dialog)
        self.frame.setObjectName(u"frame")
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_2 = QVBoxLayout(self.frame)
        self.vertical_layout_2.setObjectName(u"verticalLayout_2")
        self.label_2 = QLabel(self.frame)
        self.label_2.setObjectName(u"label_2")

        self.vertical_layout_2.addWidget(self.label_2)

        self.list_view = QListView(self.frame)
        self.list_view.setObjectName(u"listView")
        self.list_view.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_text = MainCode.data.columns[:-1:]
        self.model = QStringListModel(self.frame)
        self.model.setStringList(self.list_text)
        self.list_view.setModel(self.model)

        self.vertical_layout_2.addWidget(self.list_view)

        self.horizontal_spacer = QSpacerItem(399, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.vertical_layout_2.addItem(self.horizontal_spacer)

        self.label_3 = QLabel(self.frame)
        self.vertical_layout_2.addWidget(self.label_3)

        self.label = QLabel(self.frame)
        self.label.setObjectName(u"label")

        self.vertical_layout_2.addWidget(self.label)

        self.spin_box = QSpinBox(self.frame)
        self.spin_box.setObjectName(u"spinBox")

        self.vertical_layout_2.addWidget(self.spin_box)

        self.push_button = QPushButton(self.frame)
        self.push_button.setObjectName(u"pushButton")

        self.vertical_layout_2.addWidget(self.push_button)

        self.vertical_layout.addWidget(self.frame)

        self.button_box = QDialogButtonBox(dialog)
        self.button_box.setObjectName(u"buttonBox")
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout.addWidget(self.button_box)

        self.retranslate_ui(dialog)
        self.button_box.accepted.connect(dialog.accept)
        self.button_box.rejected.connect(dialog.reject)
        self.push_button.clicked.connect(self.shift_params)

        QMetaObject.connectSlotsByName(dialog)
        # setupUi

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"Сдвиг параметров", None))
        self.label_2.setText(QCoreApplication.translate("Dialog", "Выберите параметры для сдвига:", None))
        self.label_3.setText(QCoreApplication.translate("Dialog",
                                                        u"Выбранные параметры будут сдвинуты назад относительно\n"
                                                        u"остальных параметров на выбранное ниже количество точек.\n"
                                                        u"После сдвига обязательно откройте формулы и нажмите 'ok'.",
                                                        None))
        self.label.setText(QCoreApplication.translate("Dialog", u"Количество точек для сдвига", None))
        self.push_button.setText(QCoreApplication.translate("Dialog", u"Сдвинуть", None))

    # retranslateUi

    def shift_params(self):
        items = self.list_view.selectedIndexes()
        if items:
            parameters_names = [i.data() for i in items]
            dots = self.spin_box.value()
            success = Files.shift_analog(parameters_names=parameters_names, dots=dots)
            if success:
                self.success = QMessageBox()
                self.success.setWindowTitle("Успех!")
                self.success.setWindowIcon(QIcon("success_logo.png"))
                self.success.setFocusPolicy(Qt.StrongFocus)
                self.success.setText("Сдвиг произведен!")
                self.success.show()
            else:
                self.error1 = QMessageBox()
                self.error1.setWindowTitle("Упс!")
                self.error1.setWindowIcon(QIcon("error_logo.png"))
                self.error1.setFocusPolicy(Qt.StrongFocus)
                self.error1.setText("Что-то не получилось!")
                self.error1.show()

        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!")
            self.error.setWindowIcon(QIcon("error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Выберите данные")
            self.error.show()


################################################################################
################################################################################


class ExportUiDialog(object):
    def setup_ui(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName("Dialog")
        Dialog.resize(600, 700)
        self.item_list_1 = [i for i in MainCode.data.columns]
        self.item_list_2 = []
        self.file_name = MainCode.file_name_g
        self.verticalLayout_2 = QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget = QWidget(Dialog)
        self.widget.setObjectName(u"widget")
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.label = QLabel(self.widget)
        self.label.setObjectName(u"label")

        self.verticalLayout.addWidget(self.label)

        self.widget_4 = QWidget(self.widget)
        self.widget_4.setObjectName(u"widget_4")
        self.horizontalLayout_3 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.listView_1 = QListView(self.widget_4)
        self.listView_1.setObjectName(u"listView")
        self.model_1 = QStringListModel(self.widget)
        self.model_1.setStringList(self.item_list_1)
        self.listView_1.setModel(self.model_1)
        self.listView_1.setEditTriggers(
            QAbstractItemView.AnyKeyPressed | QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)
        self.listView_1.setTabKeyNavigation(True)
        self.listView_1.setSelectionMode(QAbstractItemView.MultiSelection)

        self.horizontalLayout_3.addWidget(self.listView_1)

        self.listView_2 = QListView(self.widget_4)
        self.listView_2.setObjectName(u"listView_2")
        self.model_2 = QStringListModel(self.widget)
        self.model_2.setStringList(self.item_list_2)
        self.listView_2.setModel(self.model_2)


        self.horizontalLayout_3.addWidget(self.listView_2)

        self.verticalLayout.addWidget(self.widget_4)

        self.pushButton_1 = QPushButton(self.widget)
        self.pushButton_1.setObjectName(u"pushButton")

        self.verticalLayout.addWidget(self.pushButton_1)

        self.pushButton_3 = QPushButton(self.widget)
        self.pushButton_3.setObjectName("pushButton_4")
        self.verticalLayout.addWidget(self.pushButton_3)

        self.widget_3 = QWidget(self.widget)
        self.widget_3.setObjectName(u"widget_3")
        self.widget_3.setMinimumSize(QSize(150, 150))
        self.horizontalLayout_2 = QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")

        self.label1 = QLabel(self.widget_3)
        self.label1.setText("Укажите диапазон данных для экспорта\nВ точках(не в секундах)\nОт:")
        self.label1.setGeometry(QRect(1, 10, 250, 40))
        self.line1 = QLineEdit(self.widget_3)
        self.line1.insert("0")
        self.line1.setGeometry(QRect(1, 50, 100, 20))

        self.label2 = QLabel(self.widget_3)
        self.label2.setText("До:")
        self.label2.setGeometry(QRect(1, 70, 100, 20))
        self.line2 = QLineEdit(self.widget_3)
        self.line2.insert(f"{len(MainCode.data)}")
        self.line2.setGeometry(QRect(1, 90, 100, 20))

        self.label3 = QLabel(self.widget_3)
        self.label3.setText("Выбор данных для экспорта")
        self.label3.setGeometry(QRect(300, 10, 150, 20))
        self.radioButton_1 = QRadioButton(self.widget_3)
        self.radioButton_1.setObjectName(u"radioButton")
        self.radioButton_1.setGeometry(QRect(300, 30, 150, 20))


        self.radioButton_2 = QRadioButton(self.widget_3)
        self.radioButton_2.setObjectName(u"radioButton_2")
        self.radioButton_2.setGeometry(QRect(300, 50, 150, 20))



        self.verticalLayout.addWidget(self.widget_3)

        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.widget_2.setMinimumSize(QSize(100, 50))
        self.horizontalLayout = QHBoxLayout(self.widget_2)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.pushButton_2 = QPushButton(self.widget_2)
        self.pushButton_2.setObjectName(u"pushButton_2")

        self.horizontalLayout.addWidget(self.pushButton_2)

        self.verticalLayout.addWidget(self.widget_2)

        self.buttonBox = QDialogButtonBox(self.widget)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)

        self.verticalLayout_2.addWidget(self.widget)

        self.retranslate_ui(Dialog)
        self.buttonBox.rejected.connect(Dialog.reject)
        self.radioButton_1.pressed.connect(self.listView_1.selectAll)
        self.radioButton_2.pressed.connect(self.listView_1.reset)
        self.listView_1.doubleClicked.connect(self.update_by_doubleclick)
        self.listView_2.doubleClicked.connect(self.delete_by_doubleclick)
        self.pushButton_1.clicked.connect(self.update_by_button)
        self.pushButton_3.clicked.connect(self.delete_by_button)
        self.pushButton_2.clicked.connect(self.export)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslate_ui(self, Dialog):
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", "Экспорт", None))
        self.pushButton_1.setText(QCoreApplication.translate("Dialog", "Добавить выбранные параметры", None))
        self.pushButton_2.setText(QCoreApplication.translate("Dialog", "Экспортировать", None))
        self.pushButton_3.setText(QCoreApplication.translate("dialog", "Очистить выбор", None))
        self.radioButton_1.setText(QCoreApplication.translate("Dialog", "Выбрать все", None))
        self.radioButton_2.setText(QCoreApplication.translate("Dialog", "Снять все", None))
        self.label.setText(QCoreApplication.translate("Dialog", "Выберите параметры для экспорта", None))

    def update_by_doubleclick(self):
        self.item_list_2.append(self.listView_1.currentIndex().data())
        self.model_2.setStringList(self.item_list_2)

    def delete_by_doubleclick(self):
        self.item_list_2.remove(self.listView_2.currentIndex().data())
        self.model_2.setStringList(self.item_list_2)

    def update_by_button(self):
        items = self.listView_1.selectedIndexes()
        self.item_list_2 = [s.data() for s in items]
        self.model_2.setStringList(self.item_list_2)

    def delete_by_button(self):
        self.item_list_2.clear()
        self.model_2.setStringList(self.item_list_2)

    def export(self):
        file_name, ok = QFileDialog.getSaveFileName(filter="*.grad\n*.csv\n*.txt")
        t0 = int(self.line1.text())
        t1 = int(self.line2.text())
        done = False
        if ok and self.item_list_2:
            done = Files.export(parameters_names=self.item_list_2, file_name=file_name, t0=t0, t1=t1)
        if done:
            self.success = QMessageBox()
            self.success.setWindowTitle("Отчёт                                               ")
            self.success.setText("Успех! Экспорт данных произведен!")
            self.success.setWindowIcon(QIcon("success_logo.png"))
            self.success.show()
        elif not done:
            self.error = QMessageBox()
            self.error.setWindowTitle("Отчёт                                                 ")
            self.error.setText("Упс! Что-то не получилось")
            self.error.setWindowIcon(QIcon("error_logo.png"))
            self.error.show()

################################################################################
################################################################################


# class SettingsManager:
#     def __init__(self, filename):
#         self.m_settings = QSettings(filename, QSettings.IniFormat)
#
#     @property
#     def settings(self):
#         return self.m_settings
#
#     def read(self, widget):
#         self.settings.beginGroup(widget.objectName())
#         if isinstance(widget, QAbstractItemView):
#             selection_mode = self.settings.value(
#                 "selectionMode", type=QAbstractItemView.SelectionMode
#             )
#             widget.setSelectionMode(selection_mode)
#
#         if isinstance(widget, QTableWidget):
#             rowCount = self.settings.value("rowCount", type=int)
#             columnCount = self.settings.value("columnCount", type=int)
#             widget.setRowCount(rowCount)
#             widget.setColumnCount(columnCount)
#             items = self.settings.value("items")
#             if items is None:
#                 self.read_defaults(widget)
#             else:
#                 stream = QDataStream(items, QIODevice.ReadOnly)
#                 while not stream.atEnd():
#                     it = QTableWidgetItem()
#                     i = stream.readInt()
#                     j = stream.readInt()
#                     stream >> it
#                     widget.setItem(i, j, it)
#                 selecteditems = self.settings.value("selecteditems")
#                 stream = QDataStream(
#                     selecteditems, QIODevice.ReadOnly
#                 )
#                 while not stream.atEnd():
#                     i = stream.readInt()
#                     j = stream.readInt()
#                     it = widget.item(i, j)
#                     if it is not None:
#                         it.setSelected(True)
#         self.settings.endGroup()
#
#     def write(self, widget):
#         self.settings.beginGroup(widget.objectName())
#         if isinstance(widget, QAbstractItemView):
#             self.settings.setValue("selectionMode", widget.selectionMode())
#
#         if isinstance(widget, QTableWidget):
#             self.settings.setValue("rowCount", widget.rowCount())
#             self.settings.setValue("columnCount", widget.columnCount())
#             items = QByteArray()
#             stream = QDataStream(items, QIODevice.WriteOnly)
#             for i in range(widget.rowCount()):
#                 for j in range(widget.columnCount()):
#                     it = widget.item(i, j)
#                     if it is not None:
#                         stream.writeInt(i)
#                         stream.writeInt(j)
#                         stream << it
#             self.settings.setValue("items", items)
#             selecteditems = QByteArray()
#             stream = QDataStream(
#                 selecteditems, QIODevice.WriteOnly
#             )
#             for it in widget.selectedItems():
#                 # print(it.row(), it.column())
#                 stream.writeInt(it.row())
#                 stream.writeInt(it.column())
#             self.settings.setValue("selecteditems", selecteditems)
#         self.settings.endGroup()
#
#     def release(self):
#         self.m_settings.sync()
#
#     def read_defaults(self, widget):
#         if widget.objectName() == "tableWidget":
#             widget.setSelectionMode(QAbstractItemView.MultiSelection)
#             widget.setRowCount(1)
#             widget.setColumnCount(5)
#             for i in range(widget.rowCount()):
#                 for j in range(widget.columnCount()):
#                     it = QTableWidgetItem("{}-{}".format(i, j))
#                     widget.setItem(i, j, it)
#
#
# @contextlib.contextmanager
# def settingsContext(filename):
#     manager = SettingsManager(filename)
#     try:
#         yield manager
#     finally:
#         manager.release()
#
#
# class Widget(QMainWindow, ParameterUiDialog):  # (QtWidgets.QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#
#         self.setupUi(self)
#         # self.pushButton.clicked.connect(self.set_row_count)
#         # self.pushButton_2.clicked.connect(self.set_row_count2)
#
#         # lay = QGridLayout(self.centralwidget)
#         # lay.addWidget(self.tableWidget, 0, 0, 1, 2)
#         # lay.addWidget(self.pushButton, 1, 0)
#         # lay.addWidget(self.pushButton_2, 1, 1)
#
#         self.read_settings()
#
#     #
#     #     @QtCore.pyqtSlot()
#     #     def set_row_count(self):
#     # #        self.rows += 1
#     # #        self.tableWidget.setRowCount(self.rows)
#     #         rowPosition = self.tableWidget.rowCount()
#     #         self.tableWidget.insertRow(rowPosition)
#     #
#     #     @QtCore.pyqtSlot()
#     #     def set_row_count2(self):
#     # #        self.rows -= 1
#     # #        self.tableWidget.setRowCount(self.rows)
#     #         if self.tableWidget.rowCount() > 0:
#     #             self.tableWidget.removeRow(self.tableWidget.rowCount()-1)
#
#     def closeEvent(self, event):
#         self.write_settings()
#         super().closeEvent(event)
#
#     def read_settings(self):
#         with settingsContext("data_T_W.ini") as m:
#             for children in self.findChildren(QWidget):
#                 if children.objectName():
#                     m.read(children)
#
#     def write_settings(self):
#         with settingsContext("data_T_W.ini") as m:
#             for children in self.findChildren(QWidget):
#                 if children.objectName():
#                     m.write(children)
#
#
# if __name__ == "__main__":
#     import sys
#
#     app = QApplication(sys.argv)
#     w = Widget()
#     w.resize(540, 380)
#     w.show()
#     sys.exit(app.exec_())
