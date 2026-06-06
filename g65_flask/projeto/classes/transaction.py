# -*- coding: utf-8 -*-
from classes.gclass import Gclass
from classes.agency import Agency
from classes.project import Project

class Transaction(Gclass):
    obj = dict()
    lst = list()
    pos = 0
    sortkey = ''
    # CORRECTED: att order must match exactly the DB column order:
    # id, payment_date, amount, project_id, agency_id
    att = ['_id', '_payment_date', '_amount', '_project_id', '_agency_id']
    header = 'Transaction'
    des = ['Id', 'Data Pagamento', 'Valor', 'Id Projeto', 'Id Agência']

    def __init__(self, id, payment_date, amount, project_id, agency_id):
        super().__init__()
        # Cast to int for FK checks (values from DB arrive as int already,
        # but from forms they arrive as strings)
        agency_id = int(agency_id)
        project_id = int(project_id)
        if agency_id in Agency.lst and project_id in Project.lst:
            id = Transaction.get_id(id)
            self._id = id
            self._payment_date = payment_date
            self._amount = float(amount)
            self._project_id = project_id
            self._agency_id = agency_id
            Transaction.obj[id] = self
            Transaction.lst.append(id)
        else:
            print('Erro ao criar Transação: Agência', agency_id,
                  'ou Projeto', project_id, 'não existem no sistema.')

    @property
    def id(self):
        return self._id

    @property
    def payment_date(self):
        return self._payment_date

    @payment_date.setter
    def payment_date(self, payment_date):
        self._payment_date = payment_date

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, amount):
        self._amount = float(amount)

    @property
    def project_id(self):
        return self._project_id

    @project_id.setter
    def project_id(self, project_id):
        project_id = int(project_id)
        if project_id in Project.lst:
            self._project_id = project_id
        else:
            print('Projeto', project_id, 'não encontrado.')

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
