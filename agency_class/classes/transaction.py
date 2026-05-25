# -*- coding: utf-8 -*-
"""
Created on Wed Apr  1 09:40:54 2026

@author: Laura
"""

from classes.gclass import Gclass
from classes.agency import Agency    # <-- ADICIONA ESTA LINHA!
from classes.project import Project

class Transaction(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    # Os atributos que o professor pediu: As duas chaves estrangeiras + Data + Valor
    att = ['_id', '_agency_id', '_project_id', '_payment_date', '_amount']
    header = 'Transação/Pagamento'
    des = ['Id', 'Id_Agência', 'Id_Projeto', 'Data_Pagamento', 'Valor']
    
    def __init__(self, id, agency_id, project_id, payment_date, amount):
        super().__init__()
        
        # SEGURANÇA DUPLO: A Agência E o Projeto têm de existir no sistema!
        if agency_id in Agency.lst and project_id in Project.lst:
            id = Transaction.get_id(id)
            self._id = id
            self._agency_id = agency_id
            self._project_id = project_id
            self._payment_date = payment_date
            self._amount = amount
            
            Transaction.obj[id] = self
            Transaction.lst.append(id)
        else:
            print('Erro ao criar Transação: Agência', agency_id, 'ou Projeto', project_id, 'não existem no sistema!')

    # Getters
    @property
    def id(self):
        return self._id
        
    @property
    def agency_id(self):
        return self._agency_id
        
    @property
    def project_id(self):
        return self._project_id
        
    @property
    def payment_date(self):
        return self._payment_date
        
    @property
    def amount(self):
        return self._amount

    # Setters (Com segurança para as chaves estrangeiras!)
    @agency_id.setter
    def agency_id(self, agency_id):
        if agency_id in Agency.lst:
            self._agency_id = agency_id
        else:
            print('Agência não encontrada.')
            
    @project_id.setter
    def project_id(self, project_id):
        if project_id in Project.lst:
            self._project_id = project_id
        else:
            print('Projeto não encontrado.')
            
    @payment_date.setter
    def payment_date(self, payment_date):
        self._payment_date = payment_date
        
    @amount.setter
    def amount(self, amount):
        self._amount = amount