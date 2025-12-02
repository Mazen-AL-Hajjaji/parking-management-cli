from datetime import datetime
import getpass


class Admin:
    # Simple admin handler used to protect sensitive operations (spots, prices, shutdown).
    password = "admin123"
    is_logged_in = False

    @classmethod
    def authentication(cls):
        # Ask for admin password up to 3 times; allow skipping to continue as normal user.
        print("=== Admin login (press Enter to skip) ===")
        max_attempts = 3
        for attempt in range(1, max_attempts + 1):

            try:
                entered = getpass.getpass("Enter admin password (or press Enter to skip)").strip().lower()
            except Exception:
                # Fallback for environments where getpass does not work.
                entered = input("Enter admin password (or press Enter to skip)").strip().lower()

            if entered == "":
                print("Continuing as a user.")
                return False
            if entered == cls.password:
                print("Admin authenticated. Admin privileges granted.")
                cls.is_logged_in = True
                return True
            else:
                remaining = max_attempts -attempt
                if remaining > 0:
                    print(f"Wrong password. Try again. ({remaining} attempt(s) left)")
                else: 
                    print("Too many incorrect attempts. continuing as a normal user")
                    return False
                
    @classmethod
    def logout(cls):
        # Clear admin session flag.
        if not cls.is_logged_in:
            print("No admin is currently logged in.")

        else:
            cls.is_logged_in = False
            print("Admin has been logged out.")

    @classmethod
    def change_password(cls):
        # Allow admin to change password after verifying current one.
        if not cls.is_logged_in:
            print("⚠️ You must be logged in as admin to change the password.")
            return False
        try:
            current = getpass.getpass("Current admin password: ").strip().lower()
        except Exception:
            current = input("Current admin password: ").strip().lower()
        
        if current != cls.password:
            print("The current password is incorrect! Password is not changing")
            return False
        
        try:
            new = getpass.getpass("Enter new password: ").strip().lower()
            confirm = getpass.getpass("Confirm new password: ").strip().lower()
        except Exception:
            new = input("Enter new password: ").strip().lower()
            confirm = input("Confirm new password: ").strip().lower()

        if new == "" or len(new) < 6:
            print("Password was less than 6 characters or empty. Password did not change")
            return False
        if new != confirm:
            print("Passwords did not match! Password did not change.")
            return False
        
        cls.password = new
        print("Password has been updated.")
        return True
    

class Vehicle:
    # Global registry of all vehicles in the current run of the program.
    Vehicles = []
    next_id = 1

    def __init__ (self, vehicle_id, plate_number, vehicle_type, spot_id, entry_time, exit_time, is_active, fee):
        # Basic information and current parking state of one vehicle.
        self.vehicle_id = vehicle_id
        self.plate_number = plate_number
        self.vehicle_type = vehicle_type
        self.spot_id = spot_id
        self.entry_time = entry_time
        self.exit_time = exit_time
        self.is_active = is_active
        self.fee = fee

        # List of all past parking sessions (entry/exit/fee/spot).
        self.history = []
    @classmethod
    def find_by_plate(cls, plate_number):
        # Look up a vehicle in the global list by its plate number.
        for v in cls.Vehicles:
            if v.plate_number == plate_number.upper():
                return v
        return None
    
    @classmethod
    def register (cls):
        # Interactively register a new vehicle and add it to the global list.
        plate_number = input("Enter the plate number: ").strip().upper()
        for v in cls.Vehicles:
            if v.plate_number == plate_number:
                print(f"Vehicle with plate number {plate_number} is already registered as {v.vehicle_id}.")
                return None
            
        vehicle_id = "V" + str(cls.next_id)
        cls.next_id += 1
        types = ["car", "motorcycle", "truck", "bus"]

        print("\nSelect vehicle type:")
        for i, t in enumerate(types, 1):
            print(f"{i}. {t.capitalize()}")

        while True:
            try:
                choice = int(input("Enter the number of the vehicle type: "))
                if 1 <= choice <= len(types):
                    vehicle_type = types[choice - 1]
                    break
                else:
                    print("Invalid choice. Please enter a valid number.")
            except ValueError:
                print("Please enter a number, not text.")
        entry_time = None
        spot_id = None
        exit_time = None
        is_active = False
        fee = 0.0 

        vehicle = cls(vehicle_id, plate_number, vehicle_type, spot_id, entry_time, exit_time, is_active, fee)

        cls.Vehicles.append(vehicle)

        print(f"Vehicle {vehicle_id} with the plate number: {plate_number}, has been registered successfully. ")

        return vehicle
    

class ParkingSpot:
    # Represents one physical parking space in the lot.
    spots = []
    next_id = 1

    def __init__(self, spot_id, is_occupied=False, current_vehicle_id=None, current_vehicle_type=None):
        # Each spot tracks whether it is free and which vehicle (if any) is parked.
        self.spot_id = spot_id
        self.is_occupied = is_occupied
        self.current_vehicle_id = current_vehicle_id
        self.current_vehicle_type =current_vehicle_type
    
    @classmethod
    def create_spots(cls, count):
        # Create N new spots with sequential IDs and store them in the class list.
        for _ in range(count):
            spot_id = "S" + str(cls.next_id)
            cls.next_id += 1 

            spot = cls(spot_id)
            cls.spots.append(spot)

        print(f"{count} parking spots created successfully.")
        return cls.spots
    
class ParkingLot:
    def __init__(self, price):
        # price = cost per hour; total_revenue accumulates all finished parking fees.
        self.price = price
        self.total_revenue = 0.0

    def find_free_spot(self):
        # Return the first free spot or None if all spots are occupied.
        for spot in ParkingSpot.spots:
            if not spot.is_occupied:
                return spot
        return None

    def park_vehicle(self, vehicle: Vehicle, spot: ParkingSpot):
        # Mark vehicle and spot as in-use and set vehicle entry time.
        if spot.is_occupied:
            print(f"Spot {spot.spot_id} is already occupied.")
            return
        spot.is_occupied = True
        spot.current_vehicle_id = vehicle.vehicle_id
        spot.current_vehicle_type = vehicle.vehicle_type

        vehicle.spot_id = spot.spot_id
        vehicle.entry_time = datetime.now()
        vehicle.is_active = True

        print(f"Vehicle {vehicle.vehicle_id} parked in spot {spot.spot_id}.")
    
    def exit_vehicle(self, vehicle: Vehicle):
        # Compute fee based on parked duration and free the spot.
        if not vehicle.is_active:
            print("This vehicle is not currently parked")
            return
        
        spot = None
        for s in ParkingSpot.spots:
            if s.spot_id == vehicle.spot_id:
                spot = s
                break
        
        if spot is None: 
            print("Error! spot not found for this vehicle.")
            return
        
        vehicle.exit_time = datetime.now()
        duration = vehicle.exit_time - vehicle.entry_time
        hours = duration.total_seconds() / 3600
        vehicle.fee = round(hours*self.price, 2)
        vehicle.history.append({
            "entry": vehicle.entry_time,
            "exit": vehicle.exit_time,
            "fee": vehicle.fee,
            "spot_id": vehicle.spot_id,
        })

        vehicle.is_active = False

        spot.is_occupied = False
        spot.current_vehicle_id = None
        spot.current_vehicle_type = None

        vehicle.spot_id = None
        vehicle.entry_time = None

        self.total_revenue += vehicle.fee

        print(f"Vehicle {vehicle.vehicle_id} exited. Fee: ${vehicle.fee}")


class App:
    def __init__(self):
        # Single parking lot instance used by the whole CLI app.
        self.parking_lot = ParkingLot(price=5.0)
        self.is_admin = False

    def run(self):
        # Main menu loop – reads user commands and calls the appropriate actions.
        while True:
            self.is_admin = Admin.is_logged_in

            choices = {
                "1" : "Register a vehicle",
                "2" : "Park a vehicle",
                "3" : "Exit a vehicle",
                "4" : "Show all vehicles",
                "5" : "Show all spots",
                "0" : "Turn the system off",
                "i" : "Info about using the system",
                "s" : "Search for a vehicle by plate number"
            }
            if not self.is_admin:
                choices["a"] = "Admin login"
            else:
                choices["q"] = "Admin logout" 
                choices["6"] = "Change admin password"
                choices["7"] = "View total revenue"
                choices["8"] = "Change price per hour"
                choices["9"] = "Create parking spots"

            print("\n=== Parking System Menu ===")
        
            for i, choice in choices.items():
                print(f"{i} : {choice}")
            
            to_do = input("\nChoice what to do:").strip().lower()
            
            if to_do == "1":
                if not ParkingSpot.spots:
                    print("WARNING! No spots created yet.")
                Vehicle.register()

            elif to_do == "2":
                if not ParkingSpot.spots:
                    print("No spots created yet.")
                    continue
                
                plate = input("Enter plate number to park: ").strip().upper()
                vehicle = Vehicle.find_by_plate(plate)
                if vehicle is None:
                    print("Vehicle not found. Please register it first.")
                    continue
                
                if vehicle.is_active and vehicle.spot_id is not None:
                    print(f"Vehicle {vehicle.vehicle_id} is already parked in spot {vehicle.spot_id}.")
                    continue
                
                spot = self.parking_lot.find_free_spot()
                if spot is None:
                    print("No free spots available.")
                    continue
                
                self.parking_lot.park_vehicle(vehicle, spot)


            elif to_do == "3":
                plate = input("Enter plate number to exit: ").strip().upper()
                vehicle = Vehicle.find_by_plate(plate)
                if vehicle is None:
                    print("Vehicle not found.")
                    continue
                
                self.parking_lot.exit_vehicle(vehicle)



            elif to_do == "4":
                if not Vehicle.Vehicles:
                    print("No vehicles registered yet.")
                else:
                    for v in Vehicle.Vehicles:
                        status = "active" if v.is_active else "inactive"
                        print(f"{v.vehicle_id} | {v.plate_number} | {v.vehicle_type} | {status} | spot={v.spot_id}")

            elif to_do == "5":
                if not ParkingSpot.spots:
                    print("No spots created yet.")
                else:
                    for s in ParkingSpot.spots:
                        status = "occupied" if s.is_occupied else "free"
                        print(f"{s.spot_id} | {status} | vehicle={s.current_vehicle_id}")
            
            elif to_do == "9" and self.is_admin:
                try:
                    count = int(input("How many spots do you want to create? ").strip())
                    ParkingSpot.create_spots(count)
                except ValueError:
                    print("You must enter a valid number of spots.")

            elif to_do == "8" and self.is_admin:
                try:
                    new_price = float(input("Enter new price per hour: ").strip())
                    self.parking_lot.price = new_price
                    print(f"Price per hour updated to {new_price}.")
                except ValueError:
                    print("Invalid price value.")

            elif to_do == "7" and self.is_admin:
                print(f"Total revenue collected so far: ${self.parking_lot.total_revenue:.2f}")

            elif to_do == "6" and self.is_admin:
                Admin.change_password()

            elif to_do == "a":
                if self.is_admin:
                    print("Admin is already logged in.")
                else:
                    Admin.authentication() 
                    self.is_admin = Admin.is_logged_in

            
            elif to_do == "q":
                if not self.is_admin:
                    print("No admin is currently logged in.")
                else:
                    Admin.logout()
                    self.is_admin = False


            elif to_do == "0":
                if not self.is_admin:
                    print("⚠️ Only admin can shut down the system.")
                    continue

                # Collect all vehicles that are still parked before shutdown.
                parked_vehicles = [
                        v for v in Vehicle.Vehicles
                        if v.is_active and v.spot_id is not None
                    ]

                # If no vehicles are parked, just turn off immediately.
                if not parked_vehicles:
                    print("Turning the system off... Goodbye!")
                    break
                    
                # Show all parked vehicles so the admin knows what is still inside.
                print("\n⚠️ There are still vehicles parked:")
                for v in parked_vehicles:
                    print(f"- {v.vehicle_id} | {v.plate_number} | spot={v.spot_id}")

                # Ask admin what to do with the remaining vehicles.
                print("\nWhat do you want to do before shutting down?")
                print("1 - Exit ALL vehicles one by one and show each fee, then show total for the day and turn off")
                print("2 - Confirm shutdown anyway (keep all vehicles as parked)")
                print("3 - Mark ALL vehicles as exited and only show the total amount, then turn off")

                choice = input("Enter your choice (1/2/3): ").strip()

                if choice == "1":
                    # Exit each vehicle using normal logic (will print fee for each).
                    for v in parked_vehicles:
                        self.parking_lot.exit_vehicle(v)

                    print(f"\nTotal revenue collected so far today: ${self.parking_lot.total_revenue:.2f}")
                    print("Turning the system off... Goodbye!")
                    break
                    
                elif choice == "2":
                    confirm = input("Are you SURE you want to shut down with vehicles still parked? (y/n): ").strip().lower()
                    if confirm == "y":
                        print("Shutting down WITHOUT exiting vehicles. Goodbye!")
                        break
                    else:
                        print("Shutdown cancelled. Returning to menu.")
                        continue
                        
                elif choice == "3":
                    # Here we close all vehicles silently, then only show totals.
                    total_before = self.parking_lot.total_revenue

                    for v in parked_vehicles:
                        v.exit_time = datetime.now()
                        duration = v.exit_time - v.entry_time
                        hours = duration.total_seconds() / 3600
                        v.fee = round(hours * self.parking_lot.price, 2)

                        v.history.append({
                            "entry": v.entry_time,
                            "exit": v.exit_time,
                            "fee": v.fee,
                            "spot_id": v.spot_id,
                        })

                        v.is_active = False

                        for s in ParkingSpot.spots:
                            if s.spot_id == v.spot_id:
                                s.is_occupied = False
                                s.current_vehicle_id = None
                                s.current_vehicle_type = None
                                break
                            
                        v.spot_id = None
                        v.entry_time = None

                        self.parking_lot.total_revenue += v.fee


                    earned_now = self.parking_lot.total_revenue - total_before

                    print("\nAll vehicles have been marked as exited.")
                    print(f"Total from these vehicles: ${earned_now:.2f}")
                    print(f"Total revenue collected so far today: ${self.parking_lot.total_revenue:.2f}")
                    print("Turning the system off... Goodbye!")
                    break
                    
                else:
                    print("Invalid shutdown option. Returning to main menu.")
                    continue

            elif to_do == "s":
                plate = input("Enter the plate number to search: ").strip().upper()
                vehicle = Vehicle.find_by_plate(plate)
    
                if vehicle is None:
                    print(f"No vehicle found with plate number {plate}.")
                else:
                    print("\n=== Vehicle Information ===")
                    print(f"ID: {vehicle.vehicle_id}")
                    print(f"Plate: {vehicle.plate_number}")
                    print(f"Type: {vehicle.vehicle_type.capitalize()}")
                    if vehicle.is_active:
                        status = "Active (Parked)"
                    else:
                        if vehicle.entry_time is None and vehicle.exit_time is None:
                            status = "Not parked yet"
                        elif vehicle.entry_time and vehicle.exit_time:
                            status = "Inactive (Exited)"
                        else:
                            status = "Inactive"
                    print(f"Status: {status}")

                    print(f"Spot ID: {vehicle.spot_id}")
        
                    if vehicle.entry_time:
                        print(f"Entry time: {vehicle.entry_time.strftime('%Y-%m-%d %H:%M:%S')}")
                    if vehicle.exit_time:
                        print(f"Exit time: {vehicle.exit_time.strftime('%Y-%m-%d %H:%M:%S')}")
                        print(f"Last fee paid: ${vehicle.fee:.2f}")
                    print("============================")
                    
                    if vehicle.history:
                        print("\n--- Parking History ---")
                        for i, session in enumerate(vehicle.history, 1):
                            print(f"Session {i}:")
                            print(f"  Entry: {session['entry'].strftime('%Y-%m-%d %H:%M:%S')}")
                            print(f"  Exit : {session['exit'].strftime('%Y-%m-%d %H:%M:%S')}")
                            print(f"  Spot : {session['spot_id']}")
                            print(f"  Fee  : ${session['fee']:.2f}")
                    else:
                        print("\nNo previous parking history for this vehicle yet.")

            elif to_do == "i":
                print("\nInfo:")
                print("- Admin can create spots with option 9 (if logged in).")
                print("- Register a vehicle with 1, then park with 2.")
                print("- Use plate numbers to park/exit vehicles.")

            else:
                print("Invalid choice or you don't have permission for that option.")




if __name__ == "__main__":
    app = App()
    app.run()