"""
This module defines the Flight class for managing flight reservations.

Classes:
    Flight: Represents a flight, including seating arrangements and boarding passes.
"""

from aircraft import Aircraft

class Flight:
    def __init__(self, number, aircraft):
        """Initializes a Flight instance with the given flight number and aircraft.
        
        Args:
            number (str): The flight number.
            aircraft (Aircraft): An instance of an Aircraft.
        """
        try:
            self.__verify_flight_number(number)
        except ValueError as e:
            print(e)
            # If you want to propagate the error, use:
            raise
    
        self.__number = number
        self.__aircraft = Aircraft(
            aircraft.get_registration(),
            aircraft.get_model(),
            aircraft.get_num_rows(),
            aircraft.get_num_seats_per_row()
        )
        
        rows, seats = self.__aircraft.seating_plan()
        # Row 0 is intentionally left as None so that the row number matches its index.
        for row_number in range(1, len(rows)):
            rows[row_number] = {letter: None for letter in seats}
        self.__seating = rows
    
    def get_number(self):
        """Gets the flight number.
        
        Returns:
            str: The flight number.
        """
        return self.__number
    
    def get_aircraft_model(self):
        """Gets the model of the aircraft used in the flight.
        
        Returns:
            str: The aircraft model.
        """
        return self.__aircraft.get_model()
    
    def get_seating(self):
        """Gets the seating plan of the flight.
        
        Returns:
            list: The seating plan represented as a list where index 0 is None and each subsequent element is a dict mapping seat letters to passenger data.
        """
        return self.__seating
    
    def allocate_passenger(self, seat, passenger):
        """Allocates a seat to a passenger.
        
        Args:
            seat (str): A seat designator such as '12C' or '21F'.
            passenger (tuple): The passenger data (e.g., ('Jack', 'Shephard', '85994003S')).
        """

        if self.num_available_seats() == 0:
            raise ValueError("No available seats")

        row, letter = self.__parse_seat(seat)

        if self.__seating[row][letter] is not None:
            raise ValueError(f"Seat {seat} is already occupied")

        self.__seating[row][letter] = passenger
        
    def reallocate_passenger(self, from_seat, to_seat):
        """Reallocates a passenger from one seat to another.
        
        Args:
            from_seat (str): The current seat designator for the passenger (e.g., '12C').
            to_seat (str): The new seat designator.
        """
        from_row, from_letter = self.__parse_seat(from_seat)
        to_row, to_letter = self.__parse_seat(to_seat)
        
        if self.__seating[from_row][from_letter] is None:
            raise ValueError(f"Initial seat {from_seat} is not occupied")
        
        if self.__seating[to_row][to_letter] is not None:
            raise ValueError(f"Wanted seat {to_seat} is already occupied")
        
        # Get the passenger, reallocate it, and remove it from the original seat.
        passenger = self.__seating[from_row][from_letter]
        self.__seating[to_row][to_letter] = passenger
        self.__seating[from_row][from_letter] = None

    def num_available_seats(self):
        """Calculates the number of available (unoccupied) seats.
        
        Returns:
            int: The number of unoccupied seats.
        """
        available_seats = 0
        for row in self.__seating:
            if row is None:  # Skip rows that are None (like row 0).
                continue
            for letter in row:  # Iterate over the seat letters in the row.
                if row[letter] is None:
                    available_seats += 1
        return available_seats

    def print_seating(self):
        """Prints the seating plan to the console.
        
        Example:
            Row 1 {'A': None, 'B': None, 'C': None, 'D': None, 'E': None, 'F': None}
        """
        i = 0
        for row in self.__seating:
            print(f"Row {i} {row}")
            i += 1

    def print_boarding_cards(self):
        """Prints the boarding cards for each passenger to the console.
        
        Each boarding card includes the passenger's name, surname, ID, seat, flight number, and aircraft model.
        """
        for passenger, seat in self.__passenger_seats():
            name, surname, id_card = passenger
            flight_number = self.__number
            aircraft_model = self.__aircraft.get_model()
            print("----------------------------------------------------------")
            print(f"|     {name} {surname} {id_card} {seat} {flight_number} {aircraft_model}      |")
            print("----------------------------------------------------------")


    def __parse_seat(self, seat):
        """Parses a seat designator into a row number and a seat letter.
        
        Args:
            seat (str): The seat designator (e.g., '12C').
        
        Returns:
            tuple: A tuple containing the row number (int) and the seat letter (str).
        """
        letter = seat[-1]
        row_str = seat[:-1]  # Keep it as string for validation
        try:
            # Validate before converting to int
            self.__verify_seat(row_str, letter)
        except ValueError as e:
            print(e)
            # If you want to propagate the error, use:
            raise

        # Now convert row_str to int after verification
        row = int(row_str)
        return row, letter

    def __passenger_seats(self):
        """Generator that yields tuples of passenger data and their seat designator.

        Yields:
            tuple: A tuple containing the passenger data and the seat designator as a string.
        """
        for row_number, row in enumerate(self.__seating):
            if row is None:
                continue
            for letter, passenger in row.items():
                if passenger is not None:
                    yield passenger, f"{row_number}{letter}"
    
    def __verify_flight_number(self, number):
        """Verifies that the flight number is valid. Returns false if 
        the first two characters of the number aren't letters, if the the 
        first two characters are lowercased, if the rest are numbers and if
        they are numbers that they are less than 9999.
        
        Args:
            number (str): The flight number.
        
        Returns:
            bool: True if the flight number is valid; False otherwise.
        """
        if not number[:2].isalpha():
            raise ValueError(f"Invalid flight number {number}. The first two characters must be letters.")
        if not number[:2].isupper():
            raise ValueError(f"Invalid flight number {number}. The first two characters must be uppercase.")
        if not number[2:].isdigit():
            raise ValueError(f"Invalid flight number {number}. The last characters must be numbers.")
        if int(number[2:]) > 9999:
            raise ValueError(f"Invalid flight number {number}. The last characters must be less than 9999.")
        return True
    
    def __verify_seat(self, row_str, letter):
        """Verifies that the seat is valid. Returns false if the row is 
        less than 1 or greater than the number of rows, if the seat letter 
        is not alphabetical, if the seat letter is greater than the number
        of seats per row and if the row characters are numbers.
        
        Args:
            row (int): The row number.
            letter (str): The seat letter.
        
        Returns:
            bool: True if the seat is valid; False otherwise.
        """
        if not row_str.isdigit():
            raise ValueError(f"Invalid row number {row_str}. The row number must be a number.")
        if not letter.isalpha():
            raise ValueError(f"Invalid seat letter {letter}. The seat letter must be alphabetical.")

        row = int(row_str)
        if row < 1 or row > self.__aircraft.get_num_rows():
            raise ValueError(f"Invalid row number {row}. The row number must be between 1 and {self.__aircraft.get_num_rows()}.")
        
        # Convert letter to a numerical index, e.g., 'A' -> 1, 'B' -> 2, etc.
        seat_index = ord(letter.upper()) - ord('A') + 1
        if seat_index > self.__aircraft.get_num_seats_per_row():
            raise ValueError(f"Invalid seat letter {letter}. The seat letter must be between 'A' and {chr(ord('A') + self.__aircraft.get_num_seats_per_row() - 1)}.")
        
        return True
        
