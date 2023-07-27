import cv2 as cv
import numpy as np

class AttackVision:
  # Class attributes
  arrow_img = None
  arrow_w = 0
  arrow_h = 0
  method = None

  # Constructor
  def __init__(self, arrow_img, method = cv.TM_CCOEFF_NORMED):
    self.arrow_img = arrow_img
    self.arrow_w = self.arrow_img.shape[1]
    self.arrow_h = self.arrow_img.shape[0]
    self.method = method

  # Find function does image processing to find the template image within the game_img
  def find(self, game_img, threshold = 0.99):
    result = cv.matchTemplate(game_img, self.arrow_img, self.method)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
    attacking = ""

    # Determines whether the character is attacking or not
    if max_val >= threshold:
      attacking = 'no'
    if max_val < threshold:
      attacking = 'yes'
    
    # Save the image of the arrows for debugging
    cv.imwrite("arrow.jpg", self.arrow_img)

    return attacking
