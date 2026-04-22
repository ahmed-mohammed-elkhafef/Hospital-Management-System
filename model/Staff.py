from .Person import Person

class Staff(Person):
    """
    Class representing a staff member, inheriting from Person.

    Attributes:
        position (str): The job title or position of the staff member.
    """
    def __init__(self, s_id, name, age, position):
        """
        Initialize a new Staff instance.

        Args:
            s_id (int): Unique Staff ID.
            name (str): Staff name.
            age (int): Staff age.
            position (str): Job position.
        """
        super().__init__(s_id, name, age)
        self.position = position

    def to_dict(self):
        """
        Convert staff data to dictionary.

        Returns:
            dict: Staff data.
        """
        data = super().to_dict()
        data["position"] = self.position
        return data

    @staticmethod
    def from_dict(data):
        """
        Create a Staff object from a dictionary.

        Args:
            data (dict): Dictionary loaded from JSON.

        Returns:
            Staff: Reconstructed Staff object.
        """
        return Staff(data["id"], data["name"], data["age"], data["position"])

    def view_info(self):
        """
        Return detailed staff information.

        Returns:
            str: Formatted staff info string.
        """
        return f"[ID: {self.person_id}] Staff: {self.name}, Pos: {self.position}"