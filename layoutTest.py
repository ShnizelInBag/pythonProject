from kivy.app import App
from kivy.uix.layout import Layout
from kivy.uix.gridlayout import *
from kivy.uix.floatlayout import *
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.behaviors import ButtonBehavior
import random
from kivy.core.window import Window
from kivy.uix.popup import *


#ship generator - chooses location for ship
def shipGen(length, board, ship):

    shipOrientation = (random.choice(['h', 'v']))  #decides randomly if ship is horizontal 'h' or vertical 'v'

    print(shipOrientation) #prints the ship orientation for debug purposes

    if shipOrientation == 'v':
        x = random.randrange(len(board)) #ship location on x axis
        y = random.randrange((len(board[0]) - length)) #ship location on y axis - makes sure it isn't out of bounds!
        print(x, ',', y) #prints the ship location for debug purposes
        i = y #i is a temporary variable for the ship.
        while i < length + y: #makes sure the ship doesn't hit anything. If it hits - calls the functuion again.
            if(board[x][i]) != 0:
                shipGen(length, board, ship)
                return
            i+=1 #next square!
        #if everything is succesful, moves onto building the ship!
        i = y #resets i
        while i < length + y:
            board[x][i] = ship #ship number. builds the ship.
            i+=1
        return board #returns the board with the new ship.

    #if the ship is horizontal
    if shipOrientation == 'h':
        x = random.randrange((len(board) - length))
        y = random.randrange(len(board[0]))
        print(x, ',', y)
        i = x
        while i < length + x:
            if (board[i][y]) != 0:
                shipGen(length, board, ship)
                return
            i+=1
        i=x
        while i < length + x:
            board[i][y] = ship
            i+=1
        return board

def checkHit(button, board, xCord, yCord, health):
    hp = 0
    temp = 0
    while((temp < len(board)) and (health[temp].ifDamaged() == False)):
        hp += 1
        temp += 1
        print(hp, temp)
    print(hp)
    if(hp == 0):
        print('You lost!')
        popup = Popup(title='You lost!',
                      content=Label(text='You ran out of health!'),
                      size_hint=(None, None), size=(400, 400))
        popup.open()
        exit()
    if(board[xCord][yCord] != 0): #if this cell isn't empty
        shipType = board[xCord][yCord]
        board[xCord][yCord] = 0 #clears this cell
        if(temp < 10):
            health[temp].addHealth()
        hp += 1
        print('hit ship at ', xCord, yCord)
        button.hit("Hit64.jpg") #changes  the button texture to mark the hit
        if(shipsLeft(board, shipType) == 0): #if the whole ship was destroyed
            #hp += 1
            #health[temp].addHealth()
            print('ship type ', shipType, ' sunk!')
            checkIfWon(board) #checks if all ships sunk
    else: #if the cell is empty
        print(temp)
        hp = hp - 1
        health[hp].loseHealth()
        print('no ship at ', xCord, yCord, ' hp: ', hp)
        button.hit("Miss64.jpg") #miss texture


def shipsLeft(board, shipType):
    num = 0 #number of ship parts of this type left
    for i in range (len(board)): #every column
        for j in range (len(board[0])): #every row
            if(board[i][j] == shipType): #if detected ship in this cell counts it
                num+=1
    return num

def checkIfWon(board): #checks for the existence of every ship, if doesnt find any ships it means the player won
    if(shipsLeft(board, 5) == 0):
        if(shipsLeft(board, 4) == 0):
            if(shipsLeft(board, 3) == 0):
                if(shipsLeft(board, 2) == 0):
                    if(shipsLeft(board,1) == 0):
                        print('you won!')
                        return True
    return False

#builds a 10 x 10 empty board board
board = [[0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0], [0,0, 0, 0, 0, 0, 0, 0, 0, 0]]
shipGen(5, board, 5) #generates a 5 tile long ship
shipGen(4, board, 4) #generates a 4 tile long ship
shipGen(3, board, 3) #generates a 3 tile long ship
shipGen(3, board, 2) #generates a 3 tile long ship
shipGen(2, board, 1) #generates a 2 tile long ship

hp = 10

for x in range(10): #prints the board for debugging
    print(board[x])

class Board(GridLayout):
    def __init__(self):
        GridLayout.__init__(self)
        GridLayout.cols = 10
        GridLayout.rows = 11
        GridLayout.col_default_width = 72
        GridLayout.row_default_height = 72
        GridLayout.col_force_default = True
        GridLayout.row_force_default = True
        GridLayout.spacing = [0, 0]
        GridLayout.padding = [4, 4, 4, 4]
        GridLayout.size_hint_y = None

        self.listboard = []
        for x in range(10):
            listline = []
            for y in range(10):
                t=imb(x,y)
                listline.append(t)
                self.add_widget(t)
            self.listboard.append(listline)
        for i in range(10):
            for j in range(10):
                print('build button', i, j)
                self.listboard[i][j].bind(on_press = self.click)

        self.health = []
        for i in range(10):
            t = im()
            self.health.append(t)
            self.add_widget(t)


    def click(self, button):
        print('button ', button.xCord, button.yCord, ' clicked')
        print(button.xCord, ',', button.yCord)
        checkHit(button, board, button.xCord, button.yCord, self.health)

class im(Image):
    def __init__(self):
        Image.__init__(self)
        self.source = "green.png"

    def addHealth(self):
        self.source = "green.png"
    def loseHealth(self):
        self.source = "red.png"
    def ifDamaged(self):
        if(self.source == "red.png"):
            return True
        else:
            return False

class imb(Image, Button):
    def __init__(self, xCord, yCord):
        Image.__init__(self)
        Button.__init__(self)
        self.source ="Sea64.jpg"
        self.xCord = xCord
        self.yCord = yCord
    def hit(self, image): #disables button and changes image after click
        self.disabled = True
        self.source = image



class Game(App):
    def build(self):
        self.icon = 'ShipIcon.png'
        Window.size = (730, 800)
        self.title = 'Battleship'
        return Board()

Game().run()