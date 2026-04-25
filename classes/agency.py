# -*- coding: utf-8 -*-
from classes.gclass import Gclass

class Agency(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_name']
    header = 'Agência'
    des = ['Id','Nome']
    
    def __init__(self, id, name):
        super().__init__()
        id = Agency.get_id(id)
        self._id = id
        self._name = name
        
        Agency.obj[id] = self
        Agency.lst.append(id)

    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        self._name = name

