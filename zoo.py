import datetime
import random
class Zoo:
    def __init__ (self): 
        self.animals = []
        self.enclosures = []
        self.employees = []
        self.cleaning_plan = {}
        self.medical_plan = {}
        self.feeding_plan = {}

    def addAnimal(self, animal): 
        self.animals.append(animal)
        
    def removeAnimal(self, animal): 
        self.animals.remove(animal) 
    
    def getAnimal(self, animal_id): 
        for animal in self.animals: 
            if animal.animal_id == animal_id: 
                return animal

    def animalsPerSpecies(self):
        all_species = []

        for animal in self.animals:
            if animal.species_name not in all_species:
                all_species.append(animal.species_name)

        animals_per_species = {}

        for species in all_species:
            animals_per_species[species] = 0
            for animal in self.animals:
                if animal.species_name == species:
                    animals_per_species[species] += 1

        return animals_per_species

    def animalsPerEnclosure(self):

        animals_per_enclosure = len(self.animals) / len(self.enclosures)

        return animals_per_enclosure

    def multipleSpeciesInEnclosure(self):
        for enclosure in self.enclosures:
            check = False
            total = 0
            for i in range(len(enclosure.animals)):
                if enclosure.animals[i] != enclosure.animals[i-1]:
                    check = True
                    break
            if check == True:
                total += 1
        return total

    def spacePerAnimal(self):
        space_per_animal = {}
        for enclosure in self.enclosures:
            space_per_animal[enclosure.enclosure_id] = enclosure.spacePerAnimal()
        return space_per_animal

    def getAnimalStats(self):
        if len(self.animals) != 0:
            stats = {}
            stats['animals per species'] = self.animalsPerSpecies()
            try:
                stats['average number of animals per enclosure'] = self.animalsPerEnclosure()
                stats['Number of enclosures with multiple species'] = self.multipleSpeciesInEnclosure()
                stats['Space per animal in each enclosure'] = self.spacePerAnimal()

                return stats
            except:
                return "No enclosures in zoo."

        else:
            return "No animals in zoo."

    def addEnclosure(self, enclosure):
        self.enclosures.append(enclosure)

    def getEnclosure(self, enclosure_id):
        for enclosure in self.enclosures:
            if enclosure.enclosure_id == enclosure_id:
                return enclosure

    def removeEnclosure(self, enclosure):
        new_enclosure = enclosure
        while new_enclosure == enclosure:
            new_enclosure = random.choice(self.enclosures)
        new_enclosure.animals += enclosure.animals
        self.enclosures.remove(enclosure)

    def addEmployee(self, employee):
        self.employees.append(employee)

    def getEmployee(self, employee_id):
        for employee in self.employees:
            if employee.employee_id == employee_id:
                return employee

    def removeEmployee(self, employee, new_caretaker):
        new_caretaker.animals = employee.animals
        self.employees.remove(employee)

    def getEmployeeStats(self):
        if len(self.employees) != 0:
            stats = {}
            number_of_animals = []
            total_animals = 0
            total_employees = 0
            for employee in self.employees:
                number_of_animals.append(len(employee.animals))
                if len(employee.animals) != 0:
                    total_animals += len(employee.animals)
                    total_employees += 1

            stats['min'] = min(number_of_animals)
            stats['max'] = max(number_of_animals)
            try:
                stats['average'] = total_animals / total_employees
            except ZeroDivisionError:
                stats['average'] = 0
            return stats
        else:
            return "No employees working in zoo."

    def createCleaningPlan(self):

        if len(self.employees) != 0:
            for enclosure in self.enclosures:
                if len(enclosure.cleaning_record) != 0:
                    last_cleaned = enclosure.cleaning_record[-1]
                    next_cleaning = last_cleaned + datetime.timedelta(days = 3)
                    employee = random.choice(self.employees)
                    self.cleaning_plan[enclosure.enclosure_id] = [next_cleaning.strftime("%d/%m/%Y"), {employee.name: employee.employee_id}]

                else:
                    date = datetime.datetime.now()

                    employee = random.choice(self.employees)
                    self.cleaning_plan[enclosure.enclosure_id] = [date.strftime("%d/%m/%Y"), {employee.name: employee.employee_id}]

            return ("Cleaning plan is provided as Enclosure ID: [Cleaning Date, {Caretaker Name: Caretaker ID}]", self.cleaning_plan)

        else:
            return "There is no caretaker to clean the enclosures."

    def createMedicalPlan(self):
        for animal in self.animals:
            if len(animal.vet_record) != 0:
                last_checkup = animal.vet_record[-1]
                next_checkup = last_checkup + datetime.timedelta(days=35)
                self.medical_plan[animal.animal_id] = next_checkup.strftime("%d/%m/%Y")

            else:
                date = datetime.datetime.now()

                self.medical_plan[animal.animal_id] = date.strftime("%d/%m/%Y")

        return self.medical_plan

    def createFeedingPlan(self):

        if len(self.employees) != 0:
            for animal in self.animals:
                if len(animal.feeding_record) != 0:
                    last_fed = animal.feeding_record[-1]
                    next_feeding = last_fed + datetime.timedelta(days = 2)
                    employee = random.choice(self.employees)
                    self.feeding_plan[animal.animal_id] = [next_feeding.strftime("%d/%m/%Y"), {employee.name: employee.employee_id}]

                else:
                    date = datetime.datetime.now()

                    employee = random.choice(self.employees)
                    self.feeding_plan[animal.animal_id] = [date.strftime("%d/%m/%Y"), {employee.name: employee.employee_id}]

            return ("Feeding plan is provided as Animal ID: [Feeding Date, {Caretaker Name: Caretaker ID}]", self.feeding_plan)

        else:
            return "There is no caretaker to feed the animals."

