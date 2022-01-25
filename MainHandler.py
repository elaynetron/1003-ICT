# Code and design done by Elayne Tan Hui Shan

import wx


from HomePage import HomePage


#Only create application when handler is executed and not imported
if __name__ == '__main__':
    cApp = wx.App()
    
    #Load home page with background image name
    HomePage("HiveTrsp.png")

    #Start application loop
    cApp.MainLoop()
