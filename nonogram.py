import pygame as pg
import sys
import random

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
CELL_SIZE = 25
BACKGROUND_COLOR = (211, 211, 211)
LINE_COLOUR = (0, 0, 0)
FILLED_COLOUR = (0, 0, 0)
EMPTY_COLOUR = (255, 255, 255)
TEXT_COLOUR = (0, 0, 0)

def gameSettings():
    screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pg.display.set_caption("Nonogram")
    return screen

def drawGrid(screen, grid, row_hints, col_hints):
    grid_width = len(grid[0]) * CELL_SIZE
    grid_height = len(grid) * CELL_SIZE
    offset_x = (SCREEN_WIDTH - grid_width) // 2
    offset_y = (SCREEN_HEIGHT - grid_height) // 2

    font = pg.font.SysFont(None, 24)

    # Draw row hints
    for i, hint in enumerate(row_hints):
        hint_text = ' '.join(map(str, hint))
        text_surface = font.render(hint_text, True, TEXT_COLOUR)
        screen.blit(text_surface, (offset_x - 50, offset_y + i * CELL_SIZE + CELL_SIZE // 4))

    # Draw column hints vertically
    for j, hint in enumerate(col_hints):
        for k, num in enumerate(hint):
            hint_text = str(num)
            text_surface = font.render(hint_text, True, TEXT_COLOUR)
            screen.blit(text_surface, (offset_x + j * CELL_SIZE + CELL_SIZE // 4, offset_y - 30 - (len(hint) - k) * 20))

    # Draw the grid
    for row in range(len(grid)):
        for col in range(len(grid[row])):
            rect = pg.Rect(offset_x + col * CELL_SIZE, offset_y + row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == 1:
                pg.draw.rect(screen, FILLED_COLOUR, rect)
            else:
                pg.draw.rect(screen, EMPTY_COLOUR, rect)
            pg.draw.rect(screen, LINE_COLOUR, rect, 1)
    pg.display.flip()

def getCellIndex(mouse_pos, grid):
    grid_width = len(grid[0]) * CELL_SIZE
    grid_height = len(grid) * CELL_SIZE
    offset_x = (SCREEN_WIDTH - grid_width) // 2
    offset_y = (SCREEN_HEIGHT - grid_height) // 2

    x, y = mouse_pos
    col = (x - offset_x) // CELL_SIZE
    row = (y - offset_y) // CELL_SIZE

    if 0 <= col < len(grid[0]) and 0 <= row < len(grid):
        return row, col
    return None

def createSolvableGrid(rows, cols):
    grid = [[0 for _ in range(cols)] for _ in range(rows)]
    for _ in range(random.randint(rows, rows * cols // 2)):
        r = random.randint(0, rows - 1)
        c = random.randint(0, cols - 1)
        grid[r][c] = 1
    return grid

def createEmptyGrid(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

def calculateHints(grid):
    row_hints = []
    col_hints = [[] for _ in range(len(grid[0]))]

    for row in grid:
        hint = []
        count = 0
        for cell in row:
            if cell == 1:
                count += 1
            elif count > 0:
                hint.append(count)
                count = 0
        if count > 0:
            hint.append(count)
        row_hints.append(hint or [0])

    for col in range(len(grid[0])):
        hint = []
        count = 0
        for row in range(len(grid)):
            if grid[row][col] == 1:
                count += 1
            elif count > 0:
                hint.append(count)
                count = 0
        if count > 0:
            hint.append(count)
        col_hints[col] = hint or [0]

    return row_hints, col_hints

def main():
    pg.init()
    screen = gameSettings()

    rows, cols = 5, 5  # Example grid size
    solution_grid = createSolvableGrid(rows, cols)
    user_grid = createEmptyGrid(rows, cols)
    row_hints, col_hints = calculateHints(solution_grid)

    solved = False

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit()
            elif event.type == pg.MOUSEBUTTONDOWN and not solved:
                cell_index = getCellIndex(pg.mouse.get_pos(), user_grid)
                if cell_index:
                    r, c = cell_index
                    user_grid[r][c] = 1 if user_grid[r][c] == 0 else 0
                    solved = user_grid == solution_grid

        screen.fill(BACKGROUND_COLOR)
        drawGrid(screen, user_grid, row_hints, col_hints)

        if solved:
            font = pg.font.Font(None, 74)
            text_surface = font.render("Solved!", True, (0, 255, 0))
            screen.blit(text_surface, (SCREEN_WIDTH // 2 - text_surface.get_width() // 2, SCREEN_HEIGHT // 2 - text_surface.get_height() // 2))
            pg.display.flip()

if __name__ == "__main__":
    main()