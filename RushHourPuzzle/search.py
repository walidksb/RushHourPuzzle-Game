from node import Node
from queue import Queue,PriorityQueue
from collections import deque
from rushHourPuzzle import RushHourPuzzle

class Search:

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
            print (f'*** Step {step} ***')
            # Check if the OPEN queue is empty => goal not found 
            if open.empty():
                return None, step            
            # Get the first element of the OPEN queue
            current = open.get()            
            # Put the current node in the CLOSED list
            closed.append(current)
            step +=1 
            # Generate the successors of the current node
            for (action, successor) in current.state.successorFunction():                
                child = Node(successor, current, action)
                # Check if the child is not in the OPEN queue and the CLOSED list
                if (child.state.board not in [node.state.board for node in closed] and \
                    child.state.board not in [node.state.board for node in list(open.queue)]):
                    # Check if the child is the goal
                    if child.state.isGoal():
                        print ("Goal reached")
                        return child, step 
                    # Put the child in the OPEN queue 
                    open.put(child)     
            
#---------------------------------------------------------------------------            
    # def sortopen(open):
    #     open = sorted(open, key=lambda x: x.f)
    #     return open

    #a function that takes the lowest heuristic value and puts it in the front of the queue
    # def sortopen(open):
    #     lowest_node = None
    #     lowest_heuristic = float('inf')
        
    #     # Find the node with the lowest heuristic value
    #     for node in open:
    #         if node.f < lowest_heuristic:
    #             lowest_node = node
    #             lowest_heuristic = node.f
        
    #     # Remove the lowest node from the queue
    #     open.remove(lowest_node)
        
    #     # Add the lowest node to the front of the queue
    #     open.appendleft(lowest_node)

    @staticmethod
    def Astar(initial_state, h):
        # Create the OPEN priority queue and the CLOSED list
        open = PriorityQueue()
        closed= list()
        initial_node = Node(initial_state)
        initial_node.setF(h)
        
         
        if initial_node.state.isGoal():
            return initial_node, 0
        
        open.put((initial_node.f,initial_node))
        step = 0
        heur=[]
        while True:
            # Check if the OPEN queue is empty => goal not found 
            if open.empty():
                return None, step

            print (f'*Step {step} *')

            # Get the first element of the OPEN queue
            _, current = open.get()
            
            # Check if the current node is the goal
            if current.state.isGoal():
                print ("Goal reached")
                return current, step,heur
            # Put the current node in the CLOSED list
            closed.append(current)
        
            heur.append(current.f)
                         
            step +=1
            # Generate the successors of the current node
            for (action, successor) in current.state.successorFunction():                
                child = Node(successor, current, action)
                child.setF(h)
                child_board = child.state.board
                
                if child.state.isGoal():
                    print("Goal reached")
                    return child, step,heur
                                
                if (child_board not in [node.state.board for node in closed]) and (child_board not in [node[1].state.board for node in list(open.queue)]):
                    open.put((child.f, child))
                else:
                    if child_board in [node[1].state.board for node in list(open.queue)]:
                        index = [node[1].state.board for node in list(open.queue)].index(child_board)
                        if child.f < open.queue[index][0]:
                            open.queue.pop(index)  # Remove the node from the queue
                            open.put((child.f, child))  # Put the updated node into the queue
                    else:
                        if child_board in [node.state.board for node in closed]:
                            index = [node.state.board for node in closed].index(child_board)
                            if child.f < closed[index].f:
                                closed.pop(index)  # Remove the node from the CLOSED list
                                open.put((child.f, child))  # Put the updated node into the OPEN queue
        return None            
                        
              
       
def main():
    initial_state = RushHourPuzzle('1.csv')
    RushHourPuzzle.printRushHourBoard(initial_state.board)   
    goal_node, step, heuristics = Search.Astar(initial_state,3)
    print(f"Path cost: {heuristics[-1]}")
    print(f"Number of steps: {step}")
    print("Moves: {}".format(" ".join(map(str, goal_node.getSolution()))))

if __name__ == "__main__":
    main()
