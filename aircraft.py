class Aircraft:
    def __init__(self, registration, model, num_rows, num_seats_per_row):
        self.__registration = registration
        self.__model = model
        self.__num_rows = num_rows
        self.__num_seats_per_row = num_seats_per_row
    
    def get_registration(self):
        return self.__registration
    
    def get_model(self):
        return self.__model
    
    def seating_plan(self):
        """Generates a seating plan for the number of rows and seats per row
        Returns:
        rows: A list of Nones (size num_rows + 1).
        seats: A string of letters such as "ABCDEF"
        """
        
        rows = [None]*(self.__num_rows + 1) # None for each cell of the array
        seats = "ABCDEF"[:self.__num_seats_per_row]
        
        return rows, seats
        
        # this is the first solution I got

        #rows = list(range(0, self.__num_rows + 1)) # Here I use the list method to to create a list of numbers from 1 to num_rows
        # for index in len(rows):
        #     rows[index] = None # Here I iterate over the list and set each element to None
        # seats = "ABCDEF"[:self.__num_seats_per_row]  

        # this is how I wanted to do it

        # rows = [None, self.__num_rows + 1]
        # seats = "ABCDEF"
        # if self.__num_seats_per_row < len(seats):
        #     for i in range(len(seats)-self.__num_seats_per_row):
        #         seats.pop()
        # return rows, seats

    def num_seats(self):
        """Calculates the number of seats
        Returns:
        seats: The number of seats
        """
        return self.__num_rows * self.__num_seats_per_row
    
class Airbus(Aircraft):
    def __init__(self, registration, variant):
        self.__variant = variant
        super().__init__(registration, "Airbus A319", 23, 6)
        
class Boeing(Aircraft):
    def __init__(self, registration, airline):
        self.__airline = airline
        super().__init__(registration, "Boeing 777", 56, 9)