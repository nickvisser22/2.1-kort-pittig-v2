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
min_temp = 18
max_temp = 20
min_licht = 100
max_licht = 100


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
    if licht < min_licht and tempratuur < min_temp and luikDicht == False :
        closeWindow()
    elif licht > max_licht and tempratuur > max_temp and luikDicht == True:
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
        line2, = ax2.plot(y_var2, label="Tempratuur")
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


def changeTemp():
    global min_temp
    global max_temp

    update_label = Label(frame, text="-waarden geupdate-", width=20, background='grey23', fg='white')
    update_label4 = Label(frame, text="-onjuiste waarde-", width=20, background='grey23', fg='white')


    try:
        waarde1 = e1.get()
        waarde2 = e2.get()

        e1.delete(0, END)
        e2.delete(0, END)
        e1.insert(0, "Max. waarde (°C)")
        e2.insert(0, "Min. waarde (°C)")

        min_temp=int(waarde2)
        max_temp=int(waarde1)

        update_label.grid(row=5)
        print(str(min_temp))
        print(str(max_temp))
    except:
        update_label4.grid(row=5)


def changeLicht():
    global min_licht
    global max_licht
    update_label2 = Label(frame2, text="-waarden geupdate-", width=20, background='grey23', fg='white')
    update_label3 = Label(frame2, text="-onjuiste waarden-", width=20, background='grey23', fg='white')
    try:
        waarde1 = e3.get()
        waarde2 = e4.get()

        e3.delete(0, END)
        e4.delete(0, END)
        e3.insert(0, "Max. waarde")
        e4.insert(0, "Min. waarde")

        min_licht=int(waarde2)
        max_licht=int(waarde1)

        update_label2.grid(row=5)

    except:
        update_label3.grid(row=5)


tkWindow = Tk()
tkWindow.geometry('800x400')
tkWindow.title('User Interface')
tkWindow.configure(background='grey15')
tkWindow.overrideredirect(1)

main_frame= LabelFrame(tkWindow, padx=15, pady=15, borderwidth=0)
main_frame.pack(padx=15, pady=15)
main_frame.configure(highlightthickness=4, highlightbackground='grey60', background='grey23')

frame = LabelFrame(main_frame, text="")
frame.grid(column=2, row=1, rowspan=2, padx=10)
frame.configure(highlightthickness=3, highlightbackground='grey60', background='grey23')

label = Label(frame, text="Verander temperatuur waarden:")
label.grid(row=1, sticky=W+E)
label.configure(bd=3, background='grey35', fg='white')
e1 = Entry(frame, width=30, background='grey23', fg= 'white')
e1.grid(row=2, sticky=N)
e1.insert(0, "Max. waarde (°C)")
e2 = Entry(frame, width=30, background='grey23', fg='white')
e2.grid(row=3, sticky=S)
e2.insert(0, "Min. waarde (°C)")
label2 = Label(frame, width=20, background='grey23', fg='white')
label2.grid(row=5, sticky=W+E)

change_button = Button(frame, command=changeTemp, text="Verander waarden")
change_button.grid(row=4, sticky=W+E)
change_button.configure(bd=3, background='grey35', fg='white', activebackground='grey80', activeforeground='grey20')

frame2 = LabelFrame(main_frame, text="")
frame2.grid(column=2, row=3, rowspan=2, padx=10)
frame2.configure(highlightthickness=3, highlightbackground='grey60', background='grey23')

label2 = Label(frame2, text="Verander licht waarden:")
label2.grid(row=1, sticky=W+E)
label2.configure(bd=3, background='grey35', fg='white')
e3 = Entry(frame2, width=30, background='grey23', fg= 'white')
e3.grid(row=2, sticky=N)
e3.insert(0, "Max. waarde")
e4 = Entry(frame2, width=30, background='grey23', fg= 'white')
e4.grid(row=3, sticky=S)
e4.insert(0, "Min. waarde")
label3 = Label(frame2, width=20, background='grey23', fg='white')
label3.grid(row=5, sticky=W+E)

change_button2 = Button(frame2, command=changeLicht, text="Verander waarden")
change_button2.grid(row=4, sticky=W+E)
change_button2.configure(bd=3, background='grey35', fg='white', activebackground='grey80', activeforeground='grey20')


start_button = Button(main_frame, command=lambda:Devices(COM5, COM4, COM6), text="Start programma", padx=60, pady=20)
if COM5 != 0:
    Button(main_frame, command=lambda: Devices(COM5), text="COM5 live data", padx=60, pady=20, background='lightblue4', fg='white', activebackground='grey80', activeforeground='lightblue4').grid(row=1, column=1, sticky=E+W)
if COM4 !=0:
    Button(main_frame, command=lambda: Devices(COM4), text="COM4 live data", padx=60, pady=20, background='lightblue4', fg='white', activebackground='grey80', activeforeground='lightblue4').grid(row=2, column=1, sticky=E+W)
if COM6 !=0:
    Button(main_frame, command=lambda: Devices(COM6), text="COM6 live data", padx=60, pady=20, background='lightblue4', fg='white', activebackground='grey80', activeforeground='lightblue4').grid(row=3, column=1, sticky=E+W)
open_button = Button(main_frame, command=openWindow, text="Open luik",padx=79, pady=20)
close_button = Button(main_frame, command=closeWindow, text="Luik dicht", padx=78, pady=20)
quit_button = Button(main_frame, text='Quit', command=tkWindow.quit, padx=93, pady=20)

start_button.grid(row=1, column=0, padx=5, sticky=E+W)
open_button.grid(row=2, column=0, padx=5, sticky=E+W)
close_button.grid(row=3, column=0, padx=5, sticky=E+W)
quit_button.grid(row=4, column=0, padx=5, sticky=E+W)

start_button.configure(bd=3, background='grey35', fg='white', activebackground='grey80', activeforeground='grey20')
open_button.configure(bd=3, background='grey35', fg='white', activebackground='grey80', activeforeground='grey20')
close_button.configure(bd=3, background='grey35', fg='white', activebackground='grey80', activeforeground='grey20')
quit_button.configure(bd=3, background='grey35', fg='white', activebackground='grey80', activeforeground='grey20')


tkWindow.mainloop()

