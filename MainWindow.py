from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QSizePolicy


class UiMainWindow(object):
    def setup_ui(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1000, 1)
        size_policy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        MainWindow.setMaximumSize(1000, 25)
        MainWindow.setMinimumSize(1000, 25)
        MainWindow.move(1, 1)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setDocumentMode(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        self.centralwidget.setMouseTracking(True)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.widget = QtWidgets.QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        self.gridLayout.addWidget(self.widget, 0, 0, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 654, 22))
        self.menubar.setAutoFillBackground(False)
        self.menubar.setObjectName("menubar")

        self.File = QtWidgets.QMenu(self.menubar)
        self.File.setObjectName("File")
        self.Parameters = QtWidgets.QMenu(self.menubar)
        self.Parameters.setObjectName("Parameters")
        self.Graphics = QtWidgets.QMenu(self.menubar)
        self.Graphics.setObjectName("Graphics")
        self.Treatment = QtWidgets.QMenu(self.menubar)
        self.Treatment.setObjectName("Treatment")

        MainWindow.setMenuBar(self.menubar)

        self.open_file_mw = QtWidgets.QAction(MainWindow)
        self.open_file_mw.setObjectName("open_file")

        self.save_file_mw = QtWidgets.QAction(MainWindow)
        self.save_file_mw.setObjectName("save_file")

        self.save_file_as_mw = QtWidgets.QAction(MainWindow)
        self.save_file_as_mw.setObjectName("save_file_as")

        self.import_files_mw = QtWidgets.QAction(MainWindow)
        self.import_files_mw.setObjectName("import_files")

        self.export_files_mw = QtWidgets.QAction(MainWindow)
        self.export_files_mw.setObjectName("export")

        self.unite_txt_data_mw = QtWidgets.QAction(MainWindow)
        self.unite_txt_data_mw.setObjectName("unite_txt_data")

        self.graphic_by_time_mw = QtWidgets.QAction(MainWindow)
        self.graphic_by_time_mw.setObjectName("graphic_by_time")

        self.linalg_mw = QtWidgets.QAction(MainWindow)
        self.linalg_mw.setObjectName("linalg")

        self.multi_linalg_mw = QtWidgets.QAction(MainWindow)
        self.multi_linalg_mw.setObjectName("multi_linalg")

        self.graphic_by_parameter_mw = QtWidgets.QAction(MainWindow)
        self.graphic_by_parameter_mw.setObjectName("graphic_by_param")

        self.open_params_mw = QtWidgets.QAction(MainWindow)
        self.open_params_mw.setObjectName("open_params")

        self.shift_params_mw = QtWidgets.QAction(MainWindow)
        self.shift_params_mw.setObjectName("shift_params")

        self.formulas_mw = QtWidgets.QAction(MainWindow)
        self.formulas_mw.setObjectName("formulas")

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
        self.menubar.addAction(self.File.menuAction())
        self.menubar.addAction(self.Parameters.menuAction())
        self.menubar.addAction(self.Graphics.menuAction())
        self.menubar.addAction(self.Treatment.menuAction())

        self.retranslate_ui(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslate_ui(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Grad"))
        self.File.setTitle(_translate("MainWindow", "Файл"))
        self.Parameters.setTitle(_translate("MainWindow", "Параметры"))
        self.Graphics.setTitle(_translate("MainWindow", "Графики"))
        self.Treatment.setTitle(_translate("MainWindow", "Обработка"))

        self.open_file_mw.setText(_translate("MainWindow", "Открыть..."))
        self.open_file_mw.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.save_file_mw.setText(_translate("MainWindow", "Сохранить"))
        self.save_file_mw.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.save_file_as_mw.setText(_translate("MainWindow", "Сохранить как..."))
        self.save_file_as_mw.setShortcut(_translate("MainWindow", "Ctrl+A"))
        self.import_files_mw.setText(_translate("MainWindow", "Импорт..."))
        self.export_files_mw.setText(_translate("MainWindow", "Экспорт"))
        self.unite_txt_data_mw.setText(_translate("MainWindow", "Объединить файлы..."))
        self.graphic_by_time_mw.setText(_translate("MainWindow", "График по времени "))
        self.graphic_by_parameter_mw.setText(_translate("MainWindow", "График по параметру"))
        self.open_params_mw.setText(_translate("MainWindow", "Таблица параметров"))
        self.formulas_mw.setText(_translate("MainWindow", "Формулы"))
        self.shift_params_mw.setText(_translate("MainWindow", "Сдвиг параметров"))
        self.linalg_mw.setText(_translate("MainWindow", "Линейная регрессия"))
        self.multi_linalg_mw.setText(_translate("MainWindow", "Множественная регрессия"))
