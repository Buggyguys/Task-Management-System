# Task Management System

This is a Python-based Task Management System that lets you:
- Create and manage users, projects, and tasks.
- Assign users to projects and tasks.
- Edit and delete users, projects, or tasks.
- Automatically handle tasks becoming "idle" if their associated user or project is deleted.

---

## How It Works
1. Run the program:
   ```bash
   python3 main.py
   ```
2. Use the menu to manage users, projects, and tasks. Each menu option guides you through the steps.
3. Data is automatically saved and loaded from `data.json`, so you don’t lose progress.

## File Structure
- [`main.py`](main.py): Runs the program and handles the menu.
- [`functions.py`](functions.py): All the main logic (create, edit, delete, etc.).
- [`user.py`](user.py), [`project.py`](project.py), and [`task.py`](task.py): defining classes.
- `data.json`: Stores all the data persistently.
