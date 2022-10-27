from PyQt5.QtCore import QSize, QMetaObject, QCoreApplication, QStringListModel, Qt, QAbstractTableModel, QRect
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QAbstractItemView, QDialogButtonBox, QVBoxLayout, \
    QWidget, QListView, QHBoxLayout, QPushButton, QRadioButton, QLabel, QInputDialog, \
    QApplication, QGridLayout, QSizePolicy, QFrame, QFileDialog, QMessageBox, QSpacerItem, QSpinBox, QDialog, \
    QPlainTextEdit, QTableView, QCheckBox, QLineEdit, QMainWindow
from pandas import DataFrame, Series, Index
import MainCode
from MainCode import Files, Methods, Parameters
import GraphicsMatplotlib


class TableModel(QAbstractTableModel):
    def __init__(self, data):
        super(TableModel, self).__init__()
        self._data = data

    def data(self, index, role):
        if role == Qt.DisplayRole or role == Qt.EditRole:
            value = self._data.iloc[index.row(), index.column()]
            return str(value)

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
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


# noinspection PyBroadException
class ParameterUiDialog(QWidget):
    grid_layout: QGridLayout
    frame: QFrame
    vertical_layout: QVBoxLayout
    widget_1: QWidget
    horizontal_layout_1: QHBoxLayout
    label_1: QLabel
    push_button_1: QPushButton
    push_button_2: QPushButton
    push_button_4: QPushButton
    push_button_3: QPushButton
    push_button_5: QPushButton
    widget_2: QWidget
    horizontal_layout_2: QHBoxLayout
    push_button_6: QPushButton
    push_button_7: QPushButton
    push_button_8: QPushButton
    push_button_9: QPushButton
    push_button_10: QPushButton
    table_view: QTableView
    label_err: QLabel
    rows_count: int
    formulas: Series
    rows_names: Index
    data: DataFrame
    model: TableModel
    buttonBox: QDialogButtonBox
    message_1: QMessageBox
    message_2: QMessageBox
    message_3: QMessageBox
    message_4: QMessageBox
    message_5: QMessageBox
    error_1: QMessageBox
    error_2: QMessageBox
    error_3: QMessageBox
    error_4: QMessageBox

    def __init__(self):
        super(ParameterUiDialog, self).__init__()

    def setup_ui(self, dialog):
        dialog.resize(700, 800)
        dialog.setSizeGripEnabled(False)
        dialog.setModal(False)
        dialog.setWindowIcon(QIcon("logos/formulas_logo.png"))
        self.grid_layout = QGridLayout(dialog)
        self.frame = QFrame(dialog)
        self.frame.setMinimumSize(QSize(100, 30))
        self.vertical_layout = QVBoxLayout(self.frame)
        self.widget_1 = QWidget(self.frame)
        self.horizontal_layout_1 = QHBoxLayout(self.widget_1)

        self.label_1 = QLabel(self.frame)
        self.label_1.setText("Будьте бдительны, 'Ctrl Z' здесь не работает!")
        self.vertical_layout.addWidget(self.label_1)
        self.push_button_1 = QPushButton(self.widget_1)

        self.horizontal_layout_1.addWidget(self.push_button_1)

        self.push_button_2 = QPushButton(self.widget_1)

        self.horizontal_layout_1.addWidget(self.push_button_2)

        self.push_button_4 = QPushButton(self.widget_1)

        self.horizontal_layout_1.addWidget(self.push_button_4)

        self.push_button_3 = QPushButton(self.widget_1)

        self.horizontal_layout_1.addWidget(self.push_button_3)

        self.push_button_5 = QPushButton(self.widget_1)

        self.horizontal_layout_1.addWidget(self.push_button_5)

        self.vertical_layout.addWidget(self.widget_1)

        self.widget_2 = QWidget(self.frame)
        self.horizontal_layout_2 = QHBoxLayout(self.widget_2)

        self.push_button_6 = QPushButton(self.widget_2)

        self.horizontal_layout_2.addWidget(self.push_button_6)

        self.push_button_7 = QPushButton(self.widget_2)

        self.horizontal_layout_2.addWidget(self.push_button_7)

        self.push_button_8 = QPushButton(self.widget_2)

        self.horizontal_layout_2.addWidget(self.push_button_8)

        self.push_button_9 = QPushButton(self.widget_2)

        self.horizontal_layout_2.addWidget(self.push_button_9)

        self.push_button_10 = QPushButton(self.widget_2)

        self.horizontal_layout_2.addWidget(self.push_button_10)

        self.vertical_layout.addWidget(self.widget_2)

        self.grid_layout.addWidget(self.frame, 1, 0, 1, 1)

        self.table_view = QTableView(dialog)
        self.table_view.setEditTriggers(QAbstractItemView.CurrentChanged | QAbstractItemView.EditKeyPressed)
        self.label_err = QLabel("Нет данных")
        try:
            data_to_show = MainCode.data.columns[:-1]
            self.rows_count = len(data_to_show)
            self.formulas = MainCode.data["__Формулы__"][:self.rows_count]
            self.rows_names = data_to_show
            data_b = {"Параметры": self.rows_names, "Формула": self.formulas}
            self.data = DataFrame(data_b)
            self.model = TableModel(self.data)
            self.table_view.setModel(self.model)
        except Exception:
            self.vertical_layout.addWidget(self.label_err)

        self.grid_layout.addWidget(self.table_view, 4, 0, 1, 1)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.grid_layout.addWidget(self.buttonBox, 5, 0, 1, 1)

        self.retranslate_ui(dialog)

        self.table_view.setAlternatingRowColors(True)
        self.table_view.horizontalHeader().setStretchLastSection(True)

        self.buttonBox.accepted.connect(self.accepted_event)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.push_button_1.clicked.connect(self.add_parameter_pd)
        self.push_button_2.clicked.connect(self.delete_parameter_pd)
        self.push_button_3.clicked.connect(self.add_formula_pd)
        self.push_button_4.clicked.connect(self.rename_parameter_pd)
        self.push_button_5.clicked.connect(self.copy_parameters_pd)
        self.push_button_6.clicked.connect(self.add_zero_parameters_pd)
        self.push_button_7.clicked.connect(self.add_h_parameters_pd)
        self.push_button_8.clicked.connect(self.key_c_pressed)
        self.table_view.doubleClicked.connect(self.db_edit)
        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "Формулы", None))
        dialog.setWhatsThis(
            QCoreApplication.translate(
                "", "Добавление формулы к какому либо параметру, меняет значения этого параметра. Поэтому не "
                    "рекомендуется добавлять формулы к физическим (записи с накопителей и тд) параметрам. "
                    "Лучше создавать свои параметры и работать уже с ними, а на физические параметры только ссылаться. "
                    "Например, можно создать копию. Или в формуле созданного параметра указать другой параметр."))
        self.push_button_1.setText(QCoreApplication.translate("dialog", "Добавить параметр", None))
        self.push_button_1.setShortcut(QCoreApplication.translate("dialog", "insert"))
        self.push_button_2.setText(QCoreApplication.translate("dialog", "Удалить параметр", None))
        self.push_button_2.setShortcut(QCoreApplication.translate("dialog", "delete"))
        self.push_button_3.setText(QCoreApplication.translate("dialog", "Добавить формулу", None))
        self.push_button_4.setText(QCoreApplication.translate("dialog", "Переименовать", None))
        self.push_button_5.setText(QCoreApplication.translate("dialog", "Создать копию", None))
        self.push_button_6.setText(QCoreApplication.translate("dialog", "Создать копию с _0", None))
        self.push_button_7.setText(QCoreApplication.translate("dialog", "Создать копию с _h", None))
        self.push_button_8.setText(QCoreApplication.translate("dialog", "Копировать в буфер", None))
        self.push_button_8.setShortcut(QCoreApplication.translate("dialog", "Ctrl+C"))
        self.push_button_9.setText(QCoreApplication.translate("dialog", "Заглушка 2", None))
        self.push_button_10.setText(QCoreApplication.translate("dialog", "Заглушка 3", None))

    def update_data(self):
        data_to_show = MainCode.data.columns[:-1]
        self.rows_count = len(data_to_show)
        self.formulas = MainCode.data["__Формулы__"][:self.rows_count]
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
        parameter_name, ok = QInputDialog.getText(
            QWidget(), "Новый параметр",
            "Введите название параметра:                                        ")
        if ok and parameter_name:
            if parameter_name in MainCode.data.columns:
                self.message_1 = QMessageBox()
                self.message_1.setWindowTitle("Новый параметр")
                self.message_1.setFocusPolicy(Qt.StrongFocus)
                self.message_1.setText("Параметр с таким названием уже существует!")
                self.message_1.show()
            elif parameter_name == "Time":
                freq, f = QInputDialog.getInt(QWidget(), "Частота", "Введите частоту: ")
                Parameters.add_parameter(input_name=parameter_name, freq=freq)
            else:
                Parameters.add_parameter(parameter_name)
        elif not ok:
            pass
        else:
            self.message_2 = QMessageBox()
            self.message_2.setWindowTitle("Новый параметр")
            self.message_2.setFocusPolicy(Qt.StrongFocus)
            self.message_2.setText("Введите название параметра!")
            self.message_2.show()
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
                    self.message_3 = QMessageBox()
                    self.message_3.setWindowTitle("Упс! Что-то не так с формулой.")
                    self.message_3.setIcon(QIcon("logos/error_logo.png"))
                    self.message_3.setText("Проверьте формулу и введите её заново!")
                    self.message_3.show()
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
                self.message_4 = QMessageBox()
                self.message_4.setWindowTitle("Новое название")
                self.message_4.setText("Параметр с таким названием уже существует!")
                self.message_4.show()
            else:
                Parameters.rename_parameter(name, new_name)
                self.update_data()
        elif not ok:
            pass
        else:
            self.message_5 = QMessageBox()
            self.message_5.setWindowTitle("Новое название")
            self.message_5.setText("Введите новое название параметра!")
            self.message_5.show()

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
            self.error_1 = QMessageBox()
            self.error_1.setWindowTitle("Ошибка!")
            self.error_1.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_1.setText("Что-то не получилось! Возможно такие параметры уже есть!")
            self.error_1.show()

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
            self.error_2 = QMessageBox()
            self.error_2.setWindowTitle("Ошибка!")
            self.error_2.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_2.setText("Что-то не получилось! Возможно такие параметры уже есть!")
            self.error_2.show()

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
            self.error_3 = QMessageBox()
            self.error_3.setWindowTitle("Ошибка!")
            self.error_3.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_3.setText("Что-то не получилось! Возможно такие параметры уже есть!")
            self.error_3.show()

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
            self.error_4 = QMessageBox()
            self.error_4.setWindowTitle("Ошибки в формулах!                                       ")
            self.error_4.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_4.setText(f"Ошибка в формуле параметра: {err_req}")
            self.error_4.show()


################################################################################


class AddFormulaDialog(object):
    vertical_layout: QVBoxLayout
    frame: QFrame
    horizontal_layout: QHBoxLayout
    text_edit: QPlainTextEdit
    vertical_spacer: QSpacerItem
    list_view: QListView
    list_text: Index
    model: QStringListModel
    buttonBox: QDialogButtonBox
    check_box: QCheckBox

    def __init__(self, parameter_name: str, index: str):
        self.parameter_name = parameter_name
        self.index = index
        self.text = MainCode.data["__Формулы__"][self.index]

    def setup_ui(self, dialog):
        dialog.resize(1100, 400)
        dialog.setMinimumSize(QSize(0, 0))
        dialog.setWindowIcon(QIcon("logos/formulas_logo.png"))
        self.vertical_layout = QVBoxLayout(dialog)
        self.frame = QFrame(dialog)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.horizontal_layout = QHBoxLayout(self.frame)
        self.text_edit = QPlainTextEdit(self.frame)
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
        self.list_view.setMinimumSize(QSize(200, 0))
        self.list_view.setMaximumSize(QSize(200, 16777215))
        self.list_view.setAlternatingRowColors(True)
        self.list_view.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.list_text = MainCode.data.columns[:-1]
        self.model = QStringListModel(self.list_text)
        self.list_view.setModel(self.model)

        self.horizontal_layout.addWidget(self.list_view)

        self.vertical_layout.addWidget(self.frame)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout.addWidget(self.buttonBox)

        self.check_box = QCheckBox(dialog)
        self.check_box.setWhatsThis(
            QCoreApplication.translate
            ("", "Эта кнопка вписывает шаблон. Логическое выражение. Данный параметр равен чему-то в зависимости от "
                 "условия. Например: \n "
                 "data.loc[:, 'L'] = np.where((data['Time'] > 0) & (data['Time'] <= data['t2']), 0.728, data['L']);"
                 "data.loc[:, 'L'] = np.where((data['Time'] > data['t2']) & (data['Time'] <= data['t3']), -0.580, "
                 "data['L']);"
                 " Данное выражение означает, что параметр 'L' равен 0.728, когда параметр 'Time' больше 0 и меньше "
                 "'t2', и равен -0.580, когда параметр 'Time' больше 't2' и меньше 't3'. Чтобы записать вместо 0.728 "
                 "зачение другого параметра, нужно написать data['название параметра']. Чтобы воспользоваться "
                 "математическими функциями, например косинусом, нужно написать np.cos()."))
        self.vertical_layout.addWidget(self.check_box)
        self.check_box.toggled.connect(self.checked)

        self.retranslate_ui(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.list_view.doubleClicked.connect(self.add_param)
        dialog.accepted.connect(self.accept)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog",
                                                         f"Ввод формулы для параметра: {self.parameter_name}",
                                                         None))
        self.check_box.setText(QCoreApplication.translate("dialog", "Логику?", None))

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
        ok = Parameters.add_formula(parameter_name=self.parameter_name, formula=formula)
        return ok


################################################################################
################################################################################


class GraphicByTimeUiDialog(object):
    item_list_1: list
    file_name: str
    vertical_layout_1: QVBoxLayout
    widget_1: QWidget
    vertical_layout_2: QVBoxLayout
    label: QLabel
    widget_2: QWidget
    horizontal_layout_1: QHBoxLayout
    list_view_1: QListView
    item_list_2: list
    model_1: QStringListModel
    list_view_2: QListView
    model_2: QStringListModel
    push_button_1: QPushButton
    push_button_2: QPushButton
    widget_3: QWidget
    horizontal_layout_2: QHBoxLayout
    radio_button_1: QRadioButton
    radio_button_2: QRadioButton
    widget_4: QWidget
    horizontal_layout_3: QHBoxLayout
    push_button_3: QPushButton
    push_button_4: QPushButton
    buttonBox: QDialogButtonBox
    error_1: QMessageBox
    error_2: QMessageBox
    error_3: QMessageBox
    error_4: QMessageBox

    def setup_ui(self, dialog):
        dialog.resize(500, 600)
        dialog.setWindowIcon(QIcon("logos/graphic_sharex_logo.png"))
        self.item_list_1 = [i for i in MainCode.data.columns[:-1]]
        self.file_name = MainCode.file_name_g
        self.vertical_layout_1 = QVBoxLayout(dialog)
        self.widget_1 = QWidget(dialog)
        self.vertical_layout_2 = QVBoxLayout(self.widget_1)
        self.label = QLabel(self.widget_1)

        self.vertical_layout_2.addWidget(self.label)

        self.widget_2 = QWidget(self.widget_1)
        self.horizontal_layout_1 = QHBoxLayout(self.widget_2)
        self.list_view_1 = QListView(self.widget_2)
        self.item_list_2 = []
        self.model_1 = QStringListModel(self.widget_1)
        self.model_1.setStringList(self.item_list_2)
        self.list_view_1.setModel(self.model_1)

        self.horizontal_layout_1.addWidget(self.list_view_1)

        self.list_view_2 = QListView(self.widget_2)
        self.model_2 = QStringListModel(self.widget_1)
        self.model_2.setStringList(self.item_list_1)
        self.list_view_2.setModel(self.model_2)
        self.list_view_2.setEditTriggers(
            QAbstractItemView.AnyKeyPressed | QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)
        self.list_view_2.setTabKeyNavigation(True)
        self.list_view_2.setSelectionMode(QAbstractItemView.MultiSelection)

        self.horizontal_layout_1.addWidget(self.list_view_2)

        self.vertical_layout_2.addWidget(self.widget_2)

        self.push_button_1 = QPushButton(self.widget_1)

        self.vertical_layout_2.addWidget(self.push_button_1)

        self.push_button_2 = QPushButton(self.widget_1)
        self.vertical_layout_2.addWidget(self.push_button_2)

        self.widget_3 = QWidget(self.widget_1)
        self.widget_3.setMinimumSize(QSize(100, 35))
        self.horizontal_layout_2 = QHBoxLayout(self.widget_3)
        self.radio_button_1 = QRadioButton(self.widget_3)

        self.horizontal_layout_2.addWidget(self.radio_button_1)

        self.radio_button_2 = QRadioButton(self.widget_3)

        self.horizontal_layout_2.addWidget(self.radio_button_2)

        self.vertical_layout_2.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_1)
        self.widget_4.setMinimumSize(QSize(100, 50))
        self.horizontal_layout_3 = QHBoxLayout(self.widget_4)
        self.push_button_3 = QPushButton(self.widget_4)

        self.horizontal_layout_3.addWidget(self.push_button_3)

        self.push_button_4 = QPushButton(self.widget_4)

        self.horizontal_layout_3.addWidget(self.push_button_4)

        self.vertical_layout_2.addWidget(self.widget_4)

        self.buttonBox = QDialogButtonBox(self.widget_1)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout_2.addWidget(self.buttonBox)

        self.vertical_layout_1.addWidget(self.widget_1)

        self.retranslate_ui(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.radio_button_1.pressed.connect(self.list_view_2.selectAll)
        self.radio_button_2.pressed.connect(self.list_view_2.reset)
        self.list_view_2.doubleClicked.connect(self.update_by_doubleclick)
        self.list_view_1.doubleClicked.connect(self.delete_by_doubleclick)
        self.push_button_1.clicked.connect(self.update_by_button)
        self.push_button_3.clicked.connect(self.draw_pdf_sharex)
        self.push_button_4.clicked.connect(self.draw_pdf_oney)
        self.push_button_2.clicked.connect(self.delete_by_button)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "График по времени. "
                                                                   "Выбор параметров для графика.", None))
        self.push_button_1.setText(QCoreApplication.translate("dialog", "Добавить выбранные параметры", None))
        self.push_button_3.setText(QCoreApplication.translate("dialog", "Графики с разными осями Y", None))
        self.push_button_4.setText(QCoreApplication.translate("dialog", "График с одной осью Y", None))
        self.push_button_2.setText(QCoreApplication.translate("dialog", "Очистить выбор", None))
        self.radio_button_1.setText(QCoreApplication.translate("dialog", "Выбрать все", None))
        self.radio_button_2.setText(QCoreApplication.translate("dialog", "Снять все", None))
        self.label.setText(QCoreApplication.translate("dialog",
                                                      "Выберите параметры (min 2)\nДля графика с разными осями "
                                                      "max рекомендуется 10", None))

    def update_by_doubleclick(self):
        self.item_list_2.append(self.list_view_2.currentIndex().data())
        self.model_1.setStringList(self.item_list_2)

    def delete_by_doubleclick(self):
        self.item_list_2.remove(self.list_view_1.currentIndex().data())
        self.model_1.setStringList(self.item_list_2)

    def update_by_button(self):
        items = self.list_view_2.selectedIndexes()
        self.item_list_2 = [s.data() for s in items]
        self.model_1.setStringList(self.item_list_2)

    def delete_by_button(self):
        self.item_list_2.clear()
        self.model_1.setStringList(self.item_list_2)

    def draw_pdf_oney(self):
        args = self.item_list_2
        if "Time" in MainCode.data.columns:
            if len(args) == 2:
                graph_title, ok = QInputDialog.getText(QWidget(), "Название", "Название графика (по желанию):")
                if ok:
                    GraphicsMatplotlib.GraphicOneY(args=args, file_name=self.file_name, graph_title=graph_title)
            else:
                self.error_1 = QMessageBox()
                self.error_1.setWindowTitle("Ошибка!                                                              ")
                self.error_1.setText("Выберите данные для графика!\nТолько 2 параметра.")
                self.error_1.setWindowIcon(QIcon("logos/error_logo.png"))
                self.error_1.show()
        else:
            self.error_2 = QMessageBox()
            self.error_2.setWindowTitle("Ошибка!                                                             ")
            self.error_2.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_2.setFocusPolicy(Qt.StrongFocus)
            self.error_2.setText(
                "В данных нет времени!\nЧтобы нарисовать графики добавьте параметр время в данные. Для этого: "
                "'Параметры' -> 'Формулы' -> 'Добавить параметр' -> "
                "назвать параметр 'Time' -> указать частоту регистрации")
            self.error_2.show()

    def draw_pdf_sharex(self):
        args = self.item_list_2
        if "Time" in MainCode.data.columns:
            if len(args) > 1:
                graph_title, ok = QInputDialog.getText(QWidget(), "Название", "Название графика (по желанию):")
                if ok:
                    GraphicsMatplotlib.GraphicShareX(args=args, file_name=self.file_name, graph_title=graph_title)
                else:
                    print("catch")
                    pass
            else:
                self.error_3 = QMessageBox()
                self.error_3.setWindowTitle("Ошибка!                                                              ")
                self.error_3.setWindowIcon(QIcon("logos/error_logo.png"))
                self.error_3.setText("Выберите данные для графика!\nМинимум 2 параметра. "
                                     "Максимум рекомендуется 10 параметров, иначе ни черта не видно.")
                self.error_3.show()
        else:
            self.error_4 = QMessageBox()
            self.error_4.setWindowTitle("Ошибка!                                                                 ")
            self.error_4.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_4.setFocusPolicy(Qt.StrongFocus)
            self.error_4.setText(
                "В данных нет времени!\nЧтобы нарисовать графики добавьте параметр время в данные. Для этого: "
                "'Параметры' -> 'Формулы' -> 'Добавить параметр' -> "
                "назвать параметр 'Time' -> указать частоту регистрации")
            self.error_4.show()


################################################################################
################################################################################


class GraphicByParameterUiDialog(object):
    item_list: list
    file_name: str
    vertical_layout: QVBoxLayout
    label_1: QLabel
    label_2: QLabel
    label_3: QLabel
    widget: QWidget
    horizontal_layout: QHBoxLayout
    list_view_1: QListView
    list_view_2: QListView
    model_1: QStringListModel
    model_2: QStringListModel
    buttonBox: QDialogButtonBox
    error: QMessageBox

    def setup_ui(self, dialog):
        dialog.resize(600, 400)
        dialog.setWindowIcon(QIcon("logos/graphic_param_logo.png"))
        self.item_list = [i for i in MainCode.data.columns[:-1]]
        self.file_name = MainCode.file_name_g
        self.vertical_layout = QVBoxLayout(dialog)
        self.label_1 = QLabel(dialog)

        self.vertical_layout.addWidget(self.label_1)

        self.widget = QWidget(dialog)
        self.horizontal_layout = QHBoxLayout(self.widget)
        self.label_2 = QLabel(self.widget)
        self.label_2.setSizeIncrement(QSize(10, 10))

        self.horizontal_layout.addWidget(self.label_2)

        self.list_view_1 = QListView(self.widget)
        self.model_1 = QStringListModel(self.widget)
        self.model_1.setStringList(self.item_list)
        self.list_view_1.setModel(self.model_1)
        self.list_view_1.setEditTriggers(
            QAbstractItemView.AnyKeyPressed | QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)

        self.horizontal_layout.addWidget(self.list_view_1)

        self.list_view_2 = QListView(self.widget)
        self.model_2 = QStringListModel(self.widget)
        self.model_2.setStringList(self.item_list)
        self.list_view_2.setModel(self.model_2)
        self.list_view_2.setEditTriggers(
            QAbstractItemView.AnyKeyPressed | QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)

        self.horizontal_layout.addWidget(self.list_view_2)

        self.label_3 = QLabel(self.widget)

        self.horizontal_layout.addWidget(self.label_3)

        self.vertical_layout.addWidget(self.widget)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout.addWidget(self.buttonBox)

        self.retranslate_ui(dialog)
        self.buttonBox.accepted.connect(self.draw_pdf_by_param)
        self.buttonBox.rejected.connect(dialog.reject)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "График ПП", None))
        self.label_1.setText(QCoreApplication.translate("dialog", "График параметр по параметру", None))
        self.label_2.setText(QCoreApplication.translate("dialog", "X(параметр)", None))
        self.label_3.setText(QCoreApplication.translate("dialog", "Y(аргумент)", None))

    def draw_pdf_by_param(self):
        x = self.list_view_1.currentIndex().data()
        y = self.list_view_2.currentIndex().data()

        if x and y:
            graph_title, ok = QInputDialog.getText(QWidget(), "Название", "Название графика (по желанию):")
            args = [x, y]
            if ok:
                GraphicsMatplotlib.GraphicParamByParam(args=args, file_name=self.file_name, graph_title=graph_title)
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!")
            self.error.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Не хватает данных!")
            self.error.show()


################################################################################
################################################################################


class LinalgUiDialog(object):
    vertical_layout_1: QVBoxLayout
    vertical_layout_2: QVBoxLayout
    vertical_layout_3: QVBoxLayout
    item_list: list
    label_1: QLabel
    label_2: QLabel
    label_3: QLabel
    label_4: QLabel
    label_5: QLabel
    label_6: QLabel
    label_7: QLabel
    widget_1: QWidget
    widget_2: QWidget
    widget_3: QWidget
    widget_4: QWidget
    horizontal_layout_1: QHBoxLayout
    horizontal_layout_2: QHBoxLayout
    list_view_1: QListView
    list_view_2: QListView
    list_view_3: QListView
    model_1: QStringListModel
    line_edit_1: QLineEdit
    line_edit_2: QLineEdit
    push_button: QPushButton
    buttonBox: QDialogButtonBox
    error_1: QMessageBox
    error_2: QMessageBox

    def setup_ui(self, dialog):
        dialog.resize(500, 700)
        dialog.setMinimumSize(QSize(300, 500))
        dialog.setWindowIcon(QIcon("logos/regression_logo.png"))
        self.vertical_layout_1 = QVBoxLayout(dialog)
        self.item_list = [i for i in MainCode.data.columns[:-1]]
        self.label_1 = QLabel(dialog)

        self.vertical_layout_1.addWidget(self.label_1)

        self.widget_1 = QWidget(dialog)
        self.horizontal_layout_1 = QHBoxLayout(self.widget_1)
        self.label_2 = QLabel(self.widget_1)
        self.label_2.setSizeIncrement(QSize(10, 10))

        self.horizontal_layout_1.addWidget(self.label_2)

        self.label_3 = QLabel(self.widget_1)

        self.horizontal_layout_1.addWidget(self.label_3)

        self.vertical_layout_1.addWidget(self.widget_1)

        self.widget_2 = QWidget(dialog)
        self.horizontal_layout_2 = QHBoxLayout(self.widget_2)
        self.list_view_1 = QListView(self.widget_2)
        self.list_view_1.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.model_1 = QStringListModel(self.widget_2)
        self.model_1.setStringList(self.item_list)
        self.list_view_1.setModel(self.model_1)
        self.list_view_1.setSelectionRectVisible(False)

        self.horizontal_layout_2.addWidget(self.list_view_1)

        self.list_view_2 = QListView(self.widget_2)
        self.list_view_2.setModel(self.model_1)

        self.horizontal_layout_2.addWidget(self.list_view_2)

        self.vertical_layout_1.addWidget(self.widget_2)

        self.widget_3 = QWidget(dialog)
        self.vertical_layout_2 = QVBoxLayout(self.widget_3)

        self.label_4 = QLabel(self.widget_3)
        self.vertical_layout_2.addWidget(self.label_4)
        self.label_5 = QLabel(self.widget_3)
        self.vertical_layout_2.addWidget(self.label_5)

        self.line_edit_1 = QLineEdit(self.widget_3)
        self.line_edit_1.insert("0")

        self.line_edit_2 = QLineEdit(self.widget_3)
        self.line_edit_2.insert(f"{len(MainCode.data)}")

        self.vertical_layout_2.addWidget(self.line_edit_1)
        self.label_6 = QLabel(self.widget_3)
        self.vertical_layout_2.addWidget(self.label_6)
        self.vertical_layout_2.addWidget(self.line_edit_2)
        self.label_7 = QLabel(self.widget_3)

        self.vertical_layout_2.addWidget(self.label_7)

        self.vertical_layout_1.addWidget(self.widget_3)

        self.widget_4 = QWidget(dialog)
        self.widget_4.setMinimumSize(QSize(100, 50))
        self.vertical_layout_3 = QVBoxLayout(self.widget_4)
        self.list_view_3 = QListView(self.widget_4)
        self.list_view_3.setMinimumSize(QSize(0, 30))

        self.vertical_layout_3.addWidget(self.list_view_3)

        self.push_button = QPushButton(self.widget_4)
        self.push_button.setMinimumSize(QSize(0, 20))

        self.vertical_layout_3.addWidget(self.push_button)

        self.vertical_layout_1.addWidget(self.widget_4)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout_1.addWidget(self.buttonBox)

        self.retranslate_ui(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.push_button.clicked.connect(self.linalg)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "Регрессия", None))
        self.label_1.setText(QCoreApplication.translate("dialog", "Линейная регрессия", None))
        self.label_2.setText(QCoreApplication.translate("dialog", "Y|функция|\n  |рассчитанный момент|", None))
        self.label_3.setText(QCoreApplication.translate("dialog",
                                                        "X|независимая переменная|\n  |тензо-параметр|", None))
        self.label_7.setText(QCoreApplication.translate("dialog", "Уравнение", None))
        self.label_4.setText(QCoreApplication.translate("dialog", "Отрезок для анализа", None))
        self.label_5.setText(QCoreApplication.translate("dialog", "От:", None))
        self.label_6.setText(QCoreApplication.translate("dialog", "До:", None))
        self.push_button.setText(QCoreApplication.translate("dialog", "Расcчитать", None))

    def linalg(self):
        f_parameter = self.list_view_1.currentIndex().data()
        tenzo_parameter = self.list_view_2.currentIndex().data()
        t0 = int(self.line_edit_1.text())
        t1 = int(self.line_edit_2.text())
        if tenzo_parameter and f_parameter:
            ok, ans = Methods.linear_regression(tenzo_parameter=tenzo_parameter, f_parameter=f_parameter, t0=t0, t1=t1)
            if ok:
                k, c = ans
                item_list_3 = [f"{f_parameter} = {round(k, 5)} * {tenzo_parameter} + {round(c, 5)}"]
                model_2 = QStringListModel(self.widget_4)
                model_2.setStringList(item_list_3)
                self.list_view_3.setModel(model_2)
            else:
                self.error_1 = QMessageBox()
                self.error_1.setWindowTitle("Ошибка!                             ")
                self.error_1.setWindowIcon(QIcon("logos/error_logo.png"))
                self.error_1.setFocusPolicy(Qt.StrongFocus)
                self.error_1.setText("Что-то не получилось! Проверьте данные!")
                self.error_1.show()
        else:
            self.error_2 = QMessageBox()
            self.error_2.setWindowTitle("Ошибка!                                  ")
            self.error_2.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_2.setFocusPolicy(Qt.StrongFocus)
            self.error_2.setText("Выберите данные!")
            self.error_2.show()


################################################################################
################################################################################

class MultiLinalgUiDialog(object):
    vertical_layout_1: QVBoxLayout
    vertical_layout_2: QVBoxLayout
    vertical_layout_3: QVBoxLayout
    item_list: list
    label_1: QLabel
    label_2: QLabel
    label_3: QLabel
    label_4: QLabel
    label_5: QLabel
    label_6: QLabel
    label_7: QLabel
    widget_1: QWidget
    widget_2: QWidget
    widget_3: QWidget
    widget_4: QWidget
    horizontal_layout_1: QHBoxLayout
    horizontal_layout_2: QHBoxLayout
    list_view_1: QListView
    list_view_2: QListView
    list_view_3: QListView
    model_1: QStringListModel
    line_edit_1: QLineEdit
    line_edit_2: QLineEdit
    push_button: QPushButton
    buttonBox: QDialogButtonBox
    error_1: QMessageBox
    error_2: QMessageBox

    def setup_ui(self, dialog):
        dialog.resize(500, 700)
        dialog.setMinimumSize(QSize(400, 500))
        dialog.setWindowIcon(QIcon("logos/regression_logo.png"))
        self.vertical_layout_1 = QVBoxLayout(dialog)
        self.item_list = [i for i in MainCode.data.columns[:-1]]
        self.label_1 = QLabel(dialog)

        self.vertical_layout_1.addWidget(self.label_1)

        self.widget_1 = QWidget(dialog)
        self.horizontal_layout_1 = QHBoxLayout(self.widget_1)
        self.label_2 = QLabel(self.widget_1)
        self.label_2.setSizeIncrement(QSize(10, 10))

        self.horizontal_layout_1.addWidget(self.label_2)

        self.label_3 = QLabel(self.widget_1)

        self.horizontal_layout_1.addWidget(self.label_3)

        self.vertical_layout_1.addWidget(self.widget_1)

        self.widget_2 = QWidget(dialog)
        self.horizontal_layout_2 = QHBoxLayout(self.widget_2)
        self.list_view_1 = QListView(self.widget_2)
        self.list_view_1.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.model_1 = QStringListModel(self.widget_2)
        self.model_1.setStringList(self.item_list)
        self.list_view_1.setModel(self.model_1)
        self.list_view_1.setMinimumSize(200, 250)
        self.list_view_1.setSelectionRectVisible(False)

        self.horizontal_layout_2.addWidget(self.list_view_1)

        self.list_view_2 = QListView(self.widget_2)
        self.list_view_2.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.list_view_2.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_view_2.setMinimumSize(200, 250)
        self.list_view_2.setModel(self.model_1)

        self.horizontal_layout_2.addWidget(self.list_view_2)

        self.vertical_layout_1.addWidget(self.widget_2)

        self.widget_3 = QWidget(dialog)
        self.vertical_layout_2 = QVBoxLayout(self.widget_3)
        self.label_4 = QLabel(self.widget_3)

        self.label_5 = QLabel(self.widget_3)
        self.vertical_layout_2.addWidget(self.label_5)
        self.label_6 = QLabel(self.widget_3)
        self.vertical_layout_2.addWidget(self.label_6)

        self.line_edit_1 = QLineEdit(self.widget_3)
        self.line_edit_1.insert("0")

        self.line_edit_2 = QLineEdit(self.widget_3)
        self.line_edit_2.insert(f"{len(MainCode.data)}")

        self.vertical_layout_2.addWidget(self.line_edit_1)
        self.label_7 = QLabel(self.widget_3)
        self.vertical_layout_2.addWidget(self.label_7)
        self.vertical_layout_2.addWidget(self.line_edit_2)

        self.vertical_layout_2.addWidget(self.label_4)

        self.vertical_layout_1.addWidget(self.widget_3)

        self.widget_4 = QWidget(dialog)
        self.widget_4.setMinimumSize(QSize(100, 50))
        self.vertical_layout_3 = QVBoxLayout(self.widget_4)
        self.list_view_3 = QListView(self.widget_4)
        self.list_view_3.setMinimumSize(QSize(0, 30))

        self.vertical_layout_3.addWidget(self.list_view_3)

        self.push_button = QPushButton(self.widget_4)
        self.push_button.setMinimumSize(QSize(0, 20))

        self.vertical_layout_3.addWidget(self.push_button)

        self.vertical_layout_1.addWidget(self.widget_4)

        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout_1.addWidget(self.buttonBox)

        self.retranslate_ui(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.push_button.clicked.connect(self.multi_reg)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "Регрессия", None))
        self.label_1.setText(QCoreApplication.translate("dialog", "Множественная регрессия", None))
        self.label_2.setText(QCoreApplication.translate("dialog", "Y|функция|\n  |рассчитанный момент|", None))
        self.label_3.setText(QCoreApplication.translate("dialog",
                                                        "X|независимые переменные|\n  |тензо-параметры|", None))
        self.label_4.setText(QCoreApplication.translate("dialog", "Коэффициенты", None))
        self.label_5.setText(QCoreApplication.translate("dialog", "Отрезок для анализа", None))
        self.label_6.setText(QCoreApplication.translate("dialog", "От:", None))
        self.label_7.setText(QCoreApplication.translate("dialog", "До:", None))
        self.push_button.setText(QCoreApplication.translate("dialog", "Расcчитать", None))

    def multi_reg(self):
        f_parameter = self.list_view_1.currentIndex().data()
        items = self.list_view_2.selectedIndexes()
        t0 = int(self.line_edit_1.text())
        t1 = int(self.line_edit_2.text())
        item_list_1 = [s.data() for s in items]
        tenzo_parameters = item_list_1
        if len(tenzo_parameters) > 1 and f_parameter:
            ok, multi_reg = Methods.multi_regression(f_parameter=f_parameter, tenzo_parameters=tenzo_parameters,
                                                     t0=t0, t1=t1)
            answer = list()
            if ok:
                answer.append(f"константа = {round(multi_reg.pop(-1), 5)}")
                for i, k in enumerate(multi_reg):
                    answer.append(f"{tenzo_parameters[i]} = {round(k, 5)}")
                item_list_3 = answer
                model_2 = QStringListModel(self.widget_4)
                model_2.setStringList(item_list_3)
                self.list_view_3.setModel(model_2)
            else:
                self.error_1 = QMessageBox()
                self.error_1.setWindowTitle("Ошибка!")
                self.error_1.setWindowIcon(QIcon("logos/error_logo.png"))
                self.error_1.setFocusPolicy(Qt.StrongFocus)
                self.error_1.setText("Что-то не получилось! Проверьте данные!")
                self.error_1.show()
        else:
            self.error_2 = QMessageBox()
            self.error_2.setWindowTitle("Ошибка!")
            self.error_2.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_2.setFocusPolicy(Qt.StrongFocus)
            self.error_2.setText("Выберите данные!")
            self.error_2.show()


################################################################################
################################################################################

class ImportUiDialog(object):
    grid_layout_1: QGridLayout
    grid_layout_2: QGridLayout
    buttonBox: QDialogButtonBox
    frame: QFrame
    line: QFrame
    list_view: QListView
    list_txt: list
    model: QStringListModel
    push_button_1: QPushButton
    push_button_2: QPushButton
    widget_1: QWidget
    widget_2: QWidget
    widget_3: QWidget
    horizontal_layout: QHBoxLayout
    vertical_layout_1: QVBoxLayout
    vertical_layout_2: QVBoxLayout
    label_1: QLabel
    label_2: QLabel
    radio_button_1: QRadioButton
    radio_button_2: QRadioButton
    radio_button_3: QRadioButton
    radio_button_4: QRadioButton
    radio_button_5: QRadioButton
    radio_button_6: QRadioButton
    successful: QMessageBox
    error: QMessageBox

    def setup_ui(self, dialog):
        dialog.resize(600, 500)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(size_policy)
        dialog.setMinimumSize(QSize(600, 500))
        dialog.setMaximumSize(QSize(1000, 900))
        self.grid_layout_1 = QGridLayout(dialog)
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.grid_layout_1.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.frame = QFrame(dialog)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.grid_layout_2 = QGridLayout(self.frame)
        self.list_view = QListView(self.frame)
        self.list_view.setMaximumSize(QSize(16777215, 200))
        self.list_txt = []
        self.model = QStringListModel(self.frame)
        self.model.setStringList(self.list_txt)
        self.list_view.setModel(self.model)

        self.grid_layout_2.addWidget(self.list_view, 2, 0, 1, 1)

        self.push_button_1 = QPushButton(self.frame)

        self.grid_layout_2.addWidget(self.push_button_1, 1, 0, 1, 1)

        self.push_button_2 = QPushButton(self.frame)

        self.grid_layout_2.addWidget(self.push_button_2, 5, 0, 1, 1)

        self.widget_1 = QWidget(self.frame)
        self.widget_1.setMaximumSize(QSize(16777215, 120))
        self.horizontal_layout = QHBoxLayout(self.widget_1)
        self.widget_2 = QWidget(self.widget_1)
        self.vertical_layout_1 = QVBoxLayout(self.widget_2)
        self.label_1 = QLabel(self.widget_2)

        self.vertical_layout_1.addWidget(self.label_1)

        self.radio_button_1 = QRadioButton(self.widget_2)

        self.vertical_layout_1.addWidget(self.radio_button_1)

        self.radio_button_2 = QRadioButton(self.widget_2)

        self.vertical_layout_1.addWidget(self.radio_button_2)

        self.radio_button_3 = QRadioButton(self.widget_2)

        self.vertical_layout_1.addWidget(self.radio_button_3)

        self.horizontal_layout.addWidget(self.widget_2)

        self.line = QFrame(self.widget_1)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout.addWidget(self.line)

        self.widget_3 = QWidget(self.widget_1)
        self.vertical_layout_2 = QVBoxLayout(self.widget_3)
        self.label_2 = QLabel(self.widget_3)

        self.vertical_layout_2.addWidget(self.label_2)

        self.radio_button_4 = QRadioButton(self.widget_3)

        self.vertical_layout_2.addWidget(self.radio_button_4)

        self.radio_button_5 = QRadioButton(self.widget_3)

        self.vertical_layout_2.addWidget(self.radio_button_5)

        self.radio_button_6 = QRadioButton(self.widget_3)

        self.vertical_layout_2.addWidget(self.radio_button_6)

        self.horizontal_layout.addWidget(self.widget_3)

        self.grid_layout_2.addWidget(self.widget_1, 0, 0, 1, 1)

        self.grid_layout_1.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslate_ui(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.push_button_1.clicked.connect(self.chose_file)
        self.push_button_2.clicked.connect(self.import_iw)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "Импорт", None))
        dialog.setWhatsThis(QCoreApplication.translate
                            ("", "Для импорта: выберите параметры входного файла (разделитель, кодировка). "
                                 "Импортируется только один файл за раз. Десятичным разделителем должна быть точка. "
                                 "Импортированный файл ничем не будет отличаться от обычного текстового файла. "
                                 "Несмотря на расширение файла '.grad'. "
                                 "Просто в конец файла будет добавлен столбец, где будут храниться все введенные "
                                 "формулы. Кодировка файла 'utf-8', разделитель ';'."))
        self.push_button_1.setText(QCoreApplication.translate("dialog", "Выбрать файл для импорта", None))
        self.push_button_2.setText(QCoreApplication.translate("dialog", "Импортировать", None))
        self.label_1.setText(QCoreApplication.translate("dialog", "Разделитель", None))
        self.radio_button_1.setText(QCoreApplication.translate("dialog", "Пробел", None))
        self.radio_button_2.setText(QCoreApplication.translate("dialog", "Точка с запятой: ';'", None))
        self.radio_button_3.setText(QCoreApplication.translate("dialog", "Запятая: ','", None))
        self.label_2.setText(QCoreApplication.translate("dialog", "Кодировка", None))
        self.radio_button_4.setText(QCoreApplication.translate("dialog", "UTF-8", None))
        self.radio_button_5.setText(QCoreApplication.translate("dialog", "CP1250", None))
        self.radio_button_6.setText(QCoreApplication.translate("dialog", "CP1251", None))

    def chose_file(self):
        file = QFileDialog.getOpenFileName(parent=None, filter="*.csv *.txt")
        self.list_txt.append(file[0])
        self.model.setStringList(self.list_txt)

    def import_iw(self):
        file = self.list_view.currentIndex().data()
        importing = False
        if not file:
            importing = False
        elif file:
            name, ok = QFileDialog.getSaveFileName(filter="*.grad")
            if ok:
                if self.radio_button_1.isChecked() and self.radio_button_4.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="utf-8", sep=True)
                elif self.radio_button_1.isChecked() and self.radio_button_5.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1250", sep=True)
                elif self.radio_button_1.isChecked() and self.radio_button_6.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1251", sep=True)
                elif self.radio_button_2.isChecked() and self.radio_button_4.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="utf-8", delimiter=";")
                elif self.radio_button_2.isChecked() and self.radio_button_5.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1250", delimiter=";")
                elif self.radio_button_2.isChecked() and self.radio_button_6.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1251", delimiter=";")
                elif self.radio_button_3.isChecked() and self.radio_button_4.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="utf-8", delimiter=",")
                elif self.radio_button_3.isChecked() and self.radio_button_5.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1250", delimiter=",")
                elif self.radio_button_3.isChecked() and self.radio_button_6.isChecked():
                    importing = Files.import_txt_file(file, ex_file_name=name, coding="cp1251", delimiter=",")
        if importing:
            self.successful = QMessageBox()
            self.successful.setWindowTitle("Успех!")
            self.successful.setWindowIcon(QIcon("logos/success_logo.png"))
            self.successful.setFocusPolicy(Qt.StrongFocus)
            self.successful.setText("Импорт данных завершен!")
            self.successful.show()
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!")
            self.error.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Что-то не получилось. Импорт не произведен!")
            self.error.show()


################################################################################
################################################################################

class UniteDataUiDialog(object):
    grid_layout_1: QGridLayout
    grid_layout_2: QGridLayout
    buttonBox: QDialogButtonBox
    frame: QFrame
    line: QFrame
    list_view: QListView
    list_txt: list
    model: QStringListModel
    push_button_1: QPushButton
    push_button_2: QPushButton
    label_1: QLabel
    label_2: QLabel
    label_3: QLabel
    label_4: QLabel
    widget_1: QWidget
    widget_2: QWidget
    widget_3: QWidget
    widget_4: QWidget
    horizontal_layout_1: QHBoxLayout
    vertical_layout_1: QVBoxLayout
    vertical_layout_2: QVBoxLayout
    vertical_layout_3: QVBoxLayout
    radio_button_1: QRadioButton
    radio_button_2: QRadioButton
    radio_button_3: QRadioButton
    radio_button_4: QRadioButton
    radio_button_5: QRadioButton
    radio_button_6: QRadioButton
    radio_button_7: QRadioButton
    radio_button_8: QRadioButton
    radio_button_9: QRadioButton
    successful: QMessageBox
    error: QMessageBox

    def setup_ui(self, dialog):
        dialog.resize(600, 500)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(dialog.sizePolicy().hasHeightForWidth())
        dialog.setSizePolicy(size_policy)
        dialog.setMinimumSize(QSize(600, 500))
        self.grid_layout_1 = QGridLayout(dialog)
        self.buttonBox = QDialogButtonBox(dialog)
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.grid_layout_1.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.frame = QFrame(dialog)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.grid_layout_2 = QGridLayout(self.frame)
        self.list_view = QListView(self.frame)

        self.list_txt = []
        self.model = QStringListModel(self.frame)
        self.model.setStringList(self.list_txt)
        self.list_view.setModel(self.model)
        self.list_view.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.list_view.setSelectionMode(QAbstractItemView.MultiSelection)

        self.grid_layout_2.addWidget(self.list_view, 2, 0, 1, 1)

        self.push_button_1 = QPushButton(self.frame)

        self.grid_layout_2.addWidget(self.push_button_1, 1, 0, 1, 1)

        self.push_button_2 = QPushButton(self.frame)

        self.grid_layout_2.addWidget(self.push_button_2, 5, 0, 1, 1)

        self.label_1 = QLabel(self.frame)
        self.label_1.setText("Выходной файл будет в кодировке 'utf-8' и с разделителем ';'")
        self.grid_layout_2.addWidget(self.label_1, 6, 0, 1, 1)

        self.widget_1 = QWidget(self.frame)
        self.widget_1.setMaximumSize(QSize(16777215, 120))
        self.horizontal_layout_1 = QHBoxLayout(self.widget_1)
        self.widget_2 = QWidget(self.widget_1)
        self.vertical_layout_1 = QVBoxLayout(self.widget_2)
        self.label_2 = QLabel(self.widget_2)

        self.vertical_layout_1.addWidget(self.label_2)

        self.radio_button_1 = QRadioButton(self.widget_2)

        self.vertical_layout_1.addWidget(self.radio_button_1)

        self.radio_button_2 = QRadioButton(self.widget_2)

        self.vertical_layout_1.addWidget(self.radio_button_2)

        self.radio_button_3 = QRadioButton(self.widget_2)

        self.vertical_layout_1.addWidget(self.radio_button_3)

        self.horizontal_layout_1.addWidget(self.widget_2)

        self.line = QFrame(self.widget_1)
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.horizontal_layout_1.addWidget(self.line)

        self.widget_3 = QWidget(self.widget_1)
        self.vertical_layout_2 = QVBoxLayout(self.widget_3)
        self.label_3 = QLabel(self.widget_3)

        self.vertical_layout_2.addWidget(self.label_3)

        self.radio_button_4 = QRadioButton(self.widget_3)

        self.vertical_layout_2.addWidget(self.radio_button_4)

        self.radio_button_5 = QRadioButton(self.widget_3)

        self.vertical_layout_2.addWidget(self.radio_button_5)

        self.radio_button_6 = QRadioButton(self.widget_3)

        self.vertical_layout_2.addWidget(self.radio_button_6)

        self.horizontal_layout_1.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_1)
        self.vertical_layout_3 = QVBoxLayout(self.widget_4)
        self.label_4 = QLabel(self.widget_4)

        self.vertical_layout_3.addWidget(self.label_4)

        self.radio_button_7 = QRadioButton(self.widget_4)
        self.vertical_layout_3.addWidget(self.radio_button_7)

        self.radio_button_8 = QRadioButton(self.widget_4)
        self.vertical_layout_3.addWidget(self.radio_button_8)

        self.radio_button_9 = QRadioButton(self.widget_4)
        self.vertical_layout_3.addWidget(self.radio_button_9)

        self.horizontal_layout_1.addWidget(self.widget_4)

        self.grid_layout_2.addWidget(self.widget_1, 0, 0, 1, 1)

        self.grid_layout_1.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslate_ui(dialog)
        self.buttonBox.accepted.connect(dialog.accept)
        self.buttonBox.rejected.connect(dialog.reject)
        self.push_button_1.clicked.connect(self.choose_file)
        self.push_button_2.clicked.connect(self.unite_data_iw)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "Склеивание", None))
        dialog.setWhatsThis(
            QCoreApplication.translate("", "Во избежание несчастных случаев крайне не рекомендуеся склеивать файлы в "
                                           "формате '.grad'! Лучше экспортировать в другой формат и затем склеивать их."
                                           " Для склеивания: укажите параметры входных файлов (разделитель, кодировка, "
                                           "способ склейки), десятичным разделителем должна быть точка. У способа "
                                           "склейки 'Одиночные' есть своя справка."))
        self.push_button_1.setText(QCoreApplication.translate("dialog", "Выбрать файлы для склейки", None))
        self.push_button_2.setText(QCoreApplication.translate("dialog", "Собрать воедино", None))
        self.label_2.setText(QCoreApplication.translate("dialog", u"Разделитель", None))
        self.radio_button_1.setText(QCoreApplication.translate("dialog", "Пробел", None))
        self.radio_button_2.setText(QCoreApplication.translate("dialog", "Точка с запятой: ';'", None))
        self.radio_button_3.setText(QCoreApplication.translate("dialog", "Запятая: ','", None))
        self.label_3.setText(QCoreApplication.translate("dialog", "Кодировка", None))
        self.radio_button_4.setText(QCoreApplication.translate("dialog", "UTF-8", None))
        self.radio_button_5.setText(QCoreApplication.translate("dialog", "CP1250", None))
        self.radio_button_6.setText(QCoreApplication.translate("dialog", "CP1251", None))
        self.label_4.setText(QCoreApplication.translate("dialog", "Как склеиваем?"))
        self.radio_button_7.setText(QCoreApplication.translate("dialog", "Последовательно", None))
        self.radio_button_8.setText(QCoreApplication.translate("dialog", "Параллельно (2 файла)", None))
        self.radio_button_9.setText(QCoreApplication.translate("dialog", "Одиночные", None))
        self.radio_button_9.setWhatsThis("Для склеивания файлов после программы TNWorks. "
                                         "Когда каждый параметр записан в отдельный текстовый файл. "
                                         "Название файла запишется как название параметра в итоговом файле.")

    def choose_file(self):
        files = QFileDialog.getOpenFileNames(filter="*.txt\n*.csv\n*.grad\n*AllFiles()")
        if self.list_view:
            self.list_txt.clear()
            self.list_txt.extend(files[0])
            self.model.setStringList(self.list_txt)
        else:
            self.list_txt.extend(files[0])
            self.model.setStringList(self.list_txt)

    def unite_data_iw(self):
        items = self.list_view.selectedIndexes()
        files = [s.data() for s in items]
        if not files:
            united = False
        else:
            name, ok = QFileDialog.getSaveFileName(filter="*.txt\n*.csv\n*.grad")
            how = "Параллельно"
            united = False
            if ok:
                if self.radio_button_7.isChecked():
                    how = "Последовательно"
                elif self.radio_button_8.isChecked():
                    how = "Параллельно"
                elif self.radio_button_9.isChecked():
                    how = "Одиночные"
                    united = Files.concat_txt_data(files, ex_file_name=name, how=how)
                if self.radio_button_1.isChecked() and self.radio_button_4.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="utf-8", sep=True, how=how)
                elif self.radio_button_1.isChecked() and self.radio_button_5.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="cp1250", sep=True, how=how)
                elif self.radio_button_1.isChecked() and self.radio_button_6.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="cp1251", sep=True, how=how)
                elif self.radio_button_2.isChecked() and self.radio_button_4.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="utf-8",
                                                   sep=False, delimiter=";", how=how)
                elif self.radio_button_2.isChecked() and self.radio_button_5.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="cp1250",
                                                   sep=False, delimiter=";", how=how)
                elif self.radio_button_2.isChecked() and self.radio_button_6.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="cp1251",
                                                   sep=False, delimiter=";", how=how)
                elif self.radio_button_3.isChecked() and self.radio_button_4.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="utf-8",
                                                   sep=False, delimiter=",", how=how)
                elif self.radio_button_3.isChecked() and self.radio_button_5.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="cp1250",
                                                   sep=False, delimiter=",", how=how)
                elif self.radio_button_3.isChecked() and self.radio_button_6.isChecked():
                    united = Files.concat_txt_data(files, ex_file_name=name, coding="cp1251",
                                                   sep=False, delimiter=",", how=how)
        if united:
            self.successful = QMessageBox()
            self.successful.setWindowTitle("Успех!")
            self.successful.setWindowIcon(QIcon("logos/success_logo.png"))
            self.successful.setFocusPolicy(Qt.StrongFocus)
            self.successful.setText("Склеивание данных завершено!")
            self.successful.show()
        else:
            self.error = QMessageBox()
            self.error.setWindowTitle("Ошибка!")
            self.error.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error.setFocusPolicy(Qt.StrongFocus)
            self.error.setText("Что-то не получилось. Склеивание не произведено!")
            self.error.show()

################################################################################
################################################################################


class ShiftParameters(object):
    vertical_layout_1: QVBoxLayout
    vertical_layout_2: QVBoxLayout
    frame: QFrame
    label_1: QLabel
    label_2: QLabel
    label_3: QLabel
    list_view: QListView
    list_text: Index
    model: QStringListModel
    horizontal_spacer: QSpacerItem
    spin_box: QSpinBox
    push_button: QPushButton
    button_box: QDialogButtonBox
    successful: QMessageBox
    error_1: QMessageBox
    error_2: QMessageBox

    def setup_ui(self, dialog):
        dialog.resize(440, 500)
        dialog.setMinimumSize(QSize(300, 500))
        dialog.setFocusPolicy(Qt.StrongFocus)
        self.vertical_layout_1 = QVBoxLayout(dialog)
        self.frame = QFrame(dialog)
        self.frame.setFrameShape(QFrame.StyledPanel)
        self.frame.setFrameShadow(QFrame.Raised)
        self.vertical_layout_2 = QVBoxLayout(self.frame)
        self.label_1 = QLabel(self.frame)

        self.vertical_layout_2.addWidget(self.label_1)

        self.list_view = QListView(self.frame)
        self.list_view.setSelectionBehavior(QAbstractItemView.SelectItems)
        self.list_view.setSelectionMode(QAbstractItemView.MultiSelection)
        self.list_text = MainCode.data.columns[:-1]
        self.model = QStringListModel(self.frame)
        self.model.setStringList(self.list_text)
        self.list_view.setModel(self.model)

        self.vertical_layout_2.addWidget(self.list_view)

        self.horizontal_spacer = QSpacerItem(399, 20, QSizePolicy.Expanding, QSizePolicy.Minimum)

        self.vertical_layout_2.addItem(self.horizontal_spacer)

        self.label_2 = QLabel(self.frame)
        self.vertical_layout_2.addWidget(self.label_2)

        self.label_3 = QLabel(self.frame)

        self.vertical_layout_2.addWidget(self.label_3)

        self.spin_box = QSpinBox(self.frame)

        self.vertical_layout_2.addWidget(self.spin_box)

        self.push_button = QPushButton(self.frame)

        self.vertical_layout_2.addWidget(self.push_button)

        self.vertical_layout_1.addWidget(self.frame)

        self.button_box = QDialogButtonBox(dialog)
        self.button_box.setOrientation(Qt.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout_1.addWidget(self.button_box)

        self.retranslate_ui(dialog)
        self.button_box.accepted.connect(dialog.accept)
        self.button_box.rejected.connect(dialog.reject)
        self.push_button.clicked.connect(self.shift_params)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "Сдвиг параметров", None))
        self.label_1.setText(QCoreApplication.translate("dialog", "Выберите параметры для сдвига:", None))
        self.label_2.setText(QCoreApplication.translate("dialog",
                                                        "Выбранные параметры будут сдвинуты назад относительно\n"
                                                        "остальных параметров на выбранное ниже количество точек.\n"
                                                        "После сдвига обязательно откройте формулы и нажмите 'ok'.",
                                                        None))
        self.label_3.setText(QCoreApplication.translate("dialog", "Количество точек для сдвига", None))
        self.push_button.setText(QCoreApplication.translate("dialog", "Сдвинуть", None))

    def shift_params(self):
        items = self.list_view.selectedIndexes()
        if items:
            parameters_names = [i.data() for i in items]
            dots = self.spin_box.value()
            success = Files.shift_analog(parameters_names=parameters_names, dots=dots)
            if success:
                self.successful = QMessageBox()
                self.successful.setWindowTitle("Успех!")
                self.successful.setWindowIcon(QIcon("logos/success_logo.png"))
                self.successful.setFocusPolicy(Qt.StrongFocus)
                self.successful.setText("Сдвиг произведен!")
                self.successful.show()
            else:
                self.error_1 = QMessageBox()
                self.error_1.setWindowTitle("Упс!")
                self.error_1.setWindowIcon(QIcon("logos/error_logo.png"))
                self.error_1.setFocusPolicy(Qt.StrongFocus)
                self.error_1.setText("Что-то не получилось!")
                self.error_1.show()

        else:
            self.error_2 = QMessageBox()
            self.error_2.setWindowTitle("Ошибка!")
            self.error_2.setWindowIcon(QIcon("logos/error_logo.png"))
            self.error_2.setFocusPolicy(Qt.StrongFocus)
            self.error_2.setText("Выберите данные")
            self.error_2.show()


################################################################################
################################################################################


class ExportUiDialog(object):
    item_list_1: list
    item_list_2: list
    file_name: str
    vertical_layout_1: QVBoxLayout
    vertical_layout_2: QVBoxLayout
    vertical_layout_3: QVBoxLayout
    widget_1: QWidget
    widget_2: QWidget
    widget_3: QWidget
    widget_4: QWidget
    label_1: QLabel
    label_2: QLabel
    label_3: QLabel
    label_4: QLabel
    label_5: QLabel
    horizontal_layout_1: QHBoxLayout
    horizontal_layout_2: QHBoxLayout
    list_view_1: QListView
    list_view_2: QListView
    model_1: QStringListModel
    model_2: QStringListModel
    push_button_1: QPushButton
    push_button_2: QPushButton
    push_button_3: QPushButton
    line_1: QLineEdit
    line_2: QLineEdit
    radio_button_1: QRadioButton
    radio_button_2: QRadioButton
    buttonBox: QDialogButtonBox
    successful: QMessageBox
    error: QMessageBox

    def setup_ui(self, dialog):
        dialog.resize(600, 700)
        self.item_list_1 = [i for i in MainCode.data.columns]
        self.item_list_2 = []
        self.file_name = MainCode.file_name_g
        self.vertical_layout_1 = QVBoxLayout(dialog)
        self.widget_1 = QWidget(dialog)
        self.vertical_layout_2 = QVBoxLayout(self.widget_1)
        self.label_1 = QLabel(self.widget_1)

        self.vertical_layout_2.addWidget(self.label_1)
        self.widget_2 = QWidget(self.widget_1)
        self.horizontal_layout_1 = QHBoxLayout(self.widget_2)
        self.list_view_1 = QListView(self.widget_2)
        self.model_1 = QStringListModel(self.widget_1)
        self.model_1.setStringList(self.item_list_1)
        self.list_view_1.setModel(self.model_1)
        self.list_view_1.setEditTriggers(
            QAbstractItemView.AnyKeyPressed | QAbstractItemView.EditKeyPressed | QAbstractItemView.SelectedClicked)
        self.list_view_1.setTabKeyNavigation(True)
        self.list_view_1.setSelectionMode(QAbstractItemView.MultiSelection)

        self.horizontal_layout_1.addWidget(self.list_view_1)

        self.list_view_2 = QListView(self.widget_2)
        self.model_2 = QStringListModel(self.widget_1)
        self.model_2.setStringList(self.item_list_2)
        self.list_view_2.setModel(self.model_2)

        self.horizontal_layout_1.addWidget(self.list_view_2)

        self.vertical_layout_2.addWidget(self.widget_2)

        self.push_button_1 = QPushButton(self.widget_1)

        self.vertical_layout_2.addWidget(self.push_button_1)

        self.push_button_2 = QPushButton(self.widget_1)
        self.vertical_layout_2.addWidget(self.push_button_2)

        self.widget_3 = QWidget(self.widget_1)
        self.widget_3.setMinimumSize(QSize(150, 150))
        self.horizontal_layout_2 = QHBoxLayout(self.widget_3)

        self.label_2 = QLabel(self.widget_3)
        self.label_2.setText("Укажите диапазон данных для экспорта\nВ точках (не в секундах)\nОт:")
        self.label_2.setGeometry(QRect(1, 10, 250, 40))
        self.line_1 = QLineEdit(self.widget_3)
        self.line_1.insert("0")
        self.line_1.setGeometry(QRect(1, 50, 100, 20))

        self.label_3 = QLabel(self.widget_3)
        self.label_3.setText("До:")
        self.label_3.setGeometry(QRect(1, 70, 100, 20))
        self.line_2 = QLineEdit(self.widget_3)
        self.line_2.insert(f"{len(MainCode.data)}")
        self.line_2.setGeometry(QRect(1, 90, 100, 20))

        self.label_4 = QLabel(self.widget_3)
        self.label_4.setText("Выбор данных для экспорта")
        self.label_4.setGeometry(QRect(300, 10, 150, 20))
        self.radio_button_1 = QRadioButton(self.widget_3)
        self.radio_button_1.setGeometry(QRect(300, 30, 150, 20))

        self.radio_button_2 = QRadioButton(self.widget_3)
        self.radio_button_2.setGeometry(QRect(300, 50, 150, 20))

        self.vertical_layout_2.addWidget(self.widget_3)

        self.widget_4 = QWidget(self.widget_1)
        self.widget_4.setMinimumSize(QSize(100, 50))
        self.vertical_layout_3 = QVBoxLayout(self.widget_4)
        self.push_button_3 = QPushButton(self.widget_4)

        self.vertical_layout_3.addWidget(self.push_button_3)

        self.label_5 = QLabel(self.widget_4)
        self.label_5.setText("Выходной файл будет в кодировке 'utf-8' и с разделителем ';'")
        self.vertical_layout_3.addWidget(self.label_5)

        self.vertical_layout_2.addWidget(self.widget_4)

        self.buttonBox = QDialogButtonBox(self.widget_1)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

        self.vertical_layout_2.addWidget(self.buttonBox)

        self.vertical_layout_1.addWidget(self.widget_1)

        self.retranslate_ui(dialog)
        self.buttonBox.rejected.connect(dialog.reject)
        self.radio_button_1.pressed.connect(self.list_view_1.selectAll)
        self.radio_button_2.pressed.connect(self.list_view_1.reset)
        self.list_view_1.doubleClicked.connect(self.update_by_doubleclick)
        self.list_view_2.doubleClicked.connect(self.delete_by_doubleclick)
        self.push_button_1.clicked.connect(self.update_by_button)
        self.push_button_2.clicked.connect(self.delete_by_button)
        self.push_button_3.clicked.connect(self.export)

        QMetaObject.connectSlotsByName(dialog)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "Экспорт", None))
        dialog.setWhatsThis(
            QCoreApplication.translate
            ("dialog",
             "Выберите необходимые для экспорта параметры в левой колонке и нажмите 'Добавить выбранные параметры'. "
             "Или добавляйте их двойным щелчком мыши. Укажите диапазон точек для экспорта. "
             "Если экспортируется весь файл, то все уже указано. После нажатия на 'Экспортировать' откроется диалоговое"
             " окно, там нужно указать имя выходного файла и формат, возможные варианты: '.grad', '.csv', '.txt'."))
        self.push_button_1.setText(QCoreApplication.translate("dialog", "Добавить выбранные параметры", None))
        self.push_button_3.setText(QCoreApplication.translate("dialog", "Экспортировать", None))
        self.push_button_2.setText(QCoreApplication.translate("dialog", "Очистить выбор", None))
        self.radio_button_1.setText(QCoreApplication.translate("dialog", "Выбрать все", None))
        self.radio_button_2.setText(QCoreApplication.translate("dialog", "Снять все", None))
        self.label_1.setText(QCoreApplication.translate("dialog", "Выберите параметры для экспорта", None))

    def update_by_doubleclick(self):
        self.item_list_2.append(self.list_view_1.currentIndex().data())
        self.model_2.setStringList(self.item_list_2)

    def delete_by_doubleclick(self):
        self.item_list_2.remove(self.list_view_2.currentIndex().data())
        self.model_2.setStringList(self.item_list_2)

    def update_by_button(self):
        items = self.list_view_1.selectedIndexes()
        self.item_list_2 = [s.data() for s in items]
        self.model_2.setStringList(self.item_list_2)

    def delete_by_button(self):
        self.item_list_2.clear()
        self.model_2.setStringList(self.item_list_2)

    def export(self):
        file_name, ok = QFileDialog.getSaveFileName(filter="*.grad\n*.csv\n*.txt")
        t0 = int(self.line_1.text())
        t1 = int(self.line_2.text())
        if ok and self.item_list_2:
            done = Files.export(parameters_names=self.item_list_2, file_name=file_name, t0=t0, t1=t1)
            if done:
                self.successful = QMessageBox()
                self.successful.setWindowTitle("Отчёт                                               ")
                self.successful.setText("Успех! Экспорт данных произведен!")
                self.successful.setWindowIcon(QIcon("logos/success_logo.png"))
                self.successful.show()
            elif not done:
                self.error = QMessageBox()
                self.error.setWindowTitle("Отчёт                                                 ")
                self.error.setText("Упс! Что-то не получилось")
                self.error.setWindowIcon(QIcon("logos/error_logo.png"))
                self.error.show()


class Que(QMainWindow):
    def __init__(self):
        super(Que, self).__init__()

        self.setWindowIcon(QIcon("icons/help_icon.png"))
        self.setWindowTitle("Справка о программе")
        self.resize(1200, 900)
        self.central_widget = QWidget()
        self.grid_layout = QGridLayout(self.central_widget)

        self.plain_text = QPlainTextEdit(self.central_widget)
        self.model = QStringListModel(self.central_widget)
        with open("que.txt", encoding="utf-8") as f:
            que_file = f.read()
        self.plain_text.setPlainText(que_file)
        self.font = QFont()
        self.font.setFamily("Arial")
        self.font.setPointSize(13)
        self.plain_text.setFont(self.font)
        self.grid_layout.addWidget(self.plain_text)
        self.setCentralWidget(self.central_widget)
