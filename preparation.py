#подготовка ингридиентов

#функции
def d_and_t(JD): #перевод даты
    JDN = int(JD)
    a = JDN + 32044
    b = (4 * a + 3) // 146097
    c = a - (146097 * b) // 4
    d = (4 * c + 3) // 1461
    e = c - 1461 * d // 4
    m = (5 * e + 2) // 153
    day = e + 1 - (153 * m + 2) // 5
    month = m + 3 - 12 * (m // 10)
    year = 100 * b + d - 4800 + m // 10
    JT = JD - JDN
    hour = int(JT * 24)
    min = int((JT * 24 - hour) * 60)
    sec = round(((JT * 24 - hour) * 60 - min) * 60)
    hour += 12
    if hour > 24:
        hour -= 24
        day += 1
    if len(str(hour)) == 1:
        hour = f'0{str(hour)}'
    if len(str(min)) == 1:
        min = f'0{str(min)}'
    if len(str(sec)) == 1:
        sec = f'0{str(sec)}'
    if len(str(day)) == 1:
        day = f'0{str(day)}'
    if len(str(month)) == 1:
        month = f'0{str(month)}'
    d_and_t = f'{day}.{month}.{year} {hour}:{min}:{sec}'
    return d_and_t

def objects_filters(name, list_with_data):  #список фильтров для определённого объекта
    filters = []
    for i in range(len(list_with_data)):
        if list_with_data[i][0] == name and list_with_data[i][2] not in filters:
            filters.append(list_with_data[i][2])
    return filters

#обработка ингридиентов

gh = open('tsk.txt')
stars = gh.read().splitlines() #список строк
gh.close()

for i in range(len(stars)): #список списков, где каждый список - строка
    stars[i] = stars[i].split()
    print(stars)

stars[0] = ['Object', 'HJD, 24', 'Filter', 'Magnitude'] #первая строка

while [] in stars:
    stars.remove([]) #удаление пустых мест

#исправление имен звёзд
#имена с пробелом
for i in range(1, len(stars)):
    if len(stars[i]) > 4:
        stars[i][0] = stars[i][0].upper() + '_' + stars[i][1].capitalize()
        del stars[i][1]
#имена без _
for i in range(1, len(stars)):
    if '_' not in stars[i][0]:
        stars[i][0] = stars[i][0][:2].upper() + '_' + stars[i][0][2:].capitalize()


#исправление имён фильтров:
for i in range(1, len(stars)):
    if stars[i][2][0].islower() == True:
        stars[i][2] = stars[i][2].capitalize()

#исправление чисел
for i in range(1, len(stars)):
    stars[i][1] = '24' + stars[i][1]
    stars[i][1] = float(stars[i][1]) #изменение типа данных

#приступим к основному блюду

#списочек имен объектов
names = []
for i in range(1, len(stars)):
    if stars[i][0] not in names:
        names.append(stars[i][0])

print('names of objects')
for i in range(len(names)):
   print(names[i])
#print()

for i in range(len(names)):
    print(f'Объект  {names[i]} имеется в фильтрах:')
    our_filters = objects_filters(names[i], stars)
    print(*our_filters)
    #print()

#сортировочка дат по возрастанию
JDL = []
for i in range(1, len(stars)):
    JDL.append(stars[i][1])

JDL.sort()
JDL.insert(0, 'JD, 24') #вставка элемента по индексу

s_list_with_data = [0] * len(stars)
s_list_with_data[0] = stars[0]

for i in range(1, len(JDL)):
    for j in range(1, len(stars)):
        if JDL[i] == stars[j][1]:
            s_list_with_data[i] = stars[j]
            continue

#обращение к конкретному объекту
star_name = input('Имя объекта:')

starl = []
for i in range(1, len(s_list_with_data)):
    if s_list_with_data[i][0] == star_name:
        starl.append(s_list_with_data[i])

#конкретные фильтры
all_filters = objects_filters(star_name, starl)
fltrs = input('Названия фильтров (через пробел):').split()

#финишная прямая перед десертом

prefinish_list = [] #для данной звезды с данными фильтрами
for i in range(len(starl)):
    if starl[i][2] in fltrs:
        prefinish_list.append(starl[i])

#даты
date = []
for i in range(len(prefinish_list)):
    usual_date = d_and_t(prefinish_list[i][1])
    date.append(usual_date)

for i in range(len(prefinish_list)):
    n = len(str(prefinish_list[i][1]))
    if n != 13:
        prefinish_list[i][1] = str(prefinish_list[i][1]) + '0' * (13 - n)
    prefinish_list[i][1] = str(prefinish_list[i][1])[2:]

#добавление даты в общий список
for i in range(len(prefinish_list)):
    prefinish_list[i].insert(0, date[i])

#сортировка по фильтрам
n_of_fltrs = len(fltrs)
final_list = []
for i in range(n_of_fltrs):
    cor_fltrs = []
    for j in range(1, len(prefinish_list)):
        if prefinish_list[j][3] == fltrs[i]:
            cor_fltrs.append(prefinish_list[j])
    final_list.extend(cor_fltrs)  #добавление значений в конец списка
print(final_list)

dessert = open(f'{star_name}.data', 'w')
dessert.write('Date\t\t\t\t\tJD, 24...  \t Magnitude \t Filter\n')
for i in range(len(final_list)):
    dessert.write(f'{final_list[i][0]}\t\t{final_list[i][2]}\t\t{final_list[i][4]}\t\t{final_list[i][3]}\n')
dessert.close()

