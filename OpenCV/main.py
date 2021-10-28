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

    global H_l
    global H_h
    global S_l
    global S_h
    global V_l
    global V_h
    global K_size

    image = cv.imread(image_name)

    kernel = cv.getStructuringElement(cv.MORPH_ELLIPSE, (K_size, K_size))
    image_erode = cv.erode(image, kernel)

    #image_erode = cv.bilateralFilter(img, 15, 75, 75)

    #cv.imshow("erode", image_erode)
    #cv.waitKey()

    hsv_img = cv.cvtColor(image_erode, cv.COLOR_BGR2HSV)
    #hsv_img = cv.cvtColor(image_erode, cv.COLOR_BGR2GRAY)

    #cv.imshow("hsv", hsv_img)
    #cv.waitKey()

    markers = np.zeros((image.shape[0], image.shape[1]), dtype = "int32")
    markers[90:140, 90:140] = 255
    markers[236:255, 0:20] = 1
    markers[0:20, 0:20] = 1
    markers[0:20, 236:255] = 1
    markers[236:255, 236:255] = 1

    leafs_area_BGR = cv.watershed(image_erode, markers)

    healthy_part = cv.inRange(hsv_img, (H_l, S_l, V_l), (H_h, S_h, V_h))
    #healthy_part = cv.inRange(hsv_img, (100), (255))

    #healthy_part = cv.dilate(healthy_part, kernel)

    cv.imshow("healthy_part", healthy_part)

    ill_part = leafs_area_BGR - healthy_part

    mask = np.zeros_like(image, np.uint8)

    mask[leafs_area_BGR > 1] = (255, 0 ,80)

    mask[ill_part > 1] = (0, 0, 255)

    return(mask)



# Функции интерфейса
#__________________________________________________#


def Mouse_Callback(event, x, y, flags, data):
     if flags == 1:
         print("kek")

def File_Callback(x):
    print("You now chose file ", x)

def Hue_low_Callback(x):
    global H_l
    global H_h
    H_l = x
    H_l = min(H_l, H_h)
    cv.setTrackbarPos("hue_low", "settings", H_l)

def Hue_high_Callback(x):
    global H_l
    global H_h
    H_h = x
    H_h = max(H_h, H_l)
    cv.setTrackbarPos("hue_high", "settings", H_h)

def Sat_low_Callback(x):
    global S_l
    global S_h
    S_l = x
    S_l = min(S_l, S_h)
    cv.setTrackbarPos("sat_low", "settings", S_l)

def Sat_high_Callback(x):
    global S_l
    global S_h
    S_h = x
    S_h = max(S_h, S_l)
    cv.setTrackbarPos("sat_high", "settings", S_h)

def Val_low_Callback(x):
    global V_l
    global V_h
    V_l = x
    V_l = min(V_l, V_h)
    cv.setTrackbarPos("val_low", "settings", V_l)

def Val_high_Callback(x):
    global V_l
    global V_h
    V_h = x
    V_h = max(V_h, V_l)
    cv.setTrackbarPos("val_high", "settings", V_h)

def K_size_Callback(x):
    global K_size
    if x < 3:
        x = 3
    K_size = x
    cv.setTrackbarPos("k_size", "settings", K_size)

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

H_l = 36
H_h = 86
S_l = 25
S_h = 255
V_l = 25
V_h = 255
K_size = 7


'''Создаем окна настроек и управления, показа изображений'''

cv.namedWindow("settings", cv.WINDOW_FULLSCREEN)
#cv.resizeWindow("settings", 1500, 450)

cv.namedWindow("image", cv.WINDOW_AUTOSIZE)

cv.namedWindow("result", cv.WINDOW_AUTOSIZE)

cv.setMouseCallback("image", Mouse_Callback)


'''Создаем трекбары управления'''

cv.createTrackbar("file", "settings", 0, len(DataList) - 1, File_Callback)

cv.createTrackbar("hue_low", "settings", 0, 179, Hue_low_Callback)

cv.createTrackbar("hue_high", "settings", 0, 179, Hue_high_Callback)

cv.createTrackbar("sat_low", "settings", 0, 179, Sat_low_Callback)

cv.createTrackbar("sat_high", "settings", 0, 179, Sat_high_Callback)

cv.createTrackbar("val_low", "settings", 0, 179, Val_low_Callback)

cv.createTrackbar("val_high", "settings", 0, 179, Val_high_Callback)

cv.createTrackbar("k_size", "settings", 0, 100, K_size_Callback)
#cv.setTrackbarMin("k_size", "settings", 100)
#cv.setTrackbarMax("k_size", "settings", 100)

cv.setTrackbarPos("hue_low", "settings", H_l)
cv.setTrackbarPos("hue_high", "settings", H_h)
cv.setTrackbarPos("sat_low", "settings", S_l)
cv.setTrackbarPos("sat_high", "settings", S_h)
cv.setTrackbarPos("val_low", "settings", V_l)
cv.setTrackbarPos("val_high", "settings", V_h)
cv.setTrackbarPos("k_size", "settings", K_size)




'''Основной блок'''

while(1):
    k = cv.waitKey(50)
    if k == 27 or k == ord("q"):
        cv.destroyAllWindows()
        break
    elif k == ord("a"):
        PrevFile()
    elif k == ord("d"):
        NextFile(DataList)
    file_num = cv.getTrackbarPos("file", "settings")
    img = cv.imread(DataList[file_num])
    result = CalcOfDamageAndNonDamage(DataList[file_num])
    cv.imshow("image", img)
    cv.imshow("result", result)