# Code and design done by Elayne Tan Hui Shan
# Bitmaps for buttons added by Chua Zhi Loon James

import wx


from CheckOHPage import CheckOHPage
from Page import Page
from SetDTPage import SetDTPage
from StartPage import StartPage


class HomePage(Page):
    def __init__(self, sBgImgName : str) -> None:
        '''Settings for the Home Page frame'''

        super().__init__(sBgImgName)
        

        '''Timer object and event to update display of current date and time'''

        
        self._cTimer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, self.OnTimer)
        #Post timer event every 0.5 s instead of 1 s to make the display more in sync with actual time
        if not self._cTimer.Start(500):
            print("Unable to display dynamic updating of current date time!")


        ''' Text Widgets'''


        #Static bitmap for displaying the application title if properly loaded
        if self._bUseBitmaps:
            self._cHeadingText = wx.StaticBitmap(self._cPanel, bitmap = wx.Image("Bitmaps/Title.png").ConvertToBitmap())

        else:
            #Static textbox for displaying program heading title
            self._cHeadingText = wx.StaticText(self._cPanel, style = wx.ALIGN_CENTER)

            #Settings for the heading title
            self._cHeadingText.SetLabel("N T U   S M A R T   C A N T E E N")
            self._cHeadingText.SetFont(wx.Font(40, wx.TELETYPE, wx.SLANT, wx.BOLD))
            #Red (191, 28, 28) for text colour
            self._cHeadingText.SetForegroundColour((191, 28, 28))
            self._cHeadingText.Wrap(0.8 * self._cScreenSize.GetWidth())
        

        #Static textbox for displaying current date and time
        self._cDTText = wx.StaticText(self._cPanel, style = wx.ALIGN_CENTER)

        #Settings for the current date and time text
        self._cDTText.SetLabel("Current Date and Time: " + self.GetDateTime())
        self._cDTText.SetFont(wx.Font(25, wx.TELETYPE, wx.NORMAL, wx.BOLD))


        ''' Buttons Widgets '''


        #Button for user to select a specific date and time
        self._cSetDTButton = wx.Button(self._cPanel)

        #Button for user to use the current date and time
        self._cUseCurrentDTButton = wx.Button(self._cPanel)
        
        #Button for user to check operating hours
        self._cCheckOHButton = wx.Button(self._cPanel)
        
        #Button for user to exit the application
        self._cExitButton = wx.Button(self._cPanel)
        
        if self._bUseBitmaps:
            self._cSetDTButton.SetBitmap(wx.Image("Bitmaps/SetDT.png").ConvertToBitmap())
            self._cUseCurrentDTButton.SetBitmap(wx.Image("Bitmaps/UseCurrentDT.png").ConvertToBitmap())
            self._cCheckOHButton.SetBitmap(wx.Image("Bitmaps/CheckOH.png").ConvertToBitmap())
            self._cExitButton.SetBitmap(wx.Image("Bitmaps/Exit.png").ConvertToBitmap())
            
        else:
            self._cSetDTButton.SetLabel("Set Date and Time")
            self._cUseCurrentDTButton.SetLabel("Use Current Date and Time")
            self._cCheckOHButton.SetLabel("Check Operating Hours")
            self._cExitButton.SetLabel("Exit")

        self._cSetDTButton.Bind(wx.EVT_BUTTON, self.PressSetDT)
        self._cUseCurrentDTButton.Bind(wx.EVT_BUTTON, self.PressUseCurrentDT)
        self._cCheckOHButton.Bind(wx.EVT_BUTTON, self.PressCheckOH)
        self._cExitButton.Bind(wx.EVT_BUTTON, self.PressExit)


        ''' Horizontal Sizer to place first row button widgets '''

        
        #Align the first row of button (widget) choices horizontally
        self._cHoriSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self._cHoriSizer.Add(self._cSetDTButton, 0, wx.RIGHT | wx.CENTER, 20)
        self._cHoriSizer.Add(self._cUseCurrentDTButton, 0, wx.CENTER)


        ''' Vertical Sizer to place widgets '''
        
        
        #Align the widgets vertically
        self._cVertSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Add space from the top to the widgets
        self._cVertSizer.AddStretchSpacer()
        
        self._cVertSizer.Add(self._cHeadingText, 0, wx.ALL | wx.CENTER, 20)
        self._cVertSizer.Add(self._cDTText, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cHoriSizer, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cCheckOHButton, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cExitButton, 0, wx.ALL | wx.CENTER, 50)
        
        #Add space to the bottom of the widgets
        self._cVertSizer.AddStretchSpacer()

    
        self._cPanel.SetSizer(self._cVertSizer)
        self.Show()


    def OnTimer(self, cTimerEvent : wx.TimerEvent) -> None:
        '''Update the display of current date and time every 0.5 seconds when timer event is posted'''

        self._cDTText.SetLabel("Current Date and Time: " + self.GetDateTime())


    def PressSetDT(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Change to the SetDT Page when user clicks on Set Date and Time button'''

        self.Hide()
        SetDTPage(self._sBgImgName)


    def PressUseCurrentDT(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Change to the Start Page when user clicks on Use Current Date and Time button with the current date and time'''

        self.Hide()
        StartPage(self._sBgImgName, self.GetDateTime())


    def PressCheckOH(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Change to the CheckOH Page when user clicks on Check Operating Hours button'''

        self.Hide()
        CheckOHPage(self._sBgImgName)


    def PressExit(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Close the application when user clicks on Exit button'''
        
        self.Destroy()


