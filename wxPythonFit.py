import os, sys, pickle

import wx # ensure this import works before starting the application
import matplotlib # ensure this import works before starting the application

import pyeq3

# local imports from application subdirectory
import guifiles.icon as icon
import guifiles.DataForControls as dfc
import guifiles.CustomDialogs as CustomDialogs
import guifiles.CustomEvents as CustomEvents
import guifiles.CustomThreads as CustomThreads


class ApplicationFrame(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, title="Example wxPython Curve And Surface Fitter",
                          size=(800,600))

        # wx converted an icon file to a Python file for embedding here, see icon.py file
        self.SetIcon(icon.icon.GetIcon()) 

        p = wx.Panel(self) # something to put the controls on

        # create the controls
        # no need to use "self." as these are not referenced by other methods
        label1 = wx.StaticText(p, -1, "--- 2D Data Text Editor ---")
        label2 = wx.StaticText(p, -1, "--- 3D Data Text Editor ---")

        # use "self" because of references in other methods
        self.text_2D = wx.TextCtrl(p, -1, dfc.exampleText_2D,
                              style=wx.TE_MULTILINE|wx.HSCROLL)
        self.text_3D = wx.TextCtrl(p, -1, dfc.exampleText_3D,
                              style=wx.TE_MULTILINE|wx.HSCROLL)
                
        # use "self" because of references in other methods
        self.rbFittingTargetChoice_2D = wx.RadioBox(
            p, -1, "--- Fitting Target 2D ---", wx.DefaultPosition, wx.DefaultSize,
            dfc.fittingTargetList, 1, wx.RA_SPECIFY_COLS
        )
        self.rbFittingTargetChoice_3D = wx.RadioBox(
            p, -1, "--- Fitting Target 3D ---", wx.DefaultPosition, wx.DefaultSize,
            dfc.fittingTargetList, 1, wx.RA_SPECIFY_COLS
        )
            
        # use "self" because of references in other methods
        self.rbEqChoice_2D = wx.RadioBox(
            p, -1, "--- Example 2D Equations ---", wx.DefaultPosition, wx.DefaultSize,
            list(dfc.eq_od2D.keys()), 1, wx.RA_SPECIFY_COLS
        )
        self.rbEqChoice_3D = wx.RadioBox(
            p, -1, "--- Example 3D Equations ---", wx.DefaultPosition, wx.DefaultSize,
            list(dfc.eq_od3D.keys()), 1, wx.RA_SPECIFY_COLS
        )

        # use "self" because of references in other methods
        self.btnFit2D = wx.Button(p, -1, "Fit 2D Text Data")
        self.btnFit3D = wx.Button(p, -1, "Fit 3D Text Data")
         
        # setup the layout with grid sizer
        fgs = wx.FlexGridSizer(5, 2, 10, 20)
        fgs.AddGrowableRow(1)
        fgs.AddGrowableCol(0)
        fgs.AddGrowableCol(1)
        fgs.Add(label1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fgs.Add(label2, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fgs.Add(self.text_2D, 0, wx.EXPAND)
        fgs.Add(self.text_3D, 0, wx.EXPAND)
        fgs.Add(self.rbEqChoice_2D, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fgs.Add(self.rbEqChoice_3D, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fgs.Add(self.rbFittingTargetChoice_2D, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fgs.Add(self.rbFittingTargetChoice_3D, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fgs.Add(self.btnFit2D, 0, wx.ALIGN_CENTER_HORIZONTAL)
        fgs.Add(self.btnFit3D, 0, wx.ALIGN_CENTER_HORIZONTAL)

        border = wx.BoxSizer()
        border.Add(fgs, 1, wx.EXPAND|wx.ALL, 10)
        p.SetSizer(border)

        # all controls on the main panel have been added with sizers,
        # now center the application window on the user's display
        self.Center()

        # this dialog will not be displayed unless fitting is in progress
        # use "self" because of references in other methods
        self.statusBox = CustomDialogs.StatusDialog(self, '', "Status")
        
        # Bind the button events to their application methods
        self.Bind(wx.EVT_BUTTON, self.OnFit2D, self.btnFit2D)
        self.Bind(wx.EVT_BUTTON, self.OnFit3D, self.btnFit3D)
        
        # Set up event handler for any worker thread results
        CustomEvents.EVT_THREADSTATUS(self, self.OnThreadStatus)
    
        self.fittingWorkerThread = None


    def OnThreadStatus(self, event):
        if type(event.data) == type(''): # strings are status updates
            self.statusBox.text.AppendText(event.data + "\n")
        else: # not string data type, the worker thread completed
            self.fittingWorkerThread = None
            
            # event.data will be the fitted equation
            pickledEquationFile = open("pickledEquationFile", "wb")
            pickle.dump(event.data, pickledEquationFile)
            pickledEquationFile.close()
            
            self.btnFit2D.Enable()
            self.btnFit3D.Enable()
            self.statusBox.Hide()

            p = os.popen(sys.executable + ' FittingResultsViewer.py')
            p.close()


    def OnFit2D(self, evt):
        textData = str(self.text_2D.GetValue())
        equationSelection = self.rbEqChoice_2D.GetStringSelection()
        fittingTargetSelection = self.rbFittingTargetChoice_2D.GetStringSelection()
        
        # the GUI's fitting target string contains what we need - extract it
        fittingTarget = fittingTargetSelection.split('(')[1].split(')')[0]

        item = dfc.eq_od2D[equationSelection]
        eqString = 'pyeq3.Models_2D.' + item[0] + '(fittingTarget, ' + "'" + item[1] + "'" + item[2] + ')'
        self.equation = eval(eqString)

        # convert text to numeric data checking for log of negative numbers, etc.
        try:
            pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(textData, self.equation, False)
        except:
            wx.MessageBox(self.equation.reasonWhyDataRejected, "Error")
            return

        # check for number of coefficients > number of data points to be fitted
        coeffCount = len(self.equation.GetCoefficientDesignators())
        dataCount = len(self.equation.dataCache.allDataCacheDictionary['DependentData'])
        if coeffCount > dataCount:
            wx.MessageBox("This equation requires a minimum of " + str(coeffCount) + " data points, you have supplied " + repr(dataCount) + ".", "Error")
            return
        
        # Now the status dialog is used. Disable fitting buttons until thread completes
        self.btnFit2D.Disable()
        self.btnFit3D.Disable()
        self.statusBox.text.SetValue('')
        self.statusBox.Show() # hidden by OnThreadStatus() when thread completes

        # thread will automatically start to tun
        self.fittingWorkerThread = CustomThreads.FittingThread(self, self.equation)
        

    def OnFit3D(self, evt):
        textData = str(self.text_3D.GetValue())
        equationSelection = self.rbEqChoice_3D.GetStringSelection()
        fittingTargetSelection = self.rbFittingTargetChoice_3D.GetStringSelection()
        
        # the GUI's fitting target string contains what we need - extract it
        fittingTarget = fittingTargetSelection.split('(')[1].split(')')[0]

        item = dfc.eq_od3D[equationSelection]
        eqString = 'pyeq3.Models_3D.' + item[0] + '(fittingTarget, ' + "'" + item[1] + "'" + item[2] + ')'
        self.equation = eval(eqString)

        # convert text to numeric data checking for log of negative numbers, etc.
        try:
            pyeq3.dataConvertorService().ConvertAndSortColumnarASCII(textData, self.equation, False)
        except:
            wx.MessageBox(self.equation.reasonWhyDataRejected, "Error")
            return

        # check for number of coefficients > number of data points to be fitted
        coeffCount = len(self.equation.GetCoefficientDesignators())
        dataCount = len(self.equation.dataCache.allDataCacheDictionary['DependentData'])
        if coeffCount > dataCount:
            wx.MessageBox("This equation requires a minimum of " + str(coeffCount) + " data points, you have supplied " + repr(dataCount) + ".", "Error")
            return

        # Now the status dialog is used. Disable fitting buttons until thread completes
        self.btnFit2D.Disable()
        self.btnFit3D.Disable()
        self.statusBox.text.SetValue('')
        self.statusBox.Show() # hidden by OnThreadStatus() when thread completes
    
        # thread will automatically start to run
        self.fittingWorkerThread = CustomThreads.FittingThread(self, self.equation)

 

if __name__ == "__main__":
    app = wx.App()
    frm = ApplicationFrame()
    frm.Show()
    app.MainLoop()
