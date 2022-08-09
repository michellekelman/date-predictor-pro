import datetime
import sys

def predict(i):
    file = open("dates.txt", "r")
    lines = file.read().splitlines()
    if len(lines) == 0:
        print("No dates available")
    elif i == 1 or i == 0:
            print("Not enough dates to form prediction")
    elif len(lines) >= i:
        if i == -1:
            i = len(lines)
        fl = lines[len(lines)-i]
        ll = lines[len(lines)-1]
        fd = datetime.datetime.strptime(fl,"%Y-%m-%d").date()
        ld = datetime.datetime.strptime(ll,"%Y-%m-%d").date()
        cycle = (ld - fd) / (i - 1)
        print("Cycle length:", cycle.days, "days")
        nextDate = ld + cycle
        print("Next date:", nextDate)
    else:
        print("Not enough dates, predicting with all available dates")
        predict(-1)
    file.close()

def add(s):
    file = open("dates.txt", "r+")
    lines = file.read().splitlines()
    if len(lines) == 0:
        file.write(s)
    else:
        file.write("\n" + s)
    file.close()

def remove():
    file = open("dates.txt", "r")
    lines = file.readlines()
    file.close()
    lines = lines[:-1]
    file = open("dates.txt", "w")
    for l in lines:
        file.write(l)
    file.close()

def display(i):
    file = open("dates.txt", "r")
    lines = file.read().splitlines()
    if len(lines) == 0:
        print("No dates available")
    elif len(lines) >= i:
        if i == -1:
            i = len(lines)
        printLines = lines[len(lines)-i:]
        for l in printLines:
            print(l)
    else:
        print("Not enough dates, displaying all available dates")
        display(-1)
    file.close()

exit = False
file = open("dates.txt", "a")
file.close()
while (not exit):
    i = input("Input menu selection or M for menu: ")
    if i == "M":
        print("M: Menu\nP: Predict (P2, P3, P4 shortcuts)\nA: Add\nR: Remove\nD: Display (D2, D3, D4 shortcuts)\nE: Exit")
    elif i == "P":
        j = input("Input number of dates to use in prediction (or A for all): ")
        if j == "A":
            predict(-1)
        else:
            predict(int(j))
    elif i == "P2":
        predict(2)
    elif i == "P3":
        predict(3)
    elif i == "P4":
        predict(4)
    elif i == "A":
        j = input("Input date to add (Format: YYYY-MM-DD): ")
        add(j)
    elif i == "R":
        remove()
    elif i == "D":
        j = input("Input number of dates to display (or A for all): ")
        if j == "A":
            display(-1)
        else:
            display(int(j))
    elif i == "D2":
        display(2)
    elif i == "D3":
        display(3)
    elif i == "D4":
        display(4)
    elif i == "E":
        exit = not exit
    print("\n")