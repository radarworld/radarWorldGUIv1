from tkinter import *
#from tkinter import Tk, Frame, Menu, messagebox, W, E, N, S, LabelFrame
from tkinter.ttk import Separator, Style, Combobox
from tkinter.scrolledtext import ScrolledText
import sys
import datetime

from radarControls import *

import matplotlib.pyplot

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

#create MyWindow class inheriting from tk.Frame
class MainWindow(Frame):
    
    #__init__ is called when ever an object of the class is constructed.
    def __init__(self, topWindow):
        #construct the main (top) window
        Frame.__init__(self, topWindow)
        
        #set topWindow to XGA resolution
        #topWindow.geometry('%dx%d' % (1024, 768))
        topWindow.state('zoomed')

        #definte winow title
        topWindow.title("RadarWorld1")

        #define rows and cols for the frames and widgets
        topWindow.columnconfigure(0, weight=20)
        topWindow.columnconfigure(1, weight=80)
        topWindow.rowconfigure(0, weight=90)
        topWindow.rowconfigure(1, weight=3)
        topWindow.rowconfigure(2, weight=1)
        topWindow.configure(background='green', relief='sunken', borderwidth=5)
        
        #define LEFT SIDE FRAME in row=col=0 to place the controls
        #Two Columns and as many rows as needed
                      # +--------++----------------+
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # |þþþþþþþþ||                |
                      # +--------++----------------+
                      # +--------------------------+
                      # |                          |
                      # +--------------------------+
                      # +--------++----------------+
                      # +--------++----------------+
        leftSideControlsFrame = LabelFrame(topWindow, bd=3, relief=GROOVE, text= "Radar Controls",
                                           background='yellow')
        leftSideControlsFrame.grid(row=0, column=0, sticky = W+E+N+S)
        leftSideControlsFrame.columnconfigure(0, weight=1)
        leftSideControlsFrame.rowconfigure(0, weight=1)
        leftSideControlsFrame.rowconfigure(1, weight=1)
        leftSideControlsFrame.rowconfigure(2, weight=98)
        #LEFT SIDE FRAME ELEMENTS:
        #LEFT SIDE FRAME ELEMENT 1: widget at row=0, col=0:
        spaceHolder = Label(leftSideControlsFrame, text="Avaiable Interfaces:",
                            background=leftSideControlsFrame['background'], bd=1, relief=FLAT, anchor=W)
        spaceHolder.grid(row=0, column=0, padx=10, pady=0, sticky=W+N+E)
        #LEFT SIDE FRAME ELEMENT 2: combobox for serial port list 
        self.serialPortCmbBox = Combobox(leftSideControlsFrame, values=serialSystemClass.getSerialPorts(),
                                         background=leftSideControlsFrame['background'])
        self.serialPortCmbBox.current(0)
        self.serialPortCmbBox.grid(row=1, column=0, padx=0, pady=0, columnspan=2, sticky = W+E+N+S)
        self.serialPortCmbBox.bind('<<ComboboxSelected>>', self.on_serialPortCmbBox_select)
    
        #define RIGHT SIDE FRAME inside row=0 col=1 for the figures
                             #+--------++----------------+
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #|        ||þþþþþþþþþþþþþþþþ|
                     #+--------++----------------+
                     #+--------------------------+
                     #|                          |
                     #+--------------------------+
                     #+--------++----------------+
                     #+--------++----------------+
        rightSideControlsFrame = LabelFrame(topWindow, bd=3, relief=GROOVE, text= "Radar Figures", background='blue')
        rightSideControlsFrame.grid(row=0, column=1, sticky = W+E+N+S)
        rightSideControlsFrame.columnconfigure(0, weight=1) # an empty column must be defined for the widgets
        #RIGHT SIDE FRAME ELEMENTS:
        #RIGHT SIDE FRAME ELEMENT 1: widget at row=0, col=1, canvas for graph:
        FigureRightSide = Figure() # create a figure object
        self.ax1 = FigureRightSide.add_subplot(2, 1, 1)
        self.ax2 = FigureRightSide.add_subplot(2, 1, 2)
        #link figure to canvas and display
        canvasForGraph = FigureCanvasTkAgg(FigureRightSide, master=rightSideControlsFrame) #create canvas for figure int the frame
        canvasForGraph.get_tk_widget().grid(sticky=S+W+N+E)


        
        #MIDDLE FRAME for Log window:
                   #+--------++----------------+
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #+--------++----------------+
                   #+--------------------------+
                   #|þþþþþþþþþþþþþþþþþþþþþþþþþþ|
                   #+--------------------------+
                   #+--------++----------------+
                   #+--------++----------------+
        logFrame = LabelFrame(topWindow, bd=3, relief=GROOVE, text= "Log messages", background='pink')
        logFrame.grid(row=1, column=0, columnspan=2,  sticky = W+E+N+S)
        logFrame.columnconfigure(0, weight=1) # an empty column must be defined for the widgets
        
        #MIDDLE FRAME ELEMENT1: Log Window at row=0, col=0
        scrolled_text = ScrolledText(logFrame, height=5)
        scrolled_text.configure(font='TkFixedFont')
        scrolled_text.insert(END, "hello")
        scrolled_text.grid(row=0, column=0, sticky = W+E+N+S)

        #STATUS BAR RIGHT:
                   #+--------++----------------+
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #+--------++----------------+
                   #+--------------------------+
                   #|                          |
                   #+--------------------------+
                   #+--------++----------------+
                   #|þþþþþþþþ||                |
                   #+--------++----------------+
        #STATUS BAR RIGHT ELEMENT 1: text at topwindow(row=2, col=0)
        self.statusbarText=StringVar()
        statusBar = Label(topWindow, textvariable=self.statusbarText, bd=5, relief=SUNKEN, anchor=W, fg="blue4", bg ="gray80")
        statusBar.grid(row=2, column=0,  sticky = W+E+N+S)
        statusBar.after(1000, self.updateStatusBar)

        #STATUS BAR RIGHT:
                   #+--------++----------------+
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #|        ||                |
                   #+--------++----------------+
                   #+--------------------------+
                   #|                          |
                   #+--------------------------+
                   #+--------++----------------+
                   #|        ||þþþþþþþþþþþþþþþþ|                |
                   #+--------++----------------+
        #STATUS BAR LEFT ELEMENT 1: Clock at topwindow(row=2, col=1)
        self.clockText=StringVar()
        clock = Label(topWindow, textvariable=self.clockText, bd=0, relief=SUNKEN, anchor=E, fg="black",
                      bg =leftSideControlsFrame['background'])
        clock.grid(row=2, column=1, sticky = W+E+N+S)
        clock.after(1000, self.updateClock)
        

              
        #* * * * * * Menu * * * * * *
        # Menubar:
        menubar = Menu(topWindow)
        topWindow.config(menu=menubar)
        # Menubar - File Menu:
        fileMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=fileMenu)
        fileMenu.add_command(label="Open", command=MainWindow.doNothing)        
        fileMenu.add_separator()
        fileMenu.add_command(label="Exit", command=MainWindow.quit)
        # Menubar - Edit Menu:
        editMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Edit", menu=editMenu)
        editMenu.add_command(label="Settings", command=MainWindow.doNothing) 
        # Menubar - Help Menu:
        helpMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpMenu)
        helpMenu.add_command(label="About", command=MainWindow.helpMenu_About)

        #* * * * * * Graph * * * * * *
        # Menubar:
        

    #* * * * * * functions to serve the Ui * * * * * *
    def helpMenu_About():
        messagebox.showinfo("About RadarWorld", "v0.0")
     
    def doNothing():
        pass
    #close the GUI (on file-exit, or window close)
    def quit():
        #loggerFunctions.closeLoggerFile()
        #serialSystemClass.closeSerialPort(MainWindow(root).serialPortCmbBox.get())
        root.destroy()
    def on_serialPortCmbBox_select(self, event=None):
        pass
        #get selection from combobox and display in log window
        #print("comboboxes:", self.serialPortCmbBox.get())
        #log_contents = loggerFunctions.sendToLogger('Selected:' + str(self.serialPortCmbBox.get()))
        #MainWindow(root).updateLogWindow(log_contents)
        
        #open serial port by with the serialUtilsClass __init__
        #ser = serialUtilsClass(self.serialPortCmbBox.get())
     
        #portList=serialSystemClass.getSerialPorts()
        #msg= serialSystemClass.openSerialPort(self.serialPortCmbBox.get())
        #log_contents = log_contents +msg
        #MainWindow(root).updateLogWindow(log_contents)
        

        
    #update log window with current message  
    def updateLogWindow(self, logTextToAppend):
        pass
        #self.scrolled_text.insert(END, logTextToAppend)
        #self.scrolled_text.see(END)
        #self.scrolled_text.grid(row=1, column=0, columnspan=2, sticky = W+E+N+S)
        
    #update the clock in given intervals with the after() function
    def updateClock(self):
        now = datetime.datetime.now()
        clockBarCurrentTime=now.strftime("%d.%m.%Y.   %H:%M:%S")
        self.clockText.set(''.join(clockBarCurrentTime))
        self.after(1000,self.updateClock)
      

    def updateStatusBar(self):
        #create the list to store the message
        #statusBarTextList=list()
        #statusBarCurrentMsg="RadarWorld 1.0"
        #place empty chars to the end of the message
        #statusBarCurrentMsgExtended=statusBarCurrentMsg.ljust(len(statusBarCurrentMsg)+1)
        #statusBarTextList.append(statusBarCurrentMsgExtended)
        #add additional text
        #statusBarCurrentState="Status: Connected via SER"
        #statusBarCurrentMsgExtended=statusBarCurrentState.ljust(len(statusBarCurrentState)+0)       
        #statusBarTextList.append(statusBarCurrentMsgExtended)
        #update the status bar with the current text
        #self.statusbarText.set(''.join(statusBarTextList))
        now = datetime.datetime.now()
        clockBarCurrentTime=now.strftime("%d.%m.%Y.   %H:%M:%S")
        self.statusbarText.set(''.join(clockBarCurrentTime))

        
        #call the own function after 1 sec
        self.after(1050,self.updateStatusBar)

    def updateGraph(self,nbytes, yValues):
        xValuesRawData = np.linspace(0, nbytes, nbytes +1)
        #yValues = np.random.rand(11)
        #yValues=np.linspace(0, 10, 11)
        print(xValuesRawData)
        print(yValues)
        self.ax1.plot(xValuesRawData, yValues, lw=2, color='red', label='rawI1')
        #self.ax1.clear()
        #self.ax2.clear()
        #xValuesRawData  = np.linspace(0, rawI1.size-1, rawI1.size)
        #ax1.plot(xValuesRawData, rawI1[0,:], lw=2, color='red', label='rawI1')
        #ax1.plot(xValuesRawData, rawQ1[0,:], lw=2, color='blue', label='rawQ1')
        self.ax1.set_title("raw data")
        self.ax1.set_xlabel('time')
        self.ax1.set_ylabel('amplitude')
        self.ax1.legend()

        #plot fft magnitude
        #xValuesMagData  = np.linspace(0, FFTmag.size-1, FFTmag.size)
        #ax2.plot(xValuesMagData, FFTmag[0,:], lw=2, color='green', label='fft mag')
        #ax2.set_title('fft mag')
        #ax2.set_xlabel('freq')
        #ax2.set_label('amplitude')
        #ax2.legend()

        
        
        


        

# * * * * * * * * * * * * * * * Main Program Starts Here * * * * * * * * * * * * * * * 
if __name__=="__main__":
    #crate the root window
    root = Tk()
    application=MainWindow(root)

    #Geometry manager Pack. Pack a widget in the parent widget with the grid() builder.
    MainWindow(root).grid()
    ser = serialUtilsClass(MainWindow(root).serialPortCmbBox.get())
    serialMsgStatus, nbytes, rawI1 = ser.parseUartFrame()
    
    if ser:
        pass
       # MainWindow(root).updateGraph(nbytes,rawI1)
        
        

   # print(serialUtilsClass.testWithRandomData())
   # x, y = serialUtilsClass.supplyRandomData()
   # print(serialUtilsClass.supplyRandomData())
   # MainWindow(root).updateGraph(x,y)

  

#tk.mainloop() blocks. What that means is that execution of your python program halts there
    root.mainloop()


'''
#functions which are running periodically

MainWindow(root).updateClock()

#setup a python logger object
loggerFunctions.buildLogger()

#update the log window through the python logger
log_contents = loggerFunctions.sendToLogger('Program started...')
MainWindow(root).updateLogWindow(log_contents)

#detect and display serial port list
str1 ='\n' + '\n'.join(map(str, serialSystemClass.getSerialPorts()))
log_contents = loggerFunctions.sendToLogger("\nSerial Ports found:" + str1 +'\n'+"Select serial port!")
MainWindow(root).updateLogWindow(log_contents)
#make default serial port selection
MainWindow(root).on_serialPortCmbBox_select()

#tmp:::::::::
#open serial port by with the serialUtilsClass __init__
ser = serialUtilsClass(MainWindow(root).serialPortCmbBox.get())



    

#ser.parseUartFrame()
#MainWindow(root).updateGraph()
print("update graph finished")

'''

#Geometry manager will pack the widgets 
#MainWindow(root).grid()

#tk.mainloop() blocks. The execution will stop here.
#root.mainloop()



