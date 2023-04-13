
from dataclasses import field
from enum import Enum

class OrganizationType:
    ORGANIZATION = (1, 'Организация')
    PERSON = (2, 'Физическое лицо')

    @classmethod
    def typeInfo(cls, type: int):
        switcher = {
            1: OrganizationType.ORGANIZATION,
            2: OrganizationType.PERSON,
        }

        fieldType = switcher.get(type, OrganizationType.PERSON)

        return {
            'id': fieldType[0],
            'name': fieldType[1],
        }

    __list__ = (ORGANIZATION, PERSON)



class Gender:
    MALE = (1, 'Male')
    FEMALE = (2, 'Female')

    __list__ = (MALE, FEMALE)

class Currency:
    SUM = (1, 'Sum')
    DOLLAR = (2, 'Dollar')
    EURO = (3, 'Euro')

    __list__ = (SUM, DOLLAR, EURO)


class Vat:
    zero = (1, 0)
    fifteen = (2, 15)

    __list__ = (zero, fifteen)


class PaymentMethod:
    any = (0, 'All')
    in_cash = (1, 'Cash')
    transfer = (2, 'Transfer money')

    __list__ = (any, in_cash, transfer)
    
class CoreEmployeeType(Enum):
    DIRECTOR = 'Director'
    MANAGER = 'Manager'
    HR = 'HR'
    ACCOUNTANT = 'Accountant'
    
    __list__ = (DIRECTOR, MANAGER, HR, ACCOUNTANT)
    
    @property
    def title(self) -> str:
        return self.value.title().upper()

    @property
    def level(self) -> int:
        switcher = {
            CoreEmployeeType.DIRECTOR: 10,
            CoreEmployeeType.MANAGER: 9,
            CoreEmployeeType.HR: 8,
            CoreEmployeeType.ACCOUNTANT: 7,
        }
        
        return switcher.get(self, 0)
    
    @staticmethod
    def get_employee_type_by_title(title: str) -> Enum:
        switcher = {
            CoreEmployeeType.DIRECTOR.title: CoreEmployeeType.DIRECTOR,
            CoreEmployeeType.MANAGER.title: CoreEmployeeType.MANAGER,
            CoreEmployeeType.HR.title: CoreEmployeeType.HR,
            CoreEmployeeType.ACCOUNTANT.title: CoreEmployeeType.ACCOUNTANT,
        }
        
        return switcher.get(title, None)
    

class PermissionType(Enum):
    ADD = 1
    VIEW = 2
    DELETE = 3
    CHANGE = 4
    
    @property
    def title(self):
        return self.name.title().lower()
    
    
    