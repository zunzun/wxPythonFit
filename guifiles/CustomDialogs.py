import  wx

from . import AdditionalInfo
from . import IndividualReports as reports


# see the included wxNestedTabsExample.py file
class TopLevelResultsNotebook(wx.Notebook):
    def __init__(self, parent, inEquation):
        wx.Notebook.__init__(self, parent, id=wx.ID_ANY, style=wx.BK_DEFAULT)
        self.equation = inEquation
        
        self.graphReportsListForPDF = []
        self.textReportsListForPDF = []
        self.sourceCodeReportsListForPDF = []

        # graphs
        graphReportsTab = wx.Notebook(self)
        self.AddPage(graphReportsTab, "Graph Reports")
        
        if self.equation.GetDimensionality() == 2:
            report = reports.ModelScatterConfidenceGraph(graphReportsTab)
            report.draw(self.equation, scatterplotOnlyFlag=False)
            reportName = "Model With 95%Confidence"
            graphReportsTab.AddPage(report, reportName)
            self.graphReportsListForPDF.append([report.figure, reportName])
            
            report = reports.ModelScatterConfidenceGraph(graphReportsTab)
            report.draw(self.equation, scatterplotOnlyFlag=True)
            reportName = "Scatter Plot"
            graphReportsTab.AddPage(report, reportName)
            self.graphReportsListForPDF.append([report.figure, reportName])
        else:
            report = reports.SurfacePlot(graphReportsTab)
            report.draw(self.equation)
            reportName = "Surface Plot"
            graphReportsTab.AddPage(report, reportName)
            self.graphReportsListForPDF.append([report.figure, reportName])
            
            report = reports.ContourPlot(graphReportsTab)
            report.draw(self.equation)
            reportName = "Contour Plot"
            graphReportsTab.AddPage(report, reportName)
            self.graphReportsListForPDF.append([report.figure, reportName])

            report = reports.ScatterPlot(graphReportsTab)
            report.draw(self.equation)
            reportName = "Scatter Plot"
            graphReportsTab.AddPage(report, reportName)
            self.graphReportsListForPDF.append([report.figure, reportName])

        report = reports.AbsoluteErrorGraph(graphReportsTab)
        report.draw(self.equation)
        reportName = "Absolute Error"
        graphReportsTab.AddPage(report, reportName)
        self.graphReportsListForPDF.append([report.figure, reportName])

        report = reports.AbsoluteErrorHistogram(graphReportsTab)
        report.draw(self.equation)
        reportName = "Absolute Error Histogram"
        graphReportsTab.AddPage(report, reportName)
        self.graphReportsListForPDF.append([report.figure, reportName])

        if self.equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = reports.PercentErrorGraph(graphReportsTab)
            report.draw(self.equation)
            reportName = "Percent Error"
            graphReportsTab.AddPage(report, reportName)
            self.graphReportsListForPDF.append([report.figure, reportName])
     
            report = reports.PercentErrorHistogram(graphReportsTab)
            report.draw(self.equation)
            reportName = "Percent Error Histogram"
            graphReportsTab.AddPage(report, reportName)
            self.graphReportsListForPDF.append([report.figure, reportName])
       
        textReportsTab = wx.Notebook(self)
        self.AddPage(textReportsTab, "Text Reports")
        
        report = reports.CoefficientAndFitStatistics(textReportsTab, self.equation)
        reportName = "Coefficient And Fit Statistics"
        textReportsTab.AddPage(report, reportName)
        self.textReportsListForPDF.append([str(report.text.GetValue()), reportName])
        
        report = reports.Coefficients(textReportsTab, self.equation)
        reportName = "Coefficient Listing"
        textReportsTab.AddPage(report, reportName)
        self.textReportsListForPDF.append([str(report.text.GetValue()), reportName])
        
        report = reports.DataArrayStatistics(textReportsTab, 'Absolute Error Statistics', self.equation.modelAbsoluteError)
        reportName = "Absolute Error Statistics"
        textReportsTab.AddPage(report, reportName)
        self.textReportsListForPDF.append([str(report.text.GetValue()), reportName])
        
        if self.equation.dataCache.DependentDataContainsZeroFlag != 1:
            report = reports.DataArrayStatistics(textReportsTab, 'Percent Error Statistics', self.equation.modelPercentError)
            reportName = "Percent Error Statistics"
            textReportsTab.AddPage(report, reportName)
            self.textReportsListForPDF.append([str(report.text.GetValue()), reportName])

        sourceCodeTab = wx.Notebook(self)
        self.AddPage(sourceCodeTab, "Source Code")

        report = reports.SourceCode(sourceCodeTab, self.equation, 'CPP')
        reportName = "C++"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])

        report = reports.SourceCode(sourceCodeTab, self.equation, 'CSHARP')
        reportName = "CSHARP"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])
    
        report = reports.SourceCode(sourceCodeTab, self.equation, 'VBA')
        reportName = "VBA"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])
    
        report = reports.SourceCode(sourceCodeTab, self.equation, 'PYTHON')
        reportName = "PYTHON"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])
    
        report = reports.SourceCode(sourceCodeTab, self.equation, 'JAVA')
        reportName = "JAVA"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])
    
        report = reports.SourceCode(sourceCodeTab, self.equation, 'JAVASCRIPT')
        reportName = "JAVASCRIPT"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])
    
        report = reports.SourceCode(sourceCodeTab, self.equation, 'JULIA')
        reportName = "JULIA"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])
    
        report = reports.SourceCode(sourceCodeTab, self.equation, 'SCILAB')
        reportName = "SCILAB"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])
    
        report = reports.SourceCode(sourceCodeTab, self.equation, 'MATLAB')
        reportName = "MATLAB"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])

        report = reports.SourceCode(sourceCodeTab, self.equation, 'FORTRAN90')
        reportName = "FORTRAN90"
        sourceCodeTab.AddPage(report, reportName)
        self.sourceCodeReportsListForPDF.append([str(report.text.GetValue()), reportName])

        # equation list
        dim = self.equation.GetDimensionality()
        equationList = reports.EquationList(self, dim)
        self.AddPage(equationList, "List Of Standard " + str(dim) + "D Equations")

        # additional information
        additionalInfoTab = wx.Notebook(self)
        self.AddPage(additionalInfoTab, "Additional Information")

        info = reports.AdditionalInfo(additionalInfoTab, AdditionalInfo.history)
        additionalInfoTab.AddPage(info, "Fitting History")

        info = reports.AdditionalInfo(additionalInfoTab, AdditionalInfo.author)
        additionalInfoTab.AddPage(info, "Author History")

        info = reports.AdditionalInfo(additionalInfoTab, AdditionalInfo.links)
        additionalInfoTab.AddPage(info, "Web Links")

        # additional information
        pdfPanel = wx.Panel(self, id=wx.ID_ANY)
        self.AddPage(pdfPanel, "Save To PDF File")

        btnCreatePDF = wx.Button(pdfPanel, -1, "Save To PDF")
        self.Bind(wx.EVT_BUTTON, self.createPDF, btnCreatePDF)


    def createPDF(self, evt):
        try:
            import reportlab
        except:
            wx.MessageBox("\nCould not import reportlab.\n\nPlease install using the command\n\n'pip3 install reportlab'", "Error")
            return

        fd =wx.FileDialog(self, "PDF file name", "", "",
                                "PDF files (*.pdf)|*.pdf", wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
                                
        fName = ''
        if fd.ShowModal() != wx.CANCEL:
            fName = fd.GetPath()
        if fName:
            from . import pdfCode
            pdfCode.CreatePDF(fName,
                              self.equation,
                              self.graphReportsListForPDF,
                              self.textReportsListForPDF,
                              self.sourceCodeReportsListForPDF
                              )
            wx.MessageBox("\nSuccessfully created PDF file.", "Success")



# see the included wxNestedTabsExample.py file
class ResultsFrame(wx.Frame):
    def __init__(self, parent, msg, caption,
                 pos=wx.DefaultPosition, size=(900,700),
                 style=wx.DEFAULT_DIALOG_STYLE | wx.RESIZE_BORDER, equation=None):
        wx.Frame.__init__(self, parent, -1, caption, pos, size, style)
        self.CenterOnParent()

        panel = wx.Panel(self)
    
        topLevelResultsNotebook = TopLevelResultsNotebook(panel, equation)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topLevelResultsNotebook, 1, wx.ALL|wx.EXPAND, 5)
        panel.SetSizer(sizer)
        self.Layout()



# Code taken from wx-3.0-gtk2/wx/lib/dialogs.py
class StatusDialog(wx.Dialog):
    def __init__(self, parent, msg, caption,
                 pos=wx.DefaultPosition, size=(500,300),
                 style=wx.DEFAULT_DIALOG_STYLE):
        wx.Dialog.__init__(self, parent, -1, caption, pos, size, style)
        self.CenterOnParent()
        self.text = wx.TextCtrl(self, -1, msg, style=wx.TE_MULTILINE | wx.TE_READONLY)
