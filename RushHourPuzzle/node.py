from copy import deepcopy

class Node:

    def __init__(self, rushHourPuzzle, parent=None, action="", c=1, heuristic=1):
        self.state = rushHourPuzzle
        self.parent = parent
        self.action = action
        self.g = 0 if not self.parent else self.parent.g + c
        self.setF(heuristic)   

    def __lt__(self, other):
        return self.f < other.f

    # Choose one of the available heuristics
    def setF(self, heuristic):
        heuristics = {1: self.heuristic1(),
                    2: self.heuristic2(),
                    3: self.heuristic3()}
        self.f = self.g + heuristics[heuristic]        

    """ First heuristic: Distance from target vehicle to the exit """
    def heuristic1(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                return self.state.board_width-2-vehicle["x"]
    
    """ Second heuristic: number of vehicles that block the way to the exit """
    def heuristic2(self):
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                unique_vehicles = set(self.state.board[vehicle["y"]][vehicle["x"]:])
                if ' ' in unique_vehicles:
                    return self.heuristic1()+len(unique_vehicles)-2
                return self.heuristic1()+len(unique_vehicles)-1
    

    # def heuristic3(self):
    #     h1 = self.heuristic1()
    #     h2 = self.heuristic2()
    #     # # Sum both heuristics
    #     return h1 +  h2
    def blocking_vehicles(self):
        unique_vehicles = set()
        for vehicle in self.state.vehicles:
            if vehicle["id"] == 'X':
                unique_vehicles = set(self.state.board[vehicle["y"]][vehicle["x"]:])
        return unique_vehicles

    # def heuristic3(self):
    #     blocking_vehicles_from_up = 0
    #     blocking_vehicles_from_down = 0
    #     unique_vehicles = self.blocking_vehicles()
        
    #     for vehicle_id in unique_vehicles:
    #         if vehicle_id != ' ' and vehicle_id != 'X':
    #             for vehicle in self.state.vehicles:
    #                 if vehicle["id"] == vehicle_id:
    #                     v1, v, h1, h = False, False, False, False
    #                     y =vehicle["y"] + int(vehicle["length"])
    #                     id2 =self.state.board[y][vehicle["x"]]
    #                     for vehicle in self.state.vehicles:
    #                         if vehicle["id"] == id2:
    #                             if vehicle["orientation"] == 'V':
    #                                 v = True
    #                             if vehicle["orientation"] == 'H':
    #                                 h = True
    #                     if self.state.board[y][vehicle["x"]] != ' ' and v == True:
    #                         blocking_vehicles_from_down += 1
    #                     if self.state.board[y][vehicle["x"]] != ' ' and h == True:
    #                         blocking_vehicles_from_down += 1
    #                     y1 = vehicle["y"] - 1
    #                     id1 = self.state.board[y1][vehicle["x"]]
    #                     for vehicle in self.state.vehicles:
    #                         if vehicle["id"] == id1:
    #                             if vehicle["orientation"] == 'V':
    #                                 v1 = True
    #                             if vehicle["orientation"] == 'H':
    #                                 h1 = True
    #                     if self.state.board[y1][vehicle["x"]] != ' ' and v1 == True:
    #                         blocking_vehicles_from_up += 1
    #                     if self.state.board[y1][vehicle["x"]] != ' ' and h1 == True:
    #                         blocking_vehicles_from_up += 1
    #     up_down = blocking_vehicles_from_up + blocking_vehicles_from_down                    
    #     return self.heuristic2() + up_down
    
    def heuristic3(self):
        blocking_vehicles_from_up = 0
        blocking_vehicles_from_down = 0
        unique_vehicles = self.blocking_vehicles()
        
        for vehicle_id in unique_vehicles:
            if vehicle_id != ' ' and vehicle_id != 'X':
                for vehicle in self.state.vehicles:
                    if vehicle["id"] == vehicle_id:
                        y =vehicle["y"] + int(vehicle["length"])
                        if self.state.board[y][vehicle["x"]] != ' ':
                            blocking_vehicles_from_down += 1
                        y1 = vehicle["y"] - 1
                        if self.state.board[y1][vehicle["x"]] != ' ':
                            blocking_vehicles_from_up += 1
        up_down = blocking_vehicles_from_up + blocking_vehicles_from_down                    
        return self.heuristic2() + up_down
    
    def getPath(self):
        states = []
        node = self
        while node != None:
            states.append(node.state)
            node = node.parent
        return states[::-1]
    
    def getSolution(self):
        actions = []
        node = self
        while node != None:
            actions.append(node.action)
            node = node.parent
        return actions[::-1]
       



