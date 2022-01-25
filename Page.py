# Code and design done by Elayne Tan Hui Shan
# Bitmaps for buttons added by Chua Zhi Loon James

import datetime
import os
import wx


from Panel import Panel


class Page(wx.Frame):
    def __init__(self, sBgImgName : str) -> None:
        '''Settings for all pages'''
        
        self._cScreenSize = wx.GetDisplaySize()
        
        #Application window is 80% of display screen size
        super().__init__(parent = None, title = 'NTU Smart Canteen', size = (0.8 * self._cScreenSize.GetWidth(), 0.8 * self._cScreenSize.GetHeight()))
        
        #Move the frame to the center of the display screen
        self.Center()

        #Setting up panel for all pages
        self._sBgImgName = sBgImgName
        self._cPanel = Panel(self, self._sBgImgName)


        ''' Button Images '''
        
        self._bUseBitmaps = True
        
        tButtonNames = ("Title.png", "Back.png", "CheckOH.png", "Confirm.png", "Exit.png", "SetDT.png", "UseCurrentDT.png", "MiniWok.png", "Vegetarian.png", "Cantonese.png", "MalayBBQ.png", "KFC.png", "CalcTime.png", "FullMenu.png", "Prompt.png")

        for sImageName in tButtonNames:
            if not os.path.exists("Bitmaps/" + sImageName):
                self._bUseBitmaps = False
                print("Unable to use bitmaps for buttons!")
                break


    def GetDateTime(self) -> str:
        '''Get the current date and time in the format "YYYY-MM-DD hh:mm:ss"'''
        
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


    
