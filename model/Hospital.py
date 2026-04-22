from .Department import Department

class Hospital:
    """
    Class for managing overall hospital data and counters.

    Attributes:
        name (str): Hospital name.
        location (str): Hospital location.
        departments (list): List of Department objects.
        patient_counter (int): Auto-increment counter for patient IDs.
        staff_counter (int): Auto-increment counter for staff IDs.
    """
    def __init__(self, name, location):
        """
        Initialize the Hospital.

        Args:
            name (str): Hospital name.
            location (str): Location string.
        """
        self.name = name
        self.location = location
        self.departments = []
        self.patient_counter = 1000 
        self.staff_counter = 5000

    def to_dict(self):
        """
        Convert hospital state to dictionary.

        Returns:
            dict: Full hospital data.
        """
        return {
            "name": self.name,
            "location": self.location,
            "patient_counter": self.patient_counter,
            "staff_counter": self.staff_counter,
            "departments": [d.to_dict() for d in self.departments]
        }

    @staticmethod
    def from_dict(data):
        """
        Reconstruct Hospital from dictionary.

        Args:
            data (dict): Loaded data.

        Returns:
            Hospital: Restored object.
        """
        h = Hospital(data["name"], data["location"])
        h.patient_counter = data["patient_counter"]
        h.staff_counter = data["staff_counter"]
        h.departments = [Department.from_dict(d) for d in data["departments"]]
        return h

    def add_department(self, department):
        """
        Add a new department if it doesn't exist.

        Args:
            department (Department): The department object.

        Returns:
            bool: True if added, False if duplicate.
        """
        if any(d.name == department.name for d in self.departments):
            return False
        self.departments.append(department)
        return True