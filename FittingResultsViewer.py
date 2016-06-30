import os, sys, pickle
import wx

import guifiles.CustomDialogs as CustomDialogs



app = wx.App()
f = open("pickledEquationFile", "rb")
unPickledEquation = pickle.load(f)
f.close()
os.remove("pickledEquationFile")
resultsFrame = CustomDialogs.ResultsFrame(None, '', "Fitting Results (resizable dialog)", equation=unPickledEquation)
resultsFrame.Show()
app.MainLoop()
