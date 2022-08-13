from tkinter import *
from tkinter import ttk
from datetime import datetime
from datetime import date
from datetime import timedelta
import tkinter.simpledialog as simpledialog
import tkinter.messagebox as messagebox

months = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", 7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}
daysInMonth = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
weekdays = {0: "S", 1: "M", 2: "T", 3: "W", 4: "T", 5: "F", 6: "S"}

def highlight(year, month):
    days = []
    s = str(year) + "-" + str(month).zfill(2)
    file = open(datefile, "r")
    for line in file:
        if s in line: 
            days.append(datetime.strptime(line[:10],"%Y-%m-%d").date().day)
    file.close()
    return days

def label(frm, year, month):
    Button(frm, text=months[month]+" "+str(year), borderwidth=0, relief=FLAT, fg="#4C4E52", font=("Malgun Gothic", 17), height=2, command=jump).grid(row=1, column=1, sticky=E+W, columnspan=5)

def dates(frm, year, month):
    dim = daysInMonth[month]
    if year%4==0: 
        if month==2: dim+=1
    d = datetime(year,month,1).weekday()
    if d==6: d=-1
    i=0-d
    for r in range(6):
        for c in range(7):
            if i-1 in range(dim):
                if i in highlight(year, month):
                    Button(frm, text=i, borderwidth=0, relief=FLAT, fg="#E6EEF7", bg="#3D3D90", font=("Malgun Gothic", 11), height=2, width=5, command=lambda text=i:toggle(year, month, text)).grid(row=r+3, column=c, sticky=N+E+S+W)
                elif i in highlightPredict(year, month):
                    Button(frm, text=i, borderwidth=0, relief=FLAT, fg="#E6EEF7", bg="#7C83BC", font=("Malgun Gothic", 11), height=2, width=5, command=lambda text=i:toggle(year, month, text)).grid(row=r+3, column=c, sticky=N+E+S+W)
                else:
                    Button(frm, text=i, borderwidth=0, relief=FLAT, fg="#6F7378", font=("Malgun Gothic", 11), height=2, width=5, command=lambda text=i:toggle(year, month, text)).grid(row=r+3, column=c, sticky=N+E+S+W)
            else:
                Button(frm, text=" ", borderwidth=0, font=("Malgun Gothic", 11), height=2, width=5, state=DISABLED).grid(row=r+3, column=c, sticky=E+W)
            i+=1

def front():
    global month
    global year
    global frm
    if month==12:
        month=1
        year+=1
    else: month+=1
    label(frm, year, month)
    dates(frm, year, month)

def back():
    global month
    global year
    global frm
    if month==1:
        month=12
        year-=1
    else: month-=1
    label(frm, year, month)
    dates(frm, year, month)

def add(s):
    file = open(datefile, "r+")
    lines = file.read().splitlines()
    if len(lines) == 0:
        file.write(s)
    else:
        lines.append(s)
        lines.sort()
        file = open(datefile, "r+")
        for line in lines:
            file.write(line+"\n")
    file.close()

def remove(s):
    file = open(datefile, "r")
    lines = file.read().splitlines()
    file = open(datefile, "w+")
    for line in lines:
        if line != s:
            file.write(line+"\n")
    file.close()

def toggle(year, month, day):
    s = str(year) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
    file = open(datefile, "r")
    lines = file.read().splitlines()
    exists = False
    for line in lines:
        if line == s: exists = True
    if exists:
        remove(s)
    else:
        add(s)
    file.close()
    dates(frm, year, month)
    predictUI()

def predict(i, c, l):
    file = open(datefile, "r")
    lines = file.read().splitlines()
    file.close()
    if len(lines) == 0:
        return [], 0, 0
    elif len(lines) == 1:
        return [], 0, 0
    elif l != 0:
        return predictc(c, l)
    elif i >= 1:
        if len(lines) <= i:    
            return predicti(len(lines)-1, c)
        return predicti(i, c)
    elif i == 0:
        return predicti(len(lines)-1, c)
    else:
        if len(lines) == 2:
            return predicti(1, c)
        elif len(lines) == 3:
            return predicti(2, c)
        else:
            return predicti(3, c)

def predicti(i, c):
    file = open(datefile, "r")
    lines = file.read().splitlines()
    file.close()
    fl = lines[len(lines)-1-i]
    ll = lines[len(lines)-1]
    fd = datetime.strptime(fl,"%Y-%m-%d")
    ld = datetime.strptime(ll,"%Y-%m-%d")
    cycle = (ld - fd) / float(i)
    nextDate = ld+cycle
    nextDates = [nextDate]
    for j in range(c-1):
        nextDate+=cycle
        nextDates.append(nextDate)
    return nextDates, cycle.total_seconds(), i

def predictc(c, l):
    file = open(datefile, "r")
    lines = file.read().splitlines()
    file.close()
    ll = lines[len(lines)-1]
    ld = datetime.strptime(ll,"%Y-%m-%d")
    nextDate = ld+timedelta(days=l)
    nextDates = [nextDate]
    for j in range(c-1):
        nextDate+=timedelta(days=l)
        nextDates.append(nextDate)
    return nextDates, timedelta(days=l).total_seconds(), 0

def predictUI():
    global pCycles
    global fCycles
    global lCycles
    _, cycleLength, pCyclesTemp = predict(pCycles, fCycles, lCycles)
    Button(frm, text="\nPrediction\nCycles", borderwidth=0, fg="#6F7378", font=("Malgun Gothic", 9), anchor="s", command=helpP).grid(row=11, column=0, sticky=E+S+W, columnspan=2)
    Button(frm, text="\nCycle\nLength", borderwidth=0, fg="#6F7378", font=("Malgun Gothic", 9), anchor="s", command=helpL).grid(row=11, column=2, sticky=E+S+W, columnspan=3)
    Button(frm, text="\nFuture\nCycles", borderwidth=0, fg="#6F7378", font=("Malgun Gothic", 9), anchor="s", command=helpF).grid(row=11, column=5, sticky=E+S+W, columnspan=2)
    file = open(datefile, "r")
    lines = file.read().splitlines()
    file.close()
    pLabelText = ""
    if pCyclesTemp!=0 and pCyclesTemp==len(lines)-1:
        pLabelText = "all"
    Button(frm, text=str(pCyclesTemp), borderwidth=0, fg="#4C4E52", font=("Malgun Gothic", 14), command=askPCycles).grid(row=12, column=0, sticky=E+W, columnspan=2)
    Label(frm, text=pLabelText, borderwidth=0, fg="#6F7378", font=("Malgun Gothic", 9),  anchor="n").grid(row=13, column=0, sticky=N+E+W, columnspan=2)
    if cycleLength%(60*60*24)==0:
        lCyclesTemp = int(cycleLength/(60*60*24))
    else:
        lCyclesTemp = round(cycleLength/float(60*60*24), 2)
    lLabelText = ""
    if lCycles!=0:
        lLabelText = "custom"
    Button(frm, text=str(lCyclesTemp), borderwidth=0, fg="#4C4E52", font=("Malgun Gothic", 14), command=askLCycles).grid(row=12, column=2, sticky=E+W, columnspan=3)
    Label(frm, text=lLabelText, borderwidth=0, fg="#6F7378", font=("Malgun Gothic", 9), anchor="n").grid(row=13, column=2, sticky=N+E+W, columnspan=3)
    Button(frm, text=str(fCycles), borderwidth=0, fg="#4C4E52", font=("Malgun Gothic", 14), command=askFCycles).grid(row=12, column=5, sticky=E+W, columnspan=2)

def highlightPredict(year, month):
    global pCycles
    global fCycles
    nextDates, _, _ = predict(pCycles, fCycles, lCycles)
    days = []
    file = open(datefile, "r")
    for date in nextDates:
        if date.year==year and date.month==month: 
            days.append(date.day)
    file.close()
    return days

def askPCycles():
    global pCycles
    global lCycles
    global month
    global year
    global frm
    ask = simpledialog.askstring("Predict", "Prediction Cycles:")
    if ask=="all" or ask=="All":
        pCycles=0
        lCycles=0
    elif ask.isnumeric():
        pCycles=int(ask)
        lCycles=0
    elif ask=="default" or ask=="Default":
        pCycles=3
        lCycles=0
    dates(frm, year, month)
    predictUI()

def askFCycles():
    global fCycles
    global month
    global year
    global frm
    ask = simpledialog.askstring("Future", "Future Cycles:")
    if ask.isnumeric() and int(ask)!=0:
        fCycles=int(ask)
    elif ask=="default" or ask=="Default":
        fCycles=3
    dates(frm, year, month)
    predictUI()

def askLCycles():
    global lCycles
    global month
    global year
    global frm
    ask = simpledialog.askstring("Length", "Length Cycles:")
    if ask.isnumeric():
        lCycles=int(ask)
    elif ask=="default" or ask=="Default":
        lCycles=0
    dates(frm, year, month)
    predictUI()

def helpP():
    messagebox.showinfo("Predict", "Click on the number below to change the number of cycles used to calculate a prediction.\n\nEnter the number of cycles you want to predict on or \"all\" to predict on all cycles.\n\nEnter \"default\" to restore default settings.")

def helpL():
    messagebox.showinfo("Length", "Click on the number below to change the cycle length, calculated using the last date selected.\n\nEnter the length of the cycles you would like to predict.\n\nTo reset cycle calculation, change the number of Prediction Cycles or enter \"default\" to restore default settings.")

def helpF():
    messagebox.showinfo("Future", "Click on the number below to change the number of future cycles predicted.\n\nEnter the number of future cycles you want to predict.\n\nEnter \"default\" to restore default settings.")

def help():
    messagebox.showinfo("Help", "Welcome to Date Predictor Pro!\n\nAdding Event Days: dark blue, click on dates to turn them into Event Days\n\nRemoving Event Days: click the Event Day again\n\nPredicted Days: light blue, predictions are formed based on Event Days\n\nChange Predictions: click on the three labels at the bottom of the window for more information\n\nHappy Predicting!")

def jump():
    global month
    global year
    global frm
    ask = simpledialog.askstring("Date", "Enter date to jump to\n(YYYY or YYYY/MM):")
    if len(ask)==4 and ask.isnumeric():
        if year!=int(ask):
            month = 1
        year = int(ask)
    elif len(ask)==7 and ask[:4].isnumeric() and ask[5:].isnumeric():
        year = int(ask[:4])
        month = int(ask[5:])
    label(frm, year, month)
    dates(frm, year, month)
    predictUI()

datefile = "dppdata/dates.txt"

year = date.today().year
month = date.today().month

pCycles = 3
fCycles = 3
lCycles = 0

gui = Tk()
gui.resizable(False,False)
gui.iconphoto(False, PhotoImage(file='dppdata/dppicon.png'))
gui.title("Date Predictor Pro")
gui_style = ttk.Style()
gui_style.configure('TFrame')
frm = ttk.Frame(gui, padding=50, style='TFrame')
frm.grid()

label(frm, year, month)

for d in weekdays:
    Label(frm, text=weekdays[d], borderwidth=10, fg="#4C4E52", font=("Malgun Gothic", 14)).grid(row=2, column=d, sticky=E+W) #Microsoft YaHei, Malgun Gothic

dates(frm, year, month)

Button(frm, text ="<", relief=FLAT, borderwidth=0, fg="#4C4E52", font=("Malgun Gothic", 17), command=back).grid(row=1, column=0, rowspan=1, columnspan=1, sticky=E+W)
Button(frm, text =">", relief=FLAT, borderwidth=0, fg="#4C4E52", font=("Malgun Gothic", 17), command=front).grid(row=1, column=6, rowspan=1, columnspan=1, sticky=E+W)

predictUI()

logo = PhotoImage(file = "dppdata/dpptitle.png")
Button(frm, image=logo, relief=FLAT, borderwidth=0, anchor="n", command=help).grid(row=0, column=0, columnspan=7, sticky=N+E+W)

gui.mainloop()