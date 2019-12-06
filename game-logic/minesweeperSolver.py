from tkinter import *
from random import randint
import numpy as np
from collections import defaultdict
import configparser, random, os, tkinter.messagebox, tkinter.simpledialog
window = tkinter.Tk()

window.title("Minesweeper")

#initial values

rows = 10
cols = 10
mines = 10
numFlag=0
field = []
buttons = []

colors = ['#FFFFFF', '#0000FF', '#008200', '#FF0000', '#000084', '#840000', '#008284', '#840084', '#000000']

tile_mine = PhotoImage(file="images/tile_mine.gif")
tile_flag = PhotoImage(file="images/tile_flag.gif")
tile_wrong = PhotoImage(file="images/tile_wrong.gif")

gameover = False
done = False
customsizes = []

#Choose the Size of Game(small, medium, big)

def createMenu():
    menubar = tkinter.Menu(window)
    menusize = tkinter.Menu(window, tearoff=0)
    menusize.add_command(label="small (10x10 with 10 mines)", command=lambda: setSize(10, 10, 10))
    menusize.add_command(label="medium (20x20 with 40 mines)", command=lambda: setSize(20, 20, 40))
    menusize.add_command(label="big (35x35 with 120 mines)", command=lambda: setSize(35, 35, 120))
    menusize.add_command(label="custom", command=setCustomSize)
    menusize.add_separator()
    for x in range(0, len(customsizes)):
        menusize.add_command(label=str(customsizes[x][0])+"x"+str(customsizes[x][1])+" with "+str(customsizes[x][2])+" mines", command=lambda customsizes=customsizes: setSize(customsizes[x][0], customsizes[x][1], customsizes[x][2]))
    menubar.add_cascade(label="size", menu=menusize)
    menubar.add_command(label="exit", command=lambda: window.destroy())
    window.config(menu=menubar)

#Custom the size of game(row, column,mines)
def setCustomSize():
    global customsizes
    r = tkinter.simpledialog.askinteger("Custom size", "Enter amount of rows")
    c = tkinter.simpledialog.askinteger("Custom size", "Enter amount of columns")
    m = tkinter.simpledialog.askinteger("Custom size", "Enter amount of mines")
    while m > r*c:
        m = tkinter.simpledialog.askinteger("Custom size", "Maximum mines for this dimension is: " + str(r*c) + "\nEnter amount of mines")
    customsizes.insert(0, (r,c,m))
    customsizes = customsizes[0:5]
    setSize(r,c,m)
    createMenu()
#Set the size of game and refresh
def setSize(r,c,m):
    global rows, cols, mines
    rows = r
    cols = c
    mines = m
    saveConfig()
    restartGame()

#SetConfiguration
def saveConfig():
    global rows, cols, mines
    #configuration
    config = configparser.ConfigParser()
    config.add_section("game")
    config.set("game", "rows", str(rows))
    config.set("game", "cols", str(cols))
    config.set("game", "mines", str(mines))
    config.add_section("sizes")
    config.set("sizes", "amount", str(min(5,len(customsizes))))
    for x in range(0,min(5,len(customsizes))):
        config.set("sizes", "row"+str(x), str(customsizes[x][0]))
        config.set("sizes", "cols"+str(x), str(customsizes[x][1]))
        config.set("sizes", "mines"+str(x), str(customsizes[x][2]))

    with open("config.ini", "w") as file:
        config.write(file)

#load the Config of the game
def loadConfig():
    global rows, cols, mines, customsizes
    config = configparser.ConfigParser()
    config.read("config.ini")
    rows = config.getint("game", "rows")
    cols = config.getint("game", "cols")
    mines = config.getint("game", "mines")
    amountofsizes = config.getint("sizes", "amount")
    for x in range(0, amountofsizes):
        customsizes.append(
            (config.getint("sizes", "row"+str(x)), config.getint("sizes", "cols"+str(x)),
             config.getint("sizes", "mines"+str(x))))

#ramdonly generator the game to distribute the mines
def prepareGame():
    global rows, cols, mines, field
    field = []
    for x in range(0, rows):
        field.append([])
        for y in range(0, cols):
            #add button and init value for game
            field[x].append(0)
    #generate mines
    for _ in range(0, mines):
        x = random.randint(0, rows-1)
        y = random.randint(0, cols-1)
        #prevent spawning mine on top of each other
        while field[x][y] == -1:
            x = random.randint(0, rows-1)
            y = random.randint(0, cols-1)
        field[x][y] = -1
        if x != 0:
            if y != 0:
                if field[x-1][y-1] != -1:
                    field[x-1][y-1] = int(field[x-1][y-1]) + 1
            if field[x-1][y] != -1:
                field[x-1][y] = int(field[x-1][y]) + 1
            if y != cols-1:
                if field[x-1][y+1] != -1:
                    field[x-1][y+1] = int(field[x-1][y+1]) + 1
        if y != 0:
            if field[x][y-1] != -1:
                field[x][y-1] = int(field[x][y-1]) + 1
        if y != cols-1:
            if field[x][y+1] != -1:
                field[x][y+1] = int(field[x][y+1]) + 1
        if x != rows-1:
            if y != 0:
                if field[x+1][y-1] != -1:
                    field[x+1][y-1] = int(field[x+1][y-1]) + 1
            if field[x+1][y] != -1:
                field[x+1][y] = int(field[x+1][y]) + 1
            if y != cols-1:
                if field[x+1][y+1] != -1:
                    field[x+1][y+1] = int(field[x+1][y+1]) + 1

def prepareWindow():
    global rows, cols, buttons
    tkinter.Button(window, text="Restart", command=restartGame).grid(row=0, column=0, columnspan=cols,
                                                                     sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
    buttons = []
    for x in range(0, rows):
        buttons.append([])
        for y in range(0, cols):
            b = tkinter.Button(window, text=" ", width=2, command=lambda x=x,y=y: clickOn(x,y))
            b.bind("<Button-3>", lambda e, x=x, y=y:onRightClick(x, y))
            b.grid(row=x+1, column=y, sticky=tkinter.N+tkinter.W+tkinter.S+tkinter.E)
            buttons[x].append(b)

#restart the game
def restartGame():
    global gameover,done
    gameover = False
    done = False
    #destroy all - prevent memory leak
    for x in window.winfo_children():
        if type(x) != tkinter.Menu:
            x.destroy()
    prepareWindow()
    prepareGame()
    autoplay()

#when click on a button, if it is mine, you lose show all the mines. if it is empty, expanding the squres.
def clickOn(x,y):
    global field, buttons, colors, gameover, rows, cols
    if gameover:
        return
    buttons[x][y]["text"] = str(field[x][y])
    #Case 1, when it is a mine
    if field[x][y] == -1:
        buttons[x][y].config(image=tile_wrong)

        gameover = True
        tkinter.messagebox.showinfo("Game Over", "You have lost.")
        #now show all other mines
        for _x in range(0, rows):
            for _y in range(cols):
                if field[_x][_y] == -1:
                    buttons[_x][_y].config(image=tile_mine)
    else:
        buttons[x][y].config(disabledforeground=colors[field[x][y]])
    #case 2 expanding when the square is empty(neither mine nor number)
    if field[x][y] == 0:
        buttons[x][y]["text"] = " "
        #now repeat for all buttons nearby which are 0... kek
        autoClickOn(x,y)
    #the clicked square should be disabled
    buttons[x][y]['state'] = 'disabled'
    buttons[x][y].config(relief=tkinter.SUNKEN)
    checkWin()

def autoClickOn(x,y):
    global field, buttons, colors, rows, cols
    if buttons[x][y]["state"] == "disabled":
        return
    #if click field is a digit, get the number in the square
    if field[x][y] != 0:
        buttons[x][y]["text"] = str(field[x][y])
    else:
        buttons[x][y]["text"] = " "
    buttons[x][y].config(disabledforeground=colors[field[x][y]])
    buttons[x][y].config(relief=tkinter.SUNKEN)
    buttons[x][y]['state'] = 'disabled'
    #if the connect field is a empty square, just expanding
    if field[x][y] == 0:
        if x != 0 and y != 0:
            autoClickOn(x-1,y-1)
        if x != 0:
            autoClickOn(x-1,y)
        if x != 0 and y != cols-1:
            autoClickOn(x-1,y+1)
        if y != 0:
            autoClickOn(x,y-1)
        if y != cols-1:
            autoClickOn(x,y+1)
        if x != rows-1 and y != 0:
            autoClickOn(x+1,y-1)
        if x != rows-1:
            autoClickOn(x+1,y)
        if x != rows-1 and y != cols-1:
            autoClickOn(x+1,y+1)
#Click right to flag or unflag
def onRightClick(x,y):
    global buttons,numFlag
    if gameover:
        return
    #Unflag
    if buttons[x][y]["state"] == "disabled":
        buttons[x][y].config(image='')
        buttons[x][y]["text"]=" "
        buttons[x][y]["state"] = "normal"
    #Flag
    elif buttons[x][y]["state"] == "normal":
        buttons[x][y]["state"] = "disabled"
        buttons[x][y]["text"] = "flag"
        buttons[x][y].config(image=tile_flag)
        numFlag +=1

#Win if all the mines are founded
def checkWin():
    global buttons, field, rows, cols,done
    win = True
    for x in range(0, rows):
        for y in range(0, cols):
            if field[x][y] != -1 and buttons[x][y]["state"] == "normal":
                win = False
    if win:
        done = True
        tkinter.messagebox.showinfo("Gave Over", "You have won.")


#AI Player
def surrounding_cells(x, y):
    global rows, cols
    cells = []
    for i in range(max(x-1, 0), min(x+2, rows)):
        for j in range(max(y-1, 0), min(y+2, cols)):
            if i==x and j==y:
                continue
            cells.append([i, j])
    return cells

def ai_player():
    global rows,cols,buttons
    numbered_cell_neighbors = defaultdict(float)
    for i, j in np.ndindex((rows, cols)):
        if buttons[i][j]["state"] == "disabled" and field[i][j]!=0:
            n = field[i][j]
            flags = [(x, y) for x, y in surrounding_cells(i, j) if buttons[x][y]["text"] == "flag"]
            safe_factor = -20 if n == len(flags) else 1
            neighbors = [(x, y) for x, y in surrounding_cells(i, j) if buttons[x][y]["state"] != "disabled" ]
            if (n - len(flags)) == len(neighbors) and len(neighbors) > 0:
                for x, y in neighbors:
                    onRightClick(x, y)
            for x, y in neighbors:
                numbered_cell_neighbors[(x, y)] += safe_factor * n/len(neighbors)
    print(len(numbered_cell_neighbors), numbered_cell_neighbors)
    if numbered_cell_neighbors:
        x, y = min(numbered_cell_neighbors, key=numbered_cell_neighbors.get)
        return x, y
    print('Choosing random cell')
    return randint(0, rows-1), randint(0, cols-1) # stuck, unable to choose next best cell

random_fails=0
def autoplay():
  global random_fails, rows, cols, gameover,done,numFlag
  #Choose first step
  x, y = randint(0, rows-1), randint(0, cols-1)
  is_random_fail = True
  while not done:
    clickOn(x, y)
    print('Computer plays', (x, y), 'Mines flagged: ', numFlag)
    if gameover:
      if is_random_fail:
        random_fails += 1
      return False
    if done:
        break
        return True
    is_random_fail = False
    x, y = ai_player()


if os.path.exists("config.ini"):
    loadConfig()
else:
    saveConfig()

createMenu()

prepareWindow()
prepareGame()
window.mainloop()
