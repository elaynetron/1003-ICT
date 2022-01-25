# Code and design done by Elayne Tan Hui Shan
# Bitmaps for buttons added by Chua Zhi Loon James

import wx


from Functions import *
from Page import Page
from StorePage import StorePage


class StartPage(Page):
    def __init__(self, sBgImgName : str, sSelectedDT : str) -> None:
        '''Settings for the Start Page frame'''

        super().__init__(sBgImgName)

        self._sSelectedDT = sSelectedDT

        #Load the data files into dictionaries
        self._dDataBase = DataBase("Data/Menu Database.txt")
        self._dOperatingHours = OperatingHours("Data/Operating Hours.txt")

        #Get menu dictionary by selected date and time, will be empty if no stores are open at the date and time
        self._dOpenStores = GetMenuByDayTime(self._dDataBase, self._dOperatingHours, GetDayTime(sSelectedDT))


        ''' Text widgets'''

        
        #Static textbox for displaying selected date and time
        self._cSelectedDTText = wx.StaticText(self._cPanel, style = wx.ALIGN_CENTER)

        #Settings for the selected date and time text
        self._cSelectedDTText.SetLabel("Selected Date and Time: " + self._sSelectedDT)
        self._cSelectedDTText.SetFont(wx.Font(25, wx.TELETYPE, wx.NORMAL, wx.BOLD))


        #Show operating hours if there are no open stores
        if not self._dOpenStores:
            #Static textbox for displaying the operating hours
            self._cOHText = wx.StaticText(self._cPanel, style = wx.ALIGN_LEFT)

            #Settings for the operating hours text
            self._cOHText.SetLabel("Sorry, no stalls are operating at the selected date and time!\n\n" + GetOHString("Data/Operating Hours.txt"))
            self._cOHText.SetFont(wx.Font(20, wx.TELETYPE, wx.NORMAL, wx.NORMAL))

        else:
            

            ''' Button Widgets '''

            
            self._lStoreButtons = []
            
            for sStoreName in self._dOpenStores:
                self._lStoreButtons.append(wx.Button(self._cPanel, name = sStoreName))

            for nIndex in range(len(self._lStoreButtons)):
                if self._bUseBitmaps:
                    self._lStoreButtons[nIndex].SetBitmap(wx.Image("Bitmaps/" + IMGNAMES[STORENAMES.index(self._lStoreButtons[nIndex].GetName())] + ".png").ConvertToBitmap())

                else:
                    self._lStoreButtons[nIndex].SetLabel(self._lStoreButtons[nIndex].GetName())

                self._lStoreButtons[nIndex].Bind(wx.EVT_BUTTON, self.PressStore)

        
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

        self._cVertSizer.Add(self._cSelectedDTText, 0, wx.ALL | wx.CENTER, 20)

        if not self._dOpenStores:
            self._cVertSizer.Add(self._cOHText, 0, wx.ALL | wx.CENTER, 10)
            
        else:
            for cStoreButton in self._lStoreButtons:
                self._cVertSizer.Add(cStoreButton, 0, wx.ALL | wx.CENTER, 10)

        self._cVertSizer.Add(self._cHoriSizer, 0, wx.ALL | wx.CENTER, 50)

        #Add space to the bottom of the widgets
        self._cVertSizer.AddStretchSpacer()


        self._cPanel.SetSizer(self._cVertSizer)
        self.Show()


    def PressStore(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Change to the Store Page when user clicks on a Store button'''

        self.Hide()
        StorePage(self._sBgImgName, self._sSelectedDT, cButtonEvent.GetEventObject().GetName(), self._dDataBase, self._dOpenStores)


    def PressBack(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Go back to the Home Page when user clicks on Back button'''

        #Placed here instead of the top to avoid infinite importing error
        from HomePage import HomePage
        
        self.Hide()
        HomePage(self._sBgImgName)
        

    def PressExit(self, cButtonEvent : wx.CommandEvent) -> None:
        '''Close the application when user clicks on Exit button'''
        
        self.Destroy()


