# Code and design done by Elayne Tan Hui Shan
# Bitmaps for buttons added by Chua Zhi Loon James

import wx


from CalcTime import CalcTime
from FullMenu import FullMenu
from Functions import *
from Page import Page


class StorePage(Page):
    def __init__(self, sBgImgName : str, sSelectedDT : str, sStoreName : str, dDataBase : dict, dOpenStores : dict) -> None:
        '''Settings for the Store Page frame'''
        
        super().__init__(sBgImgName)

        self._dDataBase = dDataBase
        self._dOpenStores = dOpenStores
        self._sSelectedDT = sSelectedDT
        self._sStoreName = sStoreName

        #Format all menu items into a string
        sMenu = ""
        for sFoodName, sPrice in dOpenStores[self._sStoreName].items():
            sMenu += sFoodName + " - " + sPrice + "\n"


        ''' Text Widgets '''
        

        #Static textbox for displaying selected date and time
        self._cSelectedDT = wx.StaticText(self._cPanel, style = wx.ALIGN_CENTER)

        #Settings for the selected date and time text
        self._cSelectedDT.SetLabel("Selected Date and Time: " + self._sSelectedDT)
        self._cSelectedDT.SetFont(wx.Font(25, wx.TELETYPE, wx.NORMAL, wx.BOLD))
        

        #Static bitmap for displaying the store name if properly loaded
        if self._bUseBitmaps:
            self._cStoreName = wx.StaticBitmap(self._cPanel, bitmap = wx.Image("Bitmaps/" + IMGNAMES[STORENAMES.index(self._sStoreName)] + ".png").ConvertToBitmap())
            
        else:
            #Static textbox for displaying the chosen store name
            self._cStoreName = wx.StaticText(self._cPanel, style = wx.ALIGN_LEFT)

            #Settings for the chosen store name text
            self._cStoreName.SetLabel(self._sStoreName.upper())
            self._cStoreName.SetFont(wx.Font(30, wx.TELETYPE, wx.NORMAL, wx.NORMAL))


        #Static textbox for displaying the food menu for the store
        self._cStoreMenu = wx.StaticText(self._cPanel, style = wx.ALIGN_LEFT)

        #Settings for the food menu text
        self._cStoreMenu.SetLabel(sMenu)
        self._cStoreMenu.SetFont(wx.Font(20, wx.TELETYPE, wx.NORMAL, wx.NORMAL))


        ''' Button Widgets '''


        #Button for user to see full menu of the store
        self._cFullMenuButton = wx.Button(self._cPanel)

        #Button for user to get waiting time for the store based on number of people waiting
        self._cCalcTimeButton = wx.Button(self._cPanel)

        #Button for user to go back to the Home Page
        self._cBackButton = wx.Button(self._cPanel)

        #Button for user to exit the application
        self._cExitButton = wx.Button(self._cPanel)

        if self._bUseBitmaps:
            self._cFullMenuButton.SetBitmap(wx.Image("Bitmaps/FullMenu.png").ConvertToBitmap())
            self._cCalcTimeButton.SetBitmap(wx.Image("Bitmaps/CalcTime.png").ConvertToBitmap())
            self._cBackButton.SetBitmap(wx.Image("Bitmaps/Back.png").ConvertToBitmap())
            self._cExitButton.SetBitmap(wx.Image("Bitmaps/Exit.png").ConvertToBitmap())
            
        else:
            self._cFullMenuButton.SetLabel("See Full Menu")
            self._cCalcTimeButton.SetLabel("Calculate Waiting Time")
            self._cBackButton.SetLabel("Back")
            self._cExitButton.SetLabel("Exit")

        self._cFullMenuButton.Bind(wx.EVT_BUTTON, self.PressFullMenu)
        self._cCalcTimeButton.Bind(wx.EVT_BUTTON, self.PressCalcTime)
        self._cBackButton.Bind(wx.EVT_BUTTON, self.PressBack)
        self._cExitButton.Bind(wx.EVT_BUTTON, self.PressExit)

        
        ''' Horizontal Sizer to place the button widgets '''


        #Align the first row of button (widget) choices horizontally
        self._cHoriSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        
        self._cHoriSizer1.Add(self._cFullMenuButton, 0, wx.RIGHT | wx.CENTER, 20)
        self._cHoriSizer1.Add(self._cCalcTimeButton, 0, wx.CENTER)

        #Align the second row of button (widget) choices horizontally
        self._cHoriSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self._cHoriSizer2.Add(self._cBackButton, 0, wx.RIGHT | wx.CENTER, 20)
        self._cHoriSizer2.Add(self._cExitButton, 0, wx.CENTER)
        

        ''' Vertical Sizer to place widgets '''
        

        #Align the widgets vertically
        self._cVertSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Add space from the top to the widgets
        self._cVertSizer.AddStretchSpacer()

        self._cVertSizer.Add(self._cSelectedDT, 0, wx.ALL | wx.CENTER, 20)
        self._cVertSizer.Add(self._cStoreName, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cStoreMenu, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cHoriSizer1, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cHoriSizer2, 0, wx.ALL | wx.CENTER, 50)

        #Add space to the bottom to the widgets
        self._cVertSizer.AddStretchSpacer()
        

        self._cPanel.SetSizer(self._cVertSizer)
        self.Show()


    def PressFullMenu(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Change to the Full Menu Page when user clicks on See Full Menu button'''
        
        self.Hide()
        FullMenu(self._sBgImgName, self._sSelectedDT, self._sStoreName, self._dDataBase, self._dOpenStores)
        
                 
    def PressCalcTime(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Change to the Calc Time Page when user clicks on Calculate Waiting Time button'''
        
        self.Hide()
        CalcTime(self._sBgImgName, self._sSelectedDT, self._sStoreName, self._dDataBase, self._dOpenStores)


    def PressBack(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Go back to the Start Page when user clicks on Back button'''

        #Placed here instead of the top to avoid infinite importing error
        from StartPage import StartPage
        
        self.Hide()
        StartPage(self._sBgImgName, self._sSelectedDT)
        

    def PressExit(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Close the application when user clicks on Exit button'''
        
        self.Destroy()


