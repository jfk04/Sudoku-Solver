import pygame
import time
import sudoku_solver

# Settings
CELL_SIZE = 60
WIDTH = HEIGHT_GRID = CELL_SIZE * 9
HEIGHT = CELL_SIZE * 9 + 80
BUTTON_SOLVE_RECT = pygame.Rect(180, 550, 180, 40)
BUTTON_COLOR = (70, 130, 180)
TEXT_COLOR = (0, 0, 0)
CURRENT_CELL = None
SELECTED_CELL = None

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FONT = pygame.font.SysFont("Arial", 32)
FONT_NUMBERS = pygame.font.SysFont("Arial", 36)
pygame.display.set_caption("Sudoku Solver")
running = True
solving = False
HIGHLIGHTED_CELLS = []

def draw_grid():
    for i in range (10):
        if i % 3 == 0:
            thickness = 3
        else:
            thickness = 1
        pygame.draw.line(screen, (0, 0, 0), (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), thickness)
        pygame.draw.line(screen, (0, 0, 0), (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT_GRID), thickness)

def draw_button():
    # Button
    pygame.draw.rect(screen, BUTTON_COLOR, BUTTON_SOLVE_RECT)
    text = FONT.render("Solve", True, TEXT_COLOR)
    screen.blit(text, text.get_rect(center=BUTTON_SOLVE_RECT.center))

def draw_sudoku_numbers(screen, board):
    for row in range(9):
        for col in range(9):
            num = board[row][col]
            if num != 0:    # Zahl gefunden
                text = FONT_NUMBERS.render(str(num), True, TEXT_COLOR)
                x = col * CELL_SIZE + CELL_SIZE // 2 - text.get_width() // 2
                y = row * CELL_SIZE + CELL_SIZE // 2 - text.get_height() // 2
                screen.blit(text, (x, y))


def draw_Screen():
    draw_grid()
    draw_button()
    draw_sudoku_numbers(screen, sudoku_solver.board)

def highlight_cell():
    for CELL in HIGHLIGHTED_CELLS:
        rect = pygame.Rect(CELL[1] * CELL_SIZE, CELL[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (0, 180, 0), rect)

def highlight_selceted_cell():
    if SELECTED_CELL:
        row, col = SELECTED_CELL
        rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, (80, 160, 255), rect, 3)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if BUTTON_SOLVE_RECT.collidepoint(event.pos):
                # Solving
                steps = sudoku_solver.solve(sudoku_solver.board)
                solving = True
            x,y = event.pos
            if x <= WIDTH and y <= HEIGHT_GRID:
                col = x // CELL_SIZE
                row = y // CELL_SIZE
                SELECTED_CELL = (row, col)
        if event.type == pygame.KEYDOWN and SELECTED_CELL and not solving:
            row, col = SELECTED_CELL
            if event.key in range(pygame.K_1, pygame.K_9 + 1):
                num = event.key - pygame.K_0
                # Abfrage ob Zahl korrekt (da "yield" in der Funktion, kein normaler Aufruf möglich)
                temp_board = [row[:] for row in sudoku_solver.board]
                for _ in sudoku_solver.solve(sudoku_solver.board):
                    pass
                if sudoku_solver.board[row][col] == num:
                    temp_board[row][col] = num
                sudoku_solver.board = temp_board
            if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                sudoku_solver.board[row][col] = 0
    if solving:
        try:
            row, col, num, action = next(steps)
            time.sleep(0.05)
            if action == "try":
                sudoku_solver.board[row][col] = num
                HIGHLIGHTED_CELLS.append((row, col))
            if action == "delete":
                sudoku_solver.board[row][col] = 0
                HIGHLIGHTED_CELLS.remove((row, col))
                pygame.draw.rect(screen, (200, 50, 50), pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        except StopIteration:
            solving = False
    screen.fill((255, 255, 255))
    highlight_cell()
    highlight_selceted_cell()
    draw_Screen()
    pygame.display.flip()
