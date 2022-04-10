import uuid
import datetime

class Enclosure :
    def __init__(self, name, space):
        self.enclosure_id = str(uuid.uuid4())
        self.name = name
        self.space = space
        self.animals = []
        self.cleaning_record = []

    def removeAnimalFromEnclosure(self, enclosure, animal):
        enclosure.animals.remove(animal)

    def clean(self):
        date = datetime.datetime.now()
        if date in self.cleaning_record:
            return "Enclosure has already been cleaned today."
        else:
            self.cleaning_record.append(date)
            return self

    def getAnimals(self):
        return self.animals

    def spacePerAnimal(self):
        return (len(self.animals)/self.space)