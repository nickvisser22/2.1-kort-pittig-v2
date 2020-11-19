import serial
import time
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from functools import partial
COM4 = 0
COM5 = 0
try:
    COM4 = serial.Serial('COM4', 9800)
    COM4.flushInput()
except: 
    print("COM 4 is niet aangesloten")
try:
    COM5 = serial.Serial('COM5', 9800)
    COM5.flushInput()
except: 
    print("COM 5 is niet aangesloten")


global luikDicht
luikDicht = False

def getLuik():
    return(luikDicht)

def setLuik(luik):
    global luikDicht
    luikDicht = luik 

def getData(device):
    ser_bytes = device.readline()
    decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
    return(decoded_bytes)

def gemiddelde(lijst):
    counter = 0
    for i in lijst:
        counter+=i
    return(counter/len(lijst))

def checkdata():
    tempraturen = []
    while True:
        print(getData())
        if len(tempraturen) > 50:
            del tempraturen[0]
            print(gemiddelde(tempraturen))
            if gemiddelde(tempraturen)>150 and getLuik()==False:
                closeWindow()
                print(gemiddelde(tempraturen))
            elif gemiddelde(tempraturen)<125 and getLuik()==True:
                openWindow()
                print(gemiddelde(tempraturen))
        tempraturen.append(getData())

def grafiek(device, device2 = 0, device3 = 0):
    plot_window = 200
    fig, ax = plt.subplots()
    y_var1 = np.array(np.zeros([plot_window]))
    line1, = ax.plot(y_var1)

    if device2 != 0:
        y_var2 = np.array(np.zeros([plot_window]))
        line2, = ax.plot(y_var2)

    axprev = plt.axes([0.7, 0.05, 0.1, 0.075])
    plt.ion()


    while True:
        y_var1 = np.append(y_var1,getData(device))
        y_var1 = y_var1[1:plot_window+1]

        if device2 != 0:        
            y_var2 = np.append(y_var2,getData(device2))
            y_var2 = y_var2[1:plot_window+1]
            line2.set_ydata(y_var2)
        line1.set_ydata(y_var1)
        ax.relim()
        ax.autoscale_view()
        fig.canvas.draw()
        fig.canvas.flush_events()

def closeWindow():
    print(getLuik())
    if getLuik() == False:
        setLuik(True)
        COM5.write(b'H')
        print("Luik gaat dicht")
    else:
        print("Het luik is al dicht zemmer")



def openWindow():
    if getLuik() == True:
        print("test")
        COM5.write(b'D')

        print("Luik gaat open")
        setLuik(False)
    else:
        print("Het luik is al open zabi")

def Devices(device, device2= 0, device3 = 0):
    grafiek(device,device2,device3)


tkWindow = Tk()  
tkWindow.geometry('400x200')  
tkWindow.title('Command control base je weet')
if COM5 != 0 and COM4 !=0:
    Button(tkWindow, command=lambda: Devices(COM5, COM4),text="Alle sensoren live data" ).pack()  

if COM5 != 0:
    Button(tkWindow, command=lambda: Devices(COM5),text="COM5 live data" ).pack()  

if COM4 !=0:
    Button(tkWindow, command=lambda: Devices(COM4),text="COM4 live data" ).pack()  
Button(tkWindow, command=openWindow,text="Open luik" ).pack()  
Button(tkWindow, command=closeWindow, text="luik dicht").pack()  

Button(tkWindow, command=checkdata, text="test dicht").pack()  
Button(tkWindow, text='Quit', command=tkWindow.quit).pack()
# tkWindowafter(2000, checkdata())

tkWindow.mainloop()

# thread1 = Thread(target=tkWindow.mainloop())

# thread1.start()
