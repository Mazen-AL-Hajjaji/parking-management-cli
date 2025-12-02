**Parking Management System (CLI)**

---

### Overview

The **Parking Management System (CLI)** is a Python-based console application for managing a simple parking lot.  
It allows you to register vehicles, assign them to parking spots, track entry and exit times, and calculate parking fees, all from a clean text-based interface.  
An admin mode enables privileged operations such as creating spots, changing pricing, viewing total revenue, and safely shutting down the system.

> This project is ideal for learning object-oriented design, console I/O, and basic state management in Python.

---

### Features

- **Vehicle Management**
  - Register vehicles with plate number and type (car, motorcycle, truck, bus).
  - Search vehicles by plate number.
  - View current status (parked / not parked) and full parking history.

- **Parking Management**
  - Create parking spots (admin-only).
  - Automatically assign the first available spot.
  - Park and exit vehicles using their plate numbers.
  - List all vehicles and all parking spots with live status.

- **Pricing & Revenue**
  - Configurable **price per hour** (admin-only).
  - Automatic fee calculation based on time parked.
  - Track **total revenue** for the current session.

- **Admin Mode**
  - Password-protected admin login (`admin123` by default).
  - Change admin password.
  - Admin-only operations: create spots, change pricing, view revenue, controlled shutdown.

- **Safe Shutdown**
  - Only admin can shut down the system.
  - If vehicles are still parked, admin can:
    1. Exit all vehicles normally (show each fee + total, then shut down).
    2. Force shutdown and keep vehicles marked as parked.
    3. Mark all vehicles as exited silently and only show totals.

---

### Folder Structure

```text
parking_management_system/
└── parking_system/
    ├── parking_system.py   # Main CLI application (core logic & menu)
    └── README.md           # Project documentation
```

---

### Requirements

- **Python**: 3.8 or higher (recommended)

Standard library only – no external dependencies are required:

- `datetime` – for time and duration calculations.
- `getpass` – for secure admin password input (hidden typing where supported).

---

### Installation & Running

1. **Clone or download** the project:

   ```bash
   git clone https://github.com/your-username/parking-management-cli.git
   cd parking_management_system/parking_system
   ```

   > Replace `your-username` and the path above with your actual repository or folder path.

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. **Run the application**:

   ```bash
   python parking_system.py
   ```

---

### Usage Example

Once you run the script, you will see a main menu similar to:

```text
=== Parking System Menu ===
1 : Register a vehicle
2 : Park a vehicle
3 : Exit a vehicle
4 : Show all vehicles
5 : Show all spots
0 : Turn the system off
i : Info about using the system
s : Search for a vehicle by plate number
a : Admin login        (if not logged in)
q : Admin logout       (if logged in)
6 : Change admin password   (admin only)
7 : View total revenue      (admin only)
8 : Change price per hour   (admin only)
9 : Create parking spots    (admin only)
```

#### Typical Workflow

```text
1. (Admin) Log in:
   - Choose "a" and enter the admin password (default: admin123).

2. (Admin) Create parking spots:
   - Choose "9" and enter how many spots you want (e.g. 10).

3. Register a vehicle:
   - Choose "1", enter the plate number, and select the vehicle type.

4. Park the vehicle:
   - Choose "2", enter the vehicle plate, and the system assigns a free spot.

5. Exit the vehicle:
   - Choose "3", enter the plate again, and the system calculates & displays the fee.
```

---

### Admin Options

When logged in as **admin**, you gain access to several protected features:

- **Admin Login (`a`)**
  - Authenticate with a password (default: `admin123`).
  - Up to 3 attempts; you can also skip and continue as a normal user.

- **Change Admin Password (`6`)**
  - Requires current password.
  - Enforces a minimal length and confirmation.

- **View Total Revenue (`7`)**
  - Displays all fees collected for the current program run.

- **Change Price per Hour (`8`)**
  - Update the hourly parking rate (affects new exits).

- **Create Parking Spots (`9`)**
  - Add new spots with auto-generated `S1`, `S2`, ... IDs.

- **Controlled Shutdown (`0`)**
  - Only available to admin.
  - If vehicles are parked, choose how to handle them:
    - Exit them one by one using normal logic (show each fee).
    - Force shutdown without exiting them.
    - Mark all as exited silently and show summary totals.

---

### Demo / Screenshots

> _Placeholder_: Add a screenshot or GIF of your terminal running the app here.

```markdown
![Parking Management System Demo](docs/demo.png)
```

You can capture a screenshot of the menu and basic workflow, save it under `docs/demo.png`, and the image above will display on GitHub.

---

### Notes & Limitations

- **In-memory data only**
  - All data (vehicles, spots, history, revenue, admin password changes) lives only while the program is running.
  - Closing the application clears all data.

- **Single parking lot**
  - The current design manages one parking lot with a single price-per-hour setting.

- **Security**
  - Admin password is stored as plain text in memory.
  - Suitable for learning and demos, but not for production use.

---

### Future Improvements

- **Persistent Storage**
  - Save vehicles, spots, history, and revenue to **JSON**, **CSV**, or **SQLite** so data survives restarts.

- **Better Security**
  - Hash & salt admin passwords.
  - Add different admin/user roles with separate capabilities.

- **Richer Interface**
  - Add a **GUI** using Tkinter or PyQt.
  - Build a **web interface** using Flask or FastAPI.

- **Advanced Features**
  - Support multiple lots or zones with different pricing.
  - Add reservations, discount codes, or monthly subscriptions.
  - Export daily reports (e.g., to CSV).

---

### License

This project is licensed under the **MIT License** – see the [`LICENSE`](./LICENSE) file for details.

---

### Author

**Developed by [Mazen AL Hajjaji](https://github.com/Mazen-AL-Hajjaji)**  

GitHub: [`@Mazen-AL-Hajjaji`](https://github.com/Mazen-AL-Hajjaji)

If you find this project useful, feel free to ⭐ star the repository or fork it for your own experiments and improvements.


