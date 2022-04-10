from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource
from zoo_json_utils import ZooJsonEncoder 
from zoo import Zoo

from animals import Animal
from enclosures import Enclosure
from employees import Employee

my_zoo = Zoo()

zooma_app = Flask(__name__)
# need to extend this class for custom objects, so that they can be jsonified
zooma_app.json_encoder = ZooJsonEncoder 
zooma_api = Api(zooma_app)


animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True, help="The scientific name of the animal, e,g. Panthera tigris")
animal_parser.add_argument('name', type=str, required=True, help="The common name of the animal, e.g., Tiger")
animal_parser.add_argument('age', type=int, required=True, help="The age of the animal, e.g., 12")

home_parser = reqparse.RequestParser()
home_parser.add_argument('enclosure_id', type=str, required=True, help="Enclosure ID")

birth_parser = reqparse.RequestParser()
birth_parser.add_argument('mother_id', type=str, required=True, help="ID of the animal's mother")

death_parser = reqparse.RequestParser()
death_parser.add_argument('animal_id', type=str, required=True, help="Animal ID")

enclosure_parser = reqparse.RequestParser()
enclosure_parser.add_argument('name', type=str, required=True, help="The name of the enclosure")
enclosure_parser.add_argument('area', type=int, required=True, help="The area of the enclosure in sq. meters")

employee_parser = reqparse.RequestParser()
employee_parser.add_argument('name', type=str, required=True, help="The name of the caretaker")
employee_parser.add_argument('address', type=str, required=True, help="The address of the caretaker")

del_employee_parser = reqparse.RequestParser()
del_employee_parser.add_argument('new_caretaker_id', type=str, required=True, help="ID of caretaker who will take care of deleted employee's animals")

@zooma_api.route('/animal')
class AddAnimalAPI(Resource):
    @zooma_api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters 
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object 
        new_animal = Animal (species, name, age) 
        #add the animal to the zoo
        my_zoo.addAnimal (new_animal) 
        return jsonify(new_animal) 
    

@zooma_api.route('/animal/<animal_id>')
class Animal_ID(Resource):
     def get(self, animal_id):
        search_result  = my_zoo.getAnimal(animal_id)
        return jsonify(search_result) # this is automatically jsonified by flask-restx
    
     def delete(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify("Animal with ID {animal_id} was not found")
        my_zoo.removeAnimal(targeted_animal)
        return jsonify("Animal with ID {animal_id} was removed") 

@zooma_api.route('/animals')
class AllAnimals(Resource):
     def get(self):
        return jsonify( my_zoo.animals)  
    
     
@zooma_api.route('/animals/<animal_id>/feed')
class FeedAnimal(Resource):
     def post(self, animal_id):
        targeted_animal  = my_zoo.getAnimal(animal_id)
        if not targeted_animal: 
            return jsonify("Animal with ID {animal_id} was not found") 
        targeted_animal.feed()
        return jsonify(targeted_animal)

@zooma_api.route('/animals/<animal_id>/vet')
class TakeToVet(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")

        targeted_animal.takeToVet()
        return jsonify(targeted_animal)

@zooma_api.route('/animals/<animal_id>/home')
class Home(Resource):
    @zooma_api.doc(parser=home_parser)
    def post(self, animal_id):
        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")

        args = home_parser.parse_args()
        enclosure_id = args['enclosure_id']

        old = my_zoo.getEnclosure(targeted_animal.enclosure)
        if old:
            Enclosure.removeAnimalFromEnclosure(old, targeted_animal)

        targeted_animal.changeEnclosure(enclosure_id, my_zoo)
        return jsonify(targeted_animal)

@zooma_api.route('/animals/birth')
class Birth(Resource):
    @zooma_api.doc(parser=birth_parser)
    def post(self):

        args = birth_parser.parse_args()
        mother_id = args['mother_id']
        mother = my_zoo.getAnimal(mother_id)

        if not mother:
            return jsonify("Animal with ID {animal_id} was not found")

        child = mother.givesBirth(my_zoo)
        return jsonify(child)

@zooma_api.route('/animal/death/')
class Death(Resource):
    @zooma_api.doc(parser=death_parser)
    def post(self):

        args = death_parser.parse_args()
        animal_id = args['animal_id']
        targeted_animal = my_zoo.getAnimal(animal_id)

        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")

        targeted_animal.dies(my_zoo)
        return jsonify(targeted_animal)

@zooma_api.route('/animals/stat')
class AnimalStats(Resource):
    def get(self):
        stats = my_zoo.getAnimalStats()
        return jsonify(stats)

@zooma_api.route('/enclosure')
class AddEnclosure(Resource):
    @zooma_api.doc(parser=enclosure_parser)
    def post(self):

        args = enclosure_parser.parse_args()
        name = args['name']
        area = args['area']

        new_enclosure = Enclosure(name, area)

        my_zoo.addEnclosure(new_enclosure)
        return jsonify(new_enclosure)

@zooma_api.route('/enclosures')
class AllEnclosures(Resource):
     def get(self):
        return jsonify(my_zoo.enclosures)

@zooma_api.route('/enclosures/<enclosure_id>/clean')
class CleanEnclosure(Resource):
     def post(self, enclosure_id):
         enclosure = my_zoo.getEnclosure(enclosure_id)
         if not enclosure:
             return jsonify("Enclosure with ID {enclosure_id} was not found")

         response = enclosure.clean()
         return jsonify(response)

@zooma_api.route('/enclosures/<enclosure_id>/animals')
class GetAnimals(Resource):
     def post(self, enclosure_id):
         enclosure = my_zoo.getEnclosure(enclosure_id)
         if not enclosure:
             return jsonify("Enclosure with ID {enclosure_id} was not found")

         animals = enclosure.getAnimals()
         return jsonify(animals)


@zooma_api.route('/enclosure/<enclosure_id>')
class DeleteEnclosure(Resource):
    def delete(self, enclosure_id):
        targeted_enclosure = my_zoo.getEnclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f"Enclosure with ID {enclosure_id} was not found")
        my_zoo.removeEnclosure(targeted_enclosure)
        return jsonify(f"Enclosure with ID {enclosure_id} was removed")

@zooma_api.route('/employee')
class AddEmployee(Resource):
    @zooma_api.doc(parser=employee_parser)
    def post(self):

        args = employee_parser.parse_args()
        name = args['name']
        address = args['address']

        new_employee = Employee(name, address)

        my_zoo.addEmployee(new_employee)
        return jsonify(new_employee)

@zooma_api.route('/employees')
class AllEmployees(Resource):
     def get(self):
        return jsonify(my_zoo.employees)

@zooma_api.route('/employee/<employee_id>/care/<animal_id>')
class AssignCaretaker(Resource):
    def post(self, employee_id, animal_id):

        targeted_employee = my_zoo.getEmployee(employee_id)
        if not targeted_employee:
            return jsonify("Employee with ID {employee_id} was not found")

        targeted_animal = my_zoo.getAnimal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")

        targeted_employee.addAnimal(targeted_animal)

        return jsonify(targeted_animal)

@zooma_api.route('/employee/<employee_id>/care/animals')
class EmployeeAnimals(Resource):
     def get(self, employee_id):

         targeted_employee = my_zoo.getEmployee(employee_id)
         if not targeted_employee:
             return jsonify("Employee with ID {employee_id} was not found")

         return jsonify(targeted_employee.animals)

@zooma_api.route('/employees/stats')
class EmployeeStats(Resource):
    def get(self):
        stats = my_zoo.getEmployeeStats()
        return jsonify(stats)

@zooma_api.route('/employee/<employee_id>')
class DeleteEmployee(Resource):

    @zooma_api.doc(parser=del_employee_parser)
    def delete(self, employee_id):

        args = del_employee_parser.parse_args()
        new_caretaker_id = args['new_caretaker_id']

        deleted_caretaker = my_zoo.getEmployee(employee_id)
        if not deleted_caretaker:
            return jsonify(f"Employee with ID {employee_id} was not found")

        new_caretaker = my_zoo.getEmployee(new_caretaker_id)
        if not new_caretaker:
            return jsonify(f"Employee with ID {new_caretaker_id} was not found")

        my_zoo.removeEmployee(deleted_caretaker, new_caretaker)
        return jsonify(f"Employee with ID {employee_id} has been deleted and animals under their care have moved to employee with ID {new_caretaker_id}.")

@zooma_api.route('/tasks/cleaning')
class CleaningPlan(Resource):
    def get(self):
        cleaning_plan = my_zoo.createCleaningPlan()
        return jsonify(cleaning_plan)

@zooma_api.route('/tasks/medical')
class MedicalPlan(Resource):
    def get(self):
        medical_plan = my_zoo.createMedicalPlan()
        return jsonify("Medical plan is provided as Animal ID: Checkup Date", medical_plan)

@zooma_api.route('/tasks/feeding')
class FeedingPlan(Resource):
    def get(self):
        feeding_plan = my_zoo.createFeedingPlan()
        return jsonify(feeding_plan)

if __name__ == '__main__':
    zooma_app.run(debug = False, port = 7890)