from tkinter import *
from tkinter import Tk, Frame, Menu, messagebox, W, E, N, S
from tkinter.ttk import Separator, Style, Combobox
from tkinter.scrolledtext import ScrolledText
from radarControls import *
from loggingFunctionsForRadar import *
import radarControls
import logging
import sys
import datetime
import config # access to the global varaibles for display

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



import numpy as np






#create MyWindow class inheriting from tk.Frame
class MainWindow(Frame):
    
    #__init__ is called when ever an object of the class is constructed.
    def __init__(self, topWindow):
        #construct the main (top) window
        Frame.__init__(self, topWindow)
        self.master  = topWindow

        #set topWindow to XGA resolution
        topWindow.geometry('%dx%d' % (1024, 768))
        #topWindow.minsize(1152,864)

        #definte winow title
        self.master.title("RadarWorld")

        #define the ratio of the columns and rows, grid geom. manager will bu used
        topWindow.columnconfigure(0, weight=20)
        topWindow.columnconfigure(1, weight=80)
        topWindow.rowconfigure(0, weight=90)
        topWindow.rowconfigure(1, weight=3)
        topWindow.rowconfigure(2, weight=1)
        
        #define left side frame INSIDE row=col=0 to place the controls
        #Two Columns and as many rows as needed
        leftSideControlsFrame = LabelFrame(topWindow, bd=3, relief=GROOVE, text= "Radar Controls")
        leftSideControlsFrame.grid(row=0, column=0, sticky = W+E+N+S)
        leftSideControlsFrame.columnconfigure(0, weight=1)
        leftSideControlsFrame.rowconfigure(0, weight=1)
        leftSideControlsFrame.rowconfigure(1, weight=1)
        leftSideControlsFrame.rowconfigure(2, weight=98)        

        #define right side frame inside row=col=1 to place the controls
        rightSideControlsFrame = Frame(topWindow)
        rightSideControlsFrame.grid(row=0, column=1, sticky = W+E+N+S)
        rightSideControlsFrame.columnconfigure(0, weight=1) # an empty column must be defined for the widgets

        #build the topwindow
        self.grid(sticky = W+E+N+S)
              
        #* * * * * * define the Ui elements * * * * * *
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
        
        # - - - - - Left side elements (controls) - - - - - -         
        spaceHolder = Label(leftSideControlsFrame, text="Avaiable Interfaces:", bd=1, relief=FLAT, anchor=W)
        spaceHolder.grid(row=0, column=0, padx=10, pady=0, sticky=W+N+E)

        
        self.serialPortCmbBox = Combobox(leftSideControlsFrame, values=serialSystemClass.getSerialPorts())
        self.serialPortCmbBox.current(0)
        self.serialPortCmbBox.grid(row=1, column=0, padx=0, pady=0, columnspan=2, sticky = W+E+N+S)
        self.serialPortCmbBox.bind('<<ComboboxSelected>>', self.on_serialPortCmbBox_select)
        
        # - - - - - Right side elements (graph) - - - - - - -
        #draw the canvas into the frame. Get max frame size after update()
        #FigureRightSide = plt.Figure(dpi=100) #create new figure from matplotlib.pyplt (plt) lib
        
        self.FigureRightSide, (self.ax1, self.ax2) = plt.subplots(2, 1)
        self.Readings=5;
        

        self.canvasForGraph = FigureCanvasTkAgg(self.FigureRightSide, master=rightSideControlsFrame) #create canvas for figure int the frame

        self.canvasForGraph.get_tk_widget().grid(sticky = W+E+N+S)

        t = np.arange(0, 100, .01) # time data
        self.ax1.plot(t, 50 * np.sin(2 * np.pi * t))
        self.ax2.plot(t, 1 * np.sin(2 * np.pi * t))
        #self.FigureRightSide.ax2.clear()
        #self.ax2.clear()
        __dir__(MainWindow)
                





        # Log Window:
        self.scrolled_text = ScrolledText(topWindow, height=5)
        self.scrolled_text.configure(font='TkFixedFont')
        self.scrolled_text.tag_config('INFO', foreground='black')
        #self.scrolled_text.insert(END, "hello")
        

        # Status bar:
        self.statusbarText=StringVar()
        self.statusBar = Label(topWindow, textvariable=self.statusbarText, bd=1, relief=SUNKEN, anchor=W)

        # Clock:
        self.clockText=StringVar()
        self.clock = Label(topWindow, textvariable=self.clockText, bd=1, relief=SUNKEN, anchor=E)



    #* * * * * * functions to serve the Ui * * * * * *
    def helpMenu_About():
        messagebox.showinfo("About RadarWorld", "v0.0")
     
    def doNothing():
        pass
    #close the GUI (on file-exit, or window close)
    def quit():
        loggerFunctions.closeLoggerFile()
        #serialSystemClass.closeSerialPort(MainWindow(root).serialPortCmbBox.get())
        root.destroy()
    def on_serialPortCmbBox_select(self, event=None):
        #get selection from combobox and display in log window
        print("comboboxes:", self.serialPortCmbBox.get())
        log_contents = loggerFunctions.sendToLogger('Selected:' + str(self.serialPortCmbBox.get()))
        MainWindow(root).updateLogWindow(log_contents)
        
        #open serial port by with the serialUtilsClass __init__
        #ser = serialUtilsClass(self.serialPortCmbBox.get())
        #ser.sendData(7)
        #test = ser.recieveData(5)
        #test=ser.recieveFrame(b'\0x16', 1031)
        #print(len(test))
        
        
        #portList=serialSystemClass.getSerialPorts()
        #msg= serialSystemClass.openSerialPort(self.serialPortCmbBox.get())
        #log_contents = log_contents + msg
        #MainWindow(root).updateLogWindow(log_contents)
        

        
    #update log window with current message  
    def updateLogWindow(self, logTextToAppend):
        self.scrolled_text.insert(END, logTextToAppend)
        self.scrolled_text.see(END)
        self.scrolled_text.grid(row=1, column=0, columnspan=2, sticky = W+E+N+S)
        
    #update the clock in given intervals with the after() function
    def updateClock(self):
        now = datetime.datetime.now()
        clockBarCurrentTime=now.strftime("%d.%m.%Y.   %H:%M:%S")
        self.clockText.set(clockBarCurrentTime)        
        self.clock.grid(row=2, column=1, sticky = W+E+N+S)
        self.after(1000,self.updateClock)
        
        

    def updateStatusBar(self):
        #create the list to store the message
        statusBarTextList=list()
        statusBarCurrentMsg="RadarWorld 1.0"
        #place empty chars to the end of the message
        statusBarCurrentMsgExtended=statusBarCurrentMsg.ljust(len(statusBarCurrentMsg)+1)
        statusBarTextList.append(statusBarCurrentMsgExtended)
        #add additional text
        statusBarCurrentState="Status: Connected via SER"
        statusBarCurrentMsgExtended=statusBarCurrentState.ljust(len(statusBarCurrentState)+0)       
        statusBarTextList.append(statusBarCurrentMsgExtended)
        #update the status bar with the current text
        self.statusbarText.set(''.join(statusBarTextList))
        self.statusBar.grid(row=2, column=0, columnspan=1, sticky = W+E+N+S)
        #call the own function after 1 sec
        self.after(1000,self.updateStatusBar)

    def updateGraph(self):
        t = np.arange(0, 100, .01) # time data
    
        
        self.ax1.clear()
        self.ax2.clear()
        print("self.Readings", self.Readings)
        #self.FigureRightSide, (ax1, ax2) = plt.subplots(2, 1)
        #ax1.plot(t, 500 * np.sin(2 * np.pi * t))
        #ax2.plot(t, 10 * np.sin(2 * np.pi * t))
        #self.FigureRightSide.canvas.draw()

        #self.ax1.line
        #self.line1.set_data(x,y)
    #ax = self.canvas.figure.axes[0]
    #ax.set_xlim(x.min(), x.max())
    #ax.set_ylim(y.min(), y.max())        
    #self.canvas.draw()


        

# * * * * * * * * * * * * * * * Main Program Starts Here * * * * * * * * * * * * * * * 
      
        

#crate the root window
root = Tk()

#functions which are running periodically
MainWindow(root).updateStatusBar()
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

MainWindow(root).updateGraph()
print("update graph finished")

'''
#plot rawI, rawQ
plt.subplot(2, 1, 1)
xValuesRawData  = np.linspace(0, radarControls.rawI1.size-1, radarControls.rawI1.size)



plt.plot(xValuesRawData, radarControls.rawI1[0,:], lw=2, color='red', label='rawI1')
plt.plot(xValuesRawData, radarControls.rawQ1[0,:], lw=2, color='blue', label='rawQ1')
plt.title('raw data')
plt.xlabel('time')
plt.ylabel('amplitude')
plt.legend()
#plot fft magnitude
plt.subplot(2, 1, 2)
xValuesMagData  = np.linspace(0, radarControls.FFTmag.size-1, radarControls.FFTmag.size)
plt.plot(xValuesRawData, radarControls.FFTmag[0,:], lw=2, color='green', label='fft mag')
plt.title('fft mag')
plt.xlabel('freq')
plt.ylabel('amplitude')
plt.legend()
plt.show()

'''







#Geometry manager will pack the widgets 
MainWindow(root).grid()

#tk.mainloop() blocks. The execution will stop here.
root.mainloop()



