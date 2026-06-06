# -*- coding: utf-8 -*-
from classes.gclass import Gclass
from classes.agency import Agency

class Officer(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id', '_role', '_agency_id']
    header = 'Officer'
    des = ['Id', 'Cargo', 'Id Agência']

    def __init__(self, id, role, agency_id):
        super().__init__()
        # Cast to int: values from DB are int, from forms are strings
        agency_id = int(agency_id)
        if agency_id in Agency.lst:
            id = Officer.get_id(id)
            self._id = id
            self._role = role
            self._agency_id = agency_id
            Officer.obj[id] = self
            Officer.lst.append(id)
        else:
            print('Agência', agency_id, 'não encontrada. Officer não criado.')

    @property
    def id(self):
        return self._id

    @property
    def role(self):
        return self._role

    @role.setter
    def role(self, role):
        self._role = role

    @property
    def agency_id(self):
        return self._agency_id

    @agency_id.setter
    def agency_id(self, agency_id):
        agency_id = int(agency_id)
        if agency_id in Agency.lst:
            self._agency_id = agency_id
        else:
            print('Agência', agency_id, 'não encontrada.')
