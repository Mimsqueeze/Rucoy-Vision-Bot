import cv2 as cv
import numpy as np

class Vision:
  # Class attributes
  template_image = None
  template_width = 0
  template_height = 0
  method = None

  # Constructor
  def __init__(self, template_image_path, method = cv.TM_CCOEFF_NORMED):
    self.template_image = cv.imread(template_image_path, cv.IMREAD_UNCHANGED)
    self.template_width = self.template_image.shape[1]
    self.template_height = self.template_image.shape[0]
    self.method = method

  # Find function does image processing to find the template image within the game_img
  def find(self, game_img, threshold = 0.50):
    # Convert game image
    game_img = np.ascontiguousarray(game_img, dtype=np.uint8)

    # Match the template image to the game image
    result = cv.matchTemplate(game_img, self.template_image, self.method)

    # Extract locations where the result is greater than the threshold
    locations = np.where(result >= threshold)
    locations = list(zip(*locations[::-1]))

    # Determine positions of rectangles to draw
    rectangles = []
    for loc in locations:
      rect = [int(loc[0]), int(loc[1]), self.template_width, self.template_height]
      rectangles.append(rect)
      rectangles.append(rect)

    # Draw the rectangles in the game image
    rectangles, weights = cv.groupRectangles(rectangles, groupThreshold = 1, eps = 0.5)
    points = []
    if len(rectangles):
      line_color = (0, 255, 0)
      line_type = cv.LINE_4

      for (x, y, w, h) in rectangles:
        center_x = x + int(w/2)
        center_y = y + int(h/2)
        if points != []:
          points.pop(0)
        points.insert(0,(center_x, center_y))

        top_left = (x, y)
        bottom_right = (x + w, y + h)

        # Shade in rectangle
        sub_img = game_img[y:y+h, x:x+w]
        white_rect = np.ones(sub_img.shape, dtype=np.uint8) * 255
        res = cv.addWeighted(sub_img, 0.5, white_rect, 0.5, 1.0)
        game_img[y:y+h, x:x+w] = res

        # Draw outline
        cv.rectangle(game_img, top_left, bottom_right, color = line_color , lineType = line_type, thickness = 2)
    
    # Save the modified game image
    cv.imwrite("game.jpg", game_img)

    return points

