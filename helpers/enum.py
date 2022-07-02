
from dataclasses import field

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


class FieldType:
    TEXT = (1, 'Text')
    CURRENCY = (2, 'Currency')
    DECIMAL = (3, 'Decimal')
    
    @classmethod
    def typeInfo(cls, type: int):
        switcher = {
            1: FieldType.TEXT,
            2: FieldType.CURRENCY,
            3: FieldType.DECIMAL,
        }
        fieldType = switcher.get(type, FieldType.TEXT)
        return {
            'id': fieldType[0],
            'name': fieldType[1],
        }

    __list__ = (TEXT, CURRENCY, DECIMAL)


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