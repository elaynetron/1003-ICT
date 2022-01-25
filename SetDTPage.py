# Code and design done by Elayne Tan Hui Shan
# Bitmaps for buttons added by Chua Zhi Loon James

import datetime
import wx
import wx.adv


from Page import Page
from StartPage import StartPage


class SetDTPage(Page):
    def __init__(self, sBgImgName : str) -> None:
        '''Settings for the Set Date and Time Page frame'''
        
        super().__init__(sBgImgName)

        #Need to set locale to prevent conflict between C and Windows
        self._cLocale = wx.Locale(wx.LANGUAGE_ENGLISH)
        

        ''' Calendar Widget for user to select date from current date to 1 year from now'''
        

        lCurrentDate = datetime.date.today().__str__().split("-")
        lCurrentDate = [int(sItem) for sItem in lCurrentDate]
        
        self._cCalendar = wx.adv.CalendarCtrl(self._cPanel, style = wx.adv.CAL_MONDAY_FIRST)
        self._cCalendar.SetDateRange(lowerdate = wx.DateTime(lCurrentDate[2], lCurrentDate[1] - 1, lCurrentDate[0]), upperdate = wx.DateTime(lCurrentDate[2], lCurrentDate[1] - 1, lCurrentDate[0] + 1))


        ''' Time Picker Widget for user to select time '''

        
        self._cTimePicker = wx.adv.TimePickerCtrl(self._cPanel)


        ''' Button Widgets '''
        

        #Button for user to confirm to use the selected date and time
        self._cConfirmButton = wx.Button(self._cPanel)

        #Button for user to use the current date and time instead
        self._cUseCurrentDTButton = wx.Button(self._cPanel)
        
        #Button for user to go back to the Home Page
        self._cBackButton = wx.Button(self._cPanel)
        
        #Button for user to exit the application
        self._cExitButton = wx.Button(self._cPanel)
        
        if self._bUseBitmaps:
            self._cConfirmButton.SetBitmap(wx.Image("Bitmaps/Confirm.png").ConvertToBitmap())
            self._cUseCurrentDTButton.SetBitmap(wx.Image("Bitmaps/UseCurrentDT.png").ConvertToBitmap())
            self._cBackButton.SetBitmap(wx.Image("Bitmaps/Back.png").ConvertToBitmap())
            self._cExitButton.SetBitmap(wx.Image("Bitmaps/Exit.png").ConvertToBitmap())
            
        else:
            self._cConfirmButton.SetLabel("Confirm")
            self._cUseCurrentDTButton.SetLabel("Set Current Date and Time")
            self._cBackButton.SetLabel("Back")
            self._cExitButton.SetLabel("Exit")
            
        self._cConfirmButton.Bind(wx.EVT_BUTTON, self.PressConfirm)
        self._cUseCurrentDTButton.Bind(wx.EVT_BUTTON, self.PressUseCurrentDT)
        self._cBackButton.Bind(wx.EVT_BUTTON, self.PressBack)
        self._cExitButton.Bind(wx.EVT_BUTTON, self.PressExit)


        ''' Horizontal Sizer to the last row button widgets '''


        #Align the first row of button (widget) choices horizontally
        self._cHoriSizer = wx.BoxSizer(wx.HORIZONTAL)
        
        self._cHoriSizer.Add(self._cBackButton, 0, wx.RIGHT | wx.CENTER, 20)
        self._cHoriSizer.Add(self._cExitButton, 0, wx.CENTER)
        

        ''' Vertical Sizer to place widgets '''
        

        #Align the widgets vertically
        self._cVertSizer = wx.BoxSizer(wx.VERTICAL)
        
        #Add space from the top to the widgets
        self._cVertSizer.AddStretchSpacer()
        
        self._cVertSizer.Add(self._cCalendar, 0, wx.ALL | wx.CENTER, 20)
        self._cVertSizer.Add(self._cTimePicker, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cConfirmButton, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cUseCurrentDTButton, 0, wx.ALL | wx.CENTER, 10)
        self._cVertSizer.Add(self._cHoriSizer, 0, wx.ALL | wx.CENTER, 50)

        #Add space to the bottom of the widgets
        self._cVertSizer.AddStretchSpacer()


        self._cPanel.SetSizer(self._cVertSizer)
        self.Show()


    def PressConfirm(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Change to the Start Page when user clicks on Confirm button with the selected date and time'''
        
        self.Hide()
        StartPage(self._sBgImgName, self._cCalendar.GetDate().FormatISODate() + " " + ":".join(['{:0>2}'.format(nItem) for nItem in self._cTimePicker.GetTime()]))
        

    def PressBack(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Go back to the Home Page when user clicks on Back button'''

        #Placed here instead of the top to avoid infinite importing error
        from HomePage import HomePage
        
        self.Hide()
        HomePage(self._sBgImgName)
        

    def PressUseCurrentDT(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Change to the Start Page when user clicks on Use Current Date and Time button with the current date and time'''
        
        self.Hide()
        StartPage(self._sBgImgName, self.GetDateTime())



    def PressExit(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Close the application when user clicks on Exit button'''
        
        self.Destroy()


