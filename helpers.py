import json


class Equipment:
    """
    This is the class which is supposed to represent an eqipment
    """

    def __init__(self, dictionary):
        """It expects a dictionary and create an instance from it"""
        self.__dict__.update(dictionary)

    def to_dict(self):
        """Can return instance as a dictionary"""
        return self.__dict__


class Inventory:
    """
    This is the representation of inventory which can consists of
    multiple instances of equipment.
    """

    def __init__(self, db_file):
        """Loads from JSON file and create instances as attributes"""
        self._db_file = db_file
        try:
            with open(self._db_file) as file:
                db_content = json.load(file)
            for key, value in db_content.items():
                setattr(self, key, Equipment(value))
        except FileNotFoundError:
            print('File not found. It will be created')

    def get_equipment(self):
        """Returns the list of equipment names"""
        return [key for key in self.__dict__.keys() if not key.startswith('_')]

    def get_equipment_attr(self, name, attr):
        """Returns an attribute for equipment"""
        equipment = getattr(self, name)
        return getattr(equipment, attr)

    def add_equipment(self, dictionary):
        """Adds another instance of Equipment as attribute"""
        setattr(self, dictionary['name'], Equipment(dictionary))
        self.sync()
        return dictionary['name']

    def del_equipment(self, name):
        """Deletes the entity by it's name"""
        eqiupment = getattr(self, name).to_dict()
        delattr(self, name)
        self.sync()
        return eqiupment

    def update_equipment_attr(self, name, dictionary):
        """Updates an attribute in equipment"""
        equipment = getattr(self, name)
        equipment.__dict__.update(dictionary)
        self.sync()
        return getattr(self, name).to_dict()

    def sync(self):
        """Dump all instances to JSON"""
        self._to_json = {}
        for key, value in self.__dict__.items():
            if not key.startswith('_'):
                self._to_json[key] = value.to_dict()
        with open(self._db_file, 'w') as file:
            json.dump(self._to_json, file)


if __name__ == '__main__':
    help(Equipment)
    help(Inventory)
