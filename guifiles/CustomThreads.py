
# see the included wxThreadExample.py file

import os, sys, time, threading
import wx
from . import CustomEvents

import pyeq3


class FittingThread(threading.Thread):
    def __init__(self, notify_window, equation):
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self.equation = equation
        # This starts the thread running on creation, but you could
        # also make the GUI thread responsible for calling this
        self.start()


    def run(self):

        statusString = 'Fitting data...'
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(statusString))
        time.sleep(0.5) # allow users to see the update
        self.equation.Solve()
    
        statusString = 'Calculating model errors...'
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(statusString))
        time.sleep(0.5) # allow users to see the update
        self.equation.CalculateModelErrors(self.equation.solvedCoefficients, self.equation.dataCache.allDataCacheDictionary)
    
        statusString = 'Calculating coefficient and fit statistics...'
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(statusString))
        time.sleep(0.5) # allow users to see the update
        self.equation.CalculateCoefficientAndFitStatistics()

        statusString = 'Fitting complete, creating graphs and reports...'
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(statusString))
        time.sleep(0.5) # allow users to see the update
            
        # the fitted equation is now the event data, not a status update string
        wx.PostEvent(self._notify_window, CustomEvents.ThreadStatusEvent(self.equation))
