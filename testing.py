import pytest

from zoo import Zoo
from animals import Animal
from enclosures import Enclosure
from employees import Employee

@pytest.fixture
def my_zoo():
    my_zoo = Zoo()
    return my_zoo

def test_animals(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    assert (len(my_zoo.animals) == 2)

def test_enclosure(my_zoo):

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    enclosure2 = Enclosure("Tiger Forest", 700)
    my_zoo.addEnclosure(enclosure2)

    assert (len(my_zoo.enclosures) == 2)

def test_home(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    enclosure2 = Enclosure("Tiger Forest", 700)
    my_zoo.addEnclosure(enclosure2)

    lion1.changeEnclosure(enclosure1.enclosure_id, my_zoo)
    tiger1.changeEnclosure(enclosure2.enclosure_id, my_zoo)

    assert (lion1.enclosure == enclosure1.enclosure_id)
    assert (tiger1.enclosure == enclosure2.enclosure_id)
    assert (len(enclosure1.animals) == 1)
    assert (len(enclosure2.animals) == 1)

def test_birth(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    enclosure2 = Enclosure("Tiger Forest", 700)
    my_zoo.addEnclosure(enclosure2)

    lion1.changeEnclosure(enclosure1.enclosure_id, my_zoo)
    tiger1.changeEnclosure(enclosure2.enclosure_id, my_zoo)

    lion1.givesBirth(my_zoo)

    assert (len(my_zoo.animals) == 3)
    assert (len(enclosure1.animals) == 2)

def test_vet(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    enclosure2 = Enclosure("Tiger Forest", 700)
    my_zoo.addEnclosure(enclosure2)

    lion1.changeEnclosure(enclosure1.enclosure_id, my_zoo)
    tiger1.changeEnclosure(enclosure2.enclosure_id, my_zoo)

    lion1.givesBirth(my_zoo)

    tiger1.takeToVet()

    assert(len(tiger1.vet_record) == 1 )

def test_getAnimal(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    enclosure2 = Enclosure("Tiger Forest", 700)
    my_zoo.addEnclosure(enclosure2)

    lion1.changeEnclosure(enclosure1.enclosure_id, my_zoo)
    tiger1.changeEnclosure(enclosure2.enclosure_id, my_zoo)

    lion1.givesBirth(my_zoo)

    lion2 = my_zoo.getAnimal(my_zoo.animals[2].animal_id)

    assert (len(lion2.animal_id) == 36)
    assert (lion2.animal_id != lion1.animal_id)
    assert (lion2.enclosure == enclosure1.enclosure_id)

def test_death(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    enclosure2 = Enclosure("Tiger Forest", 700)
    my_zoo.addEnclosure(enclosure2)

    lion1.changeEnclosure(enclosure1.enclosure_id, my_zoo)
    tiger1.changeEnclosure(enclosure2.enclosure_id, my_zoo)

    lion1.givesBirth(my_zoo)

    lion2 = my_zoo.getAnimal(my_zoo.animals[2].animal_id)

    lion2.dies(my_zoo)

    assert (len(enclosure1.animals) == 1)
    assert (len(my_zoo.animals) == 2)

def test_employee(my_zoo):
    employee1 = Employee("Nick Cage", "101 Streets Street")
    my_zoo.addEmployee(employee1)

    assert(len(my_zoo.employees) == 1)

def test_clean(my_zoo):

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    employee1 = Employee("Nick Cage", "101 Streets Street")
    my_zoo.addEmployee(employee1)

    enclosure1.clean()

    assert (len(enclosure1.cleaning_record) == 1)

def test_caretaker(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    lion1.changeEnclosure(enclosure1.enclosure_id, my_zoo)

    employee1 = Employee("Nick Cage", "101 Streets Street")
    my_zoo.addEmployee(employee1)

    employee1.addAnimal(lion1)

    assert (len(employee1.animals) == 1)
    assert (employee1.animals[0].enclosure == enclosure1.enclosure_id)

def test_cleaningPlan(my_zoo):

    enclosure1 = Enclosure("Lion Den", 650)
    my_zoo.addEnclosure(enclosure1)

    enclosure2 = Enclosure("Tiger Forest", 700)
    my_zoo.addEnclosure(enclosure2)

    employee1 = Employee("Nick Cage", "101 Streets Street")
    my_zoo.addEmployee(employee1)

    employee2 = Employee("Queen Elizabeth", "Royal Palace")
    my_zoo.addEmployee(employee2)

    my_zoo.createCleaningPlan()

    assert (len(my_zoo.cleaning_plan) == 2)

def test_medicalPlan(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    tiger1.takeToVet()

    my_zoo.createMedicalPlan()

    assert (len(my_zoo.medical_plan) == 2)

def test_feedingPlan(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    employee1 = Employee("Nick Cage", "101 Streets Street")
    my_zoo.addEmployee(employee1)

    employee2 = Employee("Queen Elizabeth", "Royal Palace")
    my_zoo.addEmployee(employee2)

    my_zoo.createFeedingPlan()

    assert (len(my_zoo.feeding_plan) == 2)

def test_deleteEmployee(my_zoo):

    lion1 = Animal("Panthera Leo", "Lion1", 10)
    my_zoo.addAnimal(lion1)

    tiger1 = Animal("Panthera Tigris", "Tiger1", 10)
    my_zoo.addAnimal(tiger1)

    employee1 = Employee("Nick Cage", "101 Streets Street")
    my_zoo.addEmployee(employee1)

    employee2 = Employee("Queen Elizabeth", "Royal Palace")
    my_zoo.addEmployee(employee2)

    employee1.addAnimal(lion1)
    employee1.addAnimal(tiger1)

    my_zoo.removeEmployee(employee1, employee2)

    assert (len(my_zoo.employees) == 1)
    assert (len(employee2.animals) == 2)




