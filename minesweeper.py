import pygame

# Constants
WIDTH, HEIGHT = 700, 800
BG_COLOUR = 250, 177, 237
ROWS, COLS = 30, 30


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

def draw(window):
    window.fill(BG_COLOUR)
    pygame.display.update()

def create_grid(rows, cols):
    pass

def main(window):
    run = True

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
        draw(window)
    pygame.quit()

if __name__ == "__main__":
    main(window)