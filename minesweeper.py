from queue import Queue
import sys
import time
import pygame
import random
pygame.init()


# Constants
WIDTH, HEIGHT = 700, 800
BG_COLOUR = 250, 177, 237
ROWS, COLS = 10, 10
SIZE = WIDTH / ROWS
MINES = 1
NUMBER_FONT = pygame.font.SysFont('Times New Roman', 22)
LOSER_FONT = pygame.font.SysFont('Impact', 26)
WINNER_FONT = pygame.font.SysFont('Impact', 26)
TIMER_FONT = pygame.font.SysFont('Impact', 26)
FLAG_COUNTER_FONT = pygame.font.SysFont('Impact', 26)
NUMBER_COLOUS = {1: "BLUE", 2: "GREEN", 3: "ORANGE", 4: "PURPLE", 5: "RED", 6: "CYAN", 7: "BLACK", 8: "GRAY"}
RECTANGLE_COLOUR = "WHITE"
FLAG_RECTANGLE_COLOUR = "RED"
CLICKED_RECTANGLE_COLOUR = 150,106,142
BOMB_COLOUR = 110, 0, 0


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")


#Handles drawing information to the screen.
def draw(window, field, cover_field, current_time, flags):
    window.fill(BG_COLOUR)  # Fill the entire window with the background color

    SIZE = WIDTH / ROWS  # Drawing the SIZE of the square
    for i, row in enumerate(field):
        y = SIZE * i
        for j, value in enumerate(row):
            x = SIZE * j

            is_covered = cover_field[i][j] == 0
            is_flag = cover_field[i][j] == -2
            is_bomb = value == -1

            # Draw the background rectangle
            pygame.draw.rect(window, BG_COLOUR, (x, y, SIZE, SIZE))

            if is_covered:
                pygame.draw.rect(window, RECTANGLE_COLOUR, (x, y, SIZE, SIZE), 2)
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
                    pygame.draw.circle(window, BOMB_COLOUR, (int(x + SIZE / 2), int(y + SIZE / 2)), int(SIZE/2 - 4))

            if value > 0:
                text = NUMBER_FONT.render(str(value), 1, NUMBER_COLOUS[value])
                window.blit(text, (x + (SIZE/2 - text.get_width()/2), y + (SIZE/2 - text.get_height()/2)))

    # Draw the time text after the grid is drawn
    time_text = TIMER_FONT.render(f"Time Elapsed: {round(current_time)}", 1, "BLACK")
    window.blit(time_text, (WIDTH / 2 - time_text.get_width() / 2, HEIGHT - time_text.get_height()))

    flag_count_text = FLAG_COUNTER_FONT.render(f"Flags: {flags}", 1, "BLACK")
    window.blit(flag_count_text, (10, HEIGHT - flag_count_text.get_height() - 10))

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

        # uncover the cell
        cover_field[row][col] = 1

        # If it's an empty cell, uncover connected empty cells
        # Queue processes all neighbouring cells of the same value - so opens up all connecting empty cells.
        if value == 0:
            neighbours = get_neighbour(row, col, ROWS, COLS)
            for r, c in neighbours:
                if (r, c) not in visited:
                    q.put((r, c))

        visited.add((row, col))

def loser(window, text):
    text_surface = LOSER_FONT.render(text, 1, "black")
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    pygame.draw.rect(window, "WHITE", (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    window.blit(text_surface, text_rect.topleft)
    pygame.display.update()
    pygame.time.delay(1000)  # Initial delay to display the losing message for a moment
    
    # Continue checking for events during the delay
    end_time = pygame.time.get_ticks() + 2000  # Set a total time limit for checking events (e.g., 2 seconds)
    
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit the game if the window is closed during the delay -> ignores the delay, pygame doesn't.

            elif event.type == pygame.MOUSEBUTTONDOWN:
                return True  # Player wants to play again
    
    return False  # Player doesn't want to play again

def winner(window, text):
    text_surface = WINNER_FONT.render(text, 1, "black")
    text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

    pygame.draw.rect(window, "WHITE", (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
    window.blit(text_surface, text_rect.topleft)
    pygame.display.update()
    pygame.time.delay(1000)  
    
    
    end_time = pygame.time.get_ticks() + 2000  
    
    while pygame.time.get_ticks() < end_time:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return True  # Player wants to play again  
    
    return False  
    


def main(window):
    run = True
    field = create_minefield(ROWS, COLS, MINES)
    cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
    flags = MINES
    clicks = 0
    lost = False
    win = False
    start_time = 0

    total_non_mine_squares = ROWS * COLS - MINES

    while run:
        
        if start_time == 0:  # Only set start_time on the first iteration
            start_time = pygame.time.get_ticks() / 1000  # Convert to seconds
        current_time = pygame.time.get_ticks() / 1000 - start_time  # Calculate elapsed time in seconds

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pressed())
                row, col = get_grid_position(pygame.mouse.get_pos())
                if row >= ROWS or col >= COLS:
                    continue

                mouse_pressed = pygame.mouse.get_pressed()
                
                if mouse_pressed[0]:  # left click
                    cover_field[row][col] = 1
                    
                    if field[row][col] == -1:  # bomb
                        lost = True

                    if clicks == 0 or field[row][col] == 0:
                        uncover_from_position(row, col, cover_field, field)
                        clicks += 1

                    uncovered_squares = sum(row.count(1) for row in cover_field)
                    if uncovered_squares == total_non_mine_squares:
                        win = True

                    elif mouse_pressed[2]:  # right click / place flag
                        if cover_field[row][col] != -2 and flags < MINES:
                            cover_field[row][col] = -2
                            flags += 1
                            
                elif mouse_pressed[1]:  # middle click has no function so this just handles that
                    pass
                
                else:
                    if cover_field[row][col] == -2:  # Check if the cell is already flagged
                        flags += 1  # If it's already flagged, increment the flags (remove the flag)
                    elif flags > 0 and cover_field[row][col] == 0:  # Check if there are remaining flags to place and the cell is not already flagged
                        cover_field[row][col] = -2
                        flags -= 1

        if lost:
            start_time = 0
            draw(window, field, cover_field, current_time, flags)
            lost = loser(window, """Skill Issue, You lost! Better luck next time... Click to reset.""")  # Update the 'lost' variable

            # Reset the game state if the player wants to play again
            if lost:
                field = create_minefield(ROWS, COLS, MINES)
                cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                flags = MINES
                clicks = 0

        if win:
            draw(window, field, cover_field, current_time, flags)
            win = winner(window, "Congratulations! You Win! Click to reset.")  # Update the 'win' variable

            # Reset the game state if the player wants to play again
            if win:
                field = create_minefield(ROWS, COLS, MINES)
                cover_field = [[0 for _ in range(COLS)] for _ in range(ROWS)]
                flags = MINES
                clicks = 0

        draw(window, field, cover_field, current_time, flags)

    pygame.quit()

if __name__ == "__main__":
    main(window)