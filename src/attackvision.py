import cv2 as cv
import numpy as np

class AttackVision:

    arrow_img = None
    arrow_w = 0
    arrow_h = 0
    method = None

    def __init__(self, arrow_img, method = cv.TM_CCOEFF_NORMED):
        self.arrow_img = arrow_img
        self.arrow_w = self.arrow_img.shape[1]
        self.arrow_h = self.arrow_img.shape[0]
        self.method = method

    def find(self, game_img, threshold = 0.99, debug_mode = None):


        result = cv.matchTemplate(game_img, self.arrow_img, self.method)
        min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
        attacking = ""

        if max_val >= threshold:
            attacking = 'no'
        if max_val < threshold:
            attacking = 'yes'
         
        cv.imwrite("arrow.jpg", self.arrow_img)
        cv.imwrite("game.jpg", game_img)

        return attacking
