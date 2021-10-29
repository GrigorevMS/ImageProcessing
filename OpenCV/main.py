import cv2 as cv
import os
import numpy as np


'''

Фотографии должны распологаться в папке data.
Папка data должна распологаться в одной дирректории со скриптом программы.

'''

# Функции фильтров
#__________________________________________________#


# Функция обнаружения повреждений
#__________________________________________________#


def CalcOfDamageAndNonDamage(image_name):

    global H_l_1
    global H_h_1
    global S_l_1
    global S_h_1
    global V_l_1
    global V_h_1
    global K_size

    image = cv.imread(image_name)

    # Применяем размытие(с ним перестает работать, поэтому размытие не применяется)
    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (10, 10))
    #image_erode = cv.erode(image, kernel)
    image_erode = image

    # Переходм в цветовое пространство HSV
    hsv_img = cv.cvtColor(image_erode, cv.COLOR_BGR2HSV)

    #leafs_area_BGR = cv.watershed(image_erode, markers)

    # С помощью порогового фильтра выделяем здоровую часть листа(параметры на ползунках)
    healthy_part = cv.inRange(hsv_img, (H_l_1, S_l_1, V_l_1), (H_h_1, S_h_1, V_h_1))

    # С помощью порогового фильтра выделяем больную часть листа(параметры на ползунках)
    ill_part = cv.inRange(hsv_img, (H_l_2, S_l_2, V_l_2) ,(H_h_2, S_h_2, V_h_2))

    cv.imshow("healthy_part", healthy_part)
    cv.imshow("ill_part", ill_part)

    # Складываем здоровую и больную части и получаем примерный контур листа. Применяем "открытие"
    leafs_area = cv.add(healthy_part, ill_part)
    leafs_area = cv.dilate(leafs_area, kernel)

    cv.imshow("leafs_area", leafs_area)

    # На сонове примерного контура листа строим маркеры для watershed(фон - 255, больная часть - 60б здоровая - 30)
    markers = np.zeros((image.shape[0], image.shape[1]), dtype = "int32")
    markers[leafs_area == 0] = 255
    markers[healthy_part > 0] = 30
    markers[ill_part > 0] = 60

    # Применяем watershed. Получаем расширенные маркеры
    markers_watershed = cv.watershed(image_erode, markers)

    # Строим итоговое изображение
    mask = np.zeros_like(image, np.uint8)
    mask[markers_watershed == 30] = (255, 0 ,80)
    mask[markers_watershed == 60] = (0, 0, 255)

    return(mask)



# Функции интерфейса
#__________________________________________________#


def Mouse_Callback(event, x, y, flags, data):
    global H_l_1
    global H_h_1
    global S_l_1
    global S_h_1
    global V_l_1
    global V_h_1

    global H_l_2
    global H_h_2
    global S_l_2
    global S_h_2
    global V_l_2
    global V_h_2

    global H_1
    global S_1
    global V_1

    global H_2
    global S_2
    global V_2

    global img

    image = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    if flags == 1:
        px = image[x, y]

        H_2.append(int(px[0]))
        S_2.append(int(px[1]))
        V_2.append(int(px[2]))

        H_l_2 = min(H_2)
        H_h_2 = max(H_2)
        S_l_2 = min(S_2)
        S_h_2 = max(S_2)
        V_l_2 = min(V_2)
        V_h_2 = max(V_2)

        cv.setTrackbarPos("hue_low_2", "settings", H_l_2)
        cv.setTrackbarPos("hue_high_2", "settings", H_h_2)
        cv.setTrackbarPos("sat_low_2", "settings", S_l_2)
        cv.setTrackbarPos("sat_high_2", "settings", S_h_2)
        cv.setTrackbarPos("val_low_2", "settings", V_l_2)
        cv.setTrackbarPos("val_high_2", "settings", V_h_2)
    elif flags == 2:
        px = image[x, y]
        
        H_1.append(int(px[0]))
        S_1.append(int(px[1]))
        V_1.append(int(px[2]))

        H_l_1 = min(H_1)
        H_h_1 = max(H_1)
        S_l_1 = min(S_1)
        S_h_1 = max(S_1)
        V_l_1 = min(V_1)
        V_h_1 = max(V_1)
        
        cv.setTrackbarPos("hue_low_1", "settings", H_l_1)
        cv.setTrackbarPos("hue_high_1", "settings", H_h_1)
        cv.setTrackbarPos("sat_low_1", "settings", S_l_1)
        cv.setTrackbarPos("sat_high_1", "settings", S_h_1)
        cv.setTrackbarPos("val_low_1", "settings", V_l_1)
        cv.setTrackbarPos("val_high_1", "settings", V_h_1)


def File_Callback(x):
    print("You now chose file ", x)

def Hue_low_1_Callback(x):
    global H_l_1
    global H_h_1
    H_l_1 = x
    H_l_1 = min(H_l_1, H_h_1)
    cv.setTrackbarPos("hue_low_1", "settings", H_l_1)

def Hue_high_1_Callback(x):
    global H_l_1
    global H_h_1
    H_h_1 = x
    H_h_1 = max(H_h_1, H_l_1)
    cv.setTrackbarPos("hue_high_1", "settings", H_h_1)

def Sat_low_1_Callback(x):
    global S_l_1
    global S_h_1
    S_l_1 = x
    S_l_1 = min(S_l_1, S_h_1)
    cv.setTrackbarPos("sat_low_1", "settings", S_l_1)

def Sat_high_1_Callback(x):
    global S_l_1
    global S_h_1
    S_h_1 = x
    S_h_1 = max(S_h_1, S_l_1)
    cv.setTrackbarPos("sat_high_1", "settings", S_h_1)

def Val_low_1_Callback(x):
    global V_l_1
    global V_h_1
    V_l_1 = x
    V_l_1 = min(V_l_1, V_h_1)
    cv.setTrackbarPos("val_low_1", "settings", V_l_1)

def Val_high_1_Callback(x):
    global V_l_1
    global V_h_1
    V_h_1 = x
    V_h_1 = max(V_h_1, V_l_1)
    cv.setTrackbarPos("val_high_1", "settings", V_h_1)


def Hue_low_2_Callback(x):
    global H_l_2
    global H_h_2
    H_l_2 = x
    H_l_2 = min(H_l_2, H_h_2)
    cv.setTrackbarPos("hue_low_2", "settings", H_l_2)

def Hue_high_2_Callback(x):
    global H_l_2
    global H_h_2
    H_h_2 = x
    H_h_2 = max(H_h_2, H_l_2)
    cv.setTrackbarPos("hue_high_2", "settings", H_h_2)

def Sat_low_2_Callback(x):
    global S_l_2
    global S_h_2
    S_l_2 = x
    S_l_2 = min(S_l_2, S_h_2)
    cv.setTrackbarPos("sat_low_2", "settings", S_l_2)

def Sat_high_2_Callback(x):
    global S_l_2
    global S_h_2
    S_h_2 = x
    S_h_2 = max(S_h_2, S_l_2)
    cv.setTrackbarPos("sat_high_2", "settings", S_h_2)

def Val_low_2_Callback(x):
    global V_l_2
    global V_h_2
    V_l_2 = x
    V_l_2 = min(V_l_2, V_h_2)
    cv.setTrackbarPos("val_low_2", "settings", V_l_2)

def Val_high_2_Callback(x):
    global V_l_2
    global V_h_2
    V_h_2 = x
    V_h_2 = max(V_h_2, V_l_2)
    cv.setTrackbarPos("val_high_2", "settings", V_h_2)

def PrevFile():
    now = cv.getTrackbarPos("file", "settings")
    if now > 0:
        cv.setTrackbarPos("file", "settings", now - 1)

def NextFile(DataList):
    now = cv.getTrackbarPos("file", "settings")
    if now < len(DataList) - 1:
        cv.setTrackbarPos("file", "settings", now + 1)



# main
#__________________________________________________#

'''Подготовка'''

HomeDir = os.getcwd()   # Путь корневой папки
DataDir = HomeDir + "/data" # Путь папки data

os.chdir(DataDir)

DataList = os.listdir() #Список файлов в папке data

H_l_1 = 40
H_h_1 = 100
S_l_1 = 22
S_h_1 = 244
V_l_1 = 33
V_h_1 = 250

H_1 = [40, 100]
S_1 = [22, 244]
V_1 = [33, 250]

H_l_2 = 4
H_h_2 = 23
S_l_2 = 56
S_h_2 = 140
V_l_2 = 110
V_h_2 = 201

H_2 = [4, 23]
S_2 = [56, 140]
V_2 = [110, 201]


'''Создаем окна настроек и управления, показа изображений'''

cv.namedWindow("settings")
cv.resizeWindow("settings", 1500, 850)

cv.namedWindow("image", cv.WINDOW_AUTOSIZE)

cv.namedWindow("result", cv.WINDOW_AUTOSIZE)

cv.setMouseCallback("image", Mouse_Callback)


'''Создаем трекбары управления'''

cv.createTrackbar("file", "settings", 0, len(DataList) - 1, File_Callback)

cv.createTrackbar("hue_low_1", "settings", 0, 179, Hue_low_1_Callback)
cv.createTrackbar("hue_high_1", "settings", 0, 179, Hue_high_1_Callback)
cv.createTrackbar("sat_low_1", "settings", 0, 255, Sat_low_1_Callback)
cv.createTrackbar("sat_high_1", "settings", 0, 255, Sat_high_1_Callback)
cv.createTrackbar("val_low_1", "settings", 0, 255, Val_low_1_Callback)
cv.createTrackbar("val_high_1", "settings", 0, 255, Val_high_1_Callback)

cv.setTrackbarPos("hue_low_1", "settings", H_l_1)
cv.setTrackbarPos("hue_high_1", "settings", H_h_1)
cv.setTrackbarPos("sat_low_1", "settings", S_l_1)
cv.setTrackbarPos("sat_high_1", "settings", S_h_1)
cv.setTrackbarPos("val_low_1", "settings", V_l_1)
cv.setTrackbarPos("val_high_1", "settings", V_h_1)


cv.createTrackbar("hue_low_2", "settings", 0, 179, Hue_low_2_Callback)
cv.createTrackbar("hue_high_2", "settings", 0, 179, Hue_high_2_Callback)
cv.createTrackbar("sat_low_2", "settings", 0, 255, Sat_low_2_Callback)
cv.createTrackbar("sat_high_2", "settings", 0, 255, Sat_high_2_Callback)
cv.createTrackbar("val_low_2", "settings", 0, 255, Val_low_2_Callback)
cv.createTrackbar("val_high_2", "settings", 0, 255, Val_high_2_Callback)

cv.setTrackbarPos("hue_low_2", "settings", H_l_2)
cv.setTrackbarPos("hue_high_2", "settings", H_h_2)
cv.setTrackbarPos("sat_low_2", "settings", S_l_2)
cv.setTrackbarPos("sat_high_2", "settings", S_h_2)
cv.setTrackbarPos("val_low_2", "settings", V_l_2)
cv.setTrackbarPos("val_high_2", "settings", V_h_2)


img = 0

f = open("settings.txt", "w")

'''Основной блок'''

while(1):
    k = cv.waitKey(5)
    if k == 27 or k == ord("q"):
        cv.destroyAllWindows()
        break
    elif k == ord("a"):
        PrevFile()
    elif k == ord("d"):
        NextFile(DataList)
    elif k == ord("e"):
        H_1 = [40, 100]
        S_1 = [22, 244]
        V_1 = [33, 250]

        H_l_1 = min(H_1)
        H_h_1 = max(H_1)
        S_l_1 = min(S_1)
        S_h_1 = max(S_1)
        V_l_1 = min(V_1)
        V_h_1 = max(V_1)
        
        cv.setTrackbarPos("hue_low_1", "settings", H_l_1)
        cv.setTrackbarPos("hue_high_1", "settings", H_h_1)
        cv.setTrackbarPos("sat_low_1", "settings", S_l_1)
        cv.setTrackbarPos("sat_high_1", "settings", S_h_1)
        cv.setTrackbarPos("val_low_1", "settings", V_l_1)
        cv.setTrackbarPos("val_high_1", "settings", V_h_1)

        H_2 = [4, 23]
        S_2 = [56, 140]
        V_2 = [110, 201]

        H_l_2 = min(H_2)
        H_h_2 = max(H_2)
        S_l_2 = min(S_2)
        S_h_2 = max(S_2)
        V_l_2 = min(V_2)
        V_h_2 = max(V_2)

        cv.setTrackbarPos("hue_low_2", "settings", H_l_2)
        cv.setTrackbarPos("hue_high_2", "settings", H_h_2)
        cv.setTrackbarPos("sat_low_2", "settings", S_l_2)
        cv.setTrackbarPos("sat_high_2", "settings", S_h_2)
        cv.setTrackbarPos("val_low_2", "settings", V_l_2)
        cv.setTrackbarPos("val_high_2", "settings", V_h_2)


    file_num = cv.getTrackbarPos("file", "settings")
    img = cv.imread(DataList[file_num])
    result = CalcOfDamageAndNonDamage(DataList[file_num])
    cv.imshow("image", img)
    cv.imshow("result", result)

os.chdir(HomeDir)

f = open("settings.txt", 'w')

f.write("H_l_1 = " + str(H_l_1) + "\n")
f.write("H_h_1 = " + str(H_h_1) + "\n")
f.write("S_l_1 = " + str(S_l_1) + "\n")
f.write("S_h_1 = " + str(S_h_1) + "\n")
f.write("V_l_1 = " + str(V_l_1) + "\n")
f.write("V_h_1 = " + str(V_h_1) + "\n" + "\n")

f.write("H_l_2 = " + str(H_l_2) + "\n")
f.write("H_h_2 = " + str(H_h_2) + "\n")
f.write("S_l_2 = " + str(S_l_2) + "\n")
f.write("S_h_2 = " + str(S_h_2) + "\n")
f.write("V_l_2 = " + str(V_l_2) + "\n")
f.write("V_h_2 = " + str(V_h_2) + "\n")

f.close()