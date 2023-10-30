
        blocking_vehicles_from_up = 0
        blocking_vehicles_from_down = 0
        unique_vehicles = self.blocking_vehicles()
        
        for vehicle_id in unique_vehicles:
            if vehicle_id != ' ' and vehicle_id != 'X':
                for vehicle in self.state.vehicles:
                    if vehicle["id"] == vehicle_id:
                        v1, v, h1, h = False, False, False, False
                        y =vehicle["y"] + int(vehicle["length"])
                        id2 =self.state.board[y][vehicle["x"]]
                        for vehicle in self.state.vehicles:
                            if vehicle["id"] == id2:
                                if vehicle["orientation"] == 'V':
                                    v = True
                                if vehicle["orientation"] == 'H':
                                    h = True
                        if self.state.board[y][vehicle["x"]] != ' ' and v == True:
                            blocking_vehicles_from_down += 1
                        if self.state.board[y][vehicle["x"]] != ' ' and h == True:
                            blocking_vehicles_from_down += 1
                        y1 = vehicle["y"] - 1
                        id1 = self.state.board[y1][vehicle["x"]]
                        for vehicle in self.state.vehicles:
                            if vehicle["id"] == id1:
                                if vehicle["orientation"] == 'V':
                                    v1 = True
                                if vehicle["orientation"] == 'H':
                                    h1 = True
                        if self.state.board[y1][vehicle["x"]] != ' ' and v1 == True:
                            blocking_vehicles_from_up += 1
                        if self.state.board[y1][vehicle["x"]] != ' ' and h1 == True:
                            blocking_vehicles_from_up += 1
        up_down = blocking_vehicles_from_up + blocking_vehicles_from_down                    
        return self.heuri