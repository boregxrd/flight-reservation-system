from aircraft import Aircraft

class Flight:
    def __init__(self, number, aircraft):
        self.__number = number
        self.__aircraft = Aircraft(aircraft.registration, aircraft.model, aircraft.num_rows, aircraft.num_seats_per_row)
        
        rows, seats = self.__aircraft.seating_plan()
        # I use in range here because I want the row 0 to be None
        for row_number in range(1, len(rows)):
            rows[row_number] = {letter: None for letter in seats}
        self.__seating = rows
    
    def get_number(self):
        return self.__number
    
    def get_aircraft_model(self):
        return self.__aircraft.get_model()
    
    def get_seating(self):
        return self.__seating
    
    # receives a passenger dupla and a string called seat with the structure "12C"
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
        
        self.__seating[row][letter] = passenger
        
    def reallocate_passenger(self, from_seat, to_seat):
        """Reallocate a passenger to a different seat
        Args:
        from_seat: The existing seat designator for the passenger such as '12C'
        to_seat: The new seat designator
        """
        from_row, from_letter = self.__parse_seat(from_seat)
        to_row, to_letter = self.__parse_seat(to_seat)
        
        if self.__seating[from_row][from_letter] is None:
            print(f"Initial seat {from_seat} is not occupied")
            return
        
        if self.__seating[to_row][to_letter] is not None:
            print(f"Wanted seat {to_seat} is already occupied")
            return
        
        # get the passenger, reallocate it and delete it from the initial seat
        passenger = self.__seating[from_seat][from_letter]
        self.__seating[to_row][to_letter] = passenger
        self.__seating[from_row][from_letter] = None

    def num_available_seats(self):
        """Obtains the amount of unoccupied seats
        Returns:
        The number of unoccupied seats  
        """
        available_seats = 0
        for row in self.__seating:
            for letter in self.__seating[row]: # accessing correctly to the dictionary
                if self.__seating[row][letter] is None:
                    # I don't use count here because its a dictionary not a list
                    available_seats += 1
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
            for letter, passenger in self.__seating[row]:
                if passenger is not None:
                    name, surname, id_card = passenger
                    seat = f"{row}{letter}"
                    flight_number = self.__number
                    aircraft_model = self.__aircraft.get_model()
                    print(f"----------------------------------------------------------")
                    print(f"|     {name} {surname} {id_card} {seat} {flight_number} {aircraft_model}      |")
                    print(f"----------------------------------------------------------")

    def __parse_seat(self, seat):
        """Divide a seat designator in row and letter
        Args:
        seat: The seat designator to be divided such as '12C'
        Returns:
        row: The row of the seat such as 12
        letter: The letter of the seat such as 'C'
        """
        letter = seat[-1]
        row = int(seat[:-1])

        # I want to make here a validation that letter is in fact a letter
        # and doesnt have numbers
        if not letter.isalpha():
            print(f"Invalid seat letter {letter}")
            return

        if row < 1 or row > self.__aircraft.__num_rows:
            print(f"Invalid row number {row}")
            return

        # ord function returns the unicode of the letter on the ascii table
        # and %32 divides the number by 32 and returns the remainder
        if self.__aircraft.__num_seats_per_row < ord(letter)%32:
            print(f"Invalid seat letter {letter}")
            return

        return row, letter

    def __passenger_seats(self):
        """A generator function to iterate the occupied seating locations
        Returns:
        generator: Tuple of the passenger data and the seat
        """
        for row in self.__seating:
                for letter, passenger in row.items():
                    if passenger is not None:
                        yield passenger, f"{row}{letter}" # creates a string with the row and the letter
                    