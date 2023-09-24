#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json
import shlex


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models cls currently in storage"""
        res = {}
        if cls is not None:
            for key, obj in self.__objects.items():
                part = key.replace('.', ' ')
                part = shlex.split(part)
                if (part[0] == cls.__name__):
                    res[key] = self.__objects[key]
                """if cls  == obj.__class__:
                    res[key] = obj"""
            return res
        return self.__objects

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if obj:
            """key = "{}.{}".format(type(obj).__name__, obj.id)
            self.__objects[key] = obj"""
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        temp = {}
        temp.update(self.__objects)
        for key, val in temp.items():
            temp[key] = val.to_dict()
        with open(FileStorage.__file_path, 'w') as f:
            json.dump(temp, f)

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            with open(self.__file_path, 'r', encoding="UTF-8") as f:
                for key, val in (json.load(f)).items():
                    val = eval(val["__class__"])(**val)
                    self.__objects[key] = val
                    """self.all()[key] = classes[val['__class__']](**val)"""
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it exist"""
        if obj is not None:
            key = type(obj).__name__ + '.' + obj.id
            FileStorage.__objects.pop(key)

    def close(self):
        """ method for deserializing the JSON file to objects """
        self.reload()

    def get(self, cls, id):
        """Retrieve an object"""
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in classes:
            key = cls + '.' + id
            obj = self.__objects.get(key, None)
            return obj
        else:
            return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) == str and cls in classes:
            total = len(self.all(cls))
        elif cls is None:
            total = len(self.__objects)
        return total
