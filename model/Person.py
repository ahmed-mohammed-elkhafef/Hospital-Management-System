class Person:
    """
    Base class representing a generic person in the hospital system.
    
    Attributes:
        person_id (int): Unique identifier for the person.
        name (str): The full name of the person.
        age (int): The age of the person.
    """
    def __init__(self, person_id, name, age):
        """
        Initialize a new Person instance.

        Args:
            person_id (int): Unique ID.
            name (str): Person's name.
            age (int): Person's age.
        """
        self.person_id = person_id
        self.name = name
        self.age = age

    def to_dict(self):
        """
        Convert the person object to a dictionary for JSON serialization.

        Returns:
            dict: A dictionary containing person data.
        """
        return {
            "id": self.person_id,
            "name": self.name,
            "age": self.age
        }

    def view_info(self):
        """
        Return a formatted string with basic person information.

        Returns:
            str: Formatted info string.
        """
        return f"[ID: {self.person_id}] Name: {self.name}, Age: {self.age}"