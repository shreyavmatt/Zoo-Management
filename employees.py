import uuid
import datetime

class Employee:
    def __init__(self, name, address):
        self.employee_id = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals = []

    def addAnimal(self, animal):
        self.animals.append(animal)
        animal.caretaker = self.employee_id