from kivy.app import App
from kivy.uix.gridlayout import *
from kivy.uix.image import Image
from kivy.uix.button import Button
import random
from kivy.core.window import Window


#ship generator - chooses a random location on the board of the ship and places it
def shipGen(length, board, ship):

    shipOrientation = (random.choice(['h', 'v']))  #decides randomly if ship is horizontal 'h' or vertical 'v'

    print(shipOrientation) #prints the ship orientation for debug purposes

    if shipOrientation == 'v':
        x = random.randrange(len(board)) #ship location on x axis
        y = random.randrange((len(board[0]) - length)) #ship location on y axis - makes sure it isn't out of bounds!
        print(x, ',', y) #prints the ship location for debug purposes
        i = y #i is a temporary variable for the ship.
        while i < length + y: #makes sure the ship doesn't hit anything. If it hits - calls the functuion again.
            if(board[x][i]) != 0: #if the ship hits something calls the function again and returns null
                shipGen(length, board, ship)
                return
            i+=1 #next square!
        #if everything is succesful, moves onto building the ship!
        i = y #resets i
        while i < length + y: #goes over every cell of the ship
            board[x][i] = ship #ship number. builds the ship.
            i+=1 #checks next square
        return board #returns the board with the new ship.

    #if the ship is horizontal
    if shipOrientation == 'h':
        x = random.randrange((len(board) - length)) #ship location on x axis - makes sure it isn't out of bounds!
        y = random.randrange(len(board[0])) #ship location on y axis
        print(x, ',', y) #prints the ship location for debug purposes
        i = x #i is a temporary variable for the ship.
        while i < length + x: #makes sure the ship doesn't hit anything. If it hits - calls the function again.
            if (board[i][y]) != 0: #if the ship hits something calls the function again and returns null
                shipGen(length, board, ship)
                return
            i+=1 #next square!
        # if everything is succesful, moves onto building the ship!
        i=x #resets i
        while i < length + x: #goes over every cell of the ship
            board[i][y] = ship #ship number. builds the ship.
            i+=1
        return board #returns the board with the new ship.

def checkHit(button, board, xCord, yCord, health):
    hp = 0
    while((hp < len(board)) and (health[hp].ifDamaged() == False)):
        hp += 1
        print(hp)
    if(hp == 0):
        print('You lost!')
        exit()
    if(board[xCord][yCord] != 0): #if this cell isn't empty
        shipType = board[xCord][yCord]
        board[xCord][yCord] = 0 #clears this cell
        if(hp < 10):
            health[hp].addHealth()
        hp += 1
        print('hit ship at ', xCord, yCord)
        button.hit("Hit64.jpg") #changes  the button texture to mark the hit
        if(shipsLeft(board, shipType) == 0): #if the whole ship was destroyed
            print('ship type ', shipType, ' sunk!')
            if (hp < 10):
                health[hp].addHealth()
            hp += 1
            checkIfWon(board, health) #checks if all ships sunk
    else: #if the cell is empty
        hp = hp - 1
        health[hp].loseHealth()
        print('no ship at ', xCord, yCord, ' hp: ', hp)
        button.hit("Miss64.jpg") #miss texture


def shipsLeft(board, shipType): #checks if there is anything of this ship left
    num = 0 #number of ship parts of this type left
    for i in range (len(board)): #every column
        for j in range (len(board[0])): #every row
            if(board[i][j] == shipType): #if detected ship in this cell counts it
                num+=1
    return num

def checkIfWon(board, health): #checks for the existence of every ship, if doesnt find any ships it means the player won
    if(shipsLeft(board, 5) == 0):
        if(shipsLeft(board, 4) == 0):
            if(shipsLeft(board, 3) == 0):
                if(shipsLeft(board, 2) == 0):
                    if(shipsLeft(board,1) == 0):
                        print('you won!')
                        for i in range(10):
                            health[i].winner()
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
                t=imb(x,y) #creates image button with the coordinates
                listline.append(t)
                self.add_widget(t)
            self.listboard.append(listline)
        for i in range(10):
            for j in range(10):
                print('built button', i, j)
                self.listboard[i][j].bind(on_press = self.click)

        self.health = [] #health bar at the bottom of the screen
        for i in range(10):
            t = im()
            self.health.append(t)
            self.add_widget(t)


    def click(self, button):
        print('button ', button.xCord, button.yCord, ' clicked') #prints which button was clicked
        if(checkIfWon(board, self.health) == True):
            exit()
        checkHit(button, board, button.xCord, button.yCord, self.health) #checks if hit at the button coordinate

class im(Image):
    def __init__(self): #builds the square, green by default
        Image.__init__(self)
        self.source = "green.png"

    def addHealth(self): #changes the square to green
        self.source = "green.png"
    def loseHealth(self): #changes the square to red
        self.source = "red.png"
    def ifDamaged(self): #checks if the square is red or green
        if(self.source == "red.png"): #if its red - true
            return True
        else: #else - false
            return False
    def winner(self): #changes the square to trophy
        self.source = "trophy.png"

class imb(Image, Button):
    def __init__(self, xCord, yCord): #builds the button
        Image.__init__(self)
        Button.__init__(self)
        self.source ="Sea64.jpg" #default sea texture
        self.xCord = xCord #the x coordinate of the button
        self.yCord = yCord #the y coordinate of the button
    def hit(self, image): #disables button and changes image to new status (hit / miss) after click
        self.disabled = True
        self.source = image

class Game(App):
    def build(self):
        self.icon = 'ShipIcon.png'
        Window.size = (730, 800)
        self.title = 'Battleship'
        return Board()

Game().run()