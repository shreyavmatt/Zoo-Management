import uuid 
import datetime

class Animal: 
    def __init__(self, species_name, common_name, age):
        self.animal_id = str(uuid.uuid4())
        self.species_name = species_name 
        self.common_name = common_name 
        self.age = age 
        self.feeding_record = []
        self.vet_record = []
        self.enclosure = None 
        self.caretaker = None
        
    # simply store the current system time when this method is called    
    def feed(self):
        date = datetime.datetime.now()
        self.feeding_record.append(date)

    def takeToVet(self):
        date = datetime.datetime.now()
        self.vet_record.append(date)

    def givesBirth(self, zoo):
        child = Animal(self.species_name, self.common_name, 0)

        if self.enclosure:
            child.enclosure = self.enclosure
            enclosure = zoo.getEnclosure(self.enclosure)
            enclosure.animals.append(child)

        zoo.addAnimal(child)

        return child

    def dies(self, zoo):
        if self.enclosure:
            enclosure = zoo.getEnclosure(self.enclosure)
            enclosure.animals.remove(self)
        zoo.removeAnimal(self)

    def changeEnclosure(self, enclosure_id, zoo):
        self.enclosure = enclosure_id
        enclosure = zoo.getEnclosure(enclosure_id)
        enclosure.animals.append(self)
