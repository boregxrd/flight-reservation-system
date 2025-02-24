"""
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
        self.__name = name
        self.__surname = surname
        self.__id_card = id_card
    
    def passenger_data(self):
        """Retrieves the passenger's data.
        
        Returns:
            tuple: A tuple containing the passenger's first name, last name, and ID card.
        """
        return (self.__name, self.__surname, self.__id_card)
