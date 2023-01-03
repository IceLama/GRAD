# GRAD
ENG
This program is intended for processing field calibration data and flight data.
But, use it however you want, if you can.


I File


1. Import.

   Any text file in the form of a table is suitable for import.
   Files are imported through the appropriate window: File → Import. The Import window opens.
   Next, you need to specify the parameters of the imported file: delimiter; encoding. To select a file to import, click the "Select a file to import" button. Then, when the file appears in the window, select it and click "Import". You can only import one file at a time.
   The result of the import will appear in a pop-up window. Ready!
   The imported file is no different from a regular text file, despite the ".grad" extension. Just a column with the name "__Formulas__" is added to the end of the table, all entered formulas will be written to this column in the future. A file with the ".grad" extension can be opened with regular notepad.


2. Export.

   Data is exported through the corresponding window: File → Export. The Export window will open.
   Next, you need to select the data to export. To do this, select the required parameters in the left list, then click on "Add selected parameters", after which they will appear in the right list. Or add parameters by double-clicking the mouse button. Then you need to select the range for export, if the entire file is exported, then the required value has already been entered in the appropriate field. Next, you need to click the "Export" button, in the pop-up window you need to specify the name for the output file, as well as the extension (.grad, .txt, .csv).
   The result of the import will appear in a pop-up window. Ready!
   Regardless of which extension is selected, the output file will be encoded "utf-8", delimited by ";", decimal delimited by ".".


3. Combine files.

   Files are merged through the appropriate window: File → Merge files. The Gluing window opens.
   Next, you need to select the parameters of the input files: delimiter; encoding; glue method. All input files must be in the same directory and have the same parameters. To select files for gluing, click on the "Select files for gluing" button. In the window that opens, select the required files. Then they will appear in the "Glue" window. Then you need to select the files to merge and click "Combine". In the pop-up window, specify the name for the final file and the extension (.txt, .csv, .grad).
   The result of merging files will appear in a pop-up window. Ready!
   Separately, it is worth mentioning the gluing method "Single". This method is intended for merging files, where each parameter is written as a separate text file. The program will collect all the selected files in one table, where the names of the columns will be the names of the files corresponding to them. Well suited for data, after processing by the TNWorks program, which just produces such files.



II Options


1. Formulas.

   This is the main window for working with data. The window is a table of two columns, in the left column - the names of the parameters, in the right - the formula corresponding to this parameter. If the right column says "no formula" - this does not mean that the parameter is empty, most likely it means that this is the original (untouched) data.
   Buttons:
      - Add a parameter: a parameter is added to the data (at the end of the data), the values of which are filled with units, you can use the "Insert" key;
      - Delete parameter: everything is clear, only you need to select the parameter(s), for deletion, you can use the "Delete" key;
      - Rename: everything is clear, you just need to select the parameter, or you can double-click on the parameter name;
      - Add a formula: you can use the button (after selecting the parameter), you can double-click in the corresponding line in the "Formula" column → a window will open in which you can specify both a prime number and a formula as a parameter value
  options:
  1) just a number;
  2) other parameter;
  3) simple formula: A1 + (-*/) A2 (A1 and A2 are other parameters)
trigonometric functions cos(), sin(), etc. (in radians);
  4) logical formulas: in the lower left corner there is a button, when clicked, an example of a logical formula will appear. Example:
data.loc[:, 'A1'] = np.where((data['Time'] > 0) & (data['Time'] <= data['t1']), 10 data['A1'] );
      data.loc[:, 'A1'] = np.where((data['Time'] > data['t1']) & (data['Time'] <= data['t2']), 5 data ['A1']);
  This logical formula assumes that there are parameters A1, Time, t1, t2 in the data and means that the parameter A1 is 10 when the Time parameter is greater than 0 and less than or equal to t1, and equal to 5 when Time is greater than t1 and less than or equal to t2. Instead of 10 and 5, there may be other parameters or formulas. The difference from a simple formula is that here the parameter names must be specified exactly like this: data[‘parameter name’], and trigonometric functions like: np.cos(), np.sin(), etc.
Also, in the window for adding a formula on the right there is a list with all available parameters, double-clicking on a parameter in this list will insert this parameter into the formula where the cursor is. The entered formula or value is not saved unless the window is closed by pressing the "Ok" button.
       - Create a copy: a complete copy of the parameter with data is created, "_copy" is added to the end of the parameter name, several parameters can be used at once;
       - Create a copy with _0: a copy of the parameter is created, "_0" is added to the end of the name, and the values are filled with units, several parameters can be used at once;
       - Create a copy with _h: a copy of the parameter is created, "_h" is added to the end of the name and a formula is inserted (example: A1 = A1_h - A1_0), several parameters can be used at once;
       - Copy to clipboard: selected columns of the table are copied to the clipboard (Ctrl+C);
   Notes:
    a) All operations are irreversible, i.e. If you delete a setting, it cannot be restored.
    b) The entered formula recalculates the parameter values, after recalculating the values, it is impossible to return the previous values. Therefore: DO NOT ADD FORMULA TO INITIAL PARAMETERS!
        If you need to cancel the change (deleting the desired parameter, recalculating the parameter values), the only way out is to close the program without saving, then all the changes made will not be saved and you can do everything again.


2. Table of parameters.

   This window displays the values of the parameters, whether they are raw data or calculated by formulas. There is no way to change the data (enter a different value or delete a value).
   Buttons:
       - Check data for gaps: The data is checked for missing values. Missing values in the table are denoted by "nan" or "None". The result of the check is a pop-up window that displays which parameters have gaps and how many of them. If all values are omitted in the parameter, or if the values have different data types, then "Game" will be written opposite the name of this parameter.
       - Fill in the gaps: The "Interpolation" window will open. You need to choose an interpolation method that will fill in the gaps in the data. If the "Polynomial" method is selected, you must specify the degree of the polynomial. After clicking on the "Interpolate" button, a pop-up window will appear with the result of the execution.
   ATTENTION! IT IS HIGHLY NOT RECOMMENDED TO KEEP THIS WINDOW OPEN WHEN CHANGES ARE MADE WITH THE NUMBER OF PARAMETERS (DELETED, NEW ADDED) IN THE "FORMULAS" WINDOW, THE PROGRAM MAY SIMPLY FLY OUT.


3. Shift parameters.

   In this window, you can shift some parameters relative to other parameters.
   To do this, select the parameters necessary for the shift, specify the number of shift points and click the "Shift" button. After that, a pop-up window will appear with the results of the operation. The selected parameters will be shifted back relative to the other parameters by the specified number of points. To be more precise: the first few (the specified number of points) values will be deleted from the selected parameters, the next value after these points will become the first value, and the missing values ​​at the end of the parameter (so that all parameters are of the same length) will be filled with the last value of this parameter.
   After the shift, you need to open "Formulas" and click "OK", after that the new values will be saved.
   This operation is necessary after data processing by the TNWorks program, after which the analog signals "lag" relative to the discrete signals (Arinc, ...).



III Graphs


1. Graphs by time.

   Window for drawing graphs, as the name implies, graphs are drawn in time. Accordingly, to draw graphs, it is necessary that the data contains a parameter called "Time". If there is no such parameter in the source data, it should be added: Parameters → Formulas → Add parameter → name the parameter "Time" → a pop-up window will appear (this window appears only when entering the name of the new parameter "Time"), in which you need to specify the frequency of registration → Ready!
  The right list displays all the parameters from which you need to select the parameters for rendering. You can select the required parameters, then click the "Add selected parameters" button, or add them by double-clicking the mouse button.
   Buttons:
       - Graphs with different y-axes: One canvas will display graphs of parameters, each of which will have a y-axis and one x-axis. At least 2 parameters must be selected, a maximum of 10 is recommended (because if there are more, then nothing is visible, plus a table that appears with statistical data (about it below) is calculated for a maximum of 10 parameters). After pressing the button, a pop-up window will appear where you can enter a name for the canvas, if you do not write anything, then the file name will be written with the name of the canvas.
- Graph with one Y axis: ONLY 2 parameters. On one canvas, 2 graphs with common X and Y axes will be displayed. Necessary for visual comparison of parameters. If the parameter values differ greatly, then the scale will be selected for large values. After pressing the button, a pop-up window will appear where you can enter a name for the canvas, if you do not write anything, then the file name will be written with the name of the canvas.
   Possibilities:
     - managing the display of charts (scale, color, etc.) is done using the buttons in the upper left corner;
     - to see the values of the parameters under the blue slider, you need to press "y" (in the English layout);
     - to set the checkbox with the value under the blue slider, you need to press the key combination "Ctrl + y", then press the right mouse button;
     - to select a segment on the charts, you need to hold down the right mouse button, the selected segment will turn turquoise, and a table with statistical data of parameters on the selected range will appear in the upper right corner;
     - to see the borders, ie. start and end time of the selected range, you need to press the "t" button;
     - if you hold down the key combination "Ctrl + Alt + t", then a window will pop up with the statistical data of the parameters on the selected range;
     - the key combination "Ctrl+Alt+d" is designed to delete the values of the selected range, when you press this combination, a confirmation window for deleting values will appear, then a window with the result of the deletion will appear, ATTENTION THE GRAPH IS NOT AUTOMATICALLY RENDERED, SO IT IS HIGHLY RECOMMENDED TO DRAW IT AGAIN AFTER EVERY DELETE ;
     - if you hold down the key combination "Ctrl+Alt+f", a window will appear with graphs of parameters in the selected range in the frequency domain;
   Note:
    Sometimes it happens that the blue slider does not appear. I don't know why this is happening. For the slider to appear, you need to reselect the parameters for the graph and draw it.



2. Graph by parameter.

   Window for drawing the graph parameter by parameter. In the left list, you need to select the parameter for the X axis, in the right list for the Y axis.
   Of the possibilities, only basic features: control of the display of the graph (scale).



IV Processing


1. Linear regression.

   The window is intended for regression analysis. The last step in determining the calibration coefficients. The calculation is carried out according to the readings of one strain gauge, suitable for calculating the coefficients of bending moments.
   To determine the calibration coefficients, it is necessary to select: in the left list is the calculated moment, in the right list is the tensor parameter. Specify the range for analysis, if the calculation is carried out over the entire data range, then the required value is already indicated. And click on the "Calculate" button. After that, upon successful completion of the calculation, an equation with coefficients will appear in the lower part of the window.


2. Multiple regression.
  
   The same as linear regression, only the calculation of the coefficients is carried out according to the readings of several (most often 2) strain bridges, suitable for calculating the coefficients of the torques. At least 2 tensor parameters are selected in the right list. After a successful calculation, calibration coefficients will appear in the lower part of the window.


V Help

1. Help
   You are reading it.




-----------------------------------------------------------------------------------------------------------------
RU
	Данная программа предназначена для обработки данных натурных градуировок и полётных данных.
	А впрочем, пользуйтесь как хотите, если сможете.  
				
				
				I Файл  


1. Импорт.

  Для импорта подходит любой текстовый файл в виде таблицы. 
  Импорт файлов производится через соответствующее окно: Файл → Импорт. Откроется окно "Импорт".
  Далее необходимо указать параметры импортируемого файла: разделитель; кодировка. Для выбора файла на импорт нажать кнопку "Выбрать файл для импорта". Затем, когда файл появится в окошке, выделить его и нажать "Импортировать". За раз можно импортировать только один файл.
  Результат импорта появится всплывающим окошком. Готово!
  Импортированный файл ничем не отличается от обычного текстового файла, несмотря на расширение ".grad". Просто в конец таблицы добавляется столбец с названием "__Формулы__", в этот столбец в дальнейшем будут записываться все введенные формулы. Файл с расширением ".grad" можно открыть обычным блокнотом.


2. Экспорт.

  Экспорт данных производится через соответствующее окно: Файл → Экспорт. Откроется окно "Экспорт".
  Далее необходимо выбрать данные для экспорта. Для этого нужно выбрать необходимые параметры в левом списке, затем нажать на "Добавить выбранные параметры", после чего они окажутся в правом списке. Или добавлять параметры двойным кликом кнопкой мыши. Затем нужно выбрать диапазон для экспорта, если экспортируется весь файл, то необходимое значение уже введено в соответствующее поле. Далее нужно нажать кнопку "Экспортировать", во всплывшем окне нужно указать название для выходного файла, а также расширение (.grad, .txt, .csv).
  Результат импорта появится всплывающим окошком. Готово!
  Независимо от того какое выбрано расширение, выходной файл будет в кодировке "utf-8", разделителем ";", десятичным разделителем ".".   


3. Объединить файлы.

  Объединение файлов производится через соответствующее окно: Файл → Объединить файлы. Откроется окно "Склеивание".
  Далее необходимо выбрать параметры входных файлов: разделитель; кодировка; метод "склеивания". Все входные файлы должны находиться в одной директории и иметь одинаковые параметры. Для выбора файлов для склеивания необходимо нажать на кнопку "Выбрать файлы для склейки". В открывшемся окне выбрать необходимые файлы. После чего они появятся в окне "Склеивание". Затем нужно выделить объединяемые файлы и нажать "Собрать воедино". Во всплывшем окне указать название для итогового файла и расширение (.txt, .csv, .grad).
  Результат склеивания файлов появится всплывающим окошком. Готово!
  Отдельно стоит упомянуть метод склеивания "Одиночные". Этот метод предназначен для склеивания файлов, где каждый параметр записан как отдельный текстовый файл. Программа соберет все выбранные файлы в одну таблицу, где названиями колонок будут соответствующие им названия файлов. Хорошо подходит для данных, после обработки программой TNWorks, которая как раз и выдает такие файлы.  



				II Параметры   


1. Формулы.

  Это основное окно для работы с данными. Окно представляет собой таблицу из двух столбцов, в левом столбце - названия параметров, в правом - соответствующая этому параметру формула. Если в правом столбце написано "no formula" - это не означает, что параметр пустой, скорее всего, это значит, что это исходные (нетронутые) данные.
  Кнопки:
     - Добавить параметр: в данные (в конец данных) добавляется параметр, значения которого заполняются единицами, можно клавишей "Insert";
     - Удалить параметр: все понятно, только нужно выделить параметр(ы), для удаления, можно клавишей "Delete";
     - Переименовать: все понятно, только нужно выделить параметр, или можно двойным кликом по названию параметра;
     - Добавить формулу: можно через кнопку (предварительно выделив параметр), можно двойным кликом в соответствующей строке в столбце "Формула" → откроется окно, в котором можно указать значением параметра как простое число, так и формулу
 	варианты:
 	    1) просто число;
 	    2) другой параметр;
 	    3) простая формула: А1 +(-*/) А2 (А1 и А2 - другие параметры) 
	        тригонометрические функции cos(), sin() и т.д. (в радианах);
 	    4) логические формулы: в левом нижнем углу есть кнопка, при нажатии на которую появится образец логической формулы. 	Пример:
	data.loc[:, 'А1'] = np.where((data['Time'] > 0) & (data['Time'] <= data['t1']), 10 data['А1']);
     	data.loc[:, 'А1'] = np.where((data['Time'] > data['t1']) & (data['Time'] <= data['t2']), 5 data['А1']);
 	Данная логическая формула предполагает, что в данных есть параметры А1, Time, t1, t2 и означает, что параметр А1 равен 10, когда параметр Time больше 0 и меньше или равно t1, и, равен 5, когда Time больше t1 и меньше или равно t2. Вместо 10 и 5 могут быть другие параметры или формулы. Отличия от простой формулы в том, что здесь названия параметров нужно указывать именно так: data[‘название параметра’], а тригонометрические функции как: np.cos(), np.sin() и т.д.
	Также, в окне добавления формулы справа есть список со всеми имеющимися параметрами, двойной клик по параметру в этом списке вставит этот параметр в формулу туд, где стоит курсор. Введенная формула или значение не сохраняются, если не закрыть окно нажатием кнопки "Ok".
      - Создать копию: создается полная копия параметра с данными, в конец названия параметра приписывается "_copy", можно несколько параметров разом;
      - Создать копию с _0: создается копия параметра, в конец названия приписывается "_0", а значения заполняются единицами, можно несколько параметров разом;
      - Создать копию с _h: создается копия параметра, в конец названия приписывается "_h" и вставляется формула (пример: А1 = А1_h - А1_0), можно несколько параметров разом;
      - Копировать в буфер: выделенные колонки таблицы копируются в буфер обмена (Ctrl+C);
  Примечания:
   а) Все операции необратимые, т.е. если удалить какой-то параметр, его нельзя будет восстановить. 
   б) Введенная формула пересчитывает значения параметра, после пересчета значений, нельзя вернуть предыдущие значения. Поэтому: НЕ ДОБАВЛЯТЬ ФОРМУЛЫ В ИСХОДНЫЕ ПАРАМЕТРЫ!
       Если же нужно отменить изменение (удаление нужного параметра, пересчет значений параметра) единственный выход - это закрыть программу без сохранения, тогда все произведенные изменения не сохранятся и можно будет все сделать заново.


2. Таблица параметров.

  В этом окне отображаются значения параметров, будь то исходные данные или рассчитанные по формулам. Здесь нет возможности изменить данные (вписать другое значение или удалить значение). 
  Кнопки:
      - Проверить данные на пропуски: Данные проверяются на пропущенные значения. Пропущенные значения в таблице обозначаются "nan" или "None". Результат проверки - всплывающее окошко, в котором отображается у каких параметров есть пропуски и сколько их. Если в параметре пропущены все значения или значения имеют разные типы данных, то напротив названия этого параметра будет написано "Дичь".
      - Заполнить пропуски: Откроется окно "Интерполяция". Нужно выбрать метод интерполяции, которым заполнятся пропуски в данных. В случае, если выбран метод "Полиномиальная", необходимо указать степень полинома. После нажатия на кнопку "Интерполировать" появится всплывающее окошко результатом выполнения.
  ВНИМАНИЕ! КРАЙНЕ НЕ РЕКОМЕНДУЕТСЯ ДЕРЖАТЬ ОТКРЫТЫМ ЭТО ОКНО, КОГДА ПРОИЗВОДЯТСЯ ИЗМЕНЕНИЯ С КОЛИЧЕСТВОМ ПАРАМЕТРОВ (УДАЛЯЮТСЯ, ДОБАВЛЯЮТСЯ НОВЫЕ) В ОКНЕ "ФОРМУЛЫ", ПРОГРАММА МОЖЕТ ПРОСТО ВЫЛЕТЕТЬ	.


3. Сдвиг параметров.

  В данном окне можно осуществить сдвиг некоторых параметров относительно других параметров.
  Для этого нужно выделить необходимые для сдвига параметры, указать количество точек сдвига и нажать кнопку "Сдвинуть". После появится всплывающее окошко с результатами операции. Выбранные параметры будут сдвинуты назад относительно остальных параметров на указанное количество точек. А точнее: у выбранных параметров удалятся первые сколько-то (указанное количество точек) значений, следующее значение после этих точек станет первым значением, а недостающие значения в конце параметра (чтобы все параметры были одной длины) заполнятся последним значением этого параметра.
  После сдвига нужно открыть "Формулы" и нажать "Ок", после этого новые значения сохранятся.
  Эта операция необходима после обработки данных программой TNWorks, после которой аналоговые сигналы "запаздывают" относительно дискретных сигналов (Arinc, ...). 



				III Графики


1. Графики по времени.

  Окно для отрисовки графиков, как понятно по названию, графики отрисовываются по времени. Соответственно, для отрисовки графиков необходимо, чтобы в данных был параметр с названием "Time". Если такого параметра нет в исходных данных, его следует добавить: Параметры → Формулы → Добавить параметр → назвать параметр "Time" → появится всплывающее окошко (такое окошко появляется только при вводе названием нового параметра "Time"), в котором нужно указать частоту регистрации → Готово! 
 В правом списке отображены все параметры, откуда нужно выбрать параметры для отрисовки. Можно выделить необходимые параметры, затем нажать кнопку "Добавить выбранные параметры", или же добавлять их двойным кликом кнопки мыши. 
  Кнопки:
      - Графики с разными осями Y: На одном полотне отобразятся графики параметров, у каждого из которых будут оси Y и одна ось X. Минимум необходимо выбрать 2 параметра, максимум рекомендуется 10 (потому что если их больше, то ничерта не видно, плюс появляющаяся таблица со статистическими данными (о ней ниже) рассчитана максимум на 10 параметров). После нажатия на кнопку появится всплывающее окошко где можно ввести название для полотна, если ничего не написать, то названием полотна запишется название файла.
      - График с одной осью Y: ТОЛЬКО 2 параметра. На одном полотне отобразятся 2 графика с общими осями X и Y. Необходимо для визуального сравнения параметров. Если значения параметров отличаются сильно, то масштаб будет подобран под большие значения. После нажатия на кнопку появится всплывающее окошко где можно ввести название для полотна, если ничего не написать, то названием полотна запишется название файла.
  Возможности:
    - управление отображением графиков (масштаб, цвет и т.д.) производится кнопками в левом верхнем углу;
    - чтобы посмотреть значения параметров под голубым ползунком, нужно нажать "y" (в англ. раскладке);
    - чтобы установить флажок со значением под голубым ползунком, нужно нажать комбинацию клавиш "Ctrl+y", затем нажать правую кнопку мыши;
    - чтобы выделить отрезок на графиках, нужно зажать правую кнопку мыши, выделенный отрезок окрасится бирюзовым цветом, а в правом верхнем углу появится таблица со статистическими данными параметров на выделенном диапазоне;
    - чтобы посмотреть границы, т.е. начальный и конечным момент времени, выделенного диапазона, нужно нажать кнопку "t";
    - если зажать комбинацию клавиш "Ctrl+Alt+t", то всплывет окно со статистическими данными параметров на выделенном диапазоне;
    - комбинация клавиш "Ctrl+Alt+d" предназначена для удаления значений выбранного диапазона, при нажатии этой комбинации появится окошко подтверждения удаления значений, затем появится окошко с результатом удаления, ВНИМАНИЕ ГРАФИК НЕ ПЕРЕРИСОВЫВАЕТСЯ АВТОМАТИЧЕСКИ, ТАК ЧТО КРАЙНЕ РЕКОМЕНДУЕТСЯ ОТРИСОВЫВАТЬ ЕГО ЗАНОВО ПОСЛЕ КАЖДОГО УДАЛЕНИЯ;
    - если зажать комбинацию клавиш "Ctrl+Alt+f", появится окно с графиками параметров в выделенном диапазоне в частотной области;
  Примечание:
   Иногда бывает такое, что голубой ползунок не появляется. Я не знаю почему так происходит. Чтобы ползунок появился, нужно заново выбрать параметры для графика и отрисовать его.



2. График по параметру.

  Окно для отрисовки графика параметр по параметру. В левом списке нужно выделить параметр для оси X, в правом списке для оси Y.
  Из возможностей только базовые возможности: управление отображением графика (масштаб).



				IV Обработка


1. Линейная регрессия.

  Окно предназначено для проведения регрессионного анализа. Последний этап в определении градуировочных коэффициентов. Расчет проводится по показаниям одного тензомоста, подходит для расчет коэффициентов моментов изгиба.
  Для определения градуировочных коэффициентов необходимо выделить:  в левом списке рассчитанный момент, в правом тензо-параметр. Указать диапазон для анализа, если расчет проводится по всему диапазону данных, то необходимое значение уже указано. И нажать на кнопку "Рассчитать". После чего, при успешном выполнении расчета, в нижней части окна появится уравнение с коэффициентами.


2. Множественная регрессия.
  
  То же, что и линейная регрессия, только расчет коэффициентов проводится по показаниям нескольких (чаще всего 2) тензомостов, подходит для расчета коэффициентов моментов кручения. В правом списке выбирается минимум 2 тензо-параметра. После успешного расчета в нижней части окна появятся градуировочные коэффициенты.


				V Справка

1. Справка
  Вы ее читаете.
