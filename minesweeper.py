from queue import Queue
import pygame
import random
pygame.init()


# Constants
WIDTH, HEIGHT = 700, 800
BG_COLOUR = 250, 177, 237
ROWS, COLS = 10, 10
SIZE = WIDTH / ROWS
MINES = 15
NUMBER_FONT = pygame.font.SysFont('Times New Roman', 22)
NUMBER_COLOUS = {1: "BLUE", 2: "GREEN", 3: "ORANGE", 4: "PURPLE", 5: "RED", 6: "CYAN", 7: "BLACK", 8: "GRAY"}
RECTANGLE_COLOUR = "WHITE"
FLAG_RECTANGLE_COLOUR = "RED"
CLICKED_RECTANGLE_COLOUR = 150,106,142
BOMB_COLOUR = 110, 0, 0


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
            is_flag = cover_field[i][j] == -2
            is_bomb = value == -1

            
            if is_covered:
                pygame.draw.rect(window, RECTANGLE_COLOUR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "BLACK", (x, y, SIZE, SIZE), 2)
                continue

            if is_flag:
                pygame.draw.rect(window, FLAG_RECTANGLE_COLOUR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "BLACK", (x, y, SIZE, SIZE), 2)
                continue
            
            else:
                pygame.draw.rect(window, CLICKED_RECTANGLE_COLOUR, (x, y, SIZE, SIZE))
                pygame.draw.rect(window, "BLACK", (x, y, SIZE, SIZE), 2)
                if is_bomb:
                    pygame.draw.circle(window, BOMB_COLOUR, (x + SIZE / 2,y + SIZE /2), SIZE/2 - 4)

            if value > 0: # value has to be greater than 0 since -1 is a bomb and -2 is a flag, 0 we want blank.
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
    mine_positions = set()

    while len(mine_positions) < mines:
        row = random.randrange(0, rows)
        col = random.randrange(0, cols)
        pos = row, col

        if pos not in mine_positions:
            mine_positions.add(pos)
            field[row][col] = -1

    for mine in mine_positions:
        r, c = mine
        neighbours = get_neighbour(r, c, rows, cols)
        for nr, nc in neighbours:
            if field[nr][nc] != -1:  # Only update counts for non-mine cells
                field[nr][nc] += 1 #new row, new col

    return field
def uncover_from_position(row, col, cover_field, field):
    q = Queue()
    q.put((row, col))
    visited = set()

    while not q.empty():
        current = q.get()

        row, col = current
        value = field[row][col]

        # Check if the cell is flagged, and skip uncovering if it is
        if cover_field[row][col] == -2:
            continue

        # Uncover the cell
        cover_field[row][col] = 1

        # If it's an empty cell, uncover connected empty cells
        # Queue processes all neighbouring cells of the same value - so opens up all connecting empty cells.
        if value == 0:
            neighbours = get_neighbour(row, col, ROWS, COLS)
            for r, c in neighbours:
                if (r, c) not in visited:
                    q.put((r, c))

        visited.add((row, col))

    


def main(window):
    run = True
    field = create_minefield(ROWS, COLS, MINES)
    cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    flags = MINES
    clicks = 0

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pressed())
                row, col = get_grid_position(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue

                mouse_pressed = (pygame.mouse.get_pressed())
                
                if mouse_pressed[0]: # left click
                    cover_field[row][col] = 1
                    if clicks == 0 or field[row][col] == 0:
                        uncover_from_position(row, col, cover_field, field)

                elif mouse_pressed[2]: #right click
                    if cover_field[row][col] != -2:
                        cover_field[row][col] = -2
                        flags -= 1

                elif mouse_pressed[1]:  # middle click has no function so this just handles that
                    pass
                
                else:
                    flags += 1
                    cover_field[row][col] = -2

        draw(window, field, cover_field)
    pygame.quit()

if __name__ == "__main__":
    main(window)