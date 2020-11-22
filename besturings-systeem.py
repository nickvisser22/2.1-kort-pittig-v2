# Command control base Python
# Project 2.1
# door Frank Kistemaker en Nick Visser
# p1 -2020


import serial
import time
import csv
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from tkinter import *
from tkinter import ttk

COM4 = 0
COM5 = 0
COM6 = 0

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

try:
    COM6 = serial.Serial('COM6', 9800)
    COM6.flushInput()

except: 
    print("COM 6 is niet aangesloten")    
#Het bovenstaande stuk code, controleert of de Arduino's beschikbaar zijn en maakt de connectie.


global luikDicht
luikDicht = False
# Deze global wordt later gebruikt voor controleren of het luik al dicht is of niet

def getLuik():
    return(luikDicht)


def setLuik(luik):
    global luikDicht
    luikDicht = luik 

# een setter en een getter voor global luik

def getData(device, type):
    if type == 'licht':
        ser_bytes = device.readline()
        decoded_bytes = float(ser_bytes[0:len(ser_bytes)-2].decode("utf-8"))
        return(decoded_bytes)
    elif type == 'temp':
        ser_bytes = device.readline()
        decoded_bytes = ser_bytes[0:5]
        flt = float(decoded_bytes)
        return(flt)
# De bovenstaande functie vraagt om een serial.device en het type, en geeft vervolgens op basis van welk type het is de juiste data terug.
# Door: Frank Kistemaker

def gemiddelde(lijst):
    counter = 0
    for i in lijst:
        counter+=i
    return(counter/len(lijst))
# De bovenstaande functie geeft het gemiddelde van een lijst
# Door: Frank Kistemaker & Nick Visser

def checkdata(licht, tempratuur):
    if licht > 100 and tempratuur >18 and luikDicht == False :
        closeWindow()
    elif licht<100 and tempratuur <20 and luikDicht == True:
        openWindow()
    



def grafiek(device, device2 = 0, device3 = 0):

    plot_window = 150
    y_var1 = np.array(np.zeros([plot_window]))

    if device2 == 0 and device == COM5:
        fig, ax1 = plt.subplots()
        line1, = ax1.plot(y_var1,label="Licht kracht")

    if device2 == 0 and device == COM4:
        fig, ax1 = plt.subplots()
        line1, = ax1.plot(y_var1,label="Tempratuur")

    if device2 != 0 and device3 == 0:
        fig, (ax1, ax2) = plt.subplots(2)
        line1, = ax1.plot(y_var1,label="Licht kracht")
        y_var2 = np.array(np.zeros([plot_window]))
        line2, = ax2.plot(y_var2, label="Tempratuur" )
        ax2.legend(loc="upper right")    
        ax2.legend()

    if device3 != 0:
        fig, (ax1, ax2, ax3) = plt.subplots(3)
        y_var3 = np.array(np.zeros([plot_window]))
        line3, = ax2.plot(y_var3,label="device 3")
        line1, = ax1.plot(y_var1,label="device 1")
        y_var2 = np.array(np.zeros([plot_window]))
        line2, = ax2.plot(y_var2, label="device 2" )
        ax2.legend(loc="upper right")    
        ax2.legend()
        ax3.legend(loc="upper right")    
        ax3.legend()

    plt.ion()
    
    ax1.legend(loc="upper right")    
    ax1.legend()
    counter = 0

    while True:

        y_var1 = np.append(y_var1,getData(device, 'licht'))
        y_var1 = y_var1[1:plot_window+1]

        if device2 != 0:        
            y_var2 = np.append(y_var2,getData(device2, 'temp'))
            y_var2 = y_var2[1:plot_window+1]
            line2.set_ydata(y_var2)

            ax2.relim()
            ax2.autoscale_view()

        if device3 != 0:        
            y_var3 = np.append(y_var3,getData(device3))
            y_var3 = y_var3[1:plot_window+1]
            line3.set_ydata(y_var3)
            ax3.relim()
            ax3.autoscale_view()


        line1.set_ydata(y_var1)
        line1.set_label('test!')
        ax1.relim()
        ax1.autoscale_view()


        fig.canvas.draw()
        if counter == 30:
            checkdata(getData(device, 'licht'),getData(device2, 'temp'))
            counter = 0
        counter +=1    


        fig.canvas.flush_events()
#deze functie kijkt eerst hoeveel devices er mee gegeven zijn in de argumenten en maakt op basis van die info een popup met 1, 2 of 3 grafieken.
#Daarnaast laadt hij elke 30 keer controleren of de tempratuur& de zonnenkracht te warm/koud etc zijn om het luik te openen/sluiten
#Door: Frank Kistemaker 




def closeWindow():
    print(getLuik())
    if getLuik() == False:
        setLuik(True)
        COM5.write(b'H')
        print("Het luik wordt nu gesloten!")

    else:
        print("Het luik was al dicht!")



def openWindow():
    if getLuik() == True:
        COM5.write(b'D')
        print("Het luik wordt nu geopend!")
        setLuik(False)

    else:
        print("Het luik was al open!")

def Devices(device, device2= 0, device3 = 0):
    grafiek(device,device2,device3)


tkWindow = Tk()  
tkWindow.geometry('800x400')  
tkWindow.title('Command control base je weet')
Button(tkWindow, command=lambda: Devices(COM5, COM4, COM6),text="Start programma" ).pack()  
if COM5 != 0:
    Button(tkWindow, command=lambda: Devices(COM5),text="COM5 live data" ).pack()  
if COM4 !=0:
    Button(tkWindow, command=lambda: Devices(COM4),text="COM4 live data" ).pack() 
if COM6 !=0:
    Button(tkWindow, command=lambda: Devices(COM6),text="COM6 live data" ).pack() 
Button(tkWindow, command=openWindow,text="Open luik" ).pack()  
Button(tkWindow, command=closeWindow, text="luik dicht").pack()  
Button(tkWindow, text='Quit', command=tkWindow.quit).pack()
tkWindow.mainloop()

