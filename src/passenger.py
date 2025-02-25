"""
Author: Manuel Borregales

This module defines the Passenger class for representing a passenger.

Classes:
    Passenger: Represents a passenger with a first name, last name, and identification card.
"""

class Passenger:
    def __init__(self, name, surname, id_card):
        """Initializes a Passenger instance.
        
        Args:
            name (str): The first name of the passenger.
            surname (str): The last name of the passenger.
            id_card (str): The identification card number of the passenger.
        """
        try:
            self.__verify_name(name, surname, id_card)
        except ValueError as e:
            print(e)
            raise

        self.__name = name
        self.__surname = surname
        self.__id_card = id_card
    
    def passenger_data(self):
        """Retrieves the passenger's data.
        
        Returns:
            tuple: A tuple containing the passenger's first name, last name, and ID card.
        """
        return (self.__name, self.__surname, self.__id_card)

    def __verify_name(self, name, surname, id_card):
        """Verifies that the name, surname, and ID card are valid.
        Returns an error if the name or surname are empty strings, if they
        aren't strings, or if the ID card doesn't end with a letter and 
        the first characters are numbers and if the ID is not nine characters long.
        
        Args:
            name (str): The first name of the passenger.
            surname (str): The last name of the passenger.
            id_card (str): The identification card number of the passenger.
        
        Raises:
            ValueError: If any of the parameters are empty strings.
        """
        if not name or not surname:
            raise ValueError("Name and surname cannot be empty.")
        if not isinstance(name, str) or not isinstance(surname, str):
            raise ValueError("Name and surname must be strings.")
        if len(id_card) != 9:
            raise ValueError("ID card must be nine characters long.")
        if not id_card[-1].isalpha() or not id_card[:-1].isdigit():
            raise ValueError("ID card must end with a letter and start with numbers.")
