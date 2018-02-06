
import time
from Tkinter import *

app = Tk();
app.title("tkinter")
app.geometry('450x300+200+200')
frame = Frame(app)

labelTempText = StringVar()
labelPresText = StringVar()
labelTemp = Label(frame, textvariable=labelTempText)
labelPres = Label(frame, textvariable=labelPresText)
while True:     #loop forever
    time.sleep(1)  # Sleep (or inWaiting() doesn't give the correct value)

    if(data != '?+/r/n'):
        pass

    tempData = float(100)
    pressData = float(200)
    labelPresText.set("Pressure :" + str(pressData))
    labelTempText.set("Temperature :" + str(tempData))
    labelTemp.pack()
    labelPres.pack()
    frame.pack()
    app.update()