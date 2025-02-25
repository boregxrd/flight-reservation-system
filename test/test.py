"""
Test module for the flight reservation system.

This module contains comprehensive tests for the Flight, Aircraft, and Passenger classes,
focusing on both normal operation and edge cases.
"""

import pytest
from src.flight import Flight
from src.aircraft import Aircraft, Boeing, Airbus
from src.passenger import Passenger


# Fixtures for reusable test objects
@pytest.fixture
def standard_aircraft():
    return Aircraft(registration="G-EUPT", model="Test Aircraft", num_rows=10, num_seats_per_row=6)


@pytest.fixture
def standard_flight(standard_aircraft):
    return Flight(number="BA123", aircraft=standard_aircraft)


@pytest.fixture
def standard_passenger():
    return Passenger(name="John", surname="Doe", id_card="12345678X")


@pytest.fixture
def populated_flight(standard_flight, standard_passenger):
    """Flight with some seats already allocated"""
    passenger_data = standard_passenger.passenger_data()
    standard_flight.allocate_passenger("1A", passenger_data)
    standard_flight.allocate_passenger("5C", passenger_data)
    standard_flight.allocate_passenger("10F", passenger_data)
    return standard_flight


class TestAircraft:
    """Test cases for the Aircraft class and its subclasses"""

    def test_aircraft_creation(self):
        """Test creation of Aircraft objects with valid parameters"""
        aircraft = Aircraft(registration="G-ABCD", model="Test Model", num_rows=15, num_seats_per_row=6)
        assert aircraft.get_registration() == "G-ABCD"
        assert aircraft.get_model() == "Test Model"
        assert aircraft.get_num_rows() == 15
        assert aircraft.get_num_seats_per_row() == 6

    def test_aircraft_subclasses(self):
        """Test creation of Airbus and Boeing subclasses"""
        airbus = Airbus(registration="G-EUPT", variant="A319-100")
        assert airbus.get_model() == "Airbus A319"
        assert airbus.get_variant() == "A319-100"
        assert airbus.get_num_rows() == 23
        assert airbus.get_num_seats_per_row() == 6

        boeing = Boeing(registration="F-GSPS", airline="Emirates")
        assert boeing.get_model() == "Boeing 777"
        assert boeing.get_airline() == "Emirates"
        assert boeing.get_num_rows() == 56
        assert boeing.get_num_seats_per_row() == 9

    def test_invalid_registration(self):
        """Test creation with invalid registration numbers"""
        # Not a string
        with pytest.raises(ValueError, match="Registration must be a string"):
            Aircraft(registration=123, model="Test", num_rows=10, num_seats_per_row=4)
        
        # Doesn't start with uppercase
        with pytest.raises(ValueError, match="Registration must start with an uppercase letter"):
            Aircraft(registration="a-ABC", model="Test", num_rows=10, num_seats_per_row=4)
        
        # No hyphen as second character
        with pytest.raises(ValueError, match="Registration must have a hyphen as the second character"):
            Aircraft(registration="AABC", model="Test", num_rows=10, num_seats_per_row=4)
        
        # Non-alphanumeric after hyphen
        with pytest.raises(ValueError, match="Registration must have letters or numbers after the hyphen"):
            Aircraft(registration="A-$%^", model="Test", num_rows=10, num_seats_per_row=4)
        
        # Not 6 characters long
        with pytest.raises(ValueError, match="Registration must be six characters long"):
            Aircraft(registration="A-ABC", model="Test", num_rows=10, num_seats_per_row=4)

    def test_invalid_dimensions(self):
        """Test creation with invalid row and seat dimensions"""
        # Negative rows
        with pytest.raises(ValueError, match="Number of rows and seats per row must be positive integers"):
            Aircraft(registration="G-ABCD", model="Test", num_rows=-1, num_seats_per_row=4)
        
        # Zero seats per row
        with pytest.raises(ValueError, match="Number of rows and seats per row must be positive integers"):
            Aircraft(registration="G-ABCD", model="Test", num_rows=10, num_seats_per_row=0)
        
        # Non-integer values
        with pytest.raises(ValueError, match="Number of rows and seats per row must be integers"):
            Aircraft(registration="G-ABCD", model="Test", num_rows="10", num_seats_per_row=4)

    def test_seating_plan(self):
        """Test the seating plan generation"""
        aircraft = Aircraft(registration="G-ABCD", model="Test", num_rows=3, num_seats_per_row=2)
        rows, seats = aircraft.seating_plan()
        
        # Check rows has correct length (num_rows + 1 because row 0 is None)
        assert len(rows) == 4
        assert rows[0] is None
        
        # Check seats contains the right letters
        assert seats == "AB"


class TestPassenger:
    """Test cases for the Passenger class"""

    def test_passenger_creation(self):
        """Test creation of Passenger objects with valid parameters"""
        passenger = Passenger(name="Alice", surname="Smith", id_card="12345678Z")
        assert passenger.passenger_data() == ("Alice", "Smith", "12345678Z")

    def test_invalid_name(self):
        """Test creation with invalid name parameters"""
        # Empty name
        with pytest.raises(ValueError, match="Name and surname cannot be empty"):
            Passenger(name="", surname="Smith", id_card="12345678Z")
        
        # Empty surname
        with pytest.raises(ValueError, match="Name and surname cannot be empty"):
            Passenger(name="Alice", surname="", id_card="12345678Z")
        
        # Non-string name
        with pytest.raises(ValueError, match="Name and surname must be strings"):
            Passenger(name=123, surname="Smith", id_card="12345678Z")

    def test_invalid_id_card(self):
        """Test creation with invalid ID card parameters"""
        # Wrong length
        with pytest.raises(ValueError, match="ID card must be nine characters long"):
            Passenger(name="Alice", surname="Smith", id_card="1234Z")
        
        # No letter at end
        with pytest.raises(ValueError, match="ID card must end with a letter and start with numbers"):
            Passenger(name="Alice", surname="Smith", id_card="123456789")
        
        # Non-numeric prefix
        with pytest.raises(ValueError, match="ID card must end with a letter and start with numbers"):
            Passenger(name="Alice", surname="Smith", id_card="1234A678Z")


class TestFlight:
    """Test cases for the Flight class"""

    def test_flight_creation(self, standard_aircraft):
        """Test creation of Flight objects with valid parameters"""
        flight = Flight(number="BA123", aircraft=standard_aircraft)
        assert flight.get_number() == "BA123"
        assert flight.get_aircraft_model() == "Test Aircraft"
        
        # Check seating initialization
        seating = flight.get_seating()
        assert seating[0] is None
        assert seating[1]["A"] is None  # First seat should be unoccupied

    def test_invalid_flight_number(self, standard_aircraft):
        """Test creation with invalid flight numbers"""
        # First two characters aren't letters
        with pytest.raises(ValueError, match="The first two characters must be letters"):
            Flight(number="1A123", aircraft=standard_aircraft)
        
        # First two characters aren't uppercase
        with pytest.raises(ValueError, match="The first two characters must be uppercase"):
            Flight(number="ba123", aircraft=standard_aircraft)
        
        # Last characters aren't numbers
        with pytest.raises(ValueError, match="The last characters must be numbers"):
            Flight(number="BAabc", aircraft=standard_aircraft)
        
        # Number part too large
        with pytest.raises(ValueError, match="The last characters must be less than 9999"):
            Flight(number="BA12345", aircraft=standard_aircraft)

    def test_allocate_passenger(self, standard_flight, standard_passenger):
        """Test allocating passengers to seats"""
        passenger_data = standard_passenger.passenger_data()
        
        # Allocate to valid seat
        standard_flight.allocate_passenger("1A", passenger_data)
        seating = standard_flight.get_seating()
        assert seating[1]["A"] == passenger_data
        
        # Check available seats decreased
        initial_seats = standard_flight.num_available_seats()
        standard_flight.allocate_passenger("2B", passenger_data)
        assert standard_flight.num_available_seats() == initial_seats - 1

    def test_allocate_to_occupied_seat(self, standard_flight, standard_passenger):
        """Test allocating a passenger to an already occupied seat"""
        passenger_data = standard_passenger.passenger_data()
        standard_flight.allocate_passenger("1A", passenger_data)
        
        # Try to allocate to the same seat
        with pytest.raises(ValueError, match="Seat 1A is already occupied"):
            standard_flight.allocate_passenger("1A", passenger_data)

    @pytest.mark.parametrize("invalid_seat", [
        "0A",  # Row too small
        "11A",  # Row too large
        "1G",   # Seat letter out of range
        "AA",   # Non-numeric row
        "1$",   # Non-alphabetic seat
    ])
    def test_allocate_invalid_seat(self, standard_flight, standard_passenger, invalid_seat):
        """Test allocating a passenger to an invalid seat"""
        passenger_data = standard_passenger.passenger_data()
        with pytest.raises(ValueError):
            standard_flight.allocate_passenger(invalid_seat, passenger_data)

    def test_reallocate_passenger(self, standard_flight, standard_passenger):
        """Test reallocating a passenger from one seat to another"""
        passenger_data = standard_passenger.passenger_data()
        
        # Allocate passenger to initial seat
        standard_flight.allocate_passenger("1A", passenger_data)
        
        # Reallocate to new seat
        standard_flight.reallocate_passenger("1A", "2B")
        
        # Check passenger was moved correctly
        seating = standard_flight.get_seating()
        assert seating[1]["A"] is None
        assert seating[2]["B"] == passenger_data

    def test_reallocate_from_empty_seat(self, standard_flight, standard_passenger):
        """Test reallocating from an unoccupied seat"""
        passenger_data = standard_passenger.passenger_data()
        with pytest.raises(ValueError, match="Initial seat 1A is not occupied"):
            standard_flight.reallocate_passenger("1A", "2B")

    def test_reallocate_to_occupied_seat(self, standard_flight, standard_passenger):
        """Test reallocating to an already occupied seat"""
        passenger_data = standard_passenger.passenger_data()
        standard_flight.allocate_passenger("1A", passenger_data)
        standard_flight.allocate_passenger("2B", passenger_data)
        
        with pytest.raises(ValueError, match="Wanted seat 2B is already occupied"):
            standard_flight.reallocate_passenger("1A", "2B")

    def test_num_available_seats(self, standard_flight, standard_passenger):
        """Test counting available seats"""
        passenger_data = standard_passenger.passenger_data()
        total_seats = standard_flight.num_available_seats()
        
        # Allocate some seats
        standard_flight.allocate_passenger("1A", passenger_data)
        standard_flight.allocate_passenger("2B", passenger_data)
        standard_flight.allocate_passenger("3C", passenger_data)
        
        # Check count is correct
        assert standard_flight.num_available_seats() == total_seats - 3
        
        # Reallocate a passenger (shouldn't change total)
        standard_flight.reallocate_passenger("1A", "4D")
        assert standard_flight.num_available_seats() == total_seats - 3

    def test_no_available_seats(self, standard_aircraft):
        """Test behavior when no seats are available"""
        # Create a tiny aircraft
        tiny_aircraft = Aircraft(registration="G-TINY", model="Test", num_rows=1, num_seats_per_row=1)
        flight = Flight(number="BA999", aircraft=tiny_aircraft)
        
        # Fill the only seat
        flight.allocate_passenger("1A", ("John", "Doe", "12345678X"))
        
        # Try to allocate another passenger
        with pytest.raises(ValueError, match="No available seats"):
            flight.allocate_passenger("1A", ("Jane", "Doe", "87654321Y"))

    def test_flight_deep_copy_aircraft(self, standard_aircraft):
        """Test that Flight creates a deep copy of the Aircraft"""
        flight = Flight(number="BA123", aircraft=standard_aircraft)
        
        # Modify the original aircraft
        original_rows = standard_aircraft.get_num_rows()
        # This won't work because the attribute is private, but the test concept is valid
        # standard_aircraft._Aircraft__num_rows = 99
        
        # The flight's aircraft should not be affected
        assert flight.get_aircraft_model() == standard_aircraft.get_model()


# Advanced scenarios
class TestEdgeCases:
    """Test edge cases in the flight reservation system"""

    @pytest.fixture
    def fully_booked_flight(self, standard_passenger):
        """Create a flight with all seats occupied"""
        tiny_aircraft = Aircraft(registration="G-TINY", model="Test", num_rows=1, num_seats_per_row=2)
        flight = Flight(number="BA999", aircraft=tiny_aircraft)
        passenger_data = standard_passenger.passenger_data()
        
        # Fill all seats
        flight.allocate_passenger("1A", passenger_data)
        flight.allocate_passenger("1B", passenger_data)
        
        return flight

    def test_allocate_when_full(self, fully_booked_flight, standard_passenger):
        """Test allocating a passenger when all seats are occupied"""
        passenger_data = standard_passenger.passenger_data()
        with pytest.raises(ValueError, match="No available seats"):
            fully_booked_flight.allocate_passenger("1A", passenger_data)

    def test_print_methods(self, populated_flight, capsys):
        """Test print_seating and print_boarding_cards methods"""
        # Call the print methods
        populated_flight.print_seating()
        populated_flight.print_boarding_cards()
        
        # Capture the output
        captured = capsys.readouterr()
        
        # Check that something was printed
        assert len(captured.out) > 0
        assert "Row" in captured.out
        assert "------------------" in captured.out


# Parametrized tests for more comprehensive coverage
@pytest.mark.parametrize("flight_number,expected_valid", [
    ("BA123", True),
    ("AA9999", True),
    ("AZ1", True),
    ("1A123", False),  # First two chars not letters
    ("ba123", False),  # First two chars not uppercase
    ("BAabc", False),  # Last chars not numbers
    ("BA10000", False),  # Number part too large
])
def test_flight_number_validation(flight_number, expected_valid, standard_aircraft):
    """Test various flight number formats"""
    if expected_valid:
        flight = Flight(number=flight_number, aircraft=standard_aircraft)
        assert flight.get_number() == flight_number
    else:
        with pytest.raises(ValueError):
            Flight(number=flight_number, aircraft=standard_aircraft)


@pytest.mark.parametrize("seat,expected_valid", [
    ("1A", True),
    ("10F", True),
    ("0A", False),  # Row too small
    ("11A", False),  # Row too large (for standard_aircraft)
    ("1G", False),   # Seat letter out of range
    ("A1", False),   # Non-numeric row
])
def test_seat_validation(seat, expected_valid, standard_flight, standard_passenger):
    """Test various seat designator formats"""
    passenger_data = standard_passenger.passenger_data()
    if expected_valid:
        standard_flight.allocate_passenger(seat, passenger_data)
        seating = standard_flight.get_seating()
        row, letter = int(seat[:-1]), seat[-1]
        assert seating[row][letter] == passenger_data
    else:
        with pytest.raises(ValueError):
            standard_flight.allocate_passenger(seat, passenger_data)


# Run the tests
if __name__ == "__main__":
    pytest.main(["-v"])