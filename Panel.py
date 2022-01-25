# Code and design done by Elayne Tan Hui Shan
# Bitmaps for buttons added by Chua Zhi Loon James

import os
import wx

#Panel used in every page
class Panel(wx.Panel):
    def __init__(self, cParent : wx.Panel, sBgImgName : str) -> None:
        '''Constructor and loading background image'''
        
        super().__init__(parent = cParent, style = wx.FULL_REPAINT_ON_RESIZE)
        
        self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
        self._sBgImgName = sBgImgName
        
        self._cBgImage = None

        #Only load background image if the file exists
        if os.path.exists("Bitmaps/" + self._sBgImgName):
            self._cBgImage = wx.Image("Bitmaps/" + self._sBgImgName)
        
        
    def OnEraseBackground(self, cEvent : wx.EraseEvent) -> None:
        '''Erase background and replace with image'''
        
        cDC = cEvent.GetDC()
        #Provide a default white background in case background image is not loaded
        cDC.Clear()

        #Only display background image if it is loaded properly
        if self._cBgImage:
            cClientSize = self.GetClientSize()
            
            #Perform scaling on image based on client window size
            cDC.DrawBitmap(self._cBgImage.Scale(cClientSize.GetWidth(), cClientSize.GetHeight()).ConvertToBitmap(), 0, 0)
