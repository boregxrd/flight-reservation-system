import string

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
    
    def get_num_rows(self):
        return self.__num_rows
    
    def get_num_seats_per_row(self):
        return self.__num_seats_per_row
    
    def seating_plan(self):
        """Generates a seating plan for the number of rows and seats per row
        Returns:
        rows: A list of Nones (size num_rows + 1).
        seats: A string of letters such as "ABCDEF"
        """
        
        rows = [None]*(self.__num_rows + 1) # None for each cell of the array
        seats = string.ascii_uppercase[:self.__num_seats_per_row] # I cut the string to the length of the number of seats per row
        
        return rows, seats

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

    def get_variant(self):
        return self.__variant
        
class Boeing(Aircraft):
    def __init__(self, registration, airline):
        self.__airline = airline
        super().__init__(registration, "Boeing 777", 56, 9)
    
    def get_airline(self):
        return self.__airline