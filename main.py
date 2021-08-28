import pygame as pg
import pandas as pd
from math import *
import time
import re
from NetTool import NetTool
from config import cfg
from interpolation import *
from PgTools import *
from CSVTools import *

NT = NetTool(cfg.IP_MAIN,
             cfg.IP_HAND,
             cfg.PORT,
             cfg.CONNECT_TO_MAIN,
             cfg.CONNECT_TO_HAND)
tn, tn_hand = NT.GetSockets()

PgTools = PgTools(NT.HandSocket != None)

CSVTools = CSVTools(cfg.CSV_PATH)
CSVTools.BakeData()

Interpolation = Interpolation()

Interpolation.build_rects(CSVTools.pointsArray)    #собираем из этого массива квадраты


while True: #основной цикл программы
    PgTools.UpdateScreen()
    PgTools.DrawAllText()
    PgTools.InterpolationVisualizer.DrawAllRects(PgTools.screen)

    PgTools.handVisualiser.calc_points(PgTools.handVisualiser.hand_input.L1,
                                       PgTools.handVisualiser.hand_input.L2,
                                       PgTools.handVisualiser.hand_input.L3,
                                       PgTools.handVisualiser.hand_input.a1,
                                       PgTools.handVisualiser.hand_input.a2,
                                       PgTools.handVisualiser.hand_input.a3)
    PgTools.handVisualiser.calc_display_points(850, 175)

    PgTools.handVisualiser.Visualise(PgTools.screen)


    for i in pointsArray:
        for i2 in i:
            try:
                pg.draw.circle(screen, 'red', (i2[0], i2[1]), 1)         #рисуем на экране все точки
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
            mousePoint.rect.center = (remap(round(hand_input.x), Configuration.HAND_MIN_X, Configuration.HAND_MAX_X, min_X, max_X), remap(round(hand_input.y), Configuration.HAND_MIN_Y, Configuration.HAND_MAX_Y, min_Y, max_Y))
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

