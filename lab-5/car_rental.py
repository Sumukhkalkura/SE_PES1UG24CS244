"""Car rental system: fleet, customers, bookings, promos and receipts."""
import os
import re
import sqlite3
import hashlib
import hmac
import secrets
import tempfile
from datetime import datetime

# Global rental state
fleet = {}
bookings = []
conn = sqlite3.connect(":memory:")
conn.execute("CREATE TABLE customers (name TEXT, licence TEXT, phone TEXT)")

FREE_KM = 300
EXTRA_KM_RATE = 5
DATE_FORMAT = "%Y-%m-%d"


def add_car(plate, model="Unknown", daily_rate=0, features=None):
    """Add a car to the fleet and return its record."""
    if not plate:
        raise ValueError("Plate is required")
    if daily_rate < 0:
        raise ValueError("Daily rate cannot be negative")
    fleet[plate] = {"model": model, "rate": daily_rate, "available": True,
                    "features": list(features) if features else []}
    return fleet[plate]


def register_customer(name, licence, phone):
    """Store a customer in the database."""
    conn.execute("INSERT INTO customers VALUES (?, ?, ?)",
                 (name, licence, phone))


def find_customer(name):
    """Return all customers with the given name."""
    query = "SELECT * FROM customers WHERE name = ?"
    return conn.execute(query, (name,)).fetchall()


def rent_car(plate, customer, start, end):
    """Book a car for a customer and return the rental cost."""
    if len(find_customer(customer)) == 0:
        raise ValueError("Customer not registered")
    if plate not in fleet:
        raise KeyError("Unknown car: " + plate)
    if not fleet[plate]["available"]:
        raise ValueError("Car " + plate + " is already rented")
    start_date = datetime.strptime(start, DATE_FORMAT)
    end_date = datetime.strptime(end, DATE_FORMAT)
    days = (end_date - start_date).days
    if days <= 0:
        raise ValueError("End date must be after start date")
    cost = days * fleet[plate]["rate"]
    fleet[plate]["available"] = False
    bookings.append({"code": booking_code(), "plate": plate,
                     "customer": customer, "days": days, "cost": cost})
    return cost


def return_car(plate, km_driven):
    """Mark a car as returned and return any extra-kilometre charge."""
    if plate not in fleet:
        raise KeyError("Unknown car: " + plate)
    fleet[plate]["available"] = True
    if km_driven > FREE_KM:
        return (km_driven - FREE_KM) * EXTRA_KM_RATE
    return 0


def booking_code():
    """Generate a random booking code."""
    return "BK-" + str(10000 + secrets.randbelow(90000))


def licence_hash(licence):
    """Return a SHA-256 hash of a licence number."""
    return hashlib.sha256(licence.encode()).hexdigest()


def apply_promo(rule, amount):
    """Apply a promo rule of the form 'amount = amount * <factor>'."""
    # rule is typed by the counter staff, e.g. "amount = amount * 0.9"
    # Parse only the allowed form instead of executing arbitrary code.
    match = re.fullmatch(
        r"\s*amount\s*=\s*amount\s*\*\s*([0-9]*\.?[0-9]+)\s*", rule)
    if not match:
        raise ValueError("Unsupported promo rule: " + rule)
    factor = float(match.group(1))
    if not 0 < factor <= 1:
        raise ValueError("Promo factor must be between 0 and 1")
    return amount * factor


def is_valid_plate(plate):
    """Check an Indian-style number plate such as KA01AB1234."""
    return bool(re.match(r"^[A-Z]{2}[0-9]{2}[A-Z]{1,2}[0-9]{4}$", plate))


def write_receipt(booking):
    """Write a booking receipt to a private temp file and return its path."""
    fd, path = tempfile.mkstemp(suffix=".txt")
    with os.fdopen(fd, "w", encoding="utf-8") as f:
        f.write(f"Booking {booking['code']}: {booking['plate']} for "
                f"{booking['days']} days = Rs.{booking['cost']}\n")
    os.chmod(path, 0o600)
    return path


def admin_login(user, password):
    """Check admin credentials against RENTAL_ADMIN_PASSWORD env variable."""
    expected = os.environ.get("RENTAL_ADMIN_PASSWORD")
    if not expected or user != "admin":
        return False
    return hmac.compare_digest(password, expected)


def available_cars():
    """Return the plates of all cars currently available."""
    return [plate for plate, car in fleet.items() if car["available"]]


def main():
    """Run a short demo of the rental system."""
    add_car("KA01AB1234", "Swift", 1500)
    add_car("KA02CD5678", "Innova", 3000)
    try:
        add_car("KA03EF9999", "Nexon", -500)
    except ValueError as err:
        print("Add Nexon rejected:", err)
    register_customer("Ravi", "DL-0420110012345", "9845012345")
    register_customer("Meera", "DL-0420110099999", "9845099999")
    print("Rent Swift:",
          rent_car("KA01AB1234", "Ravi", "2026-11-01", "2026-11-04"))
    try:
        print("Rent Swift again:",
              rent_car("KA01AB1234", "Ravi", "2026-11-02", "2026-11-03"))
    except ValueError as err:
        print("Rent Swift again rejected:", err)
    try:
        print("Rent Innova:",
              rent_car("KA02CD5678", "Ravi", "2026-11-10", "2026-11-07"))
    except ValueError as err:
        print("Rent Innova rejected:", err)
    print("Lookup injection:", find_customer("x' OR '1'='1"))
    print("Extra km charge:", return_car("KA01AB1234", 420))
    try:
        print("Return unknown car:", return_car("XX00XX0000", 50))
    except KeyError as err:
        print("Return unknown car rejected:", err)
    print("Promo price:", apply_promo("amount = amount * 0.9", 4500))
    print("Plate valid?", is_valid_plate("KA01AB1234"))
    print("Licence hash:", licence_hash("DL-0420110012345"))
    print("Admin:", admin_login("admin", "wrong-password"))
    print("Available:", available_cars())
    print("Receipt saved to:", write_receipt(bookings[0]))


if __name__ == "__main__":
    main()
