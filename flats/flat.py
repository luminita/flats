# -*- coding: utf-8 -*-
import datetime



class Flat:
    """
    def __init__(self, sold_date, price, price_per_m2, asked_price, address, area, city, broker, living_area_m2,
                 living_area_rooms, land_area, supp_area, flat_type):
        self.sold_date = sold_date
        self.price = price
        self.price_per_m2 = price_per_m2
        self.asked_price = asked_price
        self.address = address
        self.area = area
        self.city = city
        self.broker = broker
        self.living_area_m2 = living_area_m2
        self.living_area_rooms = living_area_rooms
        self.land_area = land_area
        self.supp_area = supp_area
        self.flat_type = flat_type
    """

    def __init__(self, **kwargs):
        for key, value in kwargs.iteritems():
            self.__dict__[key] = value

