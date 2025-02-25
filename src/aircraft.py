"""
Author: Manuel Borregales

This module defines the Aircraft class and its subclasses for different aircraft types.

Classes:
    Aircraft: Represents a generic aircraft.
    Airbus: Represents an Airbus A319 aircraft.
    Boeing: Represents a Boeing 777 aircraft.
"""

import string

class Aircraft:
    def __init__(self, registration, model, num_rows, num_seats_per_row):
        """Initializes an Aircraft instance.
        
        Args:
            registration (str): The registration number of the aircraft.
            model (str): The model of the aircraft.
            num_rows (int): The number of rows in the aircraft.
            num_seats_per_row (int): The number of seats per row.
        """

        try:
            self.__verify_registration(registration)
        except ValueError as e:
            print(e)
            raise

        if not isinstance(num_rows, int) or not isinstance(num_seats_per_row, int):
            raise ValueError("Number of rows and seats per row must be integers.")
        if num_rows <= 0 or num_seats_per_row <= 0:
            raise ValueError("Number of rows and seats per row must be positive integers.")
        if not isinstance(model, str):
            raise ValueError("Model must be a string.")
        
        self.__registration = registration
        self.__model = model
        self.__num_rows = num_rows
        self.__num_seats_per_row = num_seats_per_row
    
    def get_registration(self):
        """Gets the registration number of the aircraft.
        
        Returns:
            str: The registration number.
        """
        return self.__registration
    
    def get_model(self):
        """Gets the model of the aircraft.
        
        Returns:
            str: The aircraft model.
        """
        return self.__model
    
    def get_num_rows(self):
        """Gets the number of rows in the aircraft.
        
        Returns:
            int: The number of rows.
        """
        return self.__num_rows
    
    def get_num_seats_per_row(self):
        """Gets the number of seats per row.
        
        Returns:
            int: The number of seats per row.
        """
        return self.__num_seats_per_row
    
    def seating_plan(self):
        """Generates the seating plan for the aircraft.
        
        Returns:
            tuple: A tuple containing:
                - list: A list representing the rows (index 0 is None, followed by each row as a dict).
                - str: A string of seat letters (e.g., 'ABCDEF').
        """
        rows = [None] * (self.__num_rows + 1)  # Index 0 is set to None.
        seats = string.ascii_uppercase[:self.__num_seats_per_row]
        return rows, seats

    def num_seats(self):
        """Calculates the total number of seats in the aircraft.
        
        Returns:
            int: The total number of seats.
        """
        return self.__num_rows * self.__num_seats_per_row
    
    def __verify_registration(self, registration):
        """Verifies that the registration number is valid. Returns false if
        the regirstration number is not a string, if it doesn't start with an
        uppercase letter, if the second digit is not a hyphen, if the rest of
        characters aren't letters or numbers, if the registration number is not
        six characters long.
        
        Args:
            registration (str): The registration number of the aircraft.
        
        Raises:
            ValueError: If the registration number is not nine characters long or if it doesn't end with a letter.
        """
        if not isinstance(registration, str):
            raise ValueError("Registration must be a string.")
        if not registration[:1].isupper():
            raise ValueError("Registration must start with an uppercase letter.")
        if not registration[1:2] == "-":
            raise ValueError("Registration must have a hyphen as the second character.")
        if not registration[2:].isalnum():
            raise ValueError("Registration must have letters or numbers after the hyphen.")
        if len(registration) != 6:
            raise ValueError("Registration must be six characters long.")
        
class Airbus(Aircraft):
    def __init__(self, registration, variant):
        """Initializes an Airbus instance.
        
        Args:
            registration (str): The registration number of the Airbus.
            variant (str): The variant of the Airbus.
        """
        if not isinstance(variant, str):
            raise ValueError("Variant must be a string.")
        
        self.__variant = variant
        super().__init__(registration, "Airbus A319", 23, 6)

    def get_variant(self):
        """Gets the variant of the Airbus.
        
        Returns:
            str: The variant.
        """
        return self.__variant

class Boeing(Aircraft):
    def __init__(self, registration, airline):
        """Initializes a Boeing instance.
        
        Args:
            registration (str): The registration number of the Boeing.
            airline (str): The airline operating the Boeing.
        """
        if not isinstance(airline, str):
            raise ValueError("Airline must be a string.")
        
        self.__airline = airline
        super().__init__(registration, "Boeing 777", 56, 9)
    
    def get_airline(self):
        """Gets the airline operating the Boeing.
        
        Returns:
            str: The airline.
        """
        return self.__airline
    
