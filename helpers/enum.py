
class Gender:
    MALE = (1, 'Male')
    FEMALE = (2, 'Female')

    __list__ = (MALE, FEMALE)


class FieldType:
    TEXT = (1, 'Text')
    CURRENCY = (2, 'Currency')
    DECIMAL = (3, 'Decimal')

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
    in_cash = (0, 'Cash')
    transfer = (1, 'Transfer money')

    __list__ = (in_cash, transfer)