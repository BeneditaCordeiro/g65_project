# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:40:31 2026

@author: Laura
"""

from classes.gclass import Gclass

class Project(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    # Repara: Retirei o agency_id daqui! O projeto é independente.
    att = ['_id','_name','_category','_started_date']
    header = 'Projeto'
    des = ['Id','Nome','Categoria','Data Início']
    
    def __init__(self, id, name, category, started_date):
        super().__init__()
        id = Project.get_id(id)
        self._id = id
        self._name = name
        self._category = category
        self._started_date = started_date

        Project.obj[id] = self
        Project.lst.append(id)

    @property
    def id(self):
        return self._id
        
    @property
    def name(self):
        return self._name
        
    @name.setter
    def name(self, name):
        self._name = name
        
    @property
    def category(self):
        return self._category
        
    @category.setter
    def category(self, category):
        self._category = category
        
    @property
    def started_date(self):
        return self._started_date
        
    @started_date.setter
    def started_date(self, started_date):
        self._started_date = started_date