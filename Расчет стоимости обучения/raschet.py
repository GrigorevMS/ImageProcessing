def Separator(string, sep): # Разделяет строку по заданному символу, возвращает массив
    mas = []
    pos = 0
    size = len(string)
    while pos < size:
        buf = ""
        while pos < size and string[pos] != sep:
            buf += string[pos]
            pos += 1
        if buf != '\n':
            mas.append(buf)
        while pos < size and ( string[pos] == sep or string[pos] == ' ' ):
            pos += 1
    return mas

def TableOut(head, mas): # Выводит таблицу с учебным планом
    num_column = len(mas)
    num_line = len(mas[0])
    print("%-60s | %s | %s | %s | %s |" % ( head[0],
                                       head[1].center(25),
                                       head[2].center(25),
                                       head[3].center(25),
                                       head[4].center(25)))
    print('-' * 174)
    for i in range(num_line):
        print("%-60s | %s | %s | %s | %s |" % ( mas[0][i],
                                               str(mas[1][i]).center(25),
                                               str(mas[2][i]).center(25),
                                               str(mas[3][i]).center(25),
                                               str(mas[4][i]).center(25)))
    print('-' * 174)

def SummPari(num, lct, prk, lab): # Считает общее число пар
    mas = []
    for i in range(num):
        mas.append((lct[i] + prk[i] + lab[i]) / 2)
    return mas
file = open("plan.txt", "r")

def CostPari(num, mas_pari): # Считает стомость пары
    mas = []
    for i in range(num):
        mas.append()

head = Separator(file.readline(), '|') # Шапка с названиями столбоцов считанной таблицы
num = int(file.readline()) # Количество строк в таблице(количество предметов)
mas_name = [] # Массив хранящий колонку названий предметов
mas_lct = [] # Массив хранящий количество лекционных часов
mas_prk = [] # Массив хранящий количество практических часов
mas_lab = [] # Массив хранящий количество лабораторных часов
mas_sem = [] # Массив хранящий количество семестров выделяемых на предмет

for i in range(num):
    buf = Separator(file.readline(), '|')
    mas_name.append(str(buf[0]))
    mas_lct.append(int(buf[1]))
    mas_prk.append(int(buf[2]))
    mas_lab.append(int(buf[3]))
    mas_sem.append(int(buf[4]))
mas = [mas_name, mas_lct, mas_prk, mas_lab, mas_sem] # Массив хранящий сводную таблицу учебного плана

# Выведем учебный план
print("# Выведем учебный план")
TableOut(head, mas)
print()

# Подсчитаем количество пар по каждому предмету
print("# Подсчитаем количество пар по каждому предмету")
mas_pari = SummPari(num, mas_lct, mas_prk, mas_lab)
print("mas_pari", mas_pari)
print()

# Подсчитаем количество пар в семестре
print("# Подсчитаем количество пар в семестре")
mas_parzasem = []
for i in range(num):
    mas_parzasem.append(mas_pari[i] // mas_sem[i])
print("mas_parzasem", mas_parzasem)
print()

# Зададим среднее количевто недель в семестре
print("# Зададим среднее количевто недель в семестре")
weeks = round(5 * (30 + 31) / 2 / 7)
print("weeks", weeks)
print()

# Посчитаем среднее количество пар в неделю по каждому предмету
print("# Посчитаем среднее количество пар в неделю по каждому предмету")
mas_parzaned = []
for i in range(num):
    mas_parzaned.append(mas_parzasem[i] / weeks)
print("mas_parzaned", mas_parzaned)
print()

# Зададим среднюю зарплату
print("# Зададим среднюю зарплату")
avrg_sal = 76970 * 0.7 * 0.87
print("avrg_sal", avrg_sal)
print()

# Посчитаем среднее количество пар в неделю
print("# Посчитаем среднее количество пар в неделю")
avrg_zaned = sum(mas_parzaned) / 8
print("avrg_zaned", avrg_zaned)
print()

# Посчитаем среднюю стоимость одной пары
print("# Посчитаем среднюю стоимость одной пары")
avrg_costzaparu = avrg_sal / (10 * (30 + 31) / 2 / 7)
print("avrg_costzaparu", avrg_costzaparu)
print()

# Посчитаем среднюю стоимость одной недели
print("# Посчитаем среднюю стоимость одной недели")
avrg_cost = avrg_zaned * avrg_costzaparu
print("avrg_cost", avrg_cost)
print()

# Посчитаем средние затраты на семестр
print("# Посчитаем средние затраты ")
avrg_zasem = avrg_cost * weeks
print("avrg_zasem", avrg_zasem)
print()

# Зададим количество учеников в группе
print("# Зададим количество учеников в группе")
kolvo_studentov = 22
print("kolvo_studentov", kolvo_studentov)
print()

# Зададим коэфицент инфляции
print("# Зададим коэфицент инфляции")
inf = 1.07
print("inf", inf)
print()

# Посчитаем стоимость семестра с учетом инфляции
print("# Посчитаем стоимость семестра с учетом инфляции")
cost_zasem = avrg_zasem + (avrg_zasem * inf) + (avrg_zasem * inf * inf) + (avrg_zasem * inf * inf * inf)
cost_zasem = cost_zasem / 4
print("cost_zasem", cost_zasem)
print()

# Посчитаем затраты на двух бухгалтеров, расходы на 1С, системного администратора
print("# Посчитаем затраты на двух бухгалтеров, расходы на 1С, системного администратора")
cost_dop = ((31923 / 0.87 / 0.7) + (33137 / 0.87 / 0.7)) * 6 + 14400 * 2
print("cost_dop", cost_dop)
print()

# Посчитаем затраты на двух методистов
print("# Посчитаем затраты на двух методистов")
cost_met = (30000 / 0.87 / 0.7) * 2 * 6
print("cost_met", cost_met)
print()

# Расчитаем амортизацию компьютеров
print("# Расчитаем амортизацию компьютеров")
cost_pc = ((80000 * 0.04) * 6) * (avrg_zaned + 3)
print("cost_pc", cost_pc)
print()

# Расчитаем затраты на электроенергию для ПК
print("# Расчитаем затраты на электроенергию для ПК")
cost_elpc = 8 * (avrg_zaned + 3) * 6 * weeks * 5
print("cost_elpc", cost_elpc)
print()

# Расчитаем стоимость семестра в онлайн университете
print("# Расчитаем стоимость семестра в онлайн университете")
cost_onlinesem = (cost_zasem + cost_dop + cost_met + cost_pc + cost_elpc) / kolvo_studentov
print("cost_onlinesem", cost_onlinesem)
print()

file.close()
