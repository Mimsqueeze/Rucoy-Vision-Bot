import cv2 as cv
import numpy as np
import os
import time
from windowcapture import WindowCapture
from arrowcapture import ArrowCapture
from attackvision import AttackVision
from vision import Vision
import pyautogui
import math

os.chdir(os.path.dirname(os.path.abspath(__file__)))

wincap = WindowCapture()
arrowcap = ArrowCapture()
vision_dsinleft = Vision("dsin_left.png")
vision_dsinright = Vision("dsin_right.png")
vision_dsinfront = Vision("dsin_front.png")
vision_dsinback = Vision("dsin_back.png")

cords = []
locations = []
attack = "yes"
dist = 0

def checkdsin(type):

    while(True):

        screenshot = wincap.get_screenshot()
        points = []
        points = type.find(screenshot , threshold = 0.80, debug_mode = 'points')
        global cords
        cords = (str(points)[1:-1])
        break

def checkattack():
    while(True):
        arrowpic = arrowcap.get_screenshot()
        time.sleep(5)
        screenshot = wincap.get_screenshot()
        attacking = AttackVision(arrowpic).find(screenshot, threshold = 0.98)
        global attack
        attack = attacking
        break

def clickdist(clickp):
    global dist
    hypo = 0
    clicks = clickp.split(",")
    clickpx = int(clicks[0])
    clickpy = int(clicks[1])
    legx = math.fabs(960-clickpx)
    legy = math.fabs(540-clickpy)
    dist = math.sqrt(math.pow(legx, 2) + math.pow(legy, 2))
    
    

while(True):
    checkattack()

    if (attack == "yes"):
        print("Attacking...")

    if (attack == "no"):
        print("Locating target...")
        checkdsin(vision_dsinleft)
        if cords != '':
            locations.append(cords)
        checkdsin(vision_dsinright)
        if cords != '':
            locations.append(cords)
        checkdsin(vision_dsinfront)
        if cords != '':
            locations.append(cords)
        checkdsin(vision_dsinback)
        if cords != '':
            locations.append(cords)

        if locations != []:
            clickdist1 = 0
            clickdist2 = 0
            clickdist3 = 0
            clickdist4 = 0
            print(locations)

            if len(locations) >= 1:
                clickp1 = (str(locations[0]))[1:-1]
                clickdist(clickp1)
                clickdist1 = dist
            if len(locations) >= 2:
                clickp2 = (str(locations[1]))[1:-1]
                clickdist(clickp2)
                clickdist2 = dist
            if len(locations) >= 3:
                clickp3 = (str(locations[2]))[1:-1]
                clickdist(clickp3)
                clickdist3 = dist
            if len(locations) == 4:
                clickp4 = (str(locations[3]))[1:-1]
                clickdist(clickp4)
                clickdist4 = dist

            if (clickdist1 < clickdist2) and (clickdist1 < clickdist3) and (clickdist1 < clickdist4):
                clicks = clickp1.split(",")
                xpos = int(clicks[0])
                ypos = int(clicks[1])
            if (clickdist2 < clickdist1) and (clickdist2 < clickdist3) and (clickdist2 < clickdist4):
                clicks = clickp2.split(",")
                xpos = int(clicks[0])
                ypos = int(clicks[1])
            if (clickdist3 < clickdist1) and (clickdist3 < clickdist2) and (clickdist3 < clickdist4):
                clicks = clickp3.split(",")
                xpos = int(clicks[0])
                ypos = int(clicks[1])
            if (clickdist4 < clickdist2) and (clickdist4 < clickdist3) and (clickdist4 < clickdist1):
                clicks = clickp4.split(",")
                xpos = int(clicks[0])
                ypos = int(clicks[1])
            
            print()
            pyautogui.moveTo(xpos,ypos)
            pyautogui.click()
            time.sleep(0.5)
            pyautogui.click()

            cords = []
            locations = []
            
        else:
            print("No dsins found.")
            cords = []
            locations = []

        print("Finished.")
        time.sleep(5)
    else:
        time.sleep(5)
