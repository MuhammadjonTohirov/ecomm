import math
from django.test import TestCase

class Methods:

    @staticmethod
    def is_in_range(origin, destination) -> bool:
        return Methods.distance(origin, destination) <= 10

    @staticmethod
    def distance(origin, destination):
        lat1, lon1 = origin
        lat2, lon2 = destination
        
        print(lat1, lon1)
        print(lat2, lon2)
        radius = 6371e3  # meters
        pi_180 = math.pi / 180
        f1 = lat1 * pi_180
        f2 = lat2 * pi_180

        f_delta = (lat2 - lat1) * pi_180
        l_delta = (lon2 - lon1) * pi_180

        a = math.sin(f_delta/2) * math.sin(f_delta/2) + \
            math.cos(f1) * math.cos(f2) * \
            math.sin(l_delta / 2) * math.sin(l_delta / 2)

        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c
        return d



# Create your tests here.

print(Methods.distance((40.378962, 71.707145), (40.378928, 71.707335)))