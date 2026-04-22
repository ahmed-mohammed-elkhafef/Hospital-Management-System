from .Patient import Patient
from .Staff import Staff

class Department:
    """
    Class representing a hospital department containing patients and staff.
    
    Attributes:
        name (str): Department name.
        patients (list): List of Patient objects.
        staff (list): List of Staff objects.
    """
    def __init__(self, name):
        """
        Initialize a new Department.

        Args:
            name (str): Name of the department.
        """
        self.name = name
        self.patients = []
        self.staff = []

    def to_dict(self):
        """
        Convert department and its contents to a dictionary.

        Returns:
            dict: Department data with nested lists.
        """
        return {
            "name": self.name,
            "patients": [p.to_dict() for p in self.patients],
            "staff": [s.to_dict() for s in self.staff]
        }

    @staticmethod
    def from_dict(data):
        """
        Reconstruct a Department object from data.

        Args:
            data (dict): Dictionary loaded from JSON.

        Returns:
            Department: Reconstructed Department object.
        """
        dept = Department(data["name"])
        # Rebuild lists using the static methods of Patient and Staff
        dept.patients = [Patient.from_dict(p) for p in data["patients"]]
        dept.staff = [Staff.from_dict(s) for s in data["staff"]]
        return dept

    def add_patient(self, patient):
        """
        Add a patient to the department.

        Args:
            patient (Patient): The patient object to add.

        Returns:
            str: Success message.
        """
        self.patients.append(patient)
        return f"Success: Patient '{patient.name}' added to {self.name} with ID: {patient.person_id}"

    def remove_patient(self, patient_id):
        """
        Remove a patient by ID.

        Args:
            patient_id (int/str): The ID of the patient to remove.

        Returns:
            str: Success message or None if not found.
        """
        for i, p in enumerate(self.patients):
            if str(p.person_id) == str(patient_id):
                removed_name = p.name
                del self.patients[i]
                return f"Success: Patient '{removed_name}' (ID: {patient_id}) removed."
        return None

    def add_staff(self, staff_member):
        """
        Add a staff member to the department.

        Args:
            staff_member (Staff): The staff object to add.

        Returns:
            str: Success message.
        """
        self.staff.append(staff_member)
        return f"Success: Staff '{staff_member.name}' added with ID: {staff_member.person_id}"
    
    def remove_staff(self, staff_id):
        """
        Remove a staff member by ID.

        Args:
            staff_id (int/str): The ID of the staff to remove.

        Returns:
            str: Success message or None if not found.
        """
        for i, s in enumerate(self.staff):
            if str(s.person_id) == str(staff_id):
                del self.staff[i]
                return f"Success: Staff with ID {staff_id} removed."
        return None