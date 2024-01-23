import pygame
import random
from queue import Queue
import sys

WIDTH, HEIGHT = 700, 800
BG_COLOUR = 250, 177, 237
ROWS, COLS = 10, 10
SIZE = WIDTH / ROWS
MINES = 5

pygame.init()
pygame.font.init()

NUMBER_FONT = pygame.font.SysFont('Times New Roman', 22)
LOSER_FONT = pygame.font.SysFont('Impact', 26)
WINNER_FONT = pygame.font.SysFont('Impact', 26)
TIMER_FONT = pygame.font.SysFont('Impact', 26)
FLAG_COUNTER_FONT = pygame.font.SysFont('Impact', 26)
NUMBER_COLOUS = {1: "BLUE", 2: "GREEN", 3: "ORANGE", 4: "PURPLE", 5: "RED", 6: "CYAN", 7: "BLACK", 8: "GRAY"}
RECTANGLE_COLOUR = 250, 177, 237
FLAG_RECTANGLE_COLOUR = "RED"
CLICKED_RECTANGLE_COLOUR = 150, 106, 142
BOMB_COLOUR = 110, 0, 0

class MinesweeperGame:
    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.field = None
        self.cover_field = None
        self.flags = None
        self.clicks = None
        self.lost = None
        self.win = None
        self.start_time = None
        self.total_non_mine_squares = None
        self.initialize_game()

    def initialize_game(self):
        self.field = MinesweeperField(self.rows, self.cols, self.mines)
        self.cover_field = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        self.flags = self.mines
        self.clicks = 0
        self.lost = False
        self.win = False
        self.start_time = 0
        self.total_non_mine_squares = self.rows * self.cols - self.mines

    def uncover_from_position(self, row, col):
        # queue created with start point that the palyer has clicked on (row, col)
        q = Queue()
        q.put((row, col))
        visited = set()

        while not q.empty():
            current = q.get()
            row, col = current
            value = self.field.get_cell_value(row, col)

            # if the cell is a flag just ignore the loop logic. 
            if self.cover_field[row][col] == -2:
                continue

            self.cover_field[row][col] = 1

            # the cell you just clicked is a 0 -- implements the get_neighbours BFS to expand to other connecting 0's
            if value == 0:
                neighbours = self.field.get_neighbours(row, col)
                for r, c in neighbours:
                    if (r, c) not in visited:
                        q.put((r, c))

            visited.add((row, col))

    # used to the loss message, and give the user the option to replay. 
    def loser(self, window):
        text_surface = pygame.font.SysFont('Impact', 26).render(
            "Skill Issue, You lost! Better luck next time... Click to reset.", 1, "black")
        text_rect = text_surface.get_rect(center=(WIDTH / 2, HEIGHT / 2))

        #draws to the screen and updates it. 
        pygame.draw.rect(window, "WHITE", (text_rect.x - 10, text_rect.y - 10, text_rect.width + 20, text_rect.height + 20))
        window.blit(text_surface, text_rect.topleft)
        pygame.display.update()
        pygame.time.delay(1000)

        # gives the user some time to decide. 
        end_time = pygame.time.get_ticks() + 2000

        # if the user clicks, resets the game state. 
        while pygame.time.get_ticks() < end_time:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    return True

        return False

    def winner(self, window):
        text_surface = pygame.font.SysFont('Impact', 26).render("Congratulations! You Win! Click to reset.", 1, "black")
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
                    return True

        return False

    # puts everything to the screen. 
    def draw(self, window, current_time):
        window.fill(BG_COLOUR)
        SIZE = WIDTH / self.rows
        
        for i in range(self.rows):
            for j in range(self.cols):
                x, y = SIZE * j, SIZE * i
                is_covered = self.cover_field[i][j] == 0 # empty
                is_flag = self.cover_field[i][j] == -2 # flag
                is_bomb = self.field.get_cell_value(i, j) == -1 # bomb, shock.

                pygame.draw.rect(window, BG_COLOUR, (x, y, SIZE, SIZE))

                if is_covered:
                    pygame.draw.rect(window, RECTANGLE_COLOUR, (x, y, SIZE, SIZE), 2)
                    pygame.draw.rect(window, "BLACK", (x, y, SIZE, SIZE), 2) # outline
                    continue

                if is_flag:
                    pygame.draw.rect(window, FLAG_RECTANGLE_COLOUR, (x, y, SIZE, SIZE))
                    pygame.draw.rect(window, "BLACK", (x, y, SIZE, SIZE), 2)
                    continue
                else:
                    pygame.draw.rect(window, CLICKED_RECTANGLE_COLOUR, (x, y, SIZE, SIZE))
                    pygame.draw.rect(window, "BLACK", (x, y, SIZE, SIZE), 2) 
                    if is_bomb:
                        pygame.draw.circle(window, BOMB_COLOUR, (int(x + SIZE / 2), int(y + SIZE / 2)), int(SIZE / 2 - 4))

                cell_value = self.field.get_cell_value(i, j)

                # handles the number of the colours. 
                if cell_value > 0:
                    text = NUMBER_FONT.render(str(cell_value), 1, NUMBER_COLOUS[cell_value])
                    window.blit(text, (x + (SIZE / 2 - text.get_width() / 2), y + (SIZE / 2 - text.get_height() / 2)))

        # drawing thee timer and flags to the screen. 
        time_text = TIMER_FONT.render(f"Time Elapsed: {round(current_time)}", 1, "BLACK")
        window.blit(time_text, (WIDTH / 2 - time_text.get_width() / 2, HEIGHT - time_text.get_height()))

        flag_count_text = FLAG_COUNTER_FONT.render(f"Flags: {self.flags}", 1, "BLACK")
        window.blit(flag_count_text, (10, HEIGHT - flag_count_text.get_height() - 10))

        pygame.display.update()

    
    def get_grid_position(self, mouse_position):
        mouse_x, mouse_y = mouse_position
        row = int(mouse_y // (WIDTH / self.rows))
        col = int(mouse_x // (WIDTH / self.rows))
        return row, col

    def main(self, window):
        run = True

        while run:
            # initialize the timer. 
            if self.start_time == 0:
                self.start_time = pygame.time.get_ticks() / 1000
            current_time = pygame.time.get_ticks() / 1000 - self.start_time
            
            #handles "x'ing" out the game 
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    break

                # handles the clicking events. 
                if event.type == pygame.MOUSEBUTTONDOWN:
                    row, col = self.get_grid_position(pygame.mouse.get_pos())
                    if row >= self.rows or col >= self.cols:
                        continue

                    mouse_pressed = pygame.mouse.get_pressed()

                    # left click logic. 
                    if mouse_pressed[0]:
                        self.cover_field[row][col] = 1

                        if self.field.get_cell_value(row, col) == -1:
                            self.lost = True

                        if self.clicks == 0 or self.field.get_cell_value(row, col) == 0:
                            self.uncover_from_position(row, col)
                            self.clicks += 1

                        uncovered_squares = sum(row.count(1) for row in self.cover_field)
                        if uncovered_squares == self.total_non_mine_squares:
                            self.win = True

                    # right click logic.
                    elif mouse_pressed[2]:

                        if self.cover_field[row][col] == 0 and self.flags > 0:
                            self.cover_field[row][col] = -2
                            self.flags -= 1
                        elif self.cover_field[row][col] == -2:
                            self.cover_field[row][col] = 0
                            self.flags += 1

            # handles clicking a mine.
            if self.lost:
                self.start_time = 0
                self.draw(window, current_time)
                self.lost = self.loser(window)

                if self.lost:
                    self.initialize_game()

            # winning the game 
            if self.win:
                self.start_time = 0
                self.draw(window, current_time)
                self.win = self.winner(window)

                if self.win:
                    self.initialize_game()

            self.draw(window, current_time)

        pygame.quit()


class MinesweeperField:

    def __init__(self, rows, cols, mines):
        self.rows = rows
        self.cols = cols
        self.mines = mines
        self.field = self.create_minefield()

    def create_minefield(self):
        field = [[0 for _ in range(self.cols)] for _ in range(self.rows)]
        mine_positions = set()

        while len(mine_positions) < self.mines:
            row = random.randrange(0, self.rows)
            col = random.randrange(0, self.cols)
            pos = row, col

            if pos not in mine_positions:
                mine_positions.add(pos)
                field[row][col] = -1

        for mine in mine_positions:
            r, c = mine
            neighbours = self.get_neighbours(r, c)
            for nr, nc in neighbours:
                if field[nr][nc] != -1:
                    field[nr][nc] += 1

        return field

    def get_neighbours(self, row, col):
        neighbours = []

        if row > 0:
            neighbours.append((row - 1, col))
        if row < self.rows - 1:
            neighbours.append((row + 1, col))
        if col > 0:
            neighbours.append((row, col - 1))
        if col < self.cols - 1:
            neighbours.append((row, col + 1))

        if row > 0 and col > 0:
            neighbours.append((row - 1, col - 1))
        if row < self.rows - 1 and col < self.cols - 1:
            neighbours.append((row + 1, col + 1))
        if row < self.rows - 1 and col > 0:
            neighbours.append((row + 1, col - 1))
        if row > 0 and col < self.cols - 1:
            neighbours.append((row - 1, col + 1))

        return neighbours

    def get_cell_value(self, row, col):
        return self.field[row][col]


def main():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")

    minesweeper_game = MinesweeperGame(ROWS, COLS, MINES)
    minesweeper_game.main(window)

if __name__ == "__main__":
    main()