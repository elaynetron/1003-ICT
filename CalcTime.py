# Code and design done by Elayne Tan Hui Shan
# Bitmaps for buttons added by Chua Zhi Loon James

import wx


from Functions import *
from Page import Page


class CalcTime(Page):
    def __init__(self, sBgImgName : str, sSelectedDT : str, sStoreName : str, dDataBase : dict, dOpenStores : dict) -> None:
        '''Settings for the Calculate Waiting Page frame'''
        
        super().__init__(sBgImgName)
        
        self._dDataBase = dDataBase
        self._dOpenStores = dOpenStores
        self._sSelectedDT = sSelectedDT
        self._sStoreName = sStoreName

        self._sMsgDisplay = ""
            

        ''' Text Widgets '''

        
        #Static bitmap for displaying the prompt if properly loaded
        if self._bUseBitmaps:
            self._cPrompt = wx.StaticBitmap(self._cPanel, bitmap = wx.Image("Bitmaps/Prompt.png").ConvertToBitmap())
            
        else:
            #Static textbox for displaying the prompt
            self._cPrompt = wx.StaticText(self._cPanel, style = wx.ALIGN_CENTER)

            #Settings for the chosen store name text
            self._cPrompt.SetLabel("Enter Number of People Waiting: ")
            self._cPrompt.SetFont(wx.Font(20, wx.TELETYPE, wx.NORMAL, wx.NORMAL))


        #Text Control that allows the user to type in text
        self._cTextField = wx.TextCtrl(self._cPanel)


        #Static textbox for displaying the waiting time once calculated or an error message
        self._cTimeText = wx.StaticText(self._cPanel, style = wx.ALIGN_LEFT)

        #Settings for the chosen store name text
        self._cTimeText.SetFont(wx.Font(25, wx.TELETYPE, wx.NORMAL, wx.NORMAL))


        ''' Button Widgets '''
        

        #Button for user to confirm the number of people waiting
        self._cConfirmButton = wx.Button(self._cPanel)
        
        #Button for user to go back to the Home Page
        self._cBackButton = wx.Button(self._cPanel)

        #Button for user to exit the application
        self._cExitButton = wx.Button(self._cPanel)

        if self._bUseBitmaps:
            self._cConfirmButton.SetBitmap(wx.Image("Bitmaps/Confirm.png").ConvertToBitmap())
            self._cBackButton.SetBitmap(wx.Image("Bitmaps/Back.png").ConvertToBitmap())
            self._cExitButton.SetBitmap(wx.Image("Bitmaps/Exit.png").ConvertToBitmap())
            
        else:
            self._cConfirmButton.SetLabel("Confirm")
            self._cBackButton.SetLabel("Back")
            self._cExitButton.SetLabel("Exit")

        self._cConfirmButton.Bind(wx.EVT_BUTTON, self.PressConfirm)
        self._cBackButton.Bind(wx.EVT_BUTTON, self.PressBack)
        self._cExitButton.Bind(wx.EVT_BUTTON, self.PressExit)
        

        ''' Horizontal Sizer to place the widgets '''


        #Align the first row of text (widget) choices horizontally
        self._cHoriSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        
        self._cHoriSizer1.Add(self._cPrompt, 0, wx.RIGHT | wx.CENTER, 20)
        self._cHoriSizer1.Add(self._cTextField, 0, wx.RIGHT | wx.CENTER, 100)


        #Align the last row of button (widget) choices horizontally
        self._cHoriSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        
        self._cHoriSizer2.Add(self._cBackButton, 0, wx.RIGHT | wx.CENTER, 20)
        self._cHoriSizer2.Add(self._cExitButton, 0, wx.CENTER)
        

        ''' Vertical Sizer to place widgets '''
        

        #Align the widgets vertically
        self._cVertSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Add space from the top to the widgets
        self._cVertSizer.AddStretchSpacer()

        self._cVertSizer.Add(self._cHoriSizer1, 0, wx.ALL | wx.CENTER, 20)
        self._cVertSizer.Add(self._cTimeText, 0, wx.ALL | wx.CENTER, 20)
        self._cVertSizer.Add(self._cConfirmButton, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cHoriSizer2, 0, wx.ALL | wx.CENTER, 50)

        #Add space to the bottom to the widgets
        self._cVertSizer.AddStretchSpacer()
        

        self._cPanel.SetSizer(self._cVertSizer)
        self.Show()


    def PressConfirm(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Calculates and update waiting time when user clicks on Confirm button'''
        
        sNumber = self._cTextField.GetValue()
        
        if not sNumber:
            self._cTimeText.SetLabel("Nothing was keyed in.")

        elif not sNumber.isdigit():
            self._cTimeText.SetLabel("Invalid number of people.")

        elif int(sNumber) > 99:
            self._cTimeText.SetLabel("Too many people in queue.")

        else:
            self._cTimeText.SetLabel("Waiting Time: " + CalculateWaitingTime(self._dDataBase, int(sNumber), self._sStoreName))

        #Needed to resize for proper position of waiting time/error message text
        self.SetSize(0.8 * self._cScreenSize.GetWidth(), 0.8 * self._cScreenSize.GetHeight() + 1)

    def PressBack(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Go back to the Store Page when user clicks on Back button'''

        #Placed here instead of the top to avoid infinite importing error
        from StorePage import StorePage
        
        self.Hide()
        StorePage(self._sBgImgName, self._sSelectedDT, self._sStoreName, self._dDataBase, self._dOpenStores)
        

    def PressExit(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Close the application when user clicks on Exit button'''
        
        self.Destroy()


        
