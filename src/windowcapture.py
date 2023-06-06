import numpy as np
import win32gui, win32ui, win32con

class WindowCapture:
    # Declare dimensions of the window
    w = 0
    h = 0
    hwnd = None
    cropped_y = 0
    offset_y = 0

    def __init__(self, window_name = None):
        # Find the correct window
        if window_name is None:
            self.hwnd = win32gui.GetDesktopWindow()
        else:
            self.hwnd = win32gui.FindWindow(None, window_name)
            if not self.hwnd:
                raise Exception("Window not found {}".format(window_name))

        # Get window dimensions
        window_rect = win32gui.GetWindowRect(self.hwnd)
        self.w = window_rect[2] - window_rect[0]
        self.h = window_rect[3] - window_rect[1]

        topblackbar_pixels = 0
        botblackbar_pixels = 0

        self.h = self.h - topblackbar_pixels - botblackbar_pixels

        self.cropped_y = topblackbar_pixels
        self.offset_y = window_rect[1] + self.cropped_y


    def get_screenshot(self):
        # Get the window image data
        wDC = win32gui.GetWindowDC(self.hwnd)
        dcObj = win32ui.CreateDCFromHandle(wDC)
        cDC = dcObj.CreateCompatibleDC()
        dataBitMap = win32ui.CreateBitmap()
        dataBitMap.CreateCompatibleBitmap(dcObj, self.w, self.h)
        cDC.SelectObject(dataBitMap)
        cDC.BitBlt((0, 0), (self.w, self.h), dcObj, (0, self.cropped_y), win32con.SRCCOPY)
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

    @staticmethod
    def list_window_names():
        def winEnumHandler(hwnd, ctx):
            if win32gui.IsWindowVisible(hwnd):
                print(hex(hwnd), win32gui.GetWindowText(hwnd))
        win32gui.EnumWindows(winEnumHandler, None)
