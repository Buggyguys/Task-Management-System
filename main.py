from functions import (
    load_data,
    save_data,
    create_user,
    list_users,
    edit_user,
    delete_user,
    create_project,
    assign_project,
    list_projects,
    edit_project,
    delete_project,
    create_task,
    list_tasks,
    edit_task,
    delete_task,
)


def main_menu(users, projects, tasks):
    while True:
        print("\nTask Management System")
        print("1. Create user")
        print("2. List users")
        print("3. Edit user")
        print("4. Delete user")
        print("5. Create project")
        print("6. Assign users to project")
        print("7. List projects")
        print("8. Edit project")
        print("9. Delete project")
        print("10. Create task")
        print("11. List tasks")
        print("12. Edit task")
        print("13. Delete task")
        print("14. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            create_user(users, projects, tasks)
        elif choice == "2":
            list_users(users)
        elif choice == "3":
            edit_user(users, projects, tasks)
        elif choice == "4":
            delete_user(users, projects, tasks)
        elif choice == "5":
            create_project(users, projects, tasks)
        elif choice == "6":
            assign_project(users, projects, tasks)
        elif choice == "7":
            list_projects(users, projects)
        elif choice == "8":
            edit_project(users, projects, tasks)
        elif choice == "9":
            delete_project(users, projects, tasks)
        elif choice == "10":
            create_task(users, projects, tasks)
        elif choice == "11":
            list_tasks(users, projects, tasks)
        elif choice == "12":
            edit_task(users, projects, tasks)
        elif choice == "13":
            delete_task(users, projects, tasks)
        elif choice == "14":
            save_data(users, projects, tasks)
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    users, projects, tasks = load_data()
    main_menu(users, projects, tasks)
