from flask_restful import reqparse
from BusinessLayer.ProductBuilder import Director, OwnVaccancyBuilder, Service1VaccancyBuilder, Service2VaccancyBuilder, OwnVaccancy
from PersistanceLayer.SingletonDataBase import Singleton



class Facade:
    def __init__(self):
        self.director = Director()
        self.db = Singleton()
        self.parser = reqparse.RequestParser()
        self.empty_vaccancy = OwnVaccancy()
    def get_prod(self):
        director = Director()
        builder = OwnVaccancyBuilder()
        self.director.builder = builder
        self.director.build_filtered_vaccancy()
        own = builder.vaccancy

        builder = Service1VaccancyBuilder()
        self.director.builder = builder
        self.director.build_filtered_vaccancy()
        service1 = builder.vaccancy

        builder = Service2VaccancyBuilder()
        self.director.builder = builder
        self.director.build_filtered_vaccancy()
        service2 = builder.vaccancy
        own.join(service1)
        own.join(service2)
        return own.vaccancies
    def insert(self):
        self.parser.add_argument("vaccancy_name")
        self.parser.add_argument("description")
        self.parser.add_argument("salary")
        self.parser.add_argument("social_package")

        args = self.parser.parse_args()
        self.empty_vaccancy.insert(args)
    def delete(self):
        self.parser.add_argument("vaccancyId")
        args = self.parser.parse_args()
        self.empty_vaccancy.delete(args["vaccancyId"])
    def update(self):
        self.parser.add_argument("vaccancyId")
        self.parser.add_argument("vaccancy_name")
        self.parser.add_argument("description")
        self.parser.add_argument("salary")

        args = self.parser.parse_args()
        self.empty_vaccancy.update(args)
