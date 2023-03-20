from django.db.models import Func, Aggregate
from django.db.models.functions.mixins import (
    FixDurationInputMixin
)
import math

class Sin(FixDurationInputMixin, Aggregate):
    function = 'SIN'
    name = 'Sin'
    allow_distinct = True


class Cos(FixDurationInputMixin, Aggregate):
    function = 'COS'
    name = "Cos"
    allow_distinct: bool = True

class Methods:

    @staticmethod
    def is_in_range(origin, destination) -> bool:
        return Methods.distance(origin, destination)

    @staticmethod
    def distance(origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        
        radius = 6371e3  # meters
        pi_180 = math.pi / 180
        f1 = lat1 * pi_180
        f2 = lat2 * pi_180

        f_delta = (lat2 - lat1) * pi_180
        l_delta = (lon2 - lon1) * pi_180

        a = math.sin(f_delta / 2.0) ** 2.0 + \
            math.cos(f1) * math.cos(f2) * \
            math.sin(l_delta / 2.0) ** 2.0

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return d
