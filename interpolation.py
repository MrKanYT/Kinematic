import pygame as pg
import pandas as pd
from math import *
from inter_classes import *
import time
import re
from NetTool import NetTool
from config import Configuration


NT = NetTool("192.168.137.246", "192.168.137.18")
tn, tn_hand = NT.GetSockets()


if NT.HandSocket != None:
    print("CONNECTED TO HAND")

pg.init()
screen = pg.display.set_mode((Configuration.WIDTH, Configuration.HEIGHT))
clock = pg.time.Clock()                             #запуск pygame
pg.display.set_caption("Bilinear interpolation")
WORKSPACE_MOVING = 0        #смещение (не работает)

def to_pygame(coords):
    return Configuration.HEIGHT - coords

display_surface = pg.display.get_surface()
display_surface.blit(pg.transform.flip(display_surface, False, True), dest=(0, 0))

def bilinear_interpolation(x, y, points):
    points = sorted(points)
    (x1, y1, q11), (_x1, y2, q12), (x2, _y1, q21), (_x2, _y2, q22) = points

    if x1 != _x1 or x2 != _x2 or y1 != _y1 or y2 != _y2:
        raise ValueError('points do not form a rectangle')
    if not x1 <= x <= x2 or not y1 <= y <= y2:
        raise ValueError('(x, y) not within the rectangle')                 #функция интерполяции

    return (q11 * (x2 - x) * (to_pygame(y2) - to_pygame(y)) +
            q21 * (x - x1) * (to_pygame(y2) - to_pygame(y)) +
            q12 * (x2 - x) * (to_pygame(y) - to_pygame(y1)) +
            q22 * (x - x1) * (to_pygame(y) - to_pygame(y1))
           ) / ((x2 - x1) * (to_pygame(y2) - to_pygame(y1)) + 0.0)

class Point:
    def __init__(self, x=0, y=0, vars=[0, 0]):
        self.x = x
        self.y = y
        self.vars = vars    #углы моторов

    x = 0;                                  #класс точки
    y = 0;

    vars = [0, 0]

def build_rects(points):
    out_rects = []
    rect_points = [[], [], [], []]
    for row in range(len(points)):
        if row >= len(points)-1:
            break
        for point in range(len(points[row])):
            try:
                indexTest = points[row][point][1]
                indexTest = points[row + 1][point][1]
                indexTest = points[row + 1][point + 1][1]
                indexTest = points[row][point + 1][1]
            except IndexError:
                continue                                            #получение одномерного массива квадратов из двумерного массива точек
            rect_points[0] = points[row][point + 1]
            rect_points[1] = points[row + 1][point + 1]
            rect_points[2] = points[row][point]
            rect_points[3] = points[row + 1][point]
            test_points = [Point(rect_points[0][0] + WORKSPACE_MOVING, rect_points[0][1], [rect_points[0][2]]),
                           Point(rect_points[1][0] + WORKSPACE_MOVING, rect_points[1][1], [rect_points[1][2]]),
                           Point(rect_points[2][0] + WORKSPACE_MOVING, rect_points[2][1], [rect_points[2][2]]),
                           Point(rect_points[3][0] + WORKSPACE_MOVING, rect_points[3][1], [rect_points[3][2]])]

            out_rects.append(Rect(test_points))
    return out_rects

font_name = pg.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    text_surface = font.render(text, True, (0, 0, 0))
    text_rect = text_surface.get_rect()         #функция вывода текста на экран
    text_rect.topleft = (x, y)
    surf.blit(text_surface, text_rect)

allSprites = pg.sprite.Group()
testSprites = pg.sprite.Group()

data = pd.read_csv("points_new.csv", sep=",")       #загружаем файл с точками

rowsDict = {}
colsDict = {}
counter = 0
for i in sorted(data["X_pos"].unique()):
    colsDict[i] = counter
    counter += 1
counter = 0

min_X = min(data["X_pos"])
max_X = max(data["X_pos"])

min_Y = min(data["Y_pos"])
max_Y = max(data["Y_pos"])

for i in sorted(data["Y_pos"].unique()):
    rowsDict[i] = counter
    counter += 1

pointsArray = []
for i in range(len(data["Y_pos"].unique())):                        #получаем из файла двумерный массив точек в нужном порядке
    pointsArray.append([])
    for i2 in range(len(data["X_pos"].unique())):
        pointsArray[i].append([])

for i in range(len(data["X_pos"])):
    pointsArray[rowsDict[data["Y_pos"][i]]][colsDict[data["X_pos"][i]]] = [data["X_pos"][i], data["Y_pos"][i], [data["Rot1"][i], data["Rot2"][i]]]
rects = build_rects(pointsArray)    #собираем из этого массива квадраты



for rect in rects:
    allSprites.add(rect)        #добавляем все квадраты в одну группу спрайтов

outPoint = OutPoint()

mousePoint = MousePoint()

circleControlPoint = CircleControlPoint()
interpolControlPoint = InterpolControlPoint()
outPointGroup = pg.sprite.Group()
outPointGroup.add(circleControlPoint, interpolControlPoint)             #добавляем точку, для которой считаем значения, в группу
oldRect = None

input_circle_group = pg.sprite.Group()
input_circle = InputCircle()
input_circle_group.add(input_circle)
input_circle_group.add(InputCircleCenter(input_circle.x, input_circle.y))

hand_input = HandInputPoint()

hand_visualisation = HandVisualisation()


pressed = NT.HandSocket != None


last_send = 0

oldRect = None
oldPos = (0, 0)

Hand_record = False
Hand_record_list = [99999, -99999, 99999, -99999]


hand_input.L1 = Configuration.LENS["shoulder"]
hand_input.L2 = Configuration.LENS["wrist"]
hand_input.L3 = Configuration.LENS["hand"]

def remap(old_value, old_min, old_max, new_min, new_max):
    out = ((old_value - old_min) / (old_max - old_min)) * (new_max - new_min) + new_min
    if out > new_max:
        out = new_max
    elif out < new_min:
        out = new_min
    return out

while True: #основной цикл программы
    if NT.HandSocket != None:
        data = tn_hand.read_very_eager()
        if data != b'':
            try:
                splitted = re.split(r'/', data.decode('utf-8'))
                # 0 - hy, 1 - hz, 2 - wy, 3 - hy

                hand_input.a1 = float(splitted[0]) / 10
                hand_input.a2 = float(splitted[2]) / 10
                hand_input.a3 = float(splitted[3]) / 10
                hand_input.rot = float(splitted[1]) * -3
                hand_input.a4 = float(splitted[4])
                hand_input.a5 = float(splitted[5])
            except:
                pass


    screen.fill('gray')     #очищаем экран
    allSprites.draw(screen)     #выводим на экран все квадраты
    pg.draw.circle(screen, (255, 255, 255), (input_circle.x, input_circle.y), input_circle.size/2)
    input_circle_group.draw(screen)
    draw_text(screen, f"Angle A: {round(outPoint.rotA)}", 30, 5, 50)
    draw_text(screen, f"Angle B: {round(outPoint.rotB)}", 30, 5, 100)
    draw_text(screen, f"Angle C: {round(outPoint.rotC)}", 30, 5, 150)
    draw_text(screen, f"Angle D: {round(outPoint.rotD)}", 30, 5, 200)
    draw_text(screen, f"Angle E: {round(outPoint.rotE)}", 30, 5, 250)
    draw_text(screen, f"Angle F: {round(outPoint.rotF)}", 30, 5, 300)

    hand_visualisation.calc_points(hand_input.L1, hand_input.L2, hand_input.L3, hand_input.a1, hand_input.a2, hand_input.a3)
    hand_visualisation.calc_display_points(850, 175)

    pg.draw.line(screen, [255 ,0 ,0], hand_visualisation.shoulder_point_display, hand_visualisation.wrist_point_display, 3)
    pg.draw.line(screen, [0, 255, 0], hand_visualisation.wrist_point_display, hand_visualisation.hand_point_display, 3)
    pg.draw.line(screen, [0, 0, 255], hand_visualisation.hand_point_display, hand_visualisation.end_point_display, 3)

    hand_input.x, hand_input.y = hand_visualisation.hand_point

    for i in pointsArray:
        for i2 in i:
            try:
                pg.draw.circle(screen, 'red', (i2[0] + WORKSPACE_MOVING, i2[1]), 1)         #рисуем на экране все точки
            except:
                pass

    outPointGroup.draw(screen)      #рисуем на экране выходную точку
    pg.display.flip()       #обновляем окно программы

    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                Hand_record = not Hand_record
                if Hand_record:
                    print("Starting record...")
                    Configuration.HAND_MIN_X = None
                    Configuration.HAND_MAX_X = None
                    Configuration.HAND_MIN_Y = None
                    Configuration.HAND_MAX_Y = None
                else:
                    print("Ending record...")
                    print(Hand_record_list)
                    Configuration.HAND_MIN_X = Hand_record_list[0]
                    Configuration.HAND_MAX_X = Hand_record_list[1]
                    Configuration.HAND_MIN_Y = Hand_record_list[2]
                    Configuration.HAND_MAX_Y = Hand_record_list[3]
        if NT.HandSocket == None:
            if event.type == pg.MOUSEBUTTONDOWN:
                pressed = True                  #управление
            if event.type == pg.MOUSEBUTTONUP:
                pressed = False
    if pressed and Configuration.HAND_MAX_Y != None:
        if NT.HandSocket == None:
            mousePoint.rect.center = (pg.mouse.get_pos())
        else:
            mousePoint.rect.center = (remap(round(hand_input.x), Configuration.HAND_MIN_X, Configuration.HAND_MAX_X, min_X, max_X), remap(round(hand_input.y), HAND_MIN_Y, HAND_MAX_Y, min_Y, max_Y))
            input_circle.angle = hand_input.rot / 4

            pass
        collidedRect = mousePoint.GetRect(allSprites)
        if (collidedRect != None):
            interpolControlPoint.rect.center = mousePoint.rect.center
            if oldRect != None:
                oldRect.image.fill((255, 255, 255))
            oldRect = collidedRect
            collidedRect.image.fill((255, 0, 0))
            interpolationOut = [
                bilinear_interpolation(interpolControlPoint.rect.center[0], interpolControlPoint.rect.center[1],
                                       collidedRect.GetPoints(0)),
                bilinear_interpolation(interpolControlPoint.rect.center[0], interpolControlPoint.rect.center[1],
                                       collidedRect.GetPoints(1))]
            center = (input_circle.x, input_circle.y)
            angle = radians(input_circle.angle)
            radius = (input_circle.size/2) * (1 - (max_X - interpolControlPoint.rect.centerx) / (max_X - min_X))
            circleControlPoint.rect.center = (input_circle.x + (radius * cos(angle)), input_circle.y + (radius * sin(angle)))
        else:
            mouse_pos_in_circle = input_circle.GetPosInRad(mousePoint.rect.center)
            dist = input_circle.GetDistToPoint(mouse_pos_in_circle)
            if (dist <= input_circle.size/2):
                old_circle_control_pos = circleControlPoint.rect.center
                circleControlPoint.rect.center = mousePoint.rect.center
                input_circle.angle = input_circle.GetDegToPoint(circleControlPoint.rect.center)
                old_pos = interpolControlPoint.rect.center
                interpolControlPoint.rect.centerx = round((max_X - min_X) * (input_circle.GetDistToPoint(input_circle.GetPosInRad(circleControlPoint.rect.center)) / (input_circle.size/2)) + min_X)
                collidedRect = interpolControlPoint.GetRect(allSprites)
                if (collidedRect != None):
                    try:
                        if oldRect != None:
                            oldRect.image.fill((255, 255, 255))
                        oldRect = collidedRect
                        collidedRect.image.fill((255, 0, 0))
                        interpolationOut = [
                            bilinear_interpolation(interpolControlPoint.rect.center[0], interpolControlPoint.rect.center[1],
                                                   collidedRect.GetPoints(0)),
                            bilinear_interpolation(interpolControlPoint.rect.center[0], interpolControlPoint.rect.center[1],
                                                   collidedRect.GetPoints(1))]
                    except ValueError:
                        pass
                else:
                    interpolControlPoint.rect.center = old_pos

        try:
            outPoint.rotA = input_circle.angle % 360
            outPoint.rotB = interpolationOut[0]
            outPoint.rotC = interpolationOut[1]
            outPoint.rotD = 120 - remap(hand_input.a3, -8, 4, 0, 120)
            outPoint.rotE = remap(hand_input.a4, -50, 160, 10, 170)
            if (hand_input.a5 > 95):
                outPoint.rotF = 30
            elif (hand_input.a5 < 5):
                outPoint.rotF = 150
            else:
                outPoint.rotF = 90
            hand_input.old_a5 = hand_input.a5

            cur_time = time.time()
            if cur_time - last_send >= .2:
                last_send = cur_time
                try:
                    tn.write(f"A{round(outPoint.rotA)} B{round(outPoint.rotB)} C{round(outPoint.rotC)} D{round(outPoint.rotD)} E{round(outPoint.rotE)} F{round(outPoint.rotF)}\n".encode('ascii'))
                except:
                    pass
        except:
            pass

    if Hand_record:
        if hand_input.x < Hand_record_list[0]:
            Hand_record_list[0] = hand_input.x
        if hand_input.x > Hand_record_list[1]:
            Hand_record_list[1] = hand_input.x
        if hand_input.y < Hand_record_list[2]:
            Hand_record_list[2] = hand_input.y
        if hand_input.y > Hand_record_list[3]:
            Hand_record_list[3] = hand_input.y


    clock.tick(Configuration.FPS)  #ограничитель фпс

