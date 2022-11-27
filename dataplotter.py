import tkinter as tk #for creating the gui
import tkinter.filedialog #for browsing and opening files
import pandas as pd #for handling input data as a dataframe
from matplotlib.figure import Figure #for plotting
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk) #for integrating plot (figure and toolbar) into tkinter
import slider2scale #for using the slider with 2 handles

class DataPlotter(object):
    def __init__(self, parent):
        self.frame = tk.Frame(parent)
        self.frame.grid(row=0, column=0)
        tk.Label(self.frame, text="DataPlotter", justify=tk.CENTER).grid(row=0, column=0, sticky=tk.W+tk.E)
        
        self.mainMenuFrame = tk.Frame(self.frame)
        self.mainMenuFrame.grid(row=1, column=0)
        self.buttonPlot = tk.Button(master=self.mainMenuFrame, text="Load data", command=self.loadData)
        self.buttonPlot.grid(row=0, column=0)
        self.buttonPlot = tk.Button(master=self.mainMenuFrame, text="Plot data", command=self.plotData)
        self.buttonPlot.grid(row=0, column=1)
        
        self.plotDataFrame = tk.Frame(self.frame)
        self.plotDataFrame.grid(row=2, column=0)
        self.sliderFrame = tk.Frame(self.plotDataFrame)
        self.sliderFrame.grid(row=0, column=0, columnspan=3)#, sticky=tk.W+tk.E)
        self.plotFrame = tk.Frame(self.frame)
        self.plotFrame.grid(row=0, column=1, rowspan=10)
        self.slider = None
        self.quantities = {}
        
        self.plotColors = {'Temperature' : 'red',
                           'Relative humidity' : 'blue',
                           'Soil moisture' : 'green',
                           'CO2 concentration' : 'grey',
                           } #to plot more than one quantities on the same graph

    def checkbuttonChangeEvent(self, mark, quantity):
        for key, value in self.checkbuttonsXY.items():
            if key != quantity:
                value[mark].set(0)
        if mark == "X":
            defaultbg = self.frame.cget('bg')
            var1, var2 = 0, self.dataFrame.shape[0] - 1
            self.slider = slider2scale.Slider2Scale(self.sliderFrame, defaultbg, var1, var2)
            self.slider.canvas.bind("<ButtonRelease-1>", self.plotData)

    def getQuantityForMark(self, mark):
        for key, value in self.checkbuttonsXY.items():
            if value[mark].get() == 1:
                return key
        return None
    
    def loadData(self):
        if self.plotDataFrame:
            if self.slider:
                self.slider.destroy()
            for child in self.plotDataFrame.winfo_children():
                if not isinstance(child, tkinter.Frame):
                    child.destroy()
        if self.plotFrame:
            for child in self.plotFrame.winfo_children():
                child.destroy()
            
        self.quantities = {}
        #load data
        filename = tk.filedialog.askopenfilename()
        if filename == "":
            return
        self.dataFrame = pd.read_csv(filename, delimiter=';')
        self.header = self.dataFrame.columns.values.tolist()
##        print(f"self.header: {self.header}")

        self.checkbuttonsXY = {}
        tk.Label(self.plotDataFrame, text="x").grid(row=1, column=1)#, sticky=tk.W)
        tk.Label(self.plotDataFrame, text="y").grid(row=1, column=2)
        for index, quantity in enumerate(self.header, 2):
            self.checkbuttonsXY[quantity] = {}
            tk.Label(self.plotDataFrame, text=quantity).grid(row=index, column=0, sticky=tk.W)
            mark = "X"
            checkbuttonXvar = tk.IntVar()
            checkbuttonX = tk.Checkbutton(self.plotDataFrame, variable=checkbuttonXvar, command=lambda x=mark, y=quantity: self.checkbuttonChangeEvent(x, y))
            checkbuttonX.grid(row=index, column=1)
            self.checkbuttonsXY[quantity][mark] = checkbuttonXvar
            mark = "Y"
            checkbuttonYvar = tk.IntVar()
            checkbuttonY = tk.Checkbutton(self.plotDataFrame, variable=checkbuttonYvar, command=lambda x=mark, y=quantity: self.checkbuttonChangeEvent(x, y))
            checkbuttonY.grid(row=index, column=2)
            self.checkbuttonsXY[quantity][mark] = checkbuttonYvar
            
    def plotData(self, *args): #*args is needed for auto plot when x is changed
        self.figure = Figure(figsize=(7, 5), dpi=100)
        self.axis = self.figure.add_subplot(111)

        #plot one quantity againts another
        quantityX = self.getQuantityForMark("X")
        quantityY = self.getQuantityForMark("Y")
        if quantityX == None or quantityY == None:
            return
        x1, x2 = self.slider.var1.get(), self.slider.var2.get()
        tickDelta = 10 if abs(x2-x1) > 10 else 1
        if isinstance(self.dataFrame[quantityX][0], str):
            xtickLocations = [i for i in range(0, x2-x1, tickDelta)]
        else:
            xtickLocations = [self.dataFrame[quantityX][i] for i in range(0, x2-x1, tickDelta)]
        self.axis.set_xticks(xtickLocations)
        xtickLabels = [str(self.dataFrame[quantityX][i]).replace(' ', '\n') for i in range(x1, x2, tickDelta)]
        self.axis.set_xticklabels(xtickLabels)
##        print(f"xtickLocations: {xtickLocations}")
##        print(f"xtickLabels: {xtickLabels}")
        self.axis.plot(self.dataFrame[quantityX][x1:x2], self.dataFrame[quantityY][x1:x2], label=quantityY + " (" + quantityX + ")", color="red")

        self.figure.legend(loc='upper right', frameon=False)
        self.canvas = FigureCanvasTkAgg(self.figure, master=self.plotFrame) #creating the Tkinter canvasc ontaining the Matplotlib figure
        self.canvas.draw()
        self.canvas.get_tk_widget().grid(row=1, column=0, columnspan=10) #placing the canvas on the Tkinter window
        self.toolbar = NavigationToolbar2Tk(self.canvas, self.plotFrame, pack_toolbar=False)
        self.toolbar.update() #for initialization purposes
        self.toolbar.grid(row=2, column=0, columnspan=10) #placing the toolbar on the Tkinter window
        
    
if __name__ == "__main__":
    root = tk.Tk()
    root.title("DataPlotter")
    dataPlotter = DataPlotter(root)
    root.mainloop()
