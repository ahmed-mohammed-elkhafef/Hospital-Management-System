from core.SystemManager import SystemManager
import sys

# --- Auth Data ---
USERS = {
    "admin": "admin123",
    "user": "123456"
}

def login_system():
    """
    Handles user authentication with a limited number of attempts.
    Returns:
        str: The role of the logged-in user ('admin' or 'user').
    """
    print("\n🔒 --- Group 2 System Login --- 🔒")
    attempts = 3
    while attempts > 0:
        username = input("Username: ")
        password = input("Password: ")
        if username in USERS and USERS[username] == password:
            print(f"Login Successful! Welcome, {username}.")
            return "admin" if username == "admin" else "user"
        else:
            attempts -= 1
            print(f"Invalid credentials. Attempts left: {attempts}")
    print("Too many failed attempts. Exiting...")
    sys.exit()

def get_input(prompt, required_type=str):
    """
    Ensures the user provides a non-empty input of the correct data type.
    """
    while True:
        value = input(prompt)
        if not value:
            print("Input cannot be empty.")
            continue
        try:
            return required_type(value)
        except ValueError:
            print(f"Invalid input. Please enter a valid {required_type.__name__}.")

def select_department_menu(manager):
    """
    Displays a dynamic menu of existing departments and forces selection by number.
    This prevents spelling errors during data entry.
    """
    depts = manager.hospital.departments
    if not depts:
        print("⚠️ No departments found! Please add a department first (Option 7).")
        return None

    print("\n--- Select Department ---")
    for i, dept in enumerate(depts, 1):
        print(f"{i}. {dept.name} ({len(dept.patients)} Patients)")
    
    while True:
        choice = input("Enter Department Number (or '0' to cancel): ")
        if choice == '0': return None
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(depts):
                return depts[idx].name
            print("Invalid number. Choose from the list.")
        except ValueError:
            print("Please enter a valid number.")

def main():
    """
    The main entry point of the application. 
    Controls the flow between user input and the SystemManager backend.
    """
    # Initialize the system (This will create the 'database' folder automatically)
    manager = SystemManager()
    role = login_system()

    while True:
        print(f"\n🏥 --- {manager.hospital.name} Dashboard [{role.upper()}] --- 🏥")
        print("1. Add Patient          | 2. Add Staff")
        print("3. View Patient Record  | 4. Search Person (Name)")
        
        if role == "admin":
            print("---------------- ADMIN ONLY ----------------")
            print("5. Remove Patient       | 6. Remove Staff")
            print("7. Add Department       | 8. Remove Department")
            print("9. System Settings")
        
        print("0. Exit")
        print("--------------------------------------------")
        
        choice = input("Select Option: ")

        # --- Public & Admin Actions ---
        if choice == '1':
            d_name = select_department_menu(manager)
            if d_name:
                p_name = input("Patient Name: ")
                p_age = get_input("Age: ", int)
                p_rec = input("Medical Record: ")
                print(manager.add_patient(d_name, p_name, p_age, p_rec))

        elif choice == '2':
            d_name = select_department_menu(manager)
            if d_name:
                s_name = input("Staff Name: ")
                s_age = get_input("Age: ", int)
                s_pos = input("Position: ")
                print(manager.add_staff(d_name, s_name, s_age, s_pos))

        elif choice == '3':
            d_name = select_department_menu(manager)
            if d_name:
                p_id = input("Patient ID: ")
                print(manager.view_patient_record(d_name, p_id))

        elif choice == '4':
            name = input("Enter Name to Search: ")
            print(manager.search_person_by_name(name))

        elif choice == '0':
            print("Saving data to 'database' folder... Goodbye!")
            manager.save_data()
            break

        # --- Admin Specific Actions ---
        elif role == "admin":
            if choice == '5':
                d_name = select_department_menu(manager)
                if d_name:
                    p_id = input("Patient ID: ")
                    print(manager.remove_patient(d_name, p_id))

            elif choice == '7':
                d_name = input("Enter New Department Name: ")
                print(manager.add_department(d_name))

            elif choice == '8':
                d_name = select_department_menu(manager)
                if d_name:
                    confirm = input(f"Are you sure you want to delete '{d_name}'? (y/n): ")
                    if confirm.lower() == 'y':
                        print(manager.remove_department(d_name))
            
            elif choice == '9':
                manager.hospital.name = input("Enter New Hospital Name: ")
                manager.save_data()
                print("Hospital name updated successfully.")
        
        else:
            if choice in ['5', '6', '7', '8', '9']:
                print("⛔ Access Denied: Admin privileges required.")
            else:
                print("Invalid Choice.")

if __name__ == "__main__":
    main()