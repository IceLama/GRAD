import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QDialog, QMessageBox
from MainCode import Files
import MainCode
from ParametersWindow import ParameterWindow
from MainWindow import UiMainWindow
from Dialogs import ParameterUiDialog, GraphicByTimeUiDialog, GraphicByParameterUiDialog, LinalgUiDialog, \
    MultiLinalgUiDialog, ImportUiDialog, UniteDataUiDialog, ShiftParameters, ExportUiDialog, Que


class MainWindow(QMainWindow, UiMainWindow):
    help_m: Que
    open_param_m: ParameterWindow
    import_txt_file_m: QDialog
    export_m: QDialog
    unite_txt_file_m: QDialog
    open_formulas_m: QDialog
    graphic_by_time_m: QDialog
    graphic_by_parameter_m: QDialog
    lin_alg_m: QDialog
    multi_alg_m: QDialog
    shift_params_m: QDialog
    close: QMessageBox

    def __init__(self, parent=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)

        self.setup_ui(self)

        self.open_file_mw.triggered.connect(self.open_file_mf)
        self.import_files_mw.triggered.connect(self.import_txt_file_mf)
        self.export_files_mw.triggered.connect(self.export_mf)
        self.open_params_mw.triggered.connect(self.open_param_mf)
        self.shift_params_mw.triggered.connect(self.shift_parameters_mf)
        self.formulas_mw.triggered.connect(self.formulas_mf)
        self.graphic_by_time_mw.triggered.connect(self.graphic_by_time_mf)
        self.graphic_by_parameter_mw.triggered.connect(self.graphic_by_parameter_mf)
        self.save_file_mw.triggered.connect(self.save_file_mf)
        self.save_file_as_mw.triggered.connect(self.save_as_mf)
        self.unite_txt_data_mw.triggered.connect(self.unite_txt_data_mf)
        self.linalg_mw.triggered.connect(self.lin_alg_mf)
        self.multi_linalg_mw.triggered.connect(self.multi_alg_mf)
        self.faq_mw.triggered.connect(self.help_win_mf)

    def open_param_mf(self):
        self.open_param_m = ParameterWindow()
        self.open_param_m.show()

    def open_file_mf(self):
        file, ok = QFileDialog.getOpenFileName(self, "Открыть файл", filter="*.grad")
        if ok:
            Files.open_file(file)
            MainWindow.setWindowTitle(self, f"Grad      || {MainCode.file_name_g} ||")

    def import_txt_file_mf(self):
        self.import_txt_file_m = QDialog()
        self.import_txt_file_m.ui = ImportUiDialog()
        self.import_txt_file_m.ui.setup_ui(self.import_txt_file_m)
        self.import_txt_file_m.show()

    def export_mf(self):
        self.export_m = QDialog()
        self.export_m.ui = ExportUiDialog()
        self.export_m.ui.setup_ui(self.export_m)
        self.export_m.show()

    @staticmethod
    def save_file_mf():
        Files.save()

    @staticmethod
    def save_as_mf():
        file_name, ok = QFileDialog.getSaveFileName(QFileDialog(), "Сохранить файл", filter="*.grad \n *.csv")
        if ok:
            Files.save_as(file_name)

    def unite_txt_data_mf(self):
        self.unite_txt_file_m = QDialog()
        self.unite_txt_file_m.ui = UniteDataUiDialog()
        self.unite_txt_file_m.ui.setup_ui(self.unite_txt_file_m)
        self.unite_txt_file_m.show()

    def formulas_mf(self):
        self.open_formulas_m = QDialog()
        self.open_formulas_m.ui = ParameterUiDialog()
        self.open_formulas_m.ui.setup_ui(self.open_formulas_m)
        self.open_formulas_m.show()

    def graphic_by_time_mf(self):
        self.graphic_by_time_m = QDialog()
        self.graphic_by_time_m.ui = GraphicByTimeUiDialog()
        self.graphic_by_time_m.ui.setup_ui(self.graphic_by_time_m)
        self.graphic_by_time_m.show()

    def graphic_by_parameter_mf(self):
        self.graphic_by_parameter_m = QDialog()
        self.graphic_by_parameter_m.ui = GraphicByParameterUiDialog()
        self.graphic_by_parameter_m.ui.setup_ui(self.graphic_by_parameter_m)
        self.graphic_by_parameter_m.show()

    def lin_alg_mf(self):
        self.lin_alg_m = QDialog()
        self.lin_alg_m.ui = LinalgUiDialog()
        self.lin_alg_m.ui.setup_ui(self.lin_alg_m)
        self.lin_alg_m.show()

    def multi_alg_mf(self):
        self.multi_alg_m = QDialog()
        self.multi_alg_m.ui = MultiLinalgUiDialog()
        self.multi_alg_m.ui.setup_ui(self.multi_alg_m)
        self.multi_alg_m.show()

    def shift_parameters_mf(self):
        self.shift_params_m = QDialog()
        self.shift_params_m.ui = ShiftParameters()
        self.shift_params_m.ui.setup_ui(self.shift_params_m)
        self.shift_params_m.show()

    def help_win_mf(self):
        self.help_m = Que()
        self.help_m.show()

    def closeEvent(self, event):
        self.close = QMessageBox()
        ask = self.close.question(self, "", "Сохранить изменения?       ",
                                  self.close.Yes | self.close.Discard | self.close.No)

        if ask == self.close.Yes:
            Files.save()
            event.accept()
            for window in QApplication.topLevelWidgets():
                window.close()
        elif ask == self.close.Discard:
            event.ignore()
        elif ask == self.close.No:
            event.accept()
            for window in QApplication.topLevelWidgets():
                window.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon("logos/logo.png"))
    win = MainWindow()
    win.setWindowIcon(QIcon("logos/logo.png"))
    win.show()
    sys.exit(app.exec())
