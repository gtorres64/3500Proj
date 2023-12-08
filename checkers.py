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
YELLOW = (255, 255, 0)
GREENGRID = (0, 255, 0)
ENPASSANT = (0, 0, 255)

# Initialize Pygame
pygame.init()
label_gap = 20
WIN = pygame.display.set_mode((WIDTH + label_gap, WIDTH + label_gap))
pygame.display.set_caption('Checkers')
jump = False

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

# Function to create the initial test case game board grid 
def make_grid_test_case(rows, width):
    grid = []
    gap = width// rows
    count = 0
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(j,i, gap)
            if abs(i-j) % 2 == 0:
                node.colour=BLACK
            if (abs(i+j)%2==0) and (i==0) and (j!=2) and (j!=6):
                node.piece = Piece('R')
            elif (abs(i+j)%2==0) and (i==1) and (j!=1):
                node.piece = Piece('R')
            elif (abs(i+j)%2==0) and (i==2) and (j!=2) and (j!=4):
                node.piece = Piece('R')
            elif (abs(i+j)%2==0) and (i==3) and (j==1):
                node.piece = Piece('R')
            elif(abs(i+j)%2==0) and (i==3) and (j==3):
                node.piece=Piece('G')
            elif(abs(i+j)%2==0) and (i>4) and (i<7) and (j!=4) and (j!=5):
                node.piece=Piece('G')
            elif(abs(i+j)%2==0) and (i==7) and (j==3):
                node.piece=Piece('R')
                node.piece.type='KING'
                node.piece.image=REDKING
            count+=1
            grid[i].append(node)
    return grid

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

#Function for creating the chess grid test case
def make_grid_chess_test_case(rows, width):
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
            if i == 1  and j != 3 and j != 4:
                node.piece = ChessPiece('B',"B_PAWN")
            if (i == 2  and j == 3):
                node.piece = ChessPiece('B',"B_PAWN")
            if (i == 3 and j == 4):
                node.piece = ChessPiece('B',"B_PAWN")
            if i == 0 and (j == 0 or j == 7):
                node.piece = ChessPiece('B',"B_ROOK")
            if i == 2 and (j == 2 or j == 5):
                node.piece = ChessPiece('B',"B_KNIGHT")
            if j == 4 and (i == 1 or i == 2):
                node.piece = ChessPiece('B',"B_BISHOP")
            if i == 0 and j == 4:
                node.piece = ChessPiece('B',"B_QUEEN")
            if i == 2 and j == 7:
                node.piece = ChessPiece('B', "B_KING")
            if i == 4 and j == 4:
                node.piece = ChessPiece('W',"W_PAWN")
            if i == 6 and j != 4:
                node.piece = ChessPiece('W',"W_PAWN")
            if i == 7 and (j == 0 or j == 5):
                node.piece = ChessPiece('W',"W_ROOK")
            if i == 4 and (j == 0):
                node.piece = ChessPiece('W',"W_KNIGHT")
            if i == 5 and (j == 5):
                node.piece = ChessPiece('W',"W_KNIGHT")
            if i == 3 and (j == 1):
                node.piece = ChessPiece('W',"W_BISHOP")
            if i == 7 and (j == 2):
                node.piece = ChessPiece('W',"W_BISHOP")
            if i == 7 and j == 6:
                node.piece = ChessPiece('W',"W_QUEEN")
            if i == 7 and j == 3:
                node.piece = ChessPiece('W', "W_KING")
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

# function to draw labels for columns and rows
def draw_labels():
    # define font for labels
    label_font = pygame.font.Font(None, 36) 

    # draw column labels 8-1
    for i in range(ROWS):
        text = label_font.render(str(8 - i), True, WHITE)  
        # create border for labels
        text_rect = text.get_rect(center=(WIDTH + label_gap // 2, (i * (WIDTH // ROWS)) + (WIDTH // (2 * ROWS))))
        pygame.draw.rect(WIN, BLACK, text_rect)
        # draw the text onto window on top of border for labels
        WIN.blit(text, text_rect)

    # draw row labels A-H
    for i in range(ROWS):
        text = label_font.render(chr(65 + i), True, WHITE)
        text_rect = text.get_rect(center=((i * (WIDTH // ROWS)) + (WIDTH // (2 * ROWS)), WIDTH + label_gap // 2))
        pygame.draw.rect(WIN, BLACK, text_rect)
        WIN.blit(text, text_rect)


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
        self.turnCount=0
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

class PrevMove:
    def __init__(self, piece, start, end, move=None):
        self.piece=piece
        self.start=start
        self.end=end
        self.count=0
        self.move=move


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
    for nodeX in range(0,8):
        for nodeY in range(0,8):
            grid[nodeX][nodeY].colour = PINK if abs(nodeX - nodeY) % 2 == 1 else WHITE


# Function to highlight potential moves on the game board
def HighlightpotentialMoves(piecePosition, grid):
    positions = generatePotentialMoves(piecePosition, grid)
    for position in positions:
        Column,Row = position
        grid[Column][Row].colour=BLUE

def HighlightpotentialChessMoves(piecePosition, grid, lastMove):
    positions = generatePotentialChessMoves(piecePosition, grid, lastMove)
    clickedColumn, clickedRow = piecePosition
    for position in positions:
        Column,Row = position
        grid[Column][Row].colour=BLUE
        #Making sure there is a piece on the space
        if grid[Column][Row].piece:
            #If the clicked piece and a highlighted piece are not on the same team
            if grid[clickedColumn][clickedRow].piece.team != grid[Column][Row].piece.team:
                #Lets highlight capturable peices to green!
                grid[Column][Row].colour=GREENGRID

# Function to get the opposite team color
def opposite(team):
    return "R" if team=="G" else "G"

def oppositeChess(team):
    return "B" if team=="W" else "W"

# Function to check for stalemate in checkers
def check_stalemate(grid, team):
    for row in grid:
        for node in row:
            if node.piece and node.piece.team == team:
                moves = generatePotentialMoves((node.row, node.col), grid)
                if moves:
                    return False
    return True

# Function to generate potential moves for a given piece position
def generatePotentialMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    positionsJump= []
    forceJump=0
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
                        positionsJump.append((2* columnVector+ column,2* rowVector+ row ))
                        forceJump = 1
    if forceJump:
        return positionsJump
    else:
        return positions
    
def queenMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    column, row = nodePosition
    #For loop to begin calculating the new vector
    #We will append to this vector and dynamically create the moves
    vectors = []
    for vector0, vector1 in [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [-1, 1], [1, -1], [-1, -1]]:
        for j in range(1, 8):
            #We will take each vector from the inital list
            #And multiply the y and x by j then append it to the vectors list
            #This will give us the complete move list
            newvector0, newvector1 = vector0 * j, vector1 * j
            newcolumn, newrow = column + j * vector0, row + j * vector1
            #We need to check if the new vector is in bounds
            if not 0 <= newcolumn < ROWS or not 0 <= newrow < ROWS:
                break
            #Stop generating in this direction if there is a piece in the way
            #We also need to specify if its an opposite piece, which we can capture
            if grid[newcolumn][newrow].piece:
                if grid[newcolumn][newrow].piece.team != grid[column][row].piece.team:
                    vectors.append([newvector0, newvector1])
                break
            vectors.append([newvector0, newvector1])

    return vectors

def rookMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    column, row = nodePosition
    #For loop to begin calculating the new vector
    #We will append to this vector and dynamically create the moves
    vectors = []
    for vector0, vector1 in [[1, 0], [-1, 0], [0, 1], [0, -1]]:
        for j in range(1, 8):
            #We will take each vector from the inital list
            #And multiply the y and x by j then append it to the vectors list
            #This will give us the complete move list
            newvector0, newvector1 = vector0 * j, vector1 * j
            newcolumn, newrow = column + j * vector0, row + j * vector1
            #We need to check if the new vector is in bounds
            if not 0 <= newcolumn < ROWS or not 0 <= newrow < ROWS:
                break
            #Stop generating in this direction if there is a piece in the way
            #We also need to specify if its an opposite piece, which we can capture
            if grid[newcolumn][newrow].piece:
                if grid[newcolumn][newrow].piece.team != grid[column][row].piece.team:
                    vectors.append([newvector0, newvector1])
                break
            vectors.append([newvector0, newvector1])

    return vectors

def bishopMoves(nodePosition, grid):
    checker = lambda x,y: x+y>=0 and x+y<8
    column, row = nodePosition
    #For loop to begin calculating the new vector
    #We will append to this vector and dynamically create the moves
    vectors = []
    for vector0, vector1 in [[1, 1], [-1, 1], [1, -1], [-1, -1]]:
        for j in range(1, 8):
            #We will take each vector from the inital list
            #And multiply the y and x by j then append it to the vectors list
            #This will give us the complete move list
            newvector0, newvector1 = vector0 * j, vector1 * j
            newcolumn, newrow = column + j * vector0, row + j * vector1
            #We need to check if the new vector is in bounds
            if not 0 <= newcolumn < ROWS or not 0 <= newrow < ROWS:
                break
            #Stop generating in this direction if there is a piece in the way
            #We also need to specify if its an opposite piece, which we can capture
            if grid[newcolumn][newrow].piece:
                if grid[newcolumn][newrow].piece.team != grid[column][row].piece.team:
                    vectors.append([newvector0, newvector1])
                break
            vectors.append([newvector0, newvector1])

    return vectors

def pawnMoves(nodePosition, grid, lastMove):
    column, row = nodePosition
    vectors = []
    #If statement seperates white and black pawn
    if grid[column][row].piece.type == "W_PAWN":
        #Checking if there is a piece in front
        if not grid[column-1][row].piece:
            #Highlight the square in front
            vectors.append([-1, 0])
            #Checking what turn the pawn is on
            if grid[column][row].piece.turnCount == 0:
                #If its the first turn, we can go two spaces
                if not grid[column-2][row].piece:
                    vectors.append([-2, 0])
        #Now we need to check for capturable pieces
        if row != 0 and row != 7:
            if grid[column-1][row-1].piece:
                if grid[column][row].piece.team != grid[column-1][row-1].piece:
                    vectors.append([-1, -1])
            if grid[column-1][row+1].piece:
                if grid[column][row].piece.team != grid[column-1][row+1].piece:
                    vectors.append([-1, 1])
        elif row == 0:
            if grid[column-1][row+1].piece:
                if grid[column][row].piece.team != grid[column-1][row+1].piece:
                    vectors.append([-1, 1])
        elif row == 7:
            if grid[column-1][row-1].piece:
                if grid[column][row].piece.team != grid[column-1][row-1].piece:
                    vectors.append([-1, -1])
        #Checking for en passant
        if row != 0 and row != 7:
            if (grid[column][row-1].piece and grid[column][row-1].piece.type == "B_PAWN"
                and grid[column][row-1].piece.turnCount == 1):
                if (grid[column][row].piece.team != grid[column][row-1].piece and
                    row-1 == lastMove.end[1]):
                    vectors.append([-1, -1])
                    grid[column][row-1].colour = ENPASSANT
            if (grid[column][row+1].piece and grid[column][row+1].piece.type == "B_PAWN"
                and grid[column][row+1].piece.turnCount == 1):
                if (grid[column][row].piece.team != grid[column][row+1].piece and
                    row+1 == lastMove.end[1]):
                    vectors.append([-1, 1])
                    grid[column][row+1].colour = ENPASSANT
        elif row == 0:
            if (grid[column][row+1].piece and grid[column][row+1].piece.type == "B_PAWN"
                and grid[column][row+1].piece.turnCount == 1):
                if (grid[column][row].piece.team != grid[column][row+1].piece and
                    row+1 == lastMove.end[1]):
                    vectors.append([-1, 1])
                    grid[column][row+1].colour = ENPASSANT
        elif row == 7:
            if (grid[column][row-1].piece and grid[column][row-1].piece.type == "B_PAWN"
                and grid[column][row-1].piece.turnCount == 1):
                if (grid[column][row].piece.team != grid[column][row-1].piece and
                    row-1 == lastMove.end[1]):
                    vectors.append([-1, -1])
                    grid[column][row-1].colour = ENPASSANT
    #Checking the black pawn
    if grid[column][row].piece.type == "B_PAWN":
        if not grid[column+1][row].piece:
            vectors.append([1,0])
            if grid[column][row].piece.turnCount == 0:
                if not grid[column+2][row].piece:
                    vectors.append([2, 0])
        if row != 0 and row != 7:
            if grid[column+1][row-1].piece:
                if grid[column][row].piece.team != grid[column+1][row-1].piece:
                    vectors.append([1, -1])
            if grid[column+1][row+1].piece:
                if grid[column][row].piece.team != grid[column+1][row+1].piece:
                    vectors.append([1, 1])
        elif row == 0:
            if grid[column+1][row+1].piece:
                if grid[column][row].piece.team != grid[column+1][row+1].piece:
                    vectors.append([1, 1])
        elif row == 7:
            if grid[column+1][row-1].piece:
                if grid[column][row].piece.team != grid[column+1][row-1].piece:
                    vectors.append([1, -1])
        #Checking for en passant
        #Making sure we dont go out of bounds
        if row != 0 and row != 7:
            if (grid[column][row-1].piece and grid[column][row-1].piece.type == "W_PAWN"
                and grid[column][row-1].piece.turnCount == 1):
                if (grid[column][row].piece.team != grid[column][row-1].piece and
                    row-1 == lastMove.end[1]):
                    vectors.append([1, -1])
                    grid[column][row-1].colour = ENPASSANT
            if (grid[column][row+1].piece and grid[column][row+1].piece.type == "W_PAWN"
                and grid[column][row+1].piece.turnCount == 1):
                if (grid[column][row].piece.team != grid[column][row+1].piece and
                    row+1 == lastMove.end[1]):
                    vectors.append([1, 1])
                    grid[column][row+1].colour = ENPASSANT
        elif row == 0:
            if (grid[column][row+1].piece and grid[column][row+1].piece.type == "W_PAWN"
                and grid[column][row+1].piece.turnCount == 1):
                if (grid[column][row].piece.team != grid[column][row+1].piece and
                    row+1 == lastMove.end[1]):
                    vectors.append([1, 1])
                    grid[column][row+1].colour = ENPASSANT
        elif row == 7:
            if (grid[column][row-1].piece and grid[column][row-1].piece.type == "W_PAWN"
                and grid[column][row-1].piece.turnCount == 1):
                if (grid[column][row].piece.team != grid[column][row-1].piece and
                    row-1 == lastMove.end[1]):
                    vectors.append([1, -1])
                    grid[column][row-1].colour = ENPASSANT

    return vectors

def kingSideCastle(grid, nodePosition):
    column, row = nodePosition
    if (grid[column][row].piece.type == "W_KING" and grid[column][row].piece.turnCount == 0 and grid[column][row+3].piece and
        grid[column][row+3].piece.type == "W_ROOK" and grid[column][row+3].piece.turnCount == 0):
        if not grid[column][row+1].piece and not grid[column][row+2].piece:
            grid[column][row+2].colour = YELLOW
    elif (grid[column][row].piece.type == "B_KING" and grid[column][row].piece.turnCount == 0 and grid[column][row+3].piece and
        grid[column][row+3].piece.type == "B_ROOK" and grid[column][row+3].piece.turnCount == 0):
        if not grid[column][row+1].piece and not grid[column][row+2].piece:
            grid[column][row+2].colour = YELLOW
    

def queenSideCastle(grid, nodePosition):
    column, row = nodePosition
    if (grid[column][row].piece.type == "W_KING" and grid[column][row].piece.turnCount == 0 and grid[column][row-4].piece and
        grid[column][row-4].piece.type == "W_ROOK" and grid[column][row-4].piece.turnCount == 0):
        if not grid[column][row-1].piece and not grid[column][row-2].piece and not grid[column][row-3].piece:
            grid[column][row-2].colour = YELLOW
    elif (grid[column][row].piece.type == "B_KING" and grid[column][row].piece.turnCount == 0 and grid[column][row-4].piece and
        grid[column][row-4].piece.type == "B_ROOK" and grid[column][row-4].piece.turnCount == 0):
        if not grid[column][row-1].piece and not grid[column][row-2].piece and not grid[column][row-3].piece:
            grid[column][row-2].colour = YELLOW


#Generate potential chess moves
#The Pawns, King and Knights are simple enough, 
#but the Queen, Rook and Bishop can travel far
#We need to dynamically generate a vector in case there is a piece in the way
def generatePotentialChessMoves(nodePosition, grid, lastMove, castling=1):
    checker = lambda x,y: x+y>=0 and x+y<8
    positions= []
    column, row = nodePosition
    if grid[column][row].piece:
        #We need to specify the team color
        if grid[column][row].piece.team=='W':
            #Specifying each peice and their possible moves
            if grid[column][row].piece.type=='W_PAWN':
                vectors = pawnMoves(nodePosition, grid, lastMove)
            if grid[column][row].piece.type=='W_KING':
                vectors = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
                if castling:
                    kingSideCastle(grid, nodePosition)
                    queenSideCastle(grid, nodePosition)
            if grid[column][row].piece.type=='W_QUEEN':
                vectors = queenMoves(nodePosition, grid)
            if grid[column][row].piece.type=='W_ROOK':
                vectors = rookMoves(nodePosition, grid)
            if grid[column][row].piece.type=='W_KNIGHT':
                vectors = [[2, -1], [1, -2], [2, 1], [1, 2], [-2, -1], [-1, -2], [-2, 1], [-1, 2]]
            if grid[column][row].piece.type=='W_BISHOP':
                vectors = bishopMoves(nodePosition, grid)
        else:
            #Black team peices
            if grid[column][row].piece.type=='B_PAWN':
                vectors = pawnMoves(nodePosition, grid, lastMove)
            if grid[column][row].piece.type=='B_KING':
                vectors = [[1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1], [0, -1], [1, -1]]
                if castling:
                    kingSideCastle(grid, nodePosition)
                    queenSideCastle(grid, nodePosition)
            if grid[column][row].piece.type=='B_QUEEN':
                vectors = queenMoves(nodePosition, grid)
            if grid[column][row].piece.type=='B_ROOK':
                vectors = rookMoves(nodePosition, grid)
            if grid[column][row].piece.type=='B_KNIGHT':
                vectors = [[2, -1], [1, -2], [2, 1], [1, 2], [-2, -1], [-1, -2], [-2, 1], [-1, 2]]
            if grid[column][row].piece.type=='B_BISHOP':
                vectors = bishopMoves(nodePosition, grid)
        #This for loop will generate valid moves which means:
        #Making sure there is not piece in the grid vector
        for vector in vectors:
            columnVector, rowVector = vector
            if checker(columnVector,column) and checker(rowVector,row):
                #grid[(column+columnVector)][(row+rowVector)].colour=ORANGE
                #Checking if the grid does NOT have a piece, we must change to
                #Make sure the peice is actually on the same team.
                #If it is, we must change color to signify we can capture.
                if not grid[(column+columnVector)][(row+rowVector)].piece:
                    positions.append((column + columnVector, row + rowVector))
                else:
                    #Special case for pawns since they capture diagonally
                    if grid[(column)][(row)].piece.team != grid[(column+columnVector)][(row+rowVector)].piece.team:
                        positions.append((column + columnVector, row + rowVector))


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

def Chesshighlight(ClickedNode, Grid, OldHighlight, lastMove):
    Column,Row = ClickedNode
    Grid[Column][Row].colour=ORANGE
    if OldHighlight:
        resetChessColours(Grid, OldHighlight)
        Grid[Column][Row].colour=ORANGE
    HighlightpotentialChessMoves(ClickedNode, Grid, lastMove)
    return (Column,Row)

# Function to move a game piece on the board
def move(grid, piecePosition, newPosition):
    global jump
    jump = False
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
        jump = True
        return grid[newColumn][newRow].piece.team
    return opposite(grid[newColumn][newRow].piece.team)

def moveChess(grid, piecePosition, newPosition, lastMove):
    newColumn, newRow = newPosition
    oldColumn, oldRow = piecePosition

    piece = grid[oldColumn][oldRow].piece

    gridCopy = duplicateGrid(grid, oldColumn, oldRow, newColumn, newRow)
    
    if not lastMove == None:
        if checkCheck(gridCopy, piece.team, lastMove):
            print("Invalid move, cannot put king in check!")
            return False

    grid[newColumn][newRow].piece=piece
    grid[oldColumn][oldRow].piece = None
    if grid[newColumn][newRow].piece:
        grid[newColumn][newRow].piece.turnCount+=1
    

    # Special en passant case
    if grid[newColumn][newRow].piece.type == "W_PAWN":
        if (grid[newColumn+1][newRow].piece and grid[newColumn+1][newRow].colour == ENPASSANT
            and grid[newColumn][newRow].piece.type == "W_PAWN"):
            grid[newColumn+1][newRow].piece = None
    elif grid[newColumn][newRow].piece.type == "B_PAWN":
        if (grid[newColumn-1][newRow].piece and grid[newColumn-1][newRow].colour == ENPASSANT
            and grid[newColumn][newRow].piece.type == "B_PAWN"):
            grid[newColumn-1][newRow].piece = None

    # Castling
    if grid[newColumn][newRow].colour == YELLOW and grid[newColumn][newRow].piece.type == "W_KING":
        if newRow == 6:
            grid[7][5].piece = grid[7][7].piece
            grid[7][7].piece = None
            grid[7][5].piece.turnCount+=1
        elif newRow == 2:
            grid[7][3].piece = grid[7][0].piece
            grid[7][0].piece = None
            grid[7][3].piece.turnCount+=1
    elif grid[newColumn][newRow].colour == YELLOW and grid[newColumn][newRow].piece.type == "B_KING":
        if newRow == 6:
            grid[0][5].piece = grid[0][7].piece
            grid[0][7].piece = None
            grid[0][5].piece.turnCount+=1
        elif newRow == 2:
            grid[0][3].piece = grid[0][0].piece
            grid[0][0].piece = None
            grid[0][3].piece.turnCount+=1

    # Promote the pawn into another piece
    if newColumn==0 and grid[newColumn][newRow].piece.type=='W_PAWN':
        print("Pawn promotion! Enter a key to choose a piece")
        print("Queen: Q")
        print("Knight: K")
        print("Bishop: B")
        print("Rook: R")
        #While loop to get user input for pawn promotion
        promotion = True
        while promotion:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        grid[newColumn][newRow].piece.type='W_QUEEN'
                        grid[newColumn][newRow].piece.image=WHITEQUEEN
                        promotion = False
                    elif event.key == pygame.K_k:
                        grid[newColumn][newRow].piece.type='W_KNIGHT'
                        grid[newColumn][newRow].piece.image=WHITEKNIGHT
                        promotion = False
                    elif event.key == pygame.K_b:
                        grid[newColumn][newRow].piece.type='W_BISHOP'
                        grid[newColumn][newRow].piece.image=WHITEBISHOP
                        promotion = False
                    elif event.key == pygame.K_r:
                        grid[newColumn][newRow].piece.type='W_ROOK'
                        grid[newColumn][newRow].piece.image=WHITEROOK
                        promotion = False
    if newColumn==7 and grid[newColumn][newRow].piece.type=='B_PAWN':
        print("Pawn promotion! Enter a key to choose a piece")
        print("Queen: Q")
        print("Knight: K")
        print("Bishop: B")
        print("Rook: R")
        #While loop to get user input for pawn promotion
        promotion = True
        while promotion:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        grid[newColumn][newRow].piece.type='B_QUEEN'
                        grid[newColumn][newRow].piece.image=BLACKQUEEN
                        promotion = False
                    elif event.key == pygame.K_k:
                        grid[newColumn][newRow].piece.type='B_KNIGHT'
                        grid[newColumn][newRow].piece.image=BLACKKNIGHT
                        promotion = False
                    elif event.key == pygame.K_b:
                        grid[newColumn][newRow].piece.type='B_BISHOP'
                        grid[newColumn][newRow].piece.image=BLACKBISHOP
                        promotion = False
                    elif event.key == pygame.K_r:
                        grid[newColumn][newRow].piece.type='B_ROOK'
                        grid[newColumn][newRow].piece.image=BLACKROOK
                        promotion = False

    resetChessColours(grid, piecePosition)

    return True

# Use a duplicated grid that will not be displayed
# This will help check if the next move is valid before actually taking it
def duplicateGrid(grid, oldRow, oldCol, newRow, newCol, width=WIDTH, rows=ROWS):
    dupe = []
    gap = width// rows
    count = 0
    for row in grid:
        rowCopy = []
        for node in row:
            nodeCopy = Node(node.row, node.col, gap)
            nodeCopy.colour = node.colour
            if node.piece:
                pieceCopy = node.piece
                nodeCopy.piece = pieceCopy
            rowCopy.append(nodeCopy)
        dupe.append(rowCopy)

    dupe[newRow][newCol].piece = dupe[oldRow][oldCol].piece
    dupe[oldRow][oldCol].piece = None

    return dupe

#Check if king is checked
def checkCheck(grid, currMove, lastMove):
    king = None
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            node = grid[i][j]
            if node.piece and node.piece.type == "W_KING" and node.piece.team == currMove:
                king = (i, j)
                #print("White king", king)
                break
            if node.piece and node.piece.type == "B_KING" and node.piece.team == currMove:
                king = (i, j)
                #print("Black king", king)
                break

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j].piece and grid[i][j].piece.team != currMove:
                potentialMoves = generatePotentialChessMoves((i, j), grid, lastMove, 0)
                if king in potentialMoves:
                    return True
    return False

#Checking for checkmate
def checkMate(grid, currMove, lastMove, piecePosition, newPosition):
    if not checkCheck(grid, currMove, lastMove):
        return False
    
    for i in range(ROWS):
        for j in range(ROWS):
            node = grid[i][j]
            if node.piece and node.piece.team == currMove:
                potentialMoves = generatePotentialChessMoves((i, j), grid, lastMove, 0)
                for move in potentialMoves:
                    duplicatedGrid = duplicateGrid(grid, i, j, move[0], move[1])
                    if not checkCheck(duplicatedGrid, currMove, lastMove):
                        return False

    return True

def validMove(grid, currMove, lastMove, piecePosition, newPosition):
    for i in range(8):
        for j in range(8):
            node = grid[i][j]
            if node.piece and node.piece.team == currMove:
                potentialMoves = generatePotentialChessMoves((i, j), grid, lastMove, 0)

                for move in potentialMoves:
                    gridCopy = duplicateGrid(grid, i, j, move[0], move[1])

                    if not checkCheck(gridCopy, currMove, lastMove):
                        return True
    return False

#WINNER CHECKERS
def checkWinner(grid):
    red_pieces = sum(row.count(node) for row in grid for node in row if node.piece and node.piece.team == 'R')
    green_pieces = sum(row.count(node) for row in grid for node in row if node.piece and node.piece.team == 'G')

    if red_pieces == 0:
        return 'G'
    elif green_pieces == 0:
        return 'R'
    else:
        return None

#Game reset CHECKERS
def resetGame(grid):
    # Reset the board to its initial state
    for i in range(ROWS):
        for j in range(ROWS):
            grid[i][j].colour = BLACK if abs(i - j) % 2 == 0 else WHITE
            grid[i][j].piece = None
            if abs(i + j) % 2 == 0 and i < 3:
                grid[i][j].piece = Piece('R')
            elif abs(i + j) % 2 == 0 and i > 4:
                grid[i][j].piece = Piece('G')

#MENU                
# Function to display the title screen
def titleScreen():
    # Clear the screen
    WIN.fill(BLACK)
   
    # Display title and options
    font = pygame.font.Font(None, 36)
    title_text = font.render("Welcome to Board Games!", True, WHITE)
    checkers_text = font.render("1: Play Checkers", True, BLUE)
    chess_text = font.render("2: Play Chess", True, BLUE)
    test_checkers_text = font.render("3: Play Test Checkers", True, BLUE)
    test_chess_text = font.render("4: Play Test Chess", True, BLUE)
    quit_text = font.render("0: Quit", True, BLUE)

    # Position the text on the screen
    title_rect = title_text.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    checkers_rect = checkers_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    chess_rect = chess_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
    test_checkers_rect = test_checkers_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 100))
    test_chess_rect = test_chess_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
    quit_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 200))

    # Blit the text onto the screen
    WIN.blit(title_text, title_rect)
    WIN.blit(checkers_text, checkers_rect)
    WIN.blit(chess_text, chess_rect)
    WIN.blit(test_checkers_text, test_checkers_rect)
    WIN.blit(test_chess_text, test_chess_rect)
    WIN.blit(quit_text, quit_rect)

    pygame.display.flip()


#RESET CHESS GRID
def resetChessGame():
    global lastMove
    global priorMoves

    # Reset last move and prior moves
    lastMove = None
    priorMoves = []

    # Create a new chess grid
    chess_grid = make_grid_chess(ROWS, WIDTH)

    # Update the display with the new grid
    update_display(WIN, chess_grid, ROWS, WIDTH)

    return chess_grid

#CHECKMATE SCREEN
#RESTART OR QUIT CHECKERS
def endCheckers():
    print("GAME OVER!! PRESS THE FOLLOWING")
    print("0: Quit")
    print("R: Restart")

#RESTART OR QUIT CHESS
def endChess():
    print("GAME OVER!! PRESS THE FOLLOWING")
    print("0: Quit")
    print("R: Restart")                

# Main function to run the game loop
def main(WIDTH, ROWS):
    highlightedPiece = None

    game_over = False
    testcase = 0
    global jump

    #Print statements asking for a gamemode
    print("1: Play Checkers")
    print("2: Play Chess")
    print("0: Quit")

    #Loop to get user input to determine gamemode
    noInput = True
    while noInput:
        titleScreen()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print('EXIT SUCCESSFUL')
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    gameMode = 1
                    noInput = False
                elif event.key == pygame.K_2:
                    gameMode = 2
                    noInput = False
                elif event.key == pygame.K_3:
                    gameMode = 1
                    testcase = 1
                    noInput = False
                elif event.key == pygame.K_4:
                    gameMode = 2
                    testcase = 1
                    noInput = False
                elif event.key == pygame.K_0:
                    gameMode = 3
                    noInput = False

    #Lets play Checkers
    if gameMode == 1:
        #while True:
        print("Playing Checkers")
        print("0: Quit Game")
        print("R: Restart Game")
        currMove = 'G'
        if not testcase:
            grid = make_grid(ROWS, WIDTH)
        else:
             grid = make_grid_test_case(ROWS, WIDTH)
        while not game_over:
            for event in pygame.event.get():
                if event.type== pygame.QUIT:
                    print('EXIT SUCCESSFUL')
                    pygame.quit()
                    sys.exit()
                #Take action when mouse is clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if jump and not generatePotentialMoves(clickedNode, grid):
                        currMove = 'R' if currMove == 'G' else 'G'
                        jump = False
                    elif not jump:
                        clickedNode = getNode(grid, ROWS, WIDTH)
                    else: 
                        if getNode(grid, ROWS, WIDTH) in generatePotentialMoves(clickedNode, grid):
                            clickedNode = getNode(grid, ROWS, WIDTH)
                    #Gets the clicked node
                    ClickedPositionColumn, ClickedPositionRow = clickedNode
                    #If statement if the user clicks a highlighted node
                    if (
                        ClickedPositionColumn < ROWS and
                        ClickedPositionRow < ROWS and
                        grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE
                    ):
                        #Get the column and row of the highlighted piece
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        #Checking if it is the current player's turn
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            #Reset the colors after moving, then move the actual piece to the clicked node
                            resetColours(grid, highlightedPiece)
                            currMove=move(grid, highlightedPiece, clickedNode)

                            # check for stalemate after a move
                            if check_stalemate(grid, 'R') and check_stalemate(grid, 'G'):
                                print("Stalemate! It's a draw!")

                    #Nothing happens if the user clicks the selected piece
                    elif highlightedPiece == clickedNode:
                        pass
                    elif ClickedPositionColumn >= ROWS or ClickedPositionRow >= ROWS:
                        # checkif click is within grid boundaries 
                        if ClickedPositionColumn < ROWS and ClickedPositionRow < ROWS:
                            # handle clicks inside border but outside playable grid
                            pass
                    else:
                        #Highlight a piece when the player clicks if it belongs to the player
                        if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                            if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                                highlightedPiece = highlight(clickedNode, grid, highlightedPiece)

                # Check for key presses
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        resetGame(grid)
                        currMove = 'G'
                        game_over = False  # Reset the game_over variable
                    elif event.key == pygame.K_0:
                        pygame.quit()
                        sys.exit()

            
            # Check for a winning condition
            winner = checkWinner(grid)
            if winner is not None:
                print(f"Player {winner} wins!")
                resetGame(grid)
                game_over = False
            



            update_display(WIN, grid,ROWS,WIDTH)
            draw_labels()
    
    #Lets play Chess
    elif gameMode == 2:
        print("Playing Chess")
        currMove = 'W'
        if not testcase:
            grid = make_grid_chess(ROWS, WIDTH)
        else:
             grid = make_grid_chess_test_case(ROWS, WIDTH)
        lastMove = None
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
                    # Will execute when a piece is highlighted blue, move the piece to an empty space
                    if (
                        ClickedPositionColumn < ROWS and
                        ClickedPositionRow < ROWS and
                        grid[ClickedPositionColumn][ClickedPositionRow].colour == BLUE
                    ):
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            moveIsValid = moveChess(grid, highlightedPiece, clickedNode, None)
                            if moveIsValid:
                                newPiece = grid[ClickedPositionColumn][ClickedPositionRow].piece
                                lastMove = PrevMove(newPiece, highlightedPiece, clickedNode)
                                resetChessColours(grid, highlightedPiece)
                                if checkCheck(grid, oppositeChess(currMove), lastMove):
                                    print(currMove, " Check")
                                    if not validMove(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                        if checkMate(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                            
                                            print(currMove, " Checkmate")
                                            update_display(WIN, grid,ROWS,WIDTH)
                                            endChess()
                                            while True:
                                                for event in pygame.event.get():
                                                    if event.type == pygame.KEYDOWN:
                                                        if event.key == pygame.K_0:
                                                            pygame.quit()
                                                            sys.exit()
                                                        elif event.key == pygame.K_r:
                                                            resetChessGame()

                                else:
                                    if not validMove(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                        print("Stalemate")
                                currMove = oppositeChess(currMove)
                    # Code for capturing pieces, highlighted in green
                    elif (
                        ClickedPositionColumn < ROWS and
                        ClickedPositionRow < ROWS and
                        grid[ClickedPositionColumn][ClickedPositionRow].colour == GREENGRID
                    ):
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            moveIsValid = moveChess(grid, highlightedPiece, clickedNode, lastMove)
                            if moveIsValid:
                                newPiece = grid[ClickedPositionColumn][ClickedPositionRow].piece
                                lastMove = PrevMove(newPiece, highlightedPiece, clickedNode)
                                resetChessColours(grid, highlightedPiece)
                                if checkCheck(grid, oppositeChess(currMove), lastMove):
                                    print(currMove, " Check")
                                    if not validMove(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                        if checkMate(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                            print(currMove, " Checkmate")
                                            update_display(WIN, grid,ROWS,WIDTH)

                                            endChess()
                                            while True:
                                                for event in pygame.event.get():
                                                    if event.type == pygame.KEYDOWN:
                                                        if event.key == pygame.K_0:
                                                            pygame.quit()
                                                            sys.exit()
                                                        elif event.key == pygame.K_r:
                                                            resetChessGame()

                                else:
                                    if not validMove(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                        print("Stalemate")
                                currMove = oppositeChess(currMove)
                    # A yellow node means we can castle, handle that here
                    elif (
                        ClickedPositionColumn < ROWS and
                        ClickedPositionRow < ROWS and
                        grid[ClickedPositionColumn][ClickedPositionRow].colour == YELLOW
                    ):
                        if highlightedPiece:
                            pieceColumn, pieceRow = highlightedPiece
                        if currMove == grid[pieceColumn][pieceRow].piece.team:
                            moveIsValid = moveChess(grid, highlightedPiece, clickedNode, lastMove)
                            if moveIsValid:
                                newPiece = grid[ClickedPositionColumn][ClickedPositionRow].piece
                                lastMove = PrevMove(newPiece, highlightedPiece, clickedNode)
                                resetChessColours(grid, highlightedPiece)
                                if checkCheck(grid, oppositeChess(currMove), lastMove):
                                    print(currMove, " Check")
                                    if not validMove(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                        if checkMate(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                            print(currMove, " Checkmate")
                                            update_display(WIN, grid,ROWS,WIDTH)

                                            endChess()
                                            while True:
                                                for event in pygame.event.get():
                                                    if event.type == pygame.KEYDOWN:
                                                        if event.key == pygame.K_0:
                                                            pygame.quit()
                                                            sys.exit()
                                                        elif event.key == pygame.K_r:
                                                            resetChessGame()

                                else:
                                    if not validMove(grid, oppositeChess(currMove), lastMove, highlightedPiece, clickedNode):
                                        print("Stalemate")
                                currMove = oppositeChess(currMove)
                            
                    # Do nothing if we click the same peice
                    elif highlightedPiece == clickedNode:
                        pass
                    elif ClickedPositionColumn >= ROWS or ClickedPositionRow >= ROWS:
                        if ClickedPositionColumn < ROWS and ClickedPositionRow < ROWS:
                            pass
                    # Other case
                    else:
                        #If the clicked node has a piece and belongs to the same team, we can highlight it
                        if grid[ClickedPositionColumn][ClickedPositionRow].piece:
                            if currMove == grid[ClickedPositionColumn][ClickedPositionRow].piece.team:
                                highlightedPiece = Chesshighlight(clickedNode, grid, highlightedPiece, lastMove)

            # Check for a winning condition
            #winner = check_for_winner(grid)
            ##if winner is not None:
            ##    print(f"Player {winner} wins!")
            ##    reset_game(grid)
            ##    game_over = False

            update_display(WIN, grid,ROWS,WIDTH)
            draw_labels()

    #Quit the game
    else:
        # Close the pygame window
        pygame.quit()
        sys.exit()

# Constants for window size
WIDTH = 800
HEIGHT = 600

main(WIDTH, ROWS)