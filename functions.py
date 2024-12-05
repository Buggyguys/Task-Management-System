import re
import json
from user import User
from project import Project
from task import Task
from project import Project
from datetime import datetime 

#SAVE and LOAD functions ----------------------------------------------------- 
def load_data(filename="data.json"):
    try:
        with open(filename, "r") as file:
            data = json.load(file)
            users = [User.from_dict(u) for u in data.get("users", [])]
            projects = [Project.from_dict(p) for p in data.get("projects", [])]
            tasks = [Task.from_dict(t) for t in data.get("tasks", [])]
            return users, projects, tasks
    except FileNotFoundError:
        return [], [], []

def save_data(users, projects, tasks, filename="data.json"):
    with open(filename, "w") as file:
        json.dump({
            "users": [user.to_dict() for user in users],
            "projects": [project.to_dict() for project in projects],
            "tasks": [task.to_dict() for task in tasks]
        }, file, indent=4)
    print("Data saved successfully.")

#USER functions --------------------------------------------------------------


def get_by_id(items, item_id, id_field):
    for item in items:
        if getattr(item, id_field) == item_id:
            return item
    return None

def validate_name(name):
    return bool(re.match(r"^[A-Z][a-z]+$", name))

def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email))

def create_user(users, projects, tasks):
    first_name = input("Enter first name: ").strip()
    while not validate_name(first_name):
        print("Invalid name. Please use only letters and start with an uppercase.")
        first_name = input("Enter first name: ").strip()

    last_name = input("Enter last name: ").strip()
    while not validate_name(last_name):
        print("Invalid name. Please use only letters and start with an uppercase.")
        last_name = input("Enter last name: ").strip()

    email = input("Enter email: ").strip()
    while not validate_email(email):
        print("Invalid email format. Please use a valid email (e.g., example@domain.com).")
        email = input("Enter email: ").strip()

    uid = len(users) + 1
    new_user = User(uid, first_name, last_name, email)
    users.append(new_user)
    save_data(users, projects, tasks)
    print(f"User '{first_name} {last_name}' created successfully!")


def list_users(users):
    if not users:
        print("No users available.")
    else:
        print("\nUSERS -------------------------------------------------------")
        for user in users:
            print(f"User ID: {user.uid}, Name: {user.first_name} {user.last_name}, Email: {user.email}")
        print("\n-------------------------------------------------------------")
    input("\nPress any key to return to the menu...")

def edit_user(users, projects, tasks):
    if not users:
        print("No users available.")
        return

    print("\nUsers:")
    for user in users:
        print(f"User ID: {user.uid}, Name: {user.first_name} {user.last_name}, Email: {user.email}")
    
    user_id = input("Enter the ID of the user to edit: ").strip()
    user = get_by_id(users, int(user_id), "uid")
    if not user:
        print("Invalid user ID.")
        return

    print(f"Editing User: {user.first_name} {user.last_name}")

    new_first_name = input(f"Enter new first name (or press Enter to keep '{user.first_name}'): ").strip()
    new_last_name = input(f"Enter new last name (or press Enter to keep '{user.last_name}'): ").strip()
    new_email = input(f"Enter new email (or press Enter to keep '{user.email}'): ").strip()

    if new_first_name:
        if validate_name(new_first_name):
            user.first_name = new_first_name
        else:
            print("Invalid first name. Changes not applied.")
    if new_last_name:
        if validate_name(new_last_name):
            user.last_name = new_last_name
        else:
            print("Invalid last name. Changes not applied.")
    if new_email:
        if validate_email(new_email):
            user.email = new_email
        else:
            print("Invalid email format. Changes not applied.")

    save_data(users, projects, tasks)
    print(f"User '{user.first_name} {user.last_name}' updated successfully!")

def delete_user(users, projects, tasks):
    if not users:
        print("No users available to delete.")
        return

    print("\nUsers:")
    for user in users:
        print(f"User ID: {user.uid}, Name: {user.first_name} {user.last_name}, Email: {user.email}")
    
    user_id = input("Enter the ID of the user to delete: ").strip()
    user = get_by_id(users, int(user_id), "uid")
    if not user:
        print("Invalid user ID.")
        return

    users.remove(user)
    print(f"User '{user.first_name} {user.last_name}' deleted successfully.")

    for project in projects:
        if user.uid in project.assigned_users:
            project.assigned_users.remove(user.uid)

    for task in tasks:
        if task.user_id == user.uid:
            task.user_id = None

    save_data(users, projects, tasks)
    print("Data updated successfully.")

#PROJECT functions -----------------------------------------------------------

def create_project(users, projects, tasks):
    name = input("Enter project name: ").strip()
    description = input("Enter project description: ").strip()
    deadline = input("Enter deadline (YYYY-MM-DD): ").strip()

    while not validate_date(deadline):
        print("Invalid date format or date is in the past.")
        deadline = input("Enter deadline (YYYY-MM-DD): ").strip()

    pid = len(projects) + 1
    new_project = Project(pid, name, description, deadline)
    projects.append(new_project)

    save_data(users, projects, tasks)
    print(f"Project '{name}' created successfully!")

def assign_project(users, projects, tasks):
    if not projects:
        print("No projects available to assign users.")
        return

    if not users:
        print("No users available to assign to projects.")
        return

    print("\nProjects:")
    for project in projects:
        print(f"Project ID: {project.pid}, Name: {project.name}")

    project_id = input("Enter the ID of the project to assign users: ").strip()
    project = get_by_id(projects, int(project_id), "pid")
    if not project:
        print("Invalid project ID.")
        return

    print("\nUsers:")
    for user in users:
        print(f"User ID: {user.uid}, Name: {user.first_name} {user.last_name}")

    user_ids = input("Enter the IDs of users to assign (comma-separated): ").strip()
    user_ids = user_ids.split(",")
    for user_id in user_ids:
        user_id = user_id.strip()
        user = get_by_id(users, int(user_id), "uid")
        if user and user.uid not in project.assigned_users:
            project.assigned_users.append(user.uid)

    save_data(users, projects, tasks)
    print(f"Users assigned to project '{project.name}' successfully!")

def list_projects(data, projects):
    active_projects = []
    idle_projects = []

    for project in projects:
        if any(uid in [user.uid for user in data] for uid in project.assigned_users):
            active_projects.append(project)
        else:
            idle_projects.append(project)

    print("\nACTIVE PROJECTS -------------------------------------------------")
    for project in active_projects:
        assigned_user_names = [
            f"{user.first_name} {user.last_name}"
            for user in data
            if user.uid in project.assigned_users
        ]
        print(f"ID: {project.pid}, Name: {project.name}, Users: {', '.join(assigned_user_names)}")

    print("\nIDLE PROJECTS ---------------------------------------------------")
    for project in idle_projects:
        print(f"ID: {project.pid}, Name: {project.name}, No users assigned")

    input("\nPress any key to continue...")

def validate_date(date_str):
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        return date >= datetime.now()
    except ValueError:
        return False

def edit_project(users, projects, tasks):
    if not projects:
        print("No projects available.")
        return

    print("\nProjects:")
    for project in projects:
        print(f"Project ID: {project.pid}, Name: {project.name}")

    project_id = input("Enter the ID of the project to edit: ").strip()
    project = get_by_id(projects, int(project_id), "pid")
    if not project:
        print("Invalid project ID.")
        return

    print(f"Editing Project: {project.name}")
    new_name = input(f"Enter new project name (or press Enter to keep '{project.name}'): ").strip()
    new_description = input(f"Enter new description (or press Enter to keep '{project.description}'): ").strip()
    new_deadline = input(f"Enter new deadline (YYYY-MM-DD) (or press Enter to keep '{project.deadline}'): ").strip()

    if new_name:
        project.name = new_name
    if new_description:
        project.description = new_description
    if new_deadline:
        if validate_date(new_deadline):
            project.deadline = new_deadline
        else:
            print("Invalid deadline. Changes not applied.")

    save_data(users, projects, tasks)
    print(f"Project '{project.name}' updated successfully!")

def delete_project(users, projects, tasks):
    if not projects:
        print("No projects available to delete.")
        return

    print("\nProjects:")
    for project in projects:
        print(f"Project ID: {project.pid}, Name: {project.name}")

    project_id = input("Enter the ID of the project to delete: ").strip()
    project = get_by_id(projects, int(project_id), "pid")
    if not project:
        print("Invalid project ID.")
        return

    projects.remove(project)

    # Remove all tasks associated with the project
    tasks[:] = [task for task in tasks if task.project_id != project.pid]

    save_data(users, projects, tasks)
    print(f"Project '{project.name}' deleted successfully!")

#TASK functions --------------------------------------------------------------
def create_task(data, projects, tasks):
    if not projects:
        print("No projects available. Create a project first.")
        return
    
    print("Select a project:")
    for project in projects:
        print(f"ID: {project.pid}, Name: {project.name}")
    
    project_id = int(input("Enter project ID: "))
    project = get_by_id(projects, project_id, "pid")
    if not project:
        print("Invalid project ID.")
        return

    print("Select a user or leave it idle:")
    assigned_users = [
        user for user in data if user.uid in project.assigned_users
    ]
    if not assigned_users:
        print("No users assigned to this project.")
    else:
        for user in assigned_users:
            print(f"ID: {user.uid}, Name: {user.first_name} {user.last_name}")
    
    user_id = input("Enter user ID (or leave empty for idle): ").strip()
    user = get_by_id(data, int(user_id), "uid") if user_id else None

    tid = len(tasks) + 1
    name = input("Enter task name: ")
    description = input("Enter task description: ")
    priority = input("Enter task priority (LOW, MEDIUM, HIGH): ").upper()
    while priority not in ["LOW", "MEDIUM", "HIGH"]:
        print("Invalid priority. Choose LOW, MEDIUM, or HIGH.")
        priority = input("Enter task priority: ").upper()
    status = input("Enter task status (NOT_STARTED, IN_PROGRESS, COMPLETED): ").upper()
    while status not in ["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]:
        print("Invalid status. Choose NOT_STARTED, IN_PROGRESS, or COMPLETED.")
        status = input("Enter task status: ").upper()

    task = Task(tid, name, description, priority, status, project_id, user.uid if user else None)
    tasks.append(task)
    save_data(data, projects, tasks)
    print(f"Task '{name}' created successfully! ID: {tid}")

def list_tasks(data, projects, tasks):
    if not tasks:
        print("No tasks available.")
        return

    print("\nTasks by Project:")
    for project in projects:
        project_tasks = [task for task in tasks if task.project_id == project.pid]
        if project_tasks:
            print(f"\nProject ID: {project.pid}, Name: {project.name} ------------------------------")
            for task in project_tasks:
                user = get_by_id(data, task.user_id, "uid")
                user_info = f"User ID: {user.uid}, Name: {user.first_name} {user.last_name}" if user else "Idle"
                print(
                    f"Task ID: {task.tid}, Name: {task.name}, Priority: {task.priority}, "
                    f"Status: {task.status}, {user_info}"
                )
    
    idle_tasks = [task for task in tasks if not task.user_id]
    if idle_tasks:
        print("\nIDLE TASKS -------------------------------------------------")
        for task in idle_tasks:
            print(f"Task ID: {task.tid}, Name: {task.name}, Priority: {task.priority}, Status: {task.status}")

    input("\nPress any key to continue...")

def edit_task(data, projects, tasks):
    if not tasks:
        print("No tasks available.")
        return
    
    print("\nTASKS -----------------------------------------------------")
    for task in tasks:
        print(f"ID: {task.tid}, Name: {task.name}")
    
    task_id = int(input("Enter task ID to edit: "))
    task = get_by_id(tasks, task_id, "tid")
    if not task:
        print("Invalid task ID.")
        return
    
    print(f"Editing Task: {task.name}")
    new_name = input(f"Enter new name (or press Enter to keep '{task.name}'): ").strip()
    new_description = input(f"Enter new description (or press Enter to keep '{task.description}'): ").strip()
    new_priority = input(f"Enter new priority (LOW, MEDIUM, HIGH) (or press Enter to keep '{task.priority}'): ").upper()
    new_status = input(f"Enter new status (NOT_STARTED, IN_PROGRESS, COMPLETED) (or press Enter to keep '{task.status}'): ").upper()
    
    print("Reassign user (or leave idle):")
    for user in data:
        print(f"User ID: {user.uid}, Name: {user.first_name} {user.last_name}")
    
    user_id = input("Enter new user ID (or press Enter to leave idle): ").strip()
    if user_id:
        user = get_by_id(data, int(user_id), "uid")
        if user:
            task.user_id = user.uid
            print(f"Task reassigned to {user.first_name} {user.last_name}.")
        else:
            print("Invalid user ID. Keeping task idle.")
            task.user_id = None
    else:
        task.user_id = None
        print("Task set to idle.")

    if new_name:
        task.name = new_name
    if new_description:
        task.description = new_description
    if new_priority in ["LOW", "MEDIUM", "HIGH"]:
        task.priority = new_priority
    if new_status in ["NOT_STARTED", "IN_PROGRESS", "COMPLETED"]:
        task.status = new_status

    save_data(data, projects, tasks)
    print(f"Task '{task.name}' updated successfully!")

def delete_task(data, projects, tasks):
    if not tasks:
        print("No tasks available.")
        return

    print("\nTASKS -----------------------------------------------")
    for task in tasks:
        print(f"ID: {task.tid}, Name: {task.name}")
    
    task_id = int(input("Enter task ID to delete: "))
    task = get_by_id(tasks, task_id, "tid")
    if task:
        tasks.remove(task)
        save_data(data, projects, tasks)
        print(f"Task ID {task_id} deleted successfully.")
    else:
        print("Invalid task ID.")
