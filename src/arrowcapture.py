import cv2 as cv
import numpy as np
import win32gui, win32ui, win32con

class ArrowCapture:

    w = 0
    h = 0
    hwnd = None
    cropped_x = 0
    cropped_y = 0

    def __init__(self, window_name = None):

        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception("Window not found {}".format(window_name))

        self.h = 59
        self.w = 260

    def get_screenshot(self):
       
        # get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (1462, 1017), win32con.SRCCOPY)

        #dataBitMap.SaveBitmapFile(cDC, "debug.bmp")
        signedIntsArray = dataBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype = "uint8")
        img.shape = (self.h, self.w, 4)

        dcObj.DeleteDC()
        cDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, wDC)
        win32gui.DeleteObject(dataBitMap.GetHandle())

        img = img[...,:3]
        np.ascontiguousarray(img)

        return img
