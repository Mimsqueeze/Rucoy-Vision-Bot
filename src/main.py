import cv2 as cv
import os
import time
from windowcapture import WindowCapture
from arrowcapture import ArrowCapture
from attackvision import AttackVision
from vision import Vision
import pyautogui

os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Create objects
wincap = WindowCapture()
arrowcap = ArrowCapture()
vision_drangerleft = Vision("images/drow_ranger_left.png")
vision_drangerright = Vision("images/drow_ranger_right.png")
vision_drangerfront = Vision("images/drow_ranger_front.png")
vision_drangerback = Vision("images/drow_ranger_back.png")

# Define functions
def checkdranger(type):
  screenshot = cv.imread("game.jpg", cv.IMREAD_UNCHANGED)
  points = []
  points = type.find(screenshot, threshold = 0.95)
  return (str(points)[1:-1])

def checkattack():
  # Take two screenshots 3 seconds apart and compare arrow count
  arrowpic1 = arrowcap.get_screenshot()
  time.sleep(3)
  arrowpic2 = arrowcap.get_screenshot()
  return AttackVision(arrowpic1).find(arrowpic2, threshold = 0.98)

def main():
  # Use Ctrl + C to stop program
  while(True):
    # Check if character is attacking
    isAttacking = checkattack()

    # If character is attacking, continue looping. Otherwise, perform image recognition
    if (isAttacking == "yes"):
      print("Attacking...")
    else:
      # Take and save screenshot of the screen
      screenshot = wincap.get_screenshot()
      cv.imwrite("game.jpg", screenshot)

      # Try to find targets
      print("Locating target...")

      # Save locations of targets
      locations = []
      cords = checkdranger(vision_drangerback)
      if cords != '':
        locations.append(cords)
      cords = checkdranger(vision_drangerleft)
      if cords != '':
        locations.append(cords)
      cords = checkdranger(vision_drangerright)
      if cords != '':
        locations.append(cords)
      cords = checkdranger(vision_drangerfront)
      if cords != '':
        locations.append(cords)

      # If locations isn't empty, that means we've found and matched targets
      if locations != []:
        # Take the first location in locations
        target_location = (str(locations[0]))[1:-1]

        # Isolate x position and y position
        coords = target_location.split(",")
        xpos = int(coords[0])
        ypos = int(coords[1])

        # Click on the target
        print(f"Target found. Now attacking target at position {xpos}, {ypos}")
        pyautogui.moveTo(xpos, ypos)
        pyautogui.click()
      else:
        print("No dranger's found.")

    # Sleep before next loop iteration
    timeToSleep = 2
    print(f"Finished. Sleeping for {timeToSleep} seconds.")
    time.sleep(timeToSleep)

if __name__ == "__main__":
  main()