from .Person import Person

class Patient(Person):
    """
    Class representing a patient, inheriting from Person.
    
    Attributes:
        medical_record (str): Description of the patient's medical condition.
    """
    def __init__(self, p_id, name, age, medical_record):
        """
        Initialize a new Patient instance.

        Args:
            p_id (int): Unique Patient ID.
            name (str): Patient's name.
            age (int): Patient's age.
            medical_record (str): Medical history or condition.
        """
        super().__init__(p_id, name, age)
        self.medical_record = medical_record

    def to_dict(self):
        """
        Convert patient data to dictionary, including parent attributes.

        Returns:
            dict: Patient data.
        """
        data = super().to_dict()
        data["medical_record"] = self.medical_record
        return data

    @staticmethod
    def from_dict(data):
        """
        Create a Patient object from a dictionary.

        Args:
            data (dict): Dictionary loaded from JSON.

        Returns:
            Patient: Reconstructed Patient object.
        """
        return Patient(data["id"], data["name"], data["age"], data["medical_record"])

    def view_record(self):
        """
        Return the patient's specific medical record.

        Returns:
            str: Formatted medical record string.
        """
        return f"[ID: {self.person_id}] Name: {self.name} | Condition: {self.medical_record}"