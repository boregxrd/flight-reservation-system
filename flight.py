class Flight:
    def __init__(self, number, aircraft):
        self.__number = number
        self.__aircraft = aircraft
        self.__seating = aircraft.seating_plan()
    
    def get_number(self):
        return self.__number
    
    def get_aircraft_model(self):
        return self.__aircraft.get_model()
    
    def allocate_passenger(self, seat, passenger):
        """Allocate a seat to a passenger
        Args:
        seat: A seat designator such as '12C' or '21F'
        passenger: The passenger data such as ('Jack', 'Shephard', '85994003S')
        """
        if self.num_available_seats() == 0:
            print ("No available seats")
            return

        row, letter = self.__parse_seat(seat)
        
        if self.__seating[row][letter] is not None:
            print(f"Seat {seat} is already occupied")
            return
        
        self.__seating[row] = {"letter": letter, "passenger": passenger}
        
    def reallocate_passenger(self, from_seat, to_seat):
        """Reallocate a passenger to a different seat
        Args:
        from_seat: The existing seat designator for the passenger such as '12C'
        to_seat: The new seat designator
        """
        from_row, from_letter = self.__parse_seat(from_seat)
        to_row, to_letter = self.__parse_seat(to_seat)
        
        if self.__seating[from_row] is not None:
            print(f"Seat {from_seat} is not occupied")
            return
        
        if self.__seating[to_row] is not None:
            print(f"Seat {to_seat} is already occupied")
            return
        
        passenger = from_seat[from_letter]

        self.__seating[to_row] = {to_letter: passenger}


    def num_available_seats(self):
        """Obtains the amount of unoccupied seats
        Returns:
        The number of unoccupied seats  
        """
        available_seats = 0
        for row in self.__seating:
            available_seats += row.count(None)
        return available_seats
    
    def print_seating(self):
        """Prints in console the seating plan
        Example of one row:
            {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None}
        """
        for i, row in len(self.__seating):
            print(f"Row {i} {row}")

    def print_boarding_cards(self):
        """Prints in console the boarding card for each passenger
        Example of one boarding card:
        ----------------------------------------------------------
        |     Jack Sheppard 85994003S 15E BA758 Airbus A319      |
        ----------------------------------------------------------
        """
        for row in self.__seating:
            if(row is not None):
                
        flight_number = self.__number
        aircraft_model = self.__aircraft.get_model()
        print(f"----------------------------------------------------------")
        print(f"|     {name} {surname} {id_card} {seat} {flight_number} {aircraft_model}      |")
        print(f"----------------------------------------------------------")

    def __parse_seat(seat):
        """Divide a seat designator in row and letter
        Args:
        seat: The seat designator to be divided such as '12C'
        Returns:
        row: The row of the seat such as 12
        letter: The letter of the seat such as 'C'
        """
        seat = "12C"
        letter = seat[-1]
        row = seat[:-1]

        return row, letter

    def __passenger_seats(self):
        """A generator function to iterate the occupied seating locations
        Returns:
        generator: Tuple of the passenger data and the seat
        """
        for row in self.__seating:
            if row is not None:
                for key in row.keys():
                letter = row.keys()
                seat = f"{row}{letter}"
                passenger = row[letter]