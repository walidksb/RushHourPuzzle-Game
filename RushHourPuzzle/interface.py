
import pygame
import csv
from search import Search
from node import Node
from rushHourPuzzle import RushHourPuzzle

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH, WINDOW_HEIGHT = 700, 700
CELL_SIZE = 100
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Load board and vehicle information from 1.csv
board = []
vehicles = []

with open("1.csv", "r") as file:
    reader = csv.reader(file)
    rows = list(reader)
    size_x, size_y = map(int, rows[0])
    for row in rows[1:]:
        vehicles.append(row)

# Create a list of colors for each vehicle
vehicle_colors = [
    (255, 0, 0),  # Red
    (0, 255, 0),  # Green
    (0, 0, 255),  # Blue
    (255, 255, 0),  # Yellow
    (255, 0, 255),  # Magenta
    (0, 255, 255),  # Cyan
    (128, 128, 0),  # Olive
    (128, 0, 128),  # Purple
    (0, 128, 128),  # Teal
    (128, 128, 128),  # Gray
    (255, 128, 0),  # Orange
    (128, 0, 0),  # Maroon
    (0, 128, 0),  # Green
]

# Initialize Pygame window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Rush Hour Game")

button_width = 100
button_height = 40
button_x = (WINDOW_WIDTH - button_width) // 2
button_y = WINDOW_HEIGHT - 60  # Position it 60 pixels from the bottom

button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
button_text = pygame.font.SysFont("Arial", 20).render("Solve", True, BLACK)
text_rect = button_text.get_rect()
text_rect.center = button_rect.center


def draw_button():
    pygame.draw.rect(screen, (128, 182, 128), button_rect)
    screen.blit(button_text, (20, 20))


def draw_board():
    screen.fill(WHITE)
    for x in range(size_x):
        for y in range(size_y):
            rect = pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, WHITE, rect, 2)


def draw_vehicles():
    for i, vehicle in enumerate(vehicles):
        if len(vehicle) == 4:
            x, y, orientation, length = map(int, vehicle)
        elif len(vehicle) == 5:
            identifier, x, y, orientation, length = vehicle
            x, y, length = map(int, [x, y, length])

        color = vehicle_colors[i % len(vehicle_colors)]  # Cycle through colors
        if orientation == "H":
            pygame.draw.rect(
                screen,
                color,
                (x * CELL_SIZE, y * CELL_SIZE, length * CELL_SIZE, CELL_SIZE),
            )
        else:
            pygame.draw.rect(
                screen,
                color,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, length * CELL_SIZE),
            )


# Game loop
running = True
solution_path = []  # Initialize the solution path
current_game_state = None  # Initialize the current game state
game_solved = False  # Flag to check if the game is solved

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(event.pos):
            print("Solve button clicked")
            if not game_solved:
                # Initialize the game state
                current_game_state = Node(RushHourPuzzle("1.csv"), heuristic=2).state
                # Solve the game
                solution_path = Search.breadthFirst(current_game_state)
                draw_board()
                game_solved = True
            else:
                solution_path = solution_path[1:]
                print(solution_path[0].state.board)

    draw_board()
    draw_vehicles()
    draw_button()
    pygame.display.flip()

pygame.quit()