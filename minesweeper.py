from queue import Queue
import pygame
import random
pygame.init()


# Constants
WIDTH, HEIGHT = 700, 800
BG_COLOUR = 250, 177, 237
ROWS, COLS = 8, 8
SIZE = WIDTH / ROWS
MINES = 10
NUMBER_FONT = pygame.font.SysFont('Times New Roman', 22)
NUMBER_COLOUS = {1: "BLUE", 2: "GREEN", 3: "ORANGE", 4: "PURPLE", 5: "RED", 6: "CYAN", 7: "BLACK", 8: "GRAY"}
RECTANGLE_COLOUR = "WHITE"


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

def draw(window, field, cover_field):
    window.fill(BG_COLOUR)
    
    SIZE = WIDTH / ROWS ## drawing the SIZE of the square
    for i, row in enumerate(field):
        y = SIZE * i
        for j, value in enumerate(row):
            x = SIZE * j

            is_covered = cover_field[i][j] == 0
            if is_covered:
                pygame.draw.rect(window, RECTANGLE_COLOUR, (x, y, SIZE, SIZE), 2)
                pygame.draw.rect(window, "BLACK", (x, y, SIZE, SIZE), 2)
                continue
            else:
                pygame.draw.rect(window, RECTANGLE_COLOUR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "BLACK", (x, y, SIZE, SIZE), 2)

            if value > 0: # value has to be greater than 0 since -1 is a bomb and 0 we want blank.
                text = NUMBER_FONT.render(str(value), 1, NUMBER_COLOUS[value])
                window.blit(text, (x + (SIZE/2 - text.get_width()/2), y + (SIZE/2 - text.get_height()/2)))


    pygame.display.update()

def get_grid_position(mouse_position):
    mouse_x, mouse_y = mouse_position
    row = int(mouse_y // SIZE)
    col = int(mouse_x / SIZE)

    return row,  col
    
def get_neighbour(row, col, rows, cols):
    neighbours = []

    if row > 0: # UP
        neighbours.append((row -1, col))
    if row < rows -1: # DOWN
        neighbours.append((row+1, col))
    if col > 0: # LEFT 
        neighbours.append((row, col -1))
    if col < cols -1: # RIGHT
        neighbours.append((row, col +1))

    ## Diagonals
    if row > 0 and col > 0:
        neighbours.append((row -1, col -1))
    if row < rows - 1 and col < cols -1:
        neighbours.append((row +1, col +1))
    if row < rows -1 and col > 0:
        neighbours.append((row +1, col -1))
    if row > 0 and col < cols -1:
        neighbours.append((row -1, col +1)) 
    
    return neighbours

def create_minefield(rows, cols, mines):
    field = [[0 for _ in range(cols)] for _ in range(rows)]
    mine_position = set()

    while len(mine_position) < mines:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col

        if pos in mine_position:
            continue
        
        mine_position.add(pos)
        field[row][col] = -1

    for mine in mine_position:
        neighbours = get_neighbour(*mine, rows, cols)
        for r, c in neighbours: #r, c: row, column
            field[r][c] += 1

    return field

def uncover_from_position(row, col, cover_field, field):
    q = Queue()
    q.put((row, col))
    visited = set()

    while not q.empty():
        current = q.get()

        neighbours = get_neighbour(*current, ROWS, COLS)
        for row, col in neighbours:
            if (row, col) in visited:
                continue

            value = field[row][col]
            cover_field[row][col] = 1
            if value == 0: # empty
                q.put((row, col))

            visited.add((row, col))

    


def main(window):
    run = True
    field = create_minefield(ROWS, COLS, MINES)
    cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_grid_position(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue
                cover_field[row][col] = 1
                uncover_from_position(row, col, cover_field, field)

        draw(window, field, cover_field)
    pygame.quit()

if __name__ == "__main__":
    main(window)