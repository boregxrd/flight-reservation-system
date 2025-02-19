from flight import Flight
from aircraft import Aircraft, Boeing, Airbus
from passenger import Passenger

def make_flights():
    f1 = Flight(number = "BA117", aircraft = Aircraft(registration = "G-EUAH", model = "Airbus A319", num_rows = 22, num_seats_per_row=6))
    f2 = Flight(number = "AF92", aircraft = Boeing(registration = "F-GSPS", airline = "Emirates"))
    f3 = Flight(number = "BA148", aircraft = Airbus(registration = "G-EUPT", variant = "A319-100"))

    p1 = Passenger("Jack", "Shephard", "85994003S")
    p2 = Passenger("Kate", "Austen", "12589756P")
    p3 = Passenger("James", "Ford", "56278665F")
    p4 = Passenger("John", "Locke", "10265448H")
    p5 = Passenger("Sayid", "Jarrah", "15758664M")

    f1.allocate_passenger("12A", p1.passenger_data())
    f1.allocate_passenger("18F", p2.passenger_data())
    f1.allocate_passenger("18E", p3.passenger_data())
    f1.allocate_passenger("1C", p4.passenger_data())
    f1.allocate_passenger("4D", p5.passenger_data())

    return f1, f2, f3

f1, f2, f3 = make_flights()
for fl in f1, f2, f3:
  fl.print_seating()
  fl.print_boarding_cards()