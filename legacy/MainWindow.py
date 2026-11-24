from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QSizePolicy, QAction, QMenu, QMenuBar, QWidget, QGridLayout, QHBoxLayout


class UiMainWindow:
    central_widget: QWidget
    horizontal_layout: QHBoxLayout
    grid_layout: QGridLayout
    widget: QWidget
    menu_bar: QMenuBar
    File: QMenu
    Parameters: QMenu
    Graphics: QMenu
    Treatment: QMenu
    Faq: QMenu
    open_file_mw: QAction
    save_file_mw: QAction
    save_file_as_mw: QAction
    import_files_mw: QAction
    export_files_mw: QAction
    unite_txt_data_mw: QAction
    graphic_by_time_mw: QAction
    linalg_mw: QAction
    multi_linalg_mw: QAction
    graphic_by_parameter_mw: QAction
    open_params_mw: QAction
    shift_params_mw: QAction
    formulas_mw: QAction
    faq_mw: QAction

    def setup_ui(self, main_window):
        main_window.setEnabled(True)
        main_window.resize(1000, 1)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        main_window.setMaximumSize(1000, 25)
        main_window.setMinimumSize(1000, 25)
        main_window.move(1, 1)
        main_window.setAutoFillBackground(False)
        main_window.setDocumentMode(True)
        self.central_widget = QtWidgets.QWidget(main_window)
        self.central_widget.setEnabled(True)
        self.central_widget.setMouseTracking(True)
        self.horizontal_layout = QtWidgets.QHBoxLayout(self.central_widget)
        self.grid_layout = QtWidgets.QGridLayout()
        self.widget = QtWidgets.QWidget(self.central_widget)
        self.grid_layout.addWidget(self.widget, 0, 0, 1, 1)
        self.horizontal_layout.addLayout(self.grid_layout)
        main_window.setCentralWidget(self.central_widget)
        self.menu_bar = QtWidgets.QMenuBar(main_window)
        self.menu_bar.setEnabled(True)
        self.menu_bar.setGeometry(QtCore.QRect(0, 0, 654, 22))
        self.menu_bar.setAutoFillBackground(False)

        self.File = QtWidgets.QMenu(self.menu_bar)
        self.Parameters = QtWidgets.QMenu(self.menu_bar)
        self.Graphics = QtWidgets.QMenu(self.menu_bar)
        self.Treatment = QtWidgets.QMenu(self.menu_bar)
        self.Faq = QtWidgets.QMenu(self.menu_bar)

        main_window.setMenuBar(self.menu_bar)

        self.open_file_mw = QtWidgets.QAction(main_window)

        self.save_file_mw = QtWidgets.QAction(main_window)

        self.save_file_as_mw = QtWidgets.QAction(main_window)

        self.import_files_mw = QtWidgets.QAction(main_window)

        self.export_files_mw = QtWidgets.QAction(main_window)

        self.unite_txt_data_mw = QtWidgets.QAction(main_window)

        self.graphic_by_time_mw = QtWidgets.QAction(main_window)

        self.linalg_mw = QtWidgets.QAction(main_window)

        self.multi_linalg_mw = QtWidgets.QAction(main_window)

        self.graphic_by_parameter_mw = QtWidgets.QAction(main_window)

        self.open_params_mw = QtWidgets.QAction(main_window)

        self.shift_params_mw = QtWidgets.QAction(main_window)

        self.formulas_mw = QtWidgets.QAction(main_window)

        self.faq_mw = QtWidgets.QAction(main_window)

        self.File.addAction(self.open_file_mw)
        self.File.addAction(self.save_file_mw)
        self.File.addAction(self.save_file_as_mw)
        self.File.addAction(self.import_files_mw)
        self.File.addAction(self.export_files_mw)
        self.File.addAction(self.unite_txt_data_mw)

        self.Parameters.addAction(self.formulas_mw)
        self.Parameters.addAction(self.open_params_mw)
        self.Parameters.addAction(self.shift_params_mw)
        self.Graphics.addAction(self.graphic_by_time_mw)
        self.Graphics.addAction(self.graphic_by_parameter_mw)
        self.Treatment.addAction(self.linalg_mw)
        self.Treatment.addAction(self.multi_linalg_mw)
        self.Faq.addAction(self.faq_mw)
        self.menu_bar.addAction(self.File.menuAction())
        self.menu_bar.addAction(self.Parameters.menuAction())
        self.menu_bar.addAction(self.Graphics.menuAction())
        self.menu_bar.addAction(self.Treatment.menuAction())
        self.menu_bar.addAction(self.Faq.menuAction())

        self.retranslate_ui(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)

    def retranslate_ui(self, main_window):
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("main_window", "Grad"))
        self.File.setTitle(_translate("main_window", "Файл"))
        self.Parameters.setTitle(_translate("main_window", "Параметры"))
        self.Graphics.setTitle(_translate("main_window", "Графики"))
        self.Treatment.setTitle(_translate("main_window", "Обработка"))
        self.Faq.setTitle(_translate("main_window", "Справка"))

        self.open_file_mw.setText(_translate("main_window", "Открыть..."))
        self.open_file_mw.setShortcut(_translate("main_window", "Ctrl+O"))
        self.save_file_mw.setText(_translate("main_window", "Сохранить"))
        self.save_file_mw.setShortcut(_translate("main_window", "Ctrl+S"))
        self.save_file_mw.setIcon(QIcon("save_icon.png"))
        self.save_file_as_mw.setText(_translate("main_window", "Сохранить как..."))
        self.save_file_as_mw.setShortcut(_translate("main_window", "Ctrl+Shift+S"))
        self.save_file_as_mw.setIcon(QIcon("save_as_icon.png"))
        self.import_files_mw.setText(_translate("main_window", "Импорт..."))
        self.import_files_mw.setIcon(QIcon("import_icon.png"))
        self.export_files_mw.setText(_translate("main_window", "Экспорт"))
        self.export_files_mw.setIcon(QIcon("export_icon.png"))
        self.unite_txt_data_mw.setText(_translate("main_window", "Объединить файлы..."))
        self.unite_txt_data_mw.setIcon(QIcon("unite_files_icon.png"))
        self.graphic_by_time_mw.setText(_translate("main_window", "График по времени "))
        self.graphic_by_time_mw.setShortcut(_translate("main_window", "Ctrl+G"))
        self.graphic_by_time_mw.setIcon(QIcon("plot_icon.png"))
        self.graphic_by_parameter_mw.setText(_translate("main_window", "График по параметру"))
        self.graphic_by_parameter_mw.setIcon(QIcon("scatter_icon.png"))
        self.open_params_mw.setText(_translate("main_window", "Таблица параметров"))
        self.open_params_mw.setIcon(QIcon("table_icon.png"))
        self.formulas_mw.setText(_translate("main_window", "Формулы"))
        self.formulas_mw.setShortcut(_translate("main_window", "Ctrl+F"))
        self.formulas_mw.setIcon(QIcon("formula_icon.png"))
        self.shift_params_mw.setText(_translate("main_window", "Сдвиг параметров"))
        self.shift_params_mw.setIcon(QIcon("shift_analog_icon.png"))
        self.linalg_mw.setText(_translate("main_window", "Линейная регрессия"))
        self.linalg_mw.setIcon(QIcon("data_analysis_icon.png"))
        self.multi_linalg_mw.setText(_translate("main_window", "Множественная регрессия"))
        self.multi_linalg_mw.setIcon(QIcon("data_analysis_icon.png"))
        self.faq_mw.setText(_translate("main_window", "Справка"))
        self.faq_mw.setShortcut(_translate("main_window", "F1"))
        self.faq_mw.setIcon(QIcon("help_icon.png"))
