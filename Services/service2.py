from flask import Flask
from flask_restful import Resource, Api
import psycopg2
from DatabaseLayer.database import *


class SingletonMeta(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]
class SingletonDB(metaclass=SingletonMeta):
    def __init__(self):
        self.conn = psycopg2.connect(host=host, user=user,  database=db_name, password = password, port="5432")

    def select_all_salary(self):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT p1."vaccancyId", p1."vaccancy_name",  p1."salary" FROM "vaccancy" p1')
            rows = cursor.fetchall()
        return rows
    def select_all_desc(self, i):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT  p1."vaccancyId", p1."vaccancy_name",p1."description", p1."social_package", p1."salary" FROM "vaccancy" p1 WHERE p1."vaccancyId" = (%s)', str(i))
            rows = cursor.fetchall()
        return rows




class Salaries(Resource):
    #parser = reqparse.RequestParser()
    def get(self):
        db = SingletonDB()
        all_vaccancies = db.select_all_salary()
        my_list = []
        for row in all_vaccancies:
            a = {"vaccancyId": row[0], "vaccancy_name": row[1],  "salary": row[2]}
            my_list.append(a)
        return my_list

class Descript(Resource):
    #parser = reqparse.RequestParser()
    def get(self, id):
        db = SingletonDB()
        all_vaccancies = db.select_all_desc(id)
        my_list = []
        for row in all_vaccancies:
            a = {"vaccancyId": row[0], "vaccancy_name": (row[1]), "description": (row[2]), "social_package": row[3],
                 "salary": row[4]}
            my_list.append(a)

        return my_list[0]


if __name__ == "__main__":
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(Salaries, '/price-list/')
    api.add_resource(Descript, '/details/<int:id>')
    app.run(port=5002, debug=True)
