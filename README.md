# Flight Reservation System

A Python-based flight reservation system for managing aircraft, flights, and passenger bookings.

## Overview

This system allows users to:
- Create and manage different aircraft types
- Set up flights with specific aircraft
- Allocate and reallocate passenger seats
- Generate boarding passes

## Components

### Aircraft Module

Contains classes for representing different aircraft types:

- `Aircraft`: Base class representing generic aircraft
- `Airbus`: Represents Airbus A319 aircraft (23 rows, 6 seats per row)
- `Boeing`: Represents Boeing 777 aircraft (56 rows, 9 seats per row)

### Flight Module

Handles flight creation and seat management:

- `Flight`: Manages flight information, seating arrangements, and boarding passes

### Passenger Module

Manages passenger information:

- `Passenger`: Stores passenger details (name, surname, ID card)

## Usage Examples

### Creating Aircraft

```python
# Create a generic aircraft
aircraft = Aircraft("G-ABCD", "Generic Model", 10, 4)

# Create an Airbus
airbus = Airbus("A-EFGH", "Standard")

# Create a Boeing
boeing = Boeing("B-IJKL", "Example Airlines")
```

### Creating Flights

```python
# Create a flight with an aircraft
flight = Flight("BA123", aircraft)

# Get flight information
flight_number = flight.get_number()
aircraft_model = flight.get_aircraft_model()
available_seats = flight.num_available_seats()
```

### Managing Passengers

```python
# Create a passenger
passenger = Passenger("John", "Smith", "123456789X")

# Get passenger data
passenger_data = passenger.passenger_data()  # Returns a tuple: ("John", "Smith", "123456789X")
```

### Seat Allocation

```python
# Allocate a seat to a passenger
flight.allocate_passenger("1A", passenger.passenger_data())

# Reallocate a passenger to a different seat
flight.reallocate_passenger("1A", "2B")

# Print the current seating arrangement
flight.print_seating()

# Print boarding passes for all passengers
flight.print_boarding_cards()
```

## Validation

The system includes extensive validation:

- Aircraft registration must be properly formatted (letter, hyphen, alphanumeric, 6 chars total)
- Flight numbers must follow the pattern of two uppercase letters followed by numbers (≤ 9999)
- Seat designations must be valid for the aircraft (e.g., "1A", "23F")
- Passenger IDs must be 9 characters (8 digits followed by a letter)

## Error Handling

The system uses exceptions to handle errors:
- Invalid flight numbers, aircraft registrations, or seat assignments
- Attempts to allocate already occupied seats
- Passenger data validation

## Local Testing

To run the test file, execute the following commands from the root of the project:

```bash
pip install pytest  # Install pytest if not already installed

# Run tests with the correct module path
PYTHONPATH=$(pwd) pytest test/test.py -v
