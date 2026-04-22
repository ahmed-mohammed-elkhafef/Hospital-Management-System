import json
import datetime
import os
from model.Hospital import Hospital
from model.Department import Department
from model.Patient import Patient
from model.Staff import Staff

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATA_DIR = os.path.join(BASE_DIR, "database")
DATA_FILE = os.path.join(DATA_DIR, "hospital_data.json")
LOG_FILE = os.path.join(DATA_DIR, "activity_log.txt")

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

class SystemManager:
    """
    The central controller for the hospital management system.
    Handles persistence, logging, and core hospital operations.
    """

    def __init__(self):
        self.hospital = None
        self._ensure_data_dir()
        self.load_data()

    def _ensure_data_dir(self):
        """Creates the data directory if it does not already exist."""
        if not os.path.exists(DATA_DIR):
            os.makedirs(DATA_DIR)

    def save_data(self):
        """Saves current hospital state to JSON."""
        try:
            with open(DATA_FILE, 'w', encoding="utf-8") as f:
                json.dump(self.hospital.to_dict(), f, indent=4)
        except Exception as e:
            print(f"Error saving data: {e}")

    def load_data(self):
        """Loads data or initializes new hospital."""
        try:
            with open(DATA_FILE, 'r', encoding="utf-8") as f:
                data = json.load(f)
                self.hospital = Hospital.from_dict(data)
                self._log("System started - Data Loaded")
        except (FileNotFoundError, json.JSONDecodeError):
            self.hospital = Hospital("Group 2", "Main Campus")
            self._setup_defaults()
            self._log("System started - New Setup Created")

    def _log(self, message):
        """Logs timestamped activity."""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"[{timestamp}] {message}\n")

    def _setup_defaults(self):
        """Sets up default departments."""
        defaults = ["Emergency", "ICU", "Surgery"]
        for name in defaults:
            self.hospital.add_department(Department(name))
        self.save_data()

    def _get_dept(self, dept_name):
        """Helper to find a department object."""
        for d in self.hospital.departments:
            if d.name == dept_name:
                return d
        return None

    def add_department(self, dept_name):
        """Adds a new department."""
        new_dept = Department(dept_name)
        if self.hospital.add_department(new_dept):
            self.save_data()
            self._log(f"Department '{dept_name}' created.")
            return f"Success: Department '{dept_name}' added."
        return f"Error: Department '{dept_name}' already exists."

    def remove_department(self, dept_name):
        """Safely removes a department and saves state."""
        dept = self._get_dept(dept_name)
        if dept:
            self.hospital.departments.remove(dept)
            self.save_data()
            self._log(f"Department '{dept_name}' removed.")
            return f"Success: Department '{dept_name}' removed."
        return "Error: Department not found."

    def add_patient(self, dept_name, name, age, record):
        """Adds a patient and increments ID counter."""
        dept = self._get_dept(dept_name)
        if dept:
            p_id = self.hospital.patient_counter
            self.hospital.patient_counter += 1
            new_p = Patient(p_id, name, age, record)
            msg = dept.add_patient(new_p)
            self.save_data()
            self._log(f"Patient '{name}' (ID: {p_id}) added to {dept_name}.")
            return msg
        return "Error: Department not found."

    def remove_patient(self, dept_name, p_id):
        """Removes a patient from a department."""
        dept = self._get_dept(dept_name)
        if dept:
            msg = dept.remove_patient(p_id)
            if "Success" in msg:
                self.save_data()
                self._log(f"Patient ID {p_id} removed from {dept_name}.")
            return msg
        return "Error: Department not found."

    def add_staff(self, dept_name, name, age, position):
        """Adds a staff member."""
        dept = self._get_dept(dept_name)
        if dept:
            s_id = self.hospital.staff_counter
            self.hospital.staff_counter += 1
            new_s = Staff(s_id, name, age, position)
            msg = dept.add_staff(new_s)
            self.save_data()
            self._log(f"Staff '{name}' (ID: {s_id}) added to {dept_name}.")
            return msg
        return "Error: Department not found."

    def remove_staff(self, dept_name, s_id):
        """Removes staff from a department."""
        dept = self._get_dept(dept_name)
        if dept:
            msg = dept.remove_staff(s_id)
            if "Success" in msg:
                self.save_data()
                self._log(f"Staff ID {s_id} removed from {dept_name}.")
            return msg
        return "Error: Department not found."

    def search_person_by_name(self, name_query):
        """Searches across all departments."""
        results = []
        name_query = name_query.lower()
        for dept in self.hospital.departments:
            for p in dept.patients:
                if name_query in p.name.lower():
                    results.append(f"[Patient] {p.view_info()} (Dept: {dept.name})")
            for s in dept.staff:
                if name_query in s.name.lower():
                    results.append(f"[Staff] {s.view_info()} (Dept: {dept.name})")
        return "\n".join(results) if results else "No matches found."

    def view_patient_record(self, dept_name, p_id):
        """Gets medical record by ID."""
        dept = self._get_dept(dept_name)
        if dept:
            for p in dept.patients:
                if str(p.person_id) == str(p_id):
                    return p.view_record()
        return "Error: Patient not found."