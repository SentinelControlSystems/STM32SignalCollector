import serial
import numpy as np
import time
import matplotlib.pyplot as plt
from matplotlib.widgets import Button

buffer_size=8192

filename = 'output.txt'

fig, ax = plt.subplots()

ax.set_xlim(0, buffer_size/2)  # Assume you have 512 points in the array
ax.set_ylim(0, 65535)  # Assume 16-bit integers, adjust as necessary
x_data = np.arange(int(buffer_size/2))
vref_data = np.zeros(int(buffer_size/2))
in1_data = np.zeros(int(buffer_size/2))
line_vref, = ax.plot(x_data, vref_data, lw=2)
line_in1, = ax.plot(x_data, in1_data, lw=2)
ax_button = plt.axes([0.7, 0, 0.2, 0.075])  # position of the button
button = Button(ax_button, 'Get Data')  # Button text


   
def update_plot(new_vref_data,new_in1_data):
    global y_data
    vref_data[:] = new_vref_data  # Update the data array
    in1_data[:] =  new_in1_data  # Update the data array
    line_vref.set_ydata(vref_data)  # Update the line with new data
    line_in1.set_ydata(in1_data)  # Update the line with new data
    fig.canvas.draw()  # Redraw the plot

def GetSignalData(event):
    ser.write('a'.encode())
   
    buffer=ser.read(buffer_size*2)
    int_array = np.frombuffer(buffer, dtype=np.uint16)
       #elapsedtime=ser.read(2)
    #timepassed=int.from_bytes(elapsedtime,byteorder="little")
    #print(timepassed)
    if len(buffer)==buffer_size*2:
        vref_array = int_array[::2]
        in1_array = int_array[1::2]
        update_plot(vref_array,in1_array)
        with open(filename, mode='w', newline='') as file:
            for i in range(int(buffer_size/2)):
                file.write(f"{vref_array[i]},{in1_array[i]}\n")
button.on_clicked(GetSignalData)
#GetSignalData(None)
update_plot(None,None)
ser = serial.Serial(
    port='/COM8',
    baudrate=115200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
    
)
while(True):
    plt.pause(0.1) 
    
plt.show()
