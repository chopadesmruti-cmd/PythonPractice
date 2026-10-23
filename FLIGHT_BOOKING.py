
from abc import ABC, abstractmethod


# 1. Flight class
class Flight:
    def __init__(self, code, airline, source, destination, seats, fare):
        self.code = code
        self.airline = airline
        self.source = source
        self.destination = destination
        self.__seats = seats
        self.fare = fare

    @property
    def available_seats(self):
        return self.__seats

    def display(self):
        print(
            f"{self.code} | {self.airline} | "
            f"{self.source} -> {self.destination} | "
            f"Seats: {self.available_seats} | Fare: Rs.{self.fare}"
        )

    def book_seats(self, count):
        if count <= 0 or count > self.__seats:
            return False

        self.__seats -= count
        return True


# 2. Passenger abstract base class
class Passenger(ABC):
    def __init__(self, name, age):
        self.name = name
        self.age = age

    @abstractmethod
    def get_discount(self):
        pass


# 3. Regular passenger
class RegularPassenger(Passenger):
    def get_discount(self):
        return 0


# 4. Student passenger
class StudentPassenger(Passenger):
    def get_discount(self):
        return 10


# 5. Booking class
class Booking:
    def __init__(self, booking_id, passenger, flight, tickets,
                 base_total, discount, final_total):
        self.booking_id = booking_id
        self.passenger = passenger
        self.flight = flight
        self.tickets = tickets
        self.base_total = base_total
        self.discount = discount
        self.final_total = final_total

    def display_summary(self):
        print("\n===== BOOKING SUMMARY =====")
        print("Booking ID:", self.booking_id)
        print("Passenger:", self.passenger.name)
        print("Age:", self.passenger.age)
        print("Category:", type(self.passenger).__name__)
        print("Flight:", self.flight.code)
        print("Airline:", self.flight.airline)
        print("Route:", self.flight.source, "to",
              self.flight.destination)
        print("Tickets:", self.tickets)
        print("Base fare:", self.base_total)
        print("Discount:", self.discount)
        print("Final fare: Rs.", self.final_total)


# 6. Main booking system
class FlightBookingSystem:
    def __init__(self):
        self.flights = [
            Flight("F101", "Air India", "Pune", "Delhi", 5, 5000),
            Flight("F102", "IndiGo", "Mumbai", "Bengaluru", 4, 4000),
            Flight("F103", "Akasa Air", "Delhi", "Pune", 6, 4500)
        ]
        self.bookings = []

    def display_flights(self):
        print("\n===== AVAILABLE FLIGHTS =====")
        for flight in self.flights:
            flight.display()

    def find_flight(self, code):
        for flight in self.flights:
            if flight.code.lower() == code.lower():
                return flight
        return None

    def validate_details(self, flight, name, age, tickets):
        if flight is None:
            print("Error: Flight code not found.")
            return False
        if not name.strip():
            print("Error: Passenger name cannot be empty.")
            return False
        if age < 1 or age > 120:
            print("Error: Enter a valid age.")
            return False
        if tickets < 1:
            print("Error: Tickets must be at least 1.")
            return False
        if tickets > flight.available_seats:
            print("Error: Not enough seats available.")
            return False
        return True

    def calculate_fare(self, passenger, flight, tickets):
        base_total = flight.fare * tickets
        discount = base_total * passenger.get_discount() / 100
        final_total = base_total - discount
        return base_total, discount, final_total

    def book_flight(self):
        self.display_flights()

        code = input("\nEnter flight code: ").strip()
        flight = self.find_flight(code)

        name = input("Enter passenger name: ").strip()

        try:
            age = int(input("Enter passenger age: "))
            tickets = int(input("Enter number of tickets: "))
        except ValueError:
            print("Error: Age and ticket count must be numbers.")
            return

        if not self.validate_details(flight, name, age, tickets):
            return

        print("\nPassenger Category")
        print("1. Regular Passenger")
        print("2. Student Passenger")

        category = input("Choose category: ").strip()

        if category == "1":
            passenger = RegularPassenger(name, age)
        elif category == "2":
            passenger = StudentPassenger(name, age)
        else:
            print("Error: Invalid passenger category.")
            return

        base, discount, total = self.calculate_fare(
            passenger, flight, tickets
        )

        print("\nBase fare: Rs.", base)
        print("Discount: Rs.", discount)
        print("Final fare: Rs.", total)

        confirm = input("Confirm booking? (yes/no): ").strip().lower()

        if confirm != "yes":
            print("Booking cancelled. No seats were changed.")
            return

        # Change seats only after all validation and confirmation
        if not flight.book_seats(tickets):
            print("Booking failed: Seats are no longer available.")
            return

        booking_id = f"B{len(self.bookings) + 1:03d}"

        booking = Booking(
            booking_id, passenger, flight, tickets,
            base, discount, total
        )

        self.bookings.append(booking)

        print("\nBooking confirmed successfully!")
        booking.display_summary()

    def view_booking(self):
        if not self.bookings:
            print("\nNo confirmed booking found.")
            return

        self.bookings[-1].display_summary()

    def run(self):
        while True:
            print("\n===== FLIGHT BOOKING SYSTEM =====")
            print("1. View Flights")
            print("2. Book Flight")
            print("3. View Booking")
            print("4. Exit")

            choice = input("Enter your choice: ").strip()

            if choice == "1":
                self.display_flights()
            elif choice == "2":
                self.book_flight()
            elif choice == "3":
                self.view_booking()
            elif choice == "4":
                print("Thank you for using Flight Booking System!")
                break
            else:
                print("Invalid choice. Please select 1 to 4.")


# Create the system object and start the application
system = FlightBookingSystem()
system.run()
