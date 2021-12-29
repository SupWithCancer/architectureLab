from __future__ import annotations
from abc import ABC, abstractmethod
from typing import Any
from PersistanceLayer.SingletonDataBase import Singleton
import requests
from PresentationLayer.SpecificationFilter import  MaxSalary, MinSalary, VaccancyName


class VaccancyBuilder(ABC):
    @property
    @abstractmethod
    def vaccancy(self) -> None:
        pass
    @abstractmethod
    def extract_from_source(self) ->None:
        pass
    @abstractmethod
    def reformat(self) -> None:
        pass
    @abstractmethod
    def filter(self) -> None:
        pass


class Service1VaccancyBuilder(VaccancyBuilder):
    def __init__(self) -> None:
        self.reset()
    def reset(self) -> None:
        self._vaccancy = OwnVaccancy()
    @property
    def vaccancy(self) -> OwnVaccancy:
        vaccancy = self._vaccancy
        self.reset()
        return vaccancy
    def extract_from_source(self) ->None:
        self._vaccancy.set(requests.get('http://127.0.0.1:5001/search/').json())
    def reformat(self) -> None:
        pass
    def filter(self) -> None:
        self._vaccancy.filter()
class Service2VaccancyBuilder(VaccancyBuilder):
    def __init__(self) -> None:
        self.reset()
    def reset(self) -> None:
        self._vaccancy = OwnVaccancy()
    @property
    def vaccancy(self) -> OwnVaccancy:
        vaccancy = self._vaccancy
        self.reset()
        return vaccancy
    def extract_from_source(self) ->None:
        self._vaccancy.set(requests.get('http://127.0.0.1:5002/price-list/').json())
    def reformat(self) -> None:
        full_vaccancies = []
        for row in self._vaccancy.vaccancies:
            full_vaccancies.append(requests.get('http://127.0.0.1:5002/details/'+str(row["vaccancyId"])).json())
        self._vaccancy.set(full_vaccancies)
    def filter(self) -> None:
        self._vaccancy.filter()

class OwnVaccancyBuilder(VaccancyBuilder):
    def __init__(self) -> None:
        self.reset()
        self.db = Singleton()
    def reset(self) -> None:
        self._vaccancy = OwnVaccancy()
    @property
    def vaccancy(self) -> OwnVaccancy:
        vaccancy = self._vaccancy
        self.reset()
        return vaccancy
    def extract_from_source(self) ->None:
        self._vaccancy.set(self._vaccancy.select_all_prod())
    def reformat(self) -> None:
        my_list = []
        for row in self.vaccancy.vaccancies:
            a = {"vaccancyId": row[0], "vaccancy_name": (row[1]), "description": (row[2]), "social_package": row[3], "salary": row[4]}
            my_list.append(a)
        self._vaccancy.set(my_list)
    def filter(self) -> None:
        self._vaccancy.filter()
class Director:
    def __init__(self) -> None:
        self._builder = None

    @property
    def builder(self) -> builder:
        return self._builder

    @builder.setter
    def builder(self, builder: builder) -> None:
        self._builder = builder

    def build_all_vaccancy(self) -> None:
        self.builder.extract_from_source()
        self.builder.reformat()
    def build_filtered_vaccancy(self) -> None:
        self.builder.extract_from_source()
        self.builder.reformat()
        self.builder.filter()
class OwnVaccancy():
    def __init__(self):
        self.vaccancies = []
        self.conn = Singleton().conn
    def add(self, vaccancy: dict[str, Any]):
        self.vaccancies.append(vaccancy)
    def join(self, another_vaccancy):
        self.vaccancies += another_vaccancy.vaccancies
    def drop(self, id):
        del self.vaccancies[id]
    def set(self, vaccancies):
        self.vaccancies = vaccancies
    def select_all_prod(self):
        rows = []
        with self.conn.cursor() as cursor:
            cursor.execute('SELECT p1."vaccancyId", p1."vaccancy_name",p1."description", p1."social_package", p1."salary" FROM "vaccancy" p1')
            rows = cursor.fetchall()
        return rows
    def insert(self, args):
        with self.conn.cursor() as cursor:
            cursor.execute('''INSERT INTO "vaccancy" ("vaccancy_name", "description", "salary", "social_package") VALUES('%s','%s','%s', true)'''%(str(args["vaccancy_name"]), str(args["description"]), int(args["salary"])))
        self.conn.commit()
    def delete(self, id):
        with self.conn.cursor() as cursor:
            cursor.execute('DELETE FROM "vaccancy" WHERE "vaccancyId"='+str(id))
        self.conn.commit()

    def update(self, args):
        query_str = 'UPDATE "vaccancy" SET '
        for key, value in args.items():
            if key != 'vaccancyId' and value !=None:
                query_str += '"' + key + '"=' + "'" + str(value) + "',"
        query_str = query_str[0:-1]
        query_str += ' WHERE "vaccancyId"=' + str(args["vaccancyId"])
        with self.conn.cursor() as cursor:
            cursor.execute(query_str)
        self.conn.commit()

    def filter(self):
        vaccancy_filter = MaxSalary() & MinSalary() & VaccancyName()
        vaccancies = []
        for i in self.vaccancies:
            if vaccancy_filter.is_satisfied_by(i):
                vaccancies.append(i)
        self.vaccancies = vaccancies
