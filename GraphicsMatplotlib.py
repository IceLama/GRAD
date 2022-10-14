from bisect import bisect_left
import numpy as np
import matplotlib.pyplot as plt
from PyQt5.QtCore import Qt, QMetaObject, QCoreApplication
from PyQt5.QtGui import QIcon
# from matplotlib import transforms
from matplotlib.widgets import SpanSelector, Cursor, MultiCursor
from PyQt5.QtWidgets import QMessageBox, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QApplication
from pandas import merge
from scipy.fft import fft, fftfreq
import MainCode


class StatsDialog(QTableWidget):
    def __init__(self, data, ind_min, ind_max, t1, t2):
        super().__init__()
        self.data = data
        self.rows_names = data.columns
        self.rows_count = len(data.columns)
        self.ind_min = ind_min
        self.ind_max = ind_max
        self.t1 = t1
        self.t2 = t2
        self.tableWidget = QTableWidget()
        self.resize(650, 450)

        self.cols_names = ["Мин", "Макс", "Среднее", "СКО", "Дисперсия"]
        self.label = QLabel(self)
        self.label.setText(f"Статистические данные на отрезке: {self.t1} - {self.t2}")
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.addWidget(self.label)

        self.tableWidget.setColumnCount(6)

        __q_table_widget_item = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, __q_table_widget_item)

        __q_table_widget_item_1 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, __q_table_widget_item_1)

        __q_table_widget_item_2 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, __q_table_widget_item_2)

        __q_table_widget_item_3 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, __q_table_widget_item_3)

        __q_table_widget_item_4 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, __q_table_widget_item_4)

        __q_table_widget_item_5 = QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, __q_table_widget_item_5)

        self.tableWidget.setRowCount(self.rows_count)
        k = 0
        while k != self.rows_count:
            for i in self.rows_names:
                self.tableWidget.setItem(k, 0, QTableWidgetItem())
                self.tableWidget.item(k, 0).setText(i)
                k += 1

        mins = []
        maxs = []
        means = []
        stds = []
        vars_s = []
        for i in self.data:
            mins.append(np.round(np.min(self.data[i].values[self.ind_min:self.ind_max]), 6))
            maxs.append(np.round(np.max(self.data[i].values[self.ind_min:self.ind_max]), 6))
            means.append(np.round(np.mean(self.data[i].values[self.ind_min:self.ind_max]), 6))
            stds.append(np.round(np.std(self.data[i].values[self.ind_min:self.ind_max]), 6))
            vars_s.append(np.round(np.var(self.data[i].values[self.ind_min:self.ind_max]), 6))

        for i in range(self.rows_count):
            self.tableWidget.setItem(i, 1, QTableWidgetItem(str(mins[i])))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(str(maxs[i])))
            self.tableWidget.setItem(i, 3, QTableWidgetItem(str(means[i])))
            self.tableWidget.setItem(i, 4, QTableWidgetItem(str(stds[i])))
            self.tableWidget.setItem(i, 5, QTableWidgetItem(str(vars_s[i])))

        self.verticalLayout.addWidget(self.tableWidget)

        self.retranslate_ui(self)
        QMetaObject.connectSlotsByName(self)

    def retranslate_ui(self, dialog):
        dialog.setWindowTitle(QCoreApplication.translate("dialog", "Статистика", None))
        ___q_table_widget_item = self.tableWidget.horizontalHeaderItem(0)
        ___q_table_widget_item.setText(QCoreApplication.translate("dialog", "Параметры", None))

        ___q_table_widget_item_1 = self.tableWidget.horizontalHeaderItem(1)
        ___q_table_widget_item_1.setText(QCoreApplication.translate("dialog", "Мин", None))

        ___q_table_widget_item_2 = self.tableWidget.horizontalHeaderItem(2)
        ___q_table_widget_item_2.setText(QCoreApplication.translate("dialog", "Макс", None))

        ___q_table_widget_item_3 = self.tableWidget.horizontalHeaderItem(3)
        ___q_table_widget_item_3.setText(QCoreApplication.translate("dialog", "Мат. ожидание", None))

        ___q_table_widget_item_4 = self.tableWidget.horizontalHeaderItem(4)
        ___q_table_widget_item_4.setText(QCoreApplication.translate("dialog", "СКО", None))

        ___q_table_widget_item_5 = self.tableWidget.horizontalHeaderItem(5)
        ___q_table_widget_item_5.setText(QCoreApplication.translate("dialog", "Дисперсия", None))

    def keyPressEvent(self, event) -> None:
        super().keyPressEvent(event)
        if event.key() == Qt.Key.Key_C and (event.modifiers() & Qt.KeyboardModifier.ControlModifier):
            copied_cells = self.tableWidget.selectedIndexes()

            copy_text = f"Статистические данные в диапазоне: {self.t1} - {self.t2}\n"
            max_column = copied_cells[-1].column()
            for c in copied_cells:
                copy_text += self.tableWidget.item(c.row(), c.column()).text()
                if c.column() == max_column:
                    copy_text += '\n'
                else:
                    copy_text += '\t'

            QApplication.clipboard().setText(copy_text)


################################################################################
################################################################################

class GraphicShareX:
    stats_m: StatsDialog
    message: QMessageBox
    ind_min: int
    ind_max: int
    t1: float
    t2: float

    def __init__(self, args: list, width: int = 20, height: int = 12, dpi: int = 80,
                 file_name: str = "", graph_title: str = ""):
        self.parameter_qt = len(args)
        self.fig1, self.axes = plt.subplots(self.parameter_qt, 1, figsize=(width, height), sharex="all", dpi=dpi)
        self.fig1.subplots_adjust(left=0.045, bottom=0.1, right=0.83, top=0.95)

        self.data_to_plot = MainCode.data[args]
        self.x = MainCode.data["Time"].values
        self.yi = self.data_to_plot.columns

        colors = ["blue", "red", "green", "darkblue", "indigo", "crimson", "navy", "magenta", "maroon", "violet",
                  "fuchsia", "yellowgreen", "black", "orangered", "gold", "orchid", "yellow"]

        self.fig1.subplots_adjust(hspace=0.1)
        qt = 0
        self.colors_to_cursor = []
        while qt < self.parameter_qt:
            for y in self.yi[:self.parameter_qt:]:
                self.axes[qt].plot(self.x, self.data_to_plot[y].values, color=colors[qt])
                self.axes[qt].set_ylabel(y)
                self.axes[self.parameter_qt - 1].set_xlabel("Time [сек.]")
                self.axes[qt].set_xlim(xmin=0)
                self.axes[qt].axhline(y=0, color="black", linewidth=1)
                self.axes[qt].grid()
                self.axes[qt].yaxis.label.set_color(colors[qt])
                self.axes[qt].yaxis.label.set_rotation("horizontal")
                self.colors_to_cursor.append(colors[qt])
                qt += 1

        self.multi_cursor = MultiCursor(self.fig1.canvas, self.axes, useblit=True)
        b_data = args.copy()
        b_data.insert(0, "Time")
        self.data_to_cursor = [MainCode.data[i] for i in b_data]

        self.span = [SpanSelector(ax, self.onselect, "horizontal",
                                  drag_from_anywhere=True,
                                  props=dict(alpha=0.3, facecolor="tab:blue"),
                                  minspan=2, interactive=True, button=3) for ax in self.axes
                     ]

        self.fig1.canvas.mpl_connect('key_press_event', self.show_legend)

        plt.figtext(0.01, 0.01, "Значение под ползунком 'y'  |  Границы выделенного диапазона 't'  |  "
                                "Стат. данные на диапазоне Ctrl+Alt+t  |  "
                                "Удалить диапазон значений Ctrl+Alt+d  |  "
                                "Частотная область диапазона Ctrl+Alt+f")
        plt.get_current_fig_manager().set_window_title(file_name)
        title_to_graph = file_name.split("/")[-1]
        if graph_title:
            plt.suptitle(graph_title)
        else:
            plt.suptitle(title_to_graph)
        plt.plot()
        plt.show()

    def onselect(self, x_min, x_max):
        self.t1 = np.round(x_min, 2)
        self.t2 = np.round(x_max, 2)
        self.ind_min, self.ind_max = np.searchsorted(self.x, (x_min, x_max))
        self.ind_max = min(len(self.x) - 1, self.ind_max)
        self.table(ind_min=self.ind_min, ind_max=self.ind_max)

    def table(self, ind_min, ind_max):
        ys = []
        mins = []
        maxs = []
        means = []
        dat = self.data_to_cursor[1:]
        if ind_min == ind_max:
            pass
        else:
            for i, k in enumerate(dat):
                ys.append(k.name)
                minn = np.round(np.min(dat[i].values[ind_min:ind_max]), 5)
                mins.append(minn)
                maxx = np.round(np.max(dat[i].values[ind_min:ind_max]), 5)
                maxs.append(maxx)
                meann = np.round(np.std(dat[i].values[ind_min:ind_max]), 5)
                means.append(meann)
            columns = ("Мин", "Макс", "СКО")
            rows = ys
            cell_text = []
            col_widths = [0.05, 0.05, 0.05]
            b_box = (1.063, 1.8, 0.15, 0.4)
            if self.parameter_qt == 2:
                b_box = (1.063, 1.7, 0.15, 0.4)
            elif self.parameter_qt == 3:
                b_box = (1.063, 2.7, 0.15, 0.5)
            elif self.parameter_qt == 4:
                b_box = (1.063, 3.6, 0.15, 0.7)
            elif self.parameter_qt == 5:
                b_box = (1.063, 4.4, 0.15, 1)
            elif self.parameter_qt == 6:
                b_box = (1.063, 5.1, 0.15, 1.4)
            elif self.parameter_qt == 7:
                b_box = (1.063, 5.7, 0.15, 1.9)
            elif self.parameter_qt == 8:
                b_box = (1.063, 6.3, 0.15, 2.4)
            elif self.parameter_qt == 9:
                b_box = (1.063, 6.85, 0.15, 2.95)
            elif self.parameter_qt == 10:
                b_box = (1.063, 7.25, 0.15, 3.65)
            for i in range(len(ys)):
                cell_text.append([mins[i], maxs[i], means[i]])
            plt.table(cellText=cell_text,
                      cellLoc="center",
                      rowLabels=rows,
                      colLabels=columns,
                      colWidths=col_widths,
                      bbox=b_box,
                      )

    def show_legend(self, event):
        if event.key == "y":
            mouse_x_data = event.xdata

            if not type(mouse_x_data) == np.float_:
                pass
            else:
                closest_x_value, pos_closest_x_value = take_closest(self.data_to_cursor[0], mouse_x_data)

                i = 1
                for ax in self.axes:
                    y = self.data_to_cursor[i].name
                    edge_color = self.colors_to_cursor[i - 1]
                    data_legend = ax.text(1.0, 0.54, f"{y} = {self.data_to_cursor[i][pos_closest_x_value]}",
                                          fontsize=10, verticalalignment='top',
                                          bbox=dict(boxstyle='round', edgecolor=edge_color, facecolor='wheat', alpha=1),
                                          transform=ax.transAxes)
                    ax.draw_artist(data_legend)

                    i += 1
                    # это удаление необходимо, потому что в противном случае после изменения размера окна остается
                    # артефакт последней метки, которая лежит за новой
                    data_legend.remove()
                    self.fig1.canvas.update()
                text = f"T = {round(closest_x_value, 3)}"
                ax1 = self.axes[0]
                time_legend = ax1.text(1.095, 1.1, text, fontsize=10, verticalalignment='top',
                                       bbox=dict(facecolor='white', alpha=1),
                                       transform=ax1.transAxes)
                ax1.draw_artist(time_legend)
                time_legend.remove()
                self.fig1.canvas.update()

        elif event.key == "ctrl+alt+d" and self.ind_max:
            quest = QMessageBox()
            ok = quest.question(QMessageBox(), "", f"Удалить выбранный участок данных?", quest.Yes | quest.No)
            if ok == quest.Yes:
                data1 = MainCode.data
                data_tf = merge(left=data1.pop("Time"), right=data1.pop("__Формулы__"),
                                left_index=True, right_index=True)
                data1.drop(index=data1.loc[self.ind_min:self.ind_max].index, axis=0, inplace=True)
                data1.reset_index(inplace=True)
                data1.drop("index", axis=1, inplace=True)
                data1.insert(0, "Time", data_tf["Time"])
                data1.insert(len(data1.columns), "__Формулы__", data_tf["__Формулы__"])
                MainCode.data = data1
                self.fig1.canvas.draw()
                self.fig1.canvas.flush_events()
                self.message = QMessageBox()
                self.message.setWindowTitle("Удаление участка!")
                self.message.setWindowIcon(QIcon("logos/success_logo.png"))
                self.message.setText("Выбранный участок удалён! Чтобы это увидеть нужно отрисовать график заново! "
                                     "Вот так.\nЗаколебался думать как это сделать автоматически.\nПЕРЕД СЛЕДУЮЩИМ "
                                     "ОТРИСУЙТЕ ГРАФИК ЗАНОВО!")
                self.message.setFocusPolicy(Qt.StrongFocus)
                self.message.show()
            else:
                pass
        elif event.key == "ctrl+alt+f" and self.ind_max:
            qt = len(self.data_to_plot.columns)
            fig2, axes2 = plt.subplots(qt, 1, figsize=(15, 8), sharex="all")

            fig2.subplots_adjust(left=0.045, bottom=0.1, right=0.83, top=0.95)
            fig2.subplots_adjust(hspace=0.1)
            maxs = []
            q = 0
            while q < qt:
                for i in self.data_to_plot:
                    t = 1 / 128
                    x = self.data_to_plot[i].values[self.ind_min:self.ind_max]
                    n = len(x)
                    yf = fft(x)
                    xf = fftfreq(n, t)[:n//2]
                    yff = 2.0/n * np.abs(yf[0:n//2])
                    maxs.append(np.round(max(yff), 1))
                    axes2[q].plot(xf, yff)
                    axes2[q].set_ylabel(i)
                    axes2[q].grid()
                    q += 1
                axes2[-1].set_xlabel("Частота [Гц]")
            # plt.xticks(range(0, 45, 1))
            # plt.xlim(0, 45)
            plt.show()
            # nkv1 = int(np.mean(MainCode.data["Nкв1"].values[self.ind_min:self.ind_max]))
            # fkv = round(nkv1/60, 1)
            # fvv = round(fkv/2.43, 1)
            # text1 = f"Nкв1 = {nkv1} об./мин\n"  \
            #         f"fкв = {fkv} Гц - частота вращения коленвала\n" \
            #         f"fвв = {fvv} Гц - частота вращения винта воздушного"
            # v_lines_vals = [fkv, fvv, 0.5*fkv, 2*fvv]
            # v_lines_names = ["fкв", "fвв", "0.5*fкв", "2*fвв"]
            # for i, ax in enumerate(axes2):
            #     ax.vlines(x=v_lines_vals,ymin=[0 for _ in range(4)], ymax=[maxs[i] for _ in range(4)],
            #               colors=["red", "red", "red", "red"], label=["fkv", "fvv", "0.5*fkv", "2*fvv"])
            # ax1 = axes2[-1]
            # plt.text(0.0, -.22, text1, fontsize=10, verticalalignment='top',
            #                       bbox=dict(facecolor='white', alpha=1),
            #                       transform=ax1.transAxes)
            # trans = transforms.blended_transform_factory(
            #     ax1.transData, ax1.transAxes)
            # for v, n in zip(v_lines_vals, v_lines_names):
            #     plt.text(v, -.22, n, fontsize=10, verticalalignment='top',
            #              bbox=dict(facecolor='white', alpha=1), transform=trans
            #              )
        elif event.key == "t" and self.t1 and self.t2:
            text = f"T1 = {self.t1} | T2 = {self.t2}"
            ax = self.axes[0]
            time_legend = ax.text(1.09, 1.1, text, fontsize=10, verticalalignment='top',
                                  bbox=dict(facecolor='white', alpha=1),
                                  transform=ax.transAxes)
            ax.draw_artist(time_legend)
            time_legend.remove()
            self.fig1.canvas.update()
        elif event.key == "ctrl+alt+t":
            self.stats_m = StatsDialog(data=self.data_to_plot, t1=self.t1, t2=self.t2,
                                       ind_min=self.ind_min, ind_max=self.ind_max)
            self.stats_m.show()


class GraphicOneY:
    ind_min: int
    ind_max: int
    message: QMessageBox
    t1: float
    t2: float
    stats_m: StatsDialog

    def __init__(self, args: list, width: int = 20, height: int = 12, dpi: int = 80,
                 file_name: str = "", graph_title: str = ""):
        self.fig2, self.axe = plt.subplots(figsize=(width, height), dpi=dpi)
        self.fig2.subplots_adjust(left=0.03, bottom=0.1, right=0.85, top=0.95)

        self.data_to_plot = MainCode.data[args]
        self.x = MainCode.data["Time"].values
        self.yi = self.data_to_plot.columns

        self.line1, = self.axe.plot(self.x, self.data_to_plot[self.yi[0]].values, color="red", label=self.yi[0])
        self.line2, = self.axe.plot(self.x, self.data_to_plot[self.yi[1]].values, color="blue", label=self.yi[1])
        self.axe.set_xlabel("Time")
        first_legend = self.axe.legend(handles=[self.line1, self.line2], loc="upper right")

        self.axe.add_artist(first_legend)

        self.axes_cur = [self.line1, self.line2]

        self.axe.set_xlim(xmin=0)
        self.axe.grid()
        self.cursor = Cursor(self.axe, horizOn=False, useblit=True)

        b_data = args.copy()
        b_data.insert(0, "Time")
        self.data_to_cursor = [MainCode.data[i] for i in b_data]

        self.fig2.canvas.mpl_connect('key_press_event', self.show_legend)

        self.span = SpanSelector(self.axe, self.onselect, "horizontal", drag_from_anywhere=True,
                                 props=dict(alpha=0.3, facecolor="tab:blue"), button=3, minspan=1, interactive=True)

        plt.get_current_fig_manager().set_window_title(file_name)
        title_to_graph = file_name.split("/")[-1]
        if graph_title:
            plt.title(graph_title)
        else:
            plt.title(title_to_graph)
        plt.show()

    """"Функия для SpanSelector"""

    def onselect(self, x_min, x_max):
        self.t1 = np.round(x_min, 2)
        self.t2 = np.round(x_max, 2)
        self.ind_min, ind_max = np.searchsorted(self.x, (x_min, x_max))
        self.ind_max = min(len(self.x) - 1, ind_max)
        self.table(ind_min=self.ind_min, ind_max=self.ind_max)

    def table(self, ind_min, ind_max):
        y1 = self.data_to_cursor[1].name
        y2 = self.data_to_cursor[2].name
        columns = ("Мин", "Макс", "СКО")
        if ind_min == ind_max:
            pass
        else:
            min1 = np.round(np.min(self.data_to_cursor[1][ind_min:ind_max].values), 6)
            max1 = np.round(np.max(self.data_to_cursor[1][ind_min:ind_max].values), 6)
            mean1 = np.round(np.std(self.data_to_cursor[1][ind_min:ind_max].values), 6)
            min2 = np.round(np.min(self.data_to_cursor[2][ind_min:ind_max].values), 6)
            max2 = np.round(np.max(self.data_to_cursor[2][ind_min:ind_max].values), 6)
            mean2 = np.round(np.std(self.data_to_cursor[2][ind_min:ind_max].values), 6)
            rows = [y1, y2]
            cell_text = [[min1, max1, mean1], [min2, max2, mean2]]
            col_widths = [0.05, 0.05, 0.05]
            plt.table(cellText=cell_text,
                      cellLoc="center",
                      rowLabels=rows,
                      colLabels=columns,
                      loc="bottom right",
                      colWidths=col_widths,
                      bbox=(1.05, 0.9, 0.13, 0.15)
                      )

    def show_legend(self, event):
        if event.key == "y":
            mouse_xd_ata = event.xdata

            if not type(mouse_xd_ata) == np.float_:
                pass
            else:
                closest_x_value, pos_closest_x_value = take_closest(self.data_to_cursor[0], mouse_xd_ata)
                y1 = self.data_to_cursor[1].name
                y2 = self.data_to_cursor[2].name

                data_legend_1 = self.axe.text(1.01, 0.60, f"{y1} = {self.data_to_cursor[1][pos_closest_x_value]}",
                                              fontsize=10, verticalalignment='top',
                                              bbox=dict(boxstyle='round', edgecolor='red', facecolor='wheat', alpha=1),
                                              transform=self.axe.transAxes)
                data_legend_2 = self.axe.text(1.01, 0.55, f"{y2} = {self.data_to_cursor[2][pos_closest_x_value]}",
                                              fontsize=10, verticalalignment='top',
                                              bbox=dict(boxstyle='round', edgecolor='blue', facecolor='wheat', alpha=1),
                                              transform=self.axe.transAxes)
                self.axe.draw_artist(data_legend_1)
                self.axe.draw_artist(data_legend_2)

                data_legend_1.remove()
                data_legend_2.remove()

                self.fig2.canvas.update()
        elif event.key == "ctrl+alt+d" and self.ind_max:
            quest = QMessageBox()
            ok = quest.question(QMessageBox(), "", f"Удалить выбранный участок данных?", quest.Yes | quest.No)
            if ok == quest.Yes:
                data1 = MainCode.data
                data_tf = merge(left=data1.pop("Time"), right=data1.pop("__Формулы__"),
                                left_index=True, right_index=True)
                data1.drop(index=data1.loc[self.ind_min:self.ind_max].index, axis=0, inplace=True)
                data1.reset_index(inplace=True)
                data1.drop("index", axis=1, inplace=True)
                data1.insert(0, "Time", data_tf["Time"].values)
                data1.insert(len(data1.columns), "__Формулы__", data_tf["__Формулы__"].values)
                MainCode.data = data1
                self.message = QMessageBox()
                self.message.setWindowTitle("Удаление участка!")
                self.message.setWindowIcon(QIcon("logos/success_logo.png"))
                self.message.setText("Выбранный участок удалён! Чтобы это увидеть нужно нарисовать график заново! "
                                     "Вот так.\nЗаколебался думать как это сделать автоматически.")
                self.message.setFocusPolicy(Qt.StrongFocus)
                self.message.show()
            else:
                pass
        elif event.key == "ctrl+alt+f" and self.ind_max:
            qt = len(self.data_to_plot.columns)
            fig2, axes2 = plt.subplots(qt, 1, figsize=(15, 8), sharex="all")
            fig2.subplots_adjust(hspace=0.1)
            q = 0
            while q < qt:
                for i in self.data_to_plot:
                    t = 1 / 128
                    x = self.data_to_plot[i].values[self.ind_min:self.ind_max]
                    n = len(x)
                    yf = fft(x)
                    xf = fftfreq(n, t)[:n//2]
                    axes2[q].plot(xf,  2.0/n * np.abs(yf[0:n//2]))
                    axes2[q].set_ylabel(i)
                    axes2[q].grid()
                    axes2[qt-1].set_xlabel("Частота [Гц]")
                    q += 1
            plt.show()
        elif event.key == "ctrl+alt+t":
            self.stats_m = StatsDialog(data=self.data_to_plot, t1=self.t1, t2=self.t2,
                                       ind_min=self.ind_min, ind_max=self.ind_max)
            self.stats_m.show()


class GraphicParamByParam:
    def __init__(self, args: list, width: int = 20, height: int = 12, dpi: int = 80,
                 file_name: str = "", graph_title: str = ""):
        fig3, axe = plt.subplots(figsize=(width, height), dpi=dpi)

        x_label = args[0]
        y_label = args[1]
        x = MainCode.data[x_label].values
        y = MainCode.data[y_label].values

        axe.plot(x, y, ".", color="black")
        axe.set(xlabel=x_label, ylabel=y_label)

        axe.grid()
        plt.get_current_fig_manager().set_window_title(file_name)
        plt.title(graph_title)
        plt.show()


def take_closest(my_list, my_number):
    pos = bisect_left(my_list, my_number)
    if pos == 0:
        return my_list[0]
    if pos == len(my_list):
        return my_list[-1]
    before = my_list[pos - 1]
    after = my_list[pos]
    if after - my_number < my_number - before:
        return after, pos
    else:
        return before, pos - 1
