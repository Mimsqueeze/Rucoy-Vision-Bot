import cv2 as cv
import numpy as np

class Vision:

    dranger_img = None
    dranger_w = 0
    dranger_h = 0
    method = None

    def __init__(self, dranger_img_path, method = cv.TM_CCOEFF_NORMED):
        self.dranger_img = cv.imread(dranger_img_path, cv.IMREAD_UNCHANGED)
        self.dranger_w = self.dranger_img.shape[1]
        self.dranger_h = self.dranger_img.shape[0]
        self.method = method


    def find(self, game_img, threshold = 0.50, debug_mode = None):
        result = cv.matchTemplate(game_img, self.dranger_img, self.method)
        locations = np.where(result >= threshold)
        locations = list(zip(*locations[::-1]))

        rectangles = []
        for loc in locations:
            rect = [int(loc[0]), int(loc[1]), self.dranger_w, self.dranger_h]
            rectangles.append(rect)
            rectangles.append(rect)

        rectangles, weights = cv.groupRectangles(rectangles, groupThreshold = 1, eps = 0.5)

        points = []
        
        if len(rectangles):

            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            marker_color = (255, 0, 255)
            marker_type = cv.MARKER_CROSS

            for (x, y, w, h) in rectangles:
                center_x = x + int(w/2)
                center_y = y + int(h/2)
                if points != []:
                    points.pop(0)
                points.insert(0,(center_x, center_y))

                if debug_mode == 'rectangles':
                    top_left = (x, y)
                    bottom_right = (x + w, y + h)
                    cv.rectangle(game_img, top_left, bottom_right, color = line_color , lineType = line_type, thickness = 2)

                #elif debug_mode == 'points':
                    #cv.drawMarker(game_img, (center_x, center_y), color = marker_color, markerType = marker_type, markerSize = 40, thickness = 2)
        
        cv.imwrite("game.jpg", game_img)

        return points
    
