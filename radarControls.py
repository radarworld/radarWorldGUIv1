import serial.tools.list_ports
from loggingFunctionsForRadar import *
import inspect
import logging
import sys
import glob
import serial

import array
import struct
import codecs
import numpy as np
from colorama import Fore, Style #Colorama: Cross-platform colored terminal text.
import config # access to the global varaibles for display
import processingFucntionsForRadar
from main import MainWindow





from loggingFunctionsForRadar import *

#variables to store the parsed UART frame
SD           = np.uint8(0)                      #start delimiter (0xA1, d162)
FC           = np.uint8(0)                      #function code (0xE0, d224)
modulation   = np.uint8(0)                      #0-doppler, 1-FMCW
numberSample = np.uint16(0)                     #numer of samples for single measurement
rawI1        = np.zeros((1,128), dtype=np.int16)#adc values for raw I ch1
rawQ1        = np.zeros((1,128), dtype=np.int16)#adc values for raw Q ch1
FFTmag       = np.zeros((1,128), dtype=np.int32)#FFT magnitude
CS           = np.uint8(0)                      #checksum: sum of byte2 to byte1029 &0x000000FF
ED           = np.uint8(0)                      #end delimiter (0x16, d22)


class serialSystemClass(object):
       
    def getSerialPorts():
        """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        #if no serial port found (list empty) send back a value
        if not result:
            result = ["no serial port"]
        
        return result
class serialUtilsClass(object):

    
    def __init__(self, serialPort):
        self.ser = serial.Serial(port=serialPort,
                             baudrate=115200,
                             bytesize=serial.EIGHTBITS,
                             parity=serial.PARITY_NONE,
                             stopbits=serial.STOPBITS_ONE)
        
    def sendData(self, data):        
        self.ser.write(b'\x0D')
        
    def recieveData(self, numberOfBytes):
        return self.ser.read(numberOfBytes)

    def dumpArray(arr):
        print('\n'.join([
            ' '.join(['{:02d}'.format(elem) for elem in row])
            for row in arr
            ]))

    
    def parseUartFrame(self):
        #read the complete frame from sensor
        tmp=bytes(self.ser.read_until(b'\0x16', 1031))
        print("uart frame length:", len(tmp))
        print("start delimiter (162):", tmp[0])
        print("end delimiter (22):",tmp[1030])
        #check SD(162, 0xA1) and ED(22, 0x16) for frame errors
        if (tmp[0] !=162) or (tmp[1030] !=22):
            print("-----------------------------ERROR!!!!!!-retry")
            self.ser.reset_input_buffer()
            while (tmp[0] !=162) or (tmp[1030] !=22):
                #read a new frame, replace the old one
                tmp=bytes(self.ser.read_until(b'\0x16', 1031))
                print("new fream read....")
            else:
                print("-----correct frame recieved...")
                print("uart frame length:", len(tmp))
                print("start delimiter (162):", tmp[0])
                print("end delimiter (22):",tmp[1030])
                
        #create empty numPy array (uint8) 
        uartFrame = np.zeros((1,1031), dtype=np.uint8)

        #copy uart values to numPy array
        for i in range(0, len(tmp)-1, 1):
            uartFrame[0, i] = tmp[i]
            
        print("type:", type(uartFrame))
        print("ndim:", uartFrame.ndim)
        print("shape:", uartFrame.shape)
        print("size:", uartFrame.size)
        print("dtype:", uartFrame.dtype)
        print("itemsize:", uartFrame.itemsize, "bytes")
        print("nbytes:", uartFrame.nbytes, "bytes")

        #serialUtilsClass.dumpArray(uartFrame)
        
        #SD:
        SD = np.uint8(uartFrame[0,0])
        print("SD:", SD)
        
        #FC:
        FC = np.uint8(uartFrame[0,1])
        print("FC:", FC)
        
        #Modulation:
        modulation = np.uint8(uartFrame[0,2])
        print("modulation:", modulation)
        
        #numberSample: number of captured samples for single measurement
        numberSample = np.uint16(256*uartFrame[0,3] + uartFrame[0,4])        
        print("numbersample:",numberSample)
        print("type:", type(numberSample))
        print("rawI1: - - - - ")

        #rawI1:
        tmp = np.int16(0)
        cnt = 0
        for i in range(5, 260, 2):
            tmp = uartFrame[0, i] * 256
            tmp = tmp + uartFrame[0, i+1]
            rawI1[0,cnt] = tmp
            #print("cnt:", cnt, "rawI1:",  rawI1[0,cnt])
            cnt = cnt + 1
        #print("RawI[]:", end='\n')
            print("rawI1 type:", type(rawI1))
        #serialUtilsClass.dumpArray(rawI1)

        #rawQ1:
        #serialUtilsClass.dumpArray(rawQ1)
        tmp = np.int16(0)
        cnt = 0
        for i in range(261, 516, 2):
            tmp = uartFrame[0, i] * 256
            tmp = tmp + uartFrame[0, i+1]
            rawQ1[0,cnt] = tmp
            #print("cnt:", cnt, "rawQ1:",  rawQ1[0,cnt])
            cnt = cnt + 1
        #print("RawQ[]:", end='\n')
        #serialUtilsClass.dumpArray(rawQ1)

        #FFTmag:
        #serialUtilsClass.dumpArray(FFTmag)
        tmp = np.int32(0)
        cnt = 0
        for i in range(517, 1028, 4):
            tmp = uartFrame[0, i+0] << 24  
            tmp = uartFrame[0, i+1] << 16
            tmp = uartFrame[0, i+2] << 8
            tmp = uartFrame[0, i+3] << 0
            FFTmag[0,cnt] = tmp
            #print("FFTmag:", cnt, "FFTmag:",  FFTmag[0,cnt])
            cnt = cnt + 1
        #print("FFTmag[]:", end='\n')
        #serialUtilsClass.dumpArray(FFTmag)

        #CS, chekcsum=sum of byte2 to byte1029 &0x000000FF:
        CS = np.uint8(uartFrame[0,1029])
        print("CS:", CS)

        #ED, end delimiter (22=0x16):
        ED = np.uint8(uartFrame[0,1030])
        print("ED:", ED)
        return 1, uartFrame.nbytes, rawI1

    def testWithRandomData():
        return 1
    def supplyRandomData():
        xValuesRawData = np.linspace(0, 10, 11)
        yValues = np.random.rand(11)
        return xValuesRawData, yValues
    


        
        

        
            

        

        
        
        


        
    
    
        
        

        
        
        

    

    
    
