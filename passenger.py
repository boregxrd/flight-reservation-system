class Passenger:
    def __init__(self, name, surname, id_card):
        self.__name = name
        self.__surname = surname
        self.__id_card = id_card
    
    def passenger_data(self):
        return (self.__name, self.__surname, self.__id_card)
    