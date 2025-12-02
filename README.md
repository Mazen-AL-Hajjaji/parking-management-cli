**Parking Management System (CLI)**

---

### Overview

The **Parking Management System (CLI)** is a small Python console app that helps you manage a simple parking lot from your terminal.  
You can register vehicles, assign them to parking spots, track when they enter and exit, and automatically calculate how much each driver should pay – all from a clean text-based interface.  
There’s also an admin mode for the more sensitive actions, like creating spots, changing the hourly price, checking total revenue, and shutting the system down safely.

> This project is ideal for practicing object-oriented design, console I/O, and basic state management in Python.

---

### Features

- **Vehicle management**
  - Register vehicles with plate number and type (car, motorcycle, truck, bus).
  - Look up vehicles by plate number.
  - See whether a vehicle is currently parked and view its full parking history.

- **Parking management**
  - Create parking spots (admin only).
  - Automatically assign the first free spot when parking a vehicle.
  - Exit vehicles and free their spots using only the plate number.
  - List all vehicles and all spots with their current status.

- **Pricing & revenue**
  - Configurable **price per hour** (admin only).
  - Fee is calculated based on the time between entry and exit.
  - Total revenue for the current run of the program is tracked.

- **Admin mode**
  - Password-protected login (`admin123` by default).
  - Change admin password from inside the app.
  - Admin-only actions: create spots, change price, view revenue, shut down.

- **Safe shutdown**
  - Only admin is allowed to shut the system down.
  - If vehicles are still parked, the admin can:
    - Exit all vehicles one by one and see each fee.
    - Shut down anyway and leave vehicles as “still parked”.
    - Mark all vehicles as exited in one go and only show totals.

---

### Folder structure

This is how the repository is organized on GitHub:

```text
parking-management-cli/
├── parking_management_system.py   # Main CLI application (logic + menu)
├── README.md                      # Project documentation
├── LICENSE                        # MIT license
└── .gitignore                     # Git ignore rules
```

---

### Requirements

- **Python** 3.8 or higher (recommended)

The app only uses the Python standard library:

- `datetime` for time and duration calculations.
- `getpass` for password input where the characters are not shown.

---

### Installation & running

1. **Clone the repository**:

   ```bash
   git clone https://github.com/Mazen-AL-Hajjaji/parking-management-cli.git
   cd parking-management-cli
   ```

2. **(Optional) Create and activate a virtual environment**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # On Windows
   # source .venv/bin/activate  # On macOS/Linux
   ```

3. **Run the application**:

   ```bash
   python parking_management_system.py
   ```

You should now see the text menu in your terminal.

---

### Usage example

When you start the program, you’ll be greeted with a menu similar to this:

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

A typical flow might look like this:

1. Log in as admin (`a`) and enter the password (`admin123` by default).
2. Create some spots (`9`) so cars have somewhere to park.
3. Register a vehicle (`1`) with its plate number and type.
4. Park the vehicle (`2`) by entering its plate; the app picks a free spot.
5. Later, exit the vehicle (`3`) and see the calculated fee.

---

### Admin options

When you are logged in as admin, you unlock a few extra options:

- **Login / logout**
  - `a` – Log in as admin (3 attempts, or press Enter to skip).
  - `q` – Log out and return to normal user mode.

- **Security**
  - `6` – Change the admin password (asks for current password and confirmation).

- **Money & pricing**
  - `7` – Show the total revenue collected so far in this session.
  - `8` – Change the price per hour for new parking sessions.

- **Parking spots & shutdown**
  - `9` – Create new parking spots (they are given IDs like `S1`, `S2`, ...).
  - `0` – Shut down the system, with special handling if vehicles are still parked.

---

### Demo / screenshots

You can add a terminal screenshot or GIF of the app in action here.
For example, if you place an image at `docs/demo.png` in this repository, this line will show it on GitHub:

```markdown
![Parking Management System Demo](docs/demo.png)
```

---

### Notes & limitations

- **Data is not persisted** – everything lives in memory only. Once you close the program, vehicles, spots, history, and revenue are reset.
- **Single lot only** – the current design manages one parking lot with a single price per hour.
- **Simple security** – the admin password is stored in plain text and is meant for demos and learning, not production use.

---

### Future improvements

Some ideas for taking this project further:

- **Persist data** to JSON, CSV, or a database (e.g. SQLite) so information survives restarts.
- **Improve security** by hashing/salting passwords and adding richer roles.
- **Build a nicer interface**, either with a desktop GUI (Tkinter / PyQt) or a small web app (Flask / FastAPI).
- **Add advanced parking features** such as multiple zones with different prices, reservations, discounts, or daily PDF/CSV reports.

---

### License

This project is licensed under the **MIT License** – see the [`LICENSE`](./LICENSE) file for details.

---

### Author

**Developed by [Mazen AL Hajjaji](https://github.com/Mazen-AL-Hajjaji)**  

GitHub: [`@Mazen-AL-Hajjaji`](https://github.com/Mazen-AL-Hajjaji)

If you find this project helpful, feel free to ⭐ star the repository or fork it and build your own version.

