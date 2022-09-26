import pandas as pd
import numpy as np
import polars as pl

"""глобальная переменная DataFrame, в которой хранятся все переменные"""
data = pd.DataFrame()
file_name_g = ""


class Files:
    """просто открывается файл csv или txt и запихивается в DataFrame"""
    @staticmethod
    def open_file(file):
        global data
        global file_name_g
        if not file:
            pass
        else:
            data_polar = pl.read_csv(file, sep=";", encoding="utf-8")
            file_name_g = file[:-5]
            data = data_polar.to_pandas()
        return data, file_name_g

    @staticmethod
    def import_txt_file(file: str, ex_file_name: str = "New", coding: str = "utf-8",
                        sep: bool = False, delimiter: str = ";"):
        if not file:
            return False
        else:
            try:
                data_imported = pd.DataFrame(dtype="float")
                if sep:
                    data_before = pd.read_csv(file, sep="\s+", encoding=coding)
                    f = np.full(len(data_before), "no formula")
                    formulas = pd.DataFrame({"__Формулы__": f})
                    data_imported = pd.concat([data_before, formulas], axis=1)

                elif not sep:
                    data_before = pd.read_csv(file, delimiter=delimiter, encoding=coding)
                    f = np.full(len(data_before), "no formula")
                    formulas = pd.DataFrame({"__Формулы__": f})
                    data_imported = pd.concat([data_before, formulas], axis=1)
                data_imported.to_csv(ex_file_name, index=False, sep=";", encoding="utf-8")
                return True
            except ValueError:
                return False

    @staticmethod
    def save():
        if file_name_g:
            data_polar = pl.from_pandas(data)
            data_polar.write_csv(f"{file_name_g}.grad", sep=";")
        else:
            pass

    @staticmethod
    def save_as(file_name):
        global data
        if file_name == "":
            pass
        else:
            data_polar = pl.from_pandas(data)
            data_polar.write_csv(file_name, sep=";")

    """Объединение данных в формате .txt"""
    @staticmethod
    def concat_txt_data(files: list, how: str, ex_file_name: str = "New", coding: str = "utf-8",
                        sep: bool = True, delimiter: str = ";"):
        if not files:
            return False
        else:
            try:
                data_concated = pd.DataFrame()
                if how == "Последовательно":
                    if sep:
                        df_files = [pd.read_table(file, sep="\s+", encoding=coding) for file in files]
                        data_concated = pd.concat(df_files, ignore_index=True)

                    else:
                        df_files = [pd.read_csv(file, delimiter=delimiter, encoding=coding) for file in files]
                        data_concated = pd.concat(df_files, ignore_index=True)

                elif how == "Параллельно":
                    if sep:
                        df_files = [pd.read_table(file, sep="\s+", encoding=coding) for file in files]
                        data_concated = pd.concat(df_files, axis=1)
                    else:
                        df_files = [pd.read_csv(file, delimiter=delimiter, encoding=coding) for file in files]
                        data_concated = pd.concat(df_files, axis=1)

                elif how == "Одиночные":
                    data_concated = pd.DataFrame(dtype="float")
                    for file_name in files:
                        with open(file_name) as f:
                            data_concated[file_name.split("/")[-1][0:-4]] = pd.read_csv(f)
                data_to_save = pl.from_pandas(data_concated)
                data_to_save.write_csv(ex_file_name, sep=";")
                return True
            except ValueError:
                return False

    """Функция для сдвига запаздывающих параметров"""

    @staticmethod
    def shift_analog(parameters_names, dots):
        if parameters_names:
            len_of_data = len(data)
            for name in parameters_names:
                shifted_param = data[name].values[dots:len_of_data]
                val = data[name].values[-1]
                d_to_append = np.array([val for _ in range(dots)])
                data.loc[:, name] = np.concatenate((shifted_param, d_to_append), axis=None)
            return True
        else:
            return False

    @staticmethod
    def export(parameters_names: list, file_name: str, t0: int = 0, t1: int = len(data)):
        try:
            pd_data_to_export = pd.DataFrame(data=data[t0:t1], columns=parameters_names)
            pl_data_to_export = pl.from_pandas(pd_data_to_export)
            pl_data_to_export.write_csv(file_name, sep=";")
            return True
        except Exception:
            return False

class Parameters:
    """Добавляем параметр в DataFrame, если добавляемый параметр называется "Time" или "time",
    то в начало DataFrame добавляется параметр, с названием "Time"
    если называется по-другому, то в конец добавляется параметр, который заполняется единицами"""
    @staticmethod
    def add_parameter(input_name: str, freq: int = 1):
        parameter_name = input_name
        len_of_data = len(data)
        if parameter_name in data.columns or parameter_name == "":
            pass
            return False
        elif parameter_name == "Time":
            dd = [i / 1000 + j for j in range(1, int(len_of_data / freq + 1)) for i in range(freq)]
            div = len_of_data - len(dd)
            if div != 0 or div < 0:
                dd.extend([i / 1000 + j for j in range(int(dd[-1]), int(dd[-1] + abs(div))) for i in range(freq)])
            data.insert(0, "Time", dd[:len_of_data])
            return True
        else:
            param = np.ones(len_of_data)
            index = len(data.columns)-1
            data.insert(index, parameter_name, param)
            return True

    """Просто удаляем выбранный параметр"""
    @staticmethod
    def delete_parameters(parameters_names: list, indexes):
        try:
            if parameters_names:
                df = data.pop("__Формулы__")
                for parameter_name in parameters_names:
                    if parameter_name not in data.columns:
                        pass
                    else:
                        data.drop(parameter_name, axis=1, inplace=True)
                df.drop(labels=indexes, inplace=True)
                dt = pd.DataFrame(df)
                dt.reset_index(inplace=True)
                dt.drop("index", axis=1, inplace=True)
                d_to_app = pd.Series(np.full(len(parameters_names), "no formula"), name="__Формулы__")
                dt = pd.concat([dt["__Формулы__"], d_to_app], ignore_index=True)
                data.insert(len(data.columns), "__Формулы__", dt.values)
            else:
                pass
            return True
        except Exception:
            return False

    """Копируем столбцы в конец DataFrame и добавляем к названию "_copy" """
    @staticmethod
    def copy_parameters(parameters_names: list):
        try:
            for parameter_name in parameters_names:
                index = len(data.columns) - 1
                form_index = data.columns.get_loc(parameter_name)
                data.insert(index, f"{parameter_name}_copy", data[parameter_name].values)
                data.loc[index, "__Формулы__"] = data.loc[form_index, "__Формулы__"]
            return True
        except Exception:
            return False

    """Копируем столбцы в конец DataFrame и добавляем к названию "_0" """
    @staticmethod
    def add_zero_parameters(parameters_names: list):
        try:
            index = len(data.columns) - 1
            len_of_data = len(data)
            for parameter_name in parameters_names:
                data.insert(index, f"{parameter_name}_0", np.ones(len_of_data))
            return True
        except Exception:
            return False
    """Копируем столбцы в конец DataFrame и добавляем к названию "_h" """
    @staticmethod
    def add_h_parameters(parameters_names: list):
        try:
            index = len(data.columns) - 1
            len_of_data = len(data)
            for parameter_name in parameters_names:
                data.insert(index, f"{parameter_name}_h", np.ones(len_of_data))
                Parameters.add_formula(f"{parameter_name}_h", f"{parameter_name} - {parameter_name}_0")
            return True
        except Exception:
            return False

    """Переименовываем параметр"""
    @staticmethod
    def rename_parameter(name: str, new_name: str):
        if new_name in data.columns:
            return False
        else:
            data.rename(columns={name: new_name}, inplace=True)
            return True

    """Проверка на флоат"""
    @staticmethod
    def is_float(element) -> bool:
        try:
            float(element)
            return True
        except ValueError:
            return False

    """В столбец "__Формулы__" по соответствующему параметру(parameter_name) индексу(index) 
    записывается формула(formula), по которой рассчитывается значение этого параметра"""
    @staticmethod
    def add_formula(parameter_name: str, formula: str):
        try:
            index = data.columns.get_loc(parameter_name)
            data.loc[index, "__Формулы__"] = formula
            len_of_data = len(data)
            if formula == "no formula":
                pass
            elif formula.isdigit() or Parameters.is_float(formula):
                data.loc[:, parameter_name] = np.full(len_of_data, float(formula))
            elif formula.startswith("data.loc[:,"):
                for i in formula.split(";"):
                    a = compile(i, "", "exec")
                    exec(a)
            else:
                data.loc[:, parameter_name] = data.eval(formula)
            return True
        except Exception:
            return False

    """Значения параметров рассчитываются по соответсвующим формулам"""
    @staticmethod
    def accept_formulas():
        len_of_data = len(data)
        formulas_data = data["__Формулы__"].values[:len(data.columns):]
        error_index = 0
        try:
            for index, formula in np.ndenumerate(formulas_data):
                name = data.columns[index[0]]
                if formula == "no formula":
                    pass
                elif formula.isdigit() or Parameters.is_float(formula):
                    data.loc[:, name] = np.full(len_of_data, float(formula))
                elif formula.startswith("data.loc[:,"):
                    for i in formula.split(";"):
                        a = compile(i, "", "exec")
                        exec(a)
                else:
                    data.loc[:, name] = data.eval(formula)
                error_index += 1
            return True, True
        except Exception:
            return False, data.columns[error_index]


class Methods:
    """Функция для расчета градуировочного коэффициента
    при расчёте оного с использованием только одного тензомоста (метод прямой градуировки) с помощью МНК"""
    @staticmethod
    def linear_regression(tenzo_parameter: str, f_parameter: str, t0: int, t1: int):
        try:
            print("im trying")
            x = data[tenzo_parameter].values[t0:t1]
            y = data[f_parameter].values[t0:t1]
            lin = np.polyfit(x=x, y=y, deg=1)
            return True, lin
        except Exception:
            return False, False
            pass

    """Функция для расчета градуировочного коэффициента
    при расчёте оного с использованием нескольких тензомостов (метод обратной градуировки)"""
    @staticmethod
    def multi_regression(f_parameter: str, tenzo_parameters: list, t0: int, t1: int):
        try:
            x = []
            for i in tenzo_parameters:
                x.append(data[i].values[t0:t1])
            y = data[f_parameter].values[t0:t1]

            x = np.transpose(x)
            x = np.c_[x, np.ones(x.shape[0])]

            multi_reg = np.linalg.lstsq(x, y, rcond=None)[0]
            answer = multi_reg.tolist()
            return True, answer
        except Exception:
            return False, False
            pass
