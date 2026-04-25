# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:39:17 2026

@author: Laura
"""
from classes.gclass import Gclass
from classes.agency import Agency

class Officer(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    att = ['_id','_role','_agency_id']
    header = 'Trabalhador'
    des = ['Id','Cargo','Agência_id']
    
    def __init__(self, id, role, agency_id):
        super().__init__()
        # O SEGURANÇA: Só deixa criar o Officer se a Agência já existir!
        if agency_id in Agency.lst:
            id = Officer.get_id(id)
            self._id = id
            self._role = role
            self._agency_id = agency_id # Faltava-te esta linha no teu!
            
            Officer.obj[id] = self
            Officer.lst.append(id)
        else:
            print('Agência', agency_id, 'não encontrada. Não foi possível criar o Trabalhador.')

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
        if agency_id in Agency.lst:
            self._agency_id = agency_id
        else:
            print('Agência', agency_id, 'não encontrada')
            
            