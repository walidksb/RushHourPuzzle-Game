import pygame
from rushHourPuzzle import RushHourPuzzle
from node import Node
import time
from queue import Queue, PriorityQueue

# THIS IS THE LAST DANCEEEEEEEEEEEEEEEEEEEEEEEEEE WWEEEEEEEEEEEEEgit 

#path 
puzzle_path = "1.csv"
puzzle = RushHourPuzzle(puzzle_path)
for row in puzzle.board:
    print(" ".join(row))

#game initiation 
pygame.init()
screen = pygame.display.set_mode((700,700))
pygame.display.set_caption("RUSH HOUR PUZZLE")
clock = pygame.time.Clock()

titleFont = pygame.font.SysFont("Core sans c",45)


#constants
gridSize = 100
gridRows, gridCols = 6, 6
carWidth, carHeight = gridSize, gridSize // 2
#colors
vehicle_colors = {
    'X': (0, 0, 0),   # Red for 'X' vehicle
    'A': (255,0,255),  
    'B': (255,55,55),   
    'C': (255,77,33),
    'D': (255,255,120),
    'E': (255,120,255),
    'F': (255,255,0),
    'G': (255,0,255),
    'H': (255,88,88),
    'I': (0,120,120),
    'J': (88,255,0),
    'K': (25,38,255),
    'L': (255,255,0),
    'M': (255,0,255),
    'N': (255,55,55),
    'O': (255,77,33),
    'P': (255,255,120),
    'Q': (255,120,255),
    'R': (255,255,0),
    'S': (255,0,255)
}

def draw(puzzle1):
    screen.fill("white")
    for row in range(gridRows):
        for col in range(gridCols):
            pygame.draw.rect(screen, (255, 255, 255), (col * gridSize, row * gridSize, gridSize, gridSize), 1)
        for vehicle in puzzle1.vehicles:
            x_position = vehicle['x']
            y_position = vehicle['y']
            width, height = (gridSize*vehicle["length"], gridSize) if vehicle["orientation"] == "H" else (gridSize, gridSize * vehicle["length"])
            color = vehicle_colors.get(vehicle["id"], (255,255,255))  
            if width > height:
                pygame.draw.rect(screen, color, (x_position * gridSize, y_position * gridSize, width, height))
            else:
                pygame.draw.rect(screen, color, (x_position * gridSize, y_position * gridSize, gridSize, height))

#texte 
def draw_text(text, font, text_col, x, y):
    image = font.render(text,True, text_col)
    screen.blit(image , (x,y))


solved = False
""" Uninformed/Blind Search """
@staticmethod
def breadthFirst(initial_state):
    
    initial_node = Node(initial_state)   
    # Check if the start element is the goal
    if initial_node.state.isGoal():
        return initial_node, 0

    # Create the OPEN FIFO queue and the CLOSED list
    open = Queue() # A FIFO queue
    open.put(initial_node)
    closed = list()
    
    step = 0
    while True:
        global solved
        time.sleep(0.03)
        print (f'*** Step {step} ***')
        # Check if the OPEN queue is empty => goal not found 
        if open.empty():
            return None, step            
        # Get the first element of the OPEN queue
        current = open.get()  
        draw(current.state)
  
      
        # Put the current node in the CLOSED list
        closed.append(current)
        step +=1 
        # Generate the successors of the current node
        for (action, successor) in current.state.successorFunction():                
            child = Node(successor, current, action)
            # Check if the child is not in the OPEN queue and the CLOSED list
            if (child.state.board not in [node.state.board for node in closed] and 
                child.state.board not in [node.state.board for node in list(open.queue)]):
                # Check if the child is the goal
                if child.state.isGoal():
                    solved = True
                    print ("Goal reached")
                    draw(child.state)
                    draw_text("Steps : "+ str(step) ,titleFont,(255,255,255) , 60 , 50)
                    return child, step 
                # Put the child in the OPEN queue 
                open.put(child)
        # Update the main screen with the grid surface
        screen.blit(screen, (0, 0))

        pygame.display.update() 

@staticmethod
def A_Star(initial_state, h):
    global solved
    open = PriorityQueue() 
    closed = list()
    initial_node = Node(initial_state)   
    initial_node.setF(h)

    if initial_node.state.isGoal():
        return initial_node, 0
    
    open.put(initial_node)
    step = 0
    while (True):
        time.sleep(0.03)
        print (f'*** Step {step} ***')
        current = open.get()

        if current.state.isGoal():
            solved = True
            print ("Goal reached")
            for node in list(current.getPath()):
                draw(node)
                time.sleep(0.5)
                pygame.display.update()
            return current, step
        
        closed.append(current)
        step+=1

        for(action, successor) in current.state.successorFunction():
            child = Node(successor, current, action)
            child.setF(h)

            if((child.state.board not in [node.state.board for node in closed]) and 
                (child.state.board not in [node.state.board for node in list(open.queue)])):
                open.put(child)
            else: 
                if (child.state.board in [node.state.board for node in list(open.queue)]) and child.f >= current.f:
                    child = current
                else:
                    if (child.state.board in [node.state.board for node in closed]) and child.f < current.f:
                        if child in closed:
                            closed.remove(child)
                            open.put(child)
                # Update the main screen with the grid surface
        screen.blit(screen, (0, 0))

        pygame.display.update()    

#Main game loop 
running = True
isStarting = False
solved = False

# def generateBoard(board):
#     matrix = board
#     # we use the sizes to draw as well as to do our "steps" in the loops. 
#     grid_node_width = 103 
#     grid_node_height = 103
    # for node in goal_node.getNodeSolution():
    #             generateBoard(node.state.board)
while running:
    #clear the screen
    if not solved : screen.fill("purple")
    if not isStarting: 
        if not solved:
             goal_node,step = A_Star(puzzle,3)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.flip()
    clock.tick(60)

pygame.quit()