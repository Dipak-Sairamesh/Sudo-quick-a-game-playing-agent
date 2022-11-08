import pygame
import pygame_widgets as pw
import sys
import requests
from random_grid import RandomGrid

def DrawGrid():
    # Lines for the 9x9 Sudoku Grid
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                # filling non-empty cells
                pygame.draw.rect(screen, (0, 205, 205), (i * inc, j * inc, inc + 1, inc + 1))
                # inserting default values
                text = a_font.render(str(grid[i][j]), True, (0, 0, 128))
                screen.blit(text, (i * inc + 20, j * inc + 15))
    # Draw lines horizontally and vertically to form grid
    for i in range(10):
        if i % 3 == 0:
            width = 10
        else:
            width = 5
        pygame.draw.line(screen, (0, 0, 0), (i * inc, 0), (i * inc, 500), width)  # vertical
        pygame.draw.line(screen, (0, 0, 0), (0, i * inc), (500, i * inc), width)  # horizontal

# Game modes for the user
def DrawModes():
    TitleFont = pygame.font.SysFont("helvetica", 22, "bold")
    AttributeFont = pygame.font.SysFont("helvetica", 20, "bold")
    screen.blit(TitleFont.render("Game Options", True, (0, 0, 0)), (15, 505))
    screen.blit(AttributeFont.render("C: Clear", True, (0, 51, 204)), (30, 530))
    screen.blit(AttributeFont.render("S: Solve", True, (0, 51, 204)), (150, 530))
    screen.blit(AttributeFont.render("Q: Quit", True, (0, 51, 204)), (270, 530))
    screen.blit(TitleFont.render("Game Modes", True, (0, 0, 0)), (15, 555))
    screen.blit(AttributeFont.render("E: Easy", True, (0, 51, 204)), (30, 580))
    screen.blit(AttributeFont.render("M: Medium", True, (0, 51, 204)), (30, 605))
    screen.blit(AttributeFont.render("H: Hard", True, (0, 51, 204)), (30, 630))
    screen.blit(AttributeFont.render("R: Random", True, (0, 51, 204)), (30, 650))
    screen.blit(AttributeFont.render("D: Dataset Puzzle", True, (0, 51, 204)), (150, 600))

# Solving using Backtracking Algorithm
def SolveGrid(gridArray, i, j):
    global IsSolving
    IsSolving = True
    while gridArray[i][j] != 0:  # cell is not empty
        # this loop goes through the entire grid
        if i < 8:
            i += 1
        elif i == 8 and j < 8:  # go back to the first column and next row
            i = 0
            j += 1
        elif i == 8 and j == 8:  # go through all rows and columns
            return True
    pygame.event.pump()  # called once every loop
    for V in range(1, 10):  # trying values from 1->9 inclusive
        if IsValueValid(gridArray, i, j, V):  # if the value is correct, add it to the grid
            gridArray[i][j] = V
            if SolveGrid(gridArray, i, j):  # if the value is correct, keep it
                return True
            else:  # else keep the box empty
                gridArray[i][j] = 0
        screen.fill((124, 252, 0))
        DrawGrid()
        DrawModes()
        pygame.display.update()
    return False

def SetGridMode(Mode):
    global grid
    screen.fill((238, 238, 0))
    DrawModes()
    
    if Mode == 0:  # For clearing the grid
        grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]

    elif Mode == 1: # GET Puzzle - Easy Difficulty
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy")
        grid = response.json()['board']

    elif Mode == 2: # GET Puzzle - Medium Difficulty
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=medium")
        grid = response.json()['board']

    elif Mode == 3: # GET Puzzle - Hard Difficulty
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=hard")
        grid = response.json()['board']

    elif Mode == 4: # GET Puzzle - Random Difficulty
        response = requests.get("https://sugoku.herokuapp.com/board?difficulty=random")
        grid = response.json()['board']

    elif Mode == 5: # Generate random puzzle from 1,000,000 puzzle dataset
        grid = RandomGrid()

def IsValueValid(m, i, j, v): # Checks if a number between 1-9 is valid at the current cell
    for ii in range(9):
        if m[i][ii] == v or m[ii][j] == v:  # checks columns and rows
            return False
    # checks each block
    ii = i // 3
    jj = j // 3
    for i in range(ii * 3, ii * 3 + 3):
        for j in range(jj * 3, jj * 3 + 3):
            if m[i][j] == v:
                return False
    return True

def HandleEvents():
    global IsRunning, grid, x, y
    events = pygame.event.get()
    for event in events:
        # Quit the game window
        if event.type == pygame.QUIT:
            IsRunning = False
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if not IsSolving:
                if event.key == pygame.K_c:
                    SetGridMode(0)
                if event.key == pygame.K_e:
                    SetGridMode(1)
                if event.key == pygame.K_m:
                    SetGridMode(2)
                if event.key == pygame.K_h:
                    SetGridMode(3)
                if event.key == pygame.K_r:
                    SetGridMode(4)
                if event.key == pygame.K_d:
                    SetGridMode(5)
                if event.key == pygame.K_s:
                    DrawGrid()
                    DrawModes()
                    IsRunning = True
                    SolveGrid(grid, 0, 0)
                if event.key == pygame.K_q:
                    IsRunning = False
                    sys.exit()
    pw.update(events)

def InitializeComponent():
    DrawGrid()
    DrawModes()
    pygame.display.update()

def GameThread():
    InitializeComponent()
    while IsRunning:
        HandleEvents()
        DrawGrid()
        pygame.display.update()



if __name__ == '__main__':
    pygame.font.init()
    screen = pygame.display.set_mode((500, 690))  # Window size
    screen.fill((0, 205, 205))
    pygame.display.set_caption("SUDO-QU-ICK")
    a_font = pygame.font.SysFont("helvetica", 30, "bold")  
    b_font = pygame.font.SysFont("helvetica", 15, "bold")

    inc = 500 // 9  # Screen size // Number of boxes = each increment
    x = 0
    y = 0
    UserValue = 0
    grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
    IsRunning = True
    IsSolving = False
    GameThread()


