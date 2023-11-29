########################################################
# CMPS 3500 - Class Project
# Checkers game simulator
# This is a program that will simulate a checkers board
# and provide basic game functionalities.
# This program does not abide all the rules of checkers
########################################################

import pygame
import random
import sys
from itertools import combinations
import os

# current directory
dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, 'relative/path/to/file/you/want')

# Set the width and number of rows for the game board
WIDTH = 800
ROWS = 8

IMAGE_SIZE = (200, 200)

# Load images for the game pieces and board
RED= pygame.image.load(os.path.join(dirname, 'images/red.png'))
GREEN= pygame.image.load(os.path.join(dirname, 'images/green.png'))

REDKING = pygame.image.load(os.path.join(dirname, 'images/redking.png'))
GREENKING = pygame.image.load(os.path.join(dirname, 'images/greenking.png'))

#CHESS IMAGES
WHITEKING = pygame.image.load(os.path.join(dirname, 'images/wK.svg'))
WHITEQUEEN = pygame.image.load(os.path.join(dirname, 'images/wQ.svg'))
WHITEROOK = pygame.image.load(os.path.join(dirname, 'images/wR.svg'))
WHITEKNIGHT = pygame.image.load(os.path.join(dirname, 'images/wN.svg'))
WHITEBISHOP = pygame.image.load(os.path.join(dirname, 'images/wB.svg'))
WHITEPAWN = pygame.image.load(os.path.join(dirname, 'images/wP.svg'))

BLACKKING = pygame.image.load(os.path.join(dirname, 'images/bK.svg'))
BLACKQUEEN = pygame.image.load(os.path.join(dirname, 'images/bQ.svg'))
BLACKROOK = pygame.image.load(os.path.join(dirname, 'images/bR.svg'))
BLACKKNIGHT = pygame.image.load(os.path.join(dirname, 'images/bN.svg'))
BLACKBISHOP = pygame.image.load(os.path.join(dirname, 'images/bB.svg'))
BLACKPAWN = pygame.image.load(os.path.join(dirname, 'images/bP.svg'))


# Define color constants
WHITE = (255,255,255)
BLACK = (0,0,0)
ORANGE = (235, 168, 52)
BLUE = (76, 252, 241)
PINK = (255, 0, 255)

# Initialize Pygame
pygame.init()
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption('Checkers')

# Define a class for each node on the game board
priorMoves=[]
class Node:
    def __init__(self, row, col, width):
        self.row = row
        self.col = col
        self.x = int(row * width)
        self.y = int(col * width)
        self.colour = WHITE
        self.piece = None

    def draw(self, WIN):
        pygame.draw.rect(WIN, self.colour, (self.x, self.y, WIDTH / ROWS, WIDTH / ROWS))
        if self.piece:
            WIN.blit(self.piece.image, (self.x, self.y))

# Function to update and display the game board
def update_display(win, grid, rows, width):
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win, rows, width)
    pygame.display.update()

# Function to create the initial game board grid
def make_grid(rows, width):
    grid = []
    gap = width// rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap)
            if abs(i-j) % 2 == 0:
                node.colour=BLACK
            if (abs(i+j)%2==0) and (i<3):
                node.piece = Piece('R')
            elif(abs(i+j)%2==0) and i>4:
                node.piece=Piece('G')
            count+=1
            grid[i].append(node)
    return grid

#Function for creating the chess grid
def make_grid_chess(rows, width):
    grid = []
    gap = width// rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap)
            #Alternating between pink and white spaces
            #Changed to follow chess boards
            if abs(i-j) % 2 == 1:
                node.colour=PINK
            if i == 1:
                node.piece = ChessPiece('B',"B_PAWN")
            if i == 0 and (j == 0 or j == 7):
                node.piece = ChessPiece('B',"B_ROOK")
            if i == 0 and (j == 1 or j == 6):
                node.piece = ChessPiece('B',"B_KNIGHT")
            if i == 0 and (j == 2 or j == 5):
                node.piece = ChessPiece('B',"B_BISHOP")
            if i == 0 and j == 3:
                node.piece = ChessPiece('B',"B_QUEEN")
            if i == 0 and j == 4:
                node.piece = ChessPiece('B', "B_KING")
            if i == 6:
                node.piece = ChessPiece('W',"W_PAWN")
            if i == 7 and (j == 0 or j == 7):
                node.piece = ChessPiece('W',"W_ROOK")
            if i == 7 and (j == 1 or j == 6):
                node.piece = ChessPiece('W',"W_KNIGHT")
            if i == 7 and (j == 2 or j == 5):
                node.piece = ChessPiece('W',"W_BISHOP")
            if i == 7 and j == 3:
                node.piece = ChessPiece('W',"W_QUEEN")
            if i == 7 and j == 4:
                node.piece = ChessPiece('W', "W_KING")
            count+=1
            grid[i].append(node)
    return grid

# Function to draw the game board grid
def draw_grid(win, rows, width):
    gap = width // ROWS
    for i in range(rows):
        pygame.draw.line(win, BLACK, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, BLACK, (j * gap, 0), (j * gap, width))

# Class representing a game piece
class Piece:
    def __init__(self, team):
        self.team=team
        self.image= RED if self.team=='R' else GREEN
        self.type=None

    def draw(self, x, y):
        WIN.blit(self.image, (x,y))

#Class representing a chess piece
class ChessPiece:
    def __init__(self, team, type):
        self.team=team
        self.type=type
        self.turn=0
        if self.team == 'W':
            if self.type == "W_PAWN":
                self.image= WHITEPAWN
            if self.type == "W_ROOK":
                self.image = WHITEROOK
            if self.type == "W_KNIGHT":
                self.image = WHITEKNIGHT
            if self.type == "W_BISHOP":
                self.image = WHITEBISHOP
            if self.type == "W_QUEEN":
                self.image = WHITEQUEEN
            if self.type == "W_KING":
                self.image = WHITEKING
        elif self.team == 'B':
            if self.type == "B_PAWN":
                self.image= BLACKPAWN
            if self.type == "B_ROOK":
                self.image = BLACKROOK
            if self.type == "B_KNIGHT":
                self.image = BLACKKNIGHT
            if self.type == "B_BISHOP":
                self.image = BLACKBISHOP
            if self.type == "B_QUEEN":
                self.image = BLACKQUEEN
            if self.type == "B_KING":
                self.image = BLACKKING

    def draw(self, x, y):
        WIN.blit(self.image, (x,y))


# Function to get the node position based on mouse coordinates
def getNode(grid, rows, width):
    gap = width//rows
    RowX,RowY = pygame.mouse.get_pos()
    Row = RowX//gap
    Col = RowY//gap
    return (Col,Row)

# Function to reset colors on the game board
def resetColours(grid, node):
    positions = generatePotentialMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = BLACK if abs(nodeX - nodeY) % 2 == 0 else WHITE

def resetChessColours(grid, node):
    positions = generatePotentialChessMoves(node, grid)
    positions.append(node)

    for colouredNodes in positions:
        nodeX, nodeY = colouredNodes
        grid[nodeX][nodeY].colour = PINK if abs(nodeX - nodeY) % 2 == 1 else WHITE


# Function to highlight potential moves on the game board
def HighlightpotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)
    for position in positions:
        Column,Row = position
        grid[Column][Row].colour=BLUE

def HighlightpotentialChessMoves(piecePosition, grid):
    positions = generatePotentialChessMoves(piecePosition, grid)
    for position in positions:
        Column,Row = position
        grid[Column][Row].colour=BLUE

# Function to get the opposite team color
def opposite(team):
    return "R" if team=="G" else "G"

def oppositeChess(team):
    return "B" if team=="W" else "W"

# Function to generate potential moves for a given piece position
def generatePotentialMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        vectors = [[1, -1], [1, 1]] if grid[column][row].piece.team == "R" else [[-1, -1], [-1, 1]]
        if grid[column][row].piece.type=='KING':
            vectors = [[1, -1], [1, 1],[-1, -1], [-1, 1]]
        for vector in vectors:
            columnVector, rowVector = vector
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==opposite(grid[column][row].piece.team):

                    if checker((2* columnVector), column) and checker((2* rowVector), row) \
                            and not grid[(2* columnVector)+ column][(2* rowVector) + row].piece:
                        positions.append((2* columnVector+ column,2* rowVector+ row ))

    return positions

def generatePotentialChessMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        if grid[column][row].piece.team=='W':
            if grid[column][row].piece.type=='W_PAWN':
                if grid[column][row].piece.turn == 0:
                    vectors = [[-1, 0], [-2, 0]]
                else:
                    vectors = [[-1, 0]]
            if grid[column][row].piece.type=='W_KING':
                vectors = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
            if grid[column][row].piece.type=='W_QUEEN':
                vectors = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], 
                           [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0], 
                           [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                           [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7],
                           [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],
                           [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7],
                           [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7],
                           [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]]
            if grid[column][row].piece.type=='W_ROOK':
                vectors = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], 
                           [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0], 
                           [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                           [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]]
            if grid[column][row].piece.type=='W_KNIGHT':
                vectors = [[2, -1], [1, -2], [2, 1], [1, 2], [-2, -1], [-1, -2], [-2, 1], [-1, 2]]
            if grid[column][row].piece.type=='W_BISHOP':
                vectors = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],
                           [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7],
                           [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7],
                           [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]]
        else:
            if grid[column][row].piece.type=='B_PAWN':
                if grid[column][row].piece.turn == 0:
                    vectors = [[1, 0], [2, 0]]
                else:
                    vectors = [[1, 0]]
            if grid[column][row].piece.type=='B_KING':
                vectors = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
            if grid[column][row].piece.type=='B_QUEEN':
                vectors = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], 
                           [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0], 
                           [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                           [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7],
                           [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],
                           [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7],
                           [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7],
                           [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]]
            if grid[column][row].piece.type=='B_ROOK':
                vectors = [[1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [6, 0], [7, 0], 
                           [-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0], [-6, 0], [-7, 0], 
                           [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [0, 7],
                           [0, -1], [0, -2], [0, -3], [0, -4], [0, -5], [0, -6], [0, -7]]
            if grid[column][row].piece.type=='B_KNIGHT':
                vectors = [[2, -1], [1, -2], [2, 1], [1, 2], [-2, -1], [-1, -2], [-2, 1], [-1, 2]]
            if grid[column][row].piece.type=='B_BISHOP':
                vectors = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7],
                           [-1, 1], [-2, 2], [-3, 3], [-4, 4], [-5, 5], [-6, 6], [-7, 7],
                           [1, -1], [2, -2], [3, -3], [4, -4], [5, -5], [6, -6], [7, -7],
                           [-1, -1], [-2, -2], [-3, -3], [-4, -4], [-5, -5], [-6, -6], [-7, -7]]
        for vector in vectors:
            columnVector, rowVector = vector
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                elif grid[column+columnVector][row+rowVector].piece and\
                        grid[column+columnVector][row+rowVector].piece.team==oppositeChess(grid[column][row].piece.team):

                    if checker((2* columnVector), column) and checker((2* rowVector), row) \
                            and not grid[(2* columnVector)+ column][(2* rowVector) + row].piece:
                        positions.append((2* columnVector+ column,2* rowVector+ row ))

    return positions


"""
Error with locating possible moves row col error
"""
# Function to highlight the selected piece and its potential moves
def highlight(ClickedNode, Grid, OldHighlight):
    Column,Row = ClickedNode
    Grid[Column][Row].colour=ORANGE
    if OldHighlight:
        resetColours(Grid, OldHighlight)
    HighlightpotentialMoves(ClickedNode, Grid)
    return (Column,Row)

def Chesshighlight(ClickedNode, Grid, OldHighlight):
    Column,Row = ClickedNode
    Grid[Column][Row].colour=ORANGE
    if OldHighlight:
        resetChessColours(Grid, OldHighlight)
    HighlightpotentialChessMoves(ClickedNode, Grid)
    return (Column,Row)

# Function to move a game piece on the board
def move(grid, piecePosition, newPosition):
    resetColours(grid, piecePosition)
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece
    grid[newColumn][newRow].piece=piece
    grid[oldColumn][oldRow].piece = None

    # Check for king status and update piece type and image
    if newColumn==7 and grid[newColumn][newRow].piece.team=='R':
        grid[newColumn][newRow].piece.type='KING'
        grid[newColumn][newRow].piece.image=REDKING
    if newColumn==0 and grid[newColumn][newRow].piece.team=='G':
        grid[newColumn][newRow].piece.type='KING'
        grid[newColumn][newRow].piece.image=GREENKING
    # Check for capturing move and remove captured piece
    if abs(newColumn-oldColumn)==2 or abs(newRow-oldRow)==2:
        grid[int((newColumn+oldColumn)/2)][int((newRow+oldRow)/2)].piece = None
        return grid[newColumn][newRow].piece.team
    return opposite(grid[newColumn][newRow].piece.team)

def moveChess(grid, piecePosition, newPosition):
    resetChessColours(grid, piecePosition)
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece
    grid[newColumn][newRow].piece=piece
    grid[oldColumn][oldRow].piece = None

    # Check for king status and update piece type and image
    if newColumn==7 and grid[newColumn][newRow].piece.team=='W':
        grid[newColumn][newRow].piece.type='KING'
        grid[newColumn][newRow].piece.image=REDKING
    if newColumn==0 and grid[newColumn][newRow].piece.team=='B':
        grid[newColumn][newRow].piece.type='KING'
        grid[newColumn][newRow].piece.image=GREENKING
    # Check for capturing move and remove captured piece
    if abs(newColumn-oldColumn)==2 or abs(newRow-oldRow)==2:
        grid[int((newColumn+oldColumn)/2)][int((newRow+oldRow)/2)].piece = None
        return grid[newColumn][newRow].piece.team
    return oppositeChess(grid[newColumn][newRow].piece.team)

#WINNER
def check_for_winner(grid):
    # Check for a winning condition (you need to define the winning condition based on your game rules)
    # For example, if all pieces of one color are eliminated, that color is the winner.
    # You might need to adapt this based on your specific game rules.
    red_pieces = sum(row.count(node) for row in grid for node in row if node.piece and node.piece.team == 'R')
    green_pieces = sum(row.count(node) for row in grid for node in row if node.piece and node.piece.team == 'G')

    if red_pieces == 0:
        return 'G'
    elif green_pieces == 0:
        return 'R'
    else:
        return None

#Game reset
def reset_game(grid):
    # Reset the board to its initial state
    for i in range(ROWS):
        for j in range(ROWS):
            grid[i][j].colour = BLACK if abs(i - j) % 2 == 0 else WHITE
            grid[i][j].piece = None
            if abs(i + j) % 2 == 0 and i < 3:
                grid[i][j].piece = Piece('R')
            elif abs(i + j) % 2 == 0 and i > 4:
                grid[i][j].piece = Piece('G')

# Main function to run the game loop
def main(WIDTH, ROWS):
    highlightedPiece = None

    game_over = False

    #Print statements asking for a gamemode
    print("1: Play Checkers")
    print("2: Play Chess")
    print("Other: Quit")

    #Loop to get user input to determine gamemode
    while True:
        #User must enter a positive integer otherwise,
        #An exception is thrown
        try:
            gameMode = int(input(""))
            if gameMode > -1:
                break
            else:
                print("Enter a positive integer")
        except:
            print("Invalid Input. Please enter a positive integer")

    #Lets play Checkers
    if gameMode == 1:
        #while True:
        print("Playing Checkers")
        currMove = 'G'
        grid = make_grid(ROWS, WIDTH)
        while not game_over:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickedNode = getNode(grid, ROWS, WIDTH)
                    ClickedPositionColumn, ClickedPositionRow = clickedNode
                    if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            resetColours(grid, highlightedPiece)
                            currMove=move(grid, highlightedPiece, clickedNode)
                    elif highlightedPiece == clickedNode:
                        pass
                    else:
                        if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                            if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                                highlightedPiece = highlight(clickedNode, grid, highlightedPiece)

            # Check for a winning condition
            winner = check_for_winner(grid)
            if winner is not None:
                print(f"Player {winner} wins!")
                reset_game(grid)
                game_over = False

            update_display(WIN, grid,ROWS,WIDTH)
    
    #Lets play Chess
    elif gameMode == 2:
        print("Playing Chess")
        currMove = 'W'
        grid = make_grid_chess(ROWS, WIDTH)
        while not game_over:
            for event in pygame.event.get():
                #If the game exited
                if event.type== pygame.QUIT:
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()

                #When the mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    clickedNode = getNode(grid, ROWS, WIDTH)
                    ClickedPositionColumn, ClickedPositionRow = clickedNode
                    #
                    if grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE:
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            resetChessColours(grid, highlightedPiece)
                            currMove=moveChess(grid, highlightedPiece, clickedNode)
                    elif highlightedPiece == clickedNode:
                        pass
                    else:
                        if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                            if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                                highlightedPiece = Chesshighlight(clickedNode, grid, highlightedPiece)

            # Check for a winning condition
            winner = check_for_winner(grid)
            ##if winner is not None:
            ##    print(f"Player {winner} wins!")
            ##    reset_game(grid)
            ##    game_over = False

            update_display(WIN, grid,ROWS,WIDTH)

    #Quit the game
    else:
        # Close the pygame window
        pygame.quit()
        sys.exit()



main(WIDTH, ROWS)
