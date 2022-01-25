# Code and design done by Elayne Tan Hui Shan
# Bitmaps for buttons added by Chua Zhi Loon James

import wx


from Functions import *
from Page import Page
from Panel import Panel


class CheckOHPage(Page):
    def __init__(self, sBgImgName : str) -> None:
        '''Settings for the Check Operating Hours Frame'''
        
        super().__init__(sBgImgName)

        
        ''' Text Widget'''


        #Static bitmap for displaying the operating hours title if properly loaded
        if self._bUseBitmaps:
            self._cOHTitle = wx.StaticBitmap(self._cPanel, bitmap = wx.Image("Bitmaps/OHTitle.png").ConvertToBitmap())

        else:
            #Static textbox for displaying operating hours title
            self._cOHTitle = wx.StaticText(self._cPanel, style = wx.ALIGN_CENTER)

            #Settings for the heading title
            self._cOHTitle.SetLabel("Operating Hours")
            self._cOHTitle.SetFont(wx.Font(30, wx.TELETYPE, wx.NORMAL, wx.BOLD))


        #Static textbox for displaying the operating hours
        self._cOHText = wx.StaticText(self._cPanel, style = wx.ALIGN_LEFT)

        #Settings for the operating hours text
        self._cOHText.SetLabel(GetOHString("Data/Operating Hours.txt"))
        self._cOHText.SetFont(wx.Font(20, wx.TELETYPE, wx.NORMAL, wx.NORMAL))


        ''' Button Widgets '''


        #Button for user to go back to the Home Page
        self._cBackButton = wx.Button(self._cPanel)

        #Button for user to exit the application
        self._cExitButton = wx.Button(self._cPanel)

        if self._bUseBitmaps:
            self._cBackButton.SetBitmap(wx.Image("Bitmaps/Back.png").ConvertToBitmap())
            self._cExitButton.SetBitmap(wx.Image("Bitmaps/Exit.png").ConvertToBitmap())
            
        else:
            self._cBackButton.SetLabel("Back")
            self._cExitButton.SetLabel("Exit")
            
        self._cBackButton.Bind(wx.EVT_BUTTON, self.PressBack)
        self._cExitButton.Bind(wx.EVT_BUTTON, self.PressExit)


        ''' Horizontal Sizer to place the button widgets '''


        #Align the first row of button (widget) choices horizontally
        self._cHoriSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self._cHoriSizer.Add(self._cBackButton, 0, wx.RIGHT | wx.CENTER, 20)
        self._cHoriSizer.Add(self._cExitButton, 0, wx.CENTER)

        
        ''' Vertical Sizer to place widgets '''
        
        
        #Align the widgets vertically
        self._cVertSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Add space from the top to the widgets
        self._cVertSizer.AddStretchSpacer()

        self._cVertSizer.Add(self._cOHTitle, 0, wx.ALL | wx.CENTER, 20)
        self._cVertSizer.Add(self._cOHText, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cHoriSizer, 0, wx.ALL | wx.CENTER, 50)

        #Add space to the bottom of the widgets
        self._cVertSizer.AddStretchSpacer()


        self._cPanel.SetSizer(self._cVertSizer)
        self.Show()
        
        
    def PressBack(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Go back to the Home Page when user clicks on Back button'''

        #Placed here instead of the top to avoid infinite importing error
        from HomePage import HomePage
        
        self.Hide()
        HomePage(self._sBgImgName)
        

    def PressExit(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Close the application when user clicks on Exit button'''
        
        self.Destroy()


