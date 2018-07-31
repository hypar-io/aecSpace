import traceback

from typing import NamedTuple

from .aecPoint import aecPoint

class aecCompass:
    """
    Manages a collection of points at positions relative to one another according to 16 notional compass points.
    """
    N, NNE, NE, ENE, E, ESE, SE, SSE, S, SSW, SW, WSW, W, WNW, NW, NNW = range(0, 16)

    __slots__ = \
        [
            '__orient',
        ] 

    def __init__(self):
        """
        Constructor by default creates an Equatorial corridor.       
        """
        self.__orient = \
            NamedTuple(
            'orient',
            [
                ('N', aecPoint),
                ('NNE', aecPoint),
                ('NE', aecPoint),
                ('ENE', aecPoint),
                ('E', aecPoint),
                ('ESE', aecPoint),
                ('SE', aecPoint),
                ('SSE', aecPoint),
                ('S', aecPoint),
                ('SSW', aecPoint),
                ('SW', aecPoint),
                ('WSW', aecPoint),
                ('W', aecPoint),
                ('WNW', aecPoint),
                ('NW', aecPoint),
                ('NNW', aecPoint),            
            ])
        self.__orient.N = aecPoint()
        self.__orient.NNE = aecPoint()
        self.__orient.NE = aecPoint()
        self.__orient.ENE = aecPoint()
        self.__orient.E = aecPoint()
        self.__orient.ESE = aecPoint()
        self.__orient.SE = aecPoint()
        self.__orient.SSE = aecPoint()
        self.__orient.S = aecPoint()
        self.__orient.SSW = aecPoint()
        self.__orient.SW = aecPoint()
        self.__orient.WSW = aecPoint()
        self.__orient.W = aecPoint()
        self.__orient.WNW = aecPoint()
        self.__orient.NW = aecPoint()
        self.__orient.NNW = aecPoint()


    @property
    def orient(self) -> NamedTuple:
        """
        Returns the orientation list.
        """
        try:
            return self.__orient
        except Exception:
            traceback.print_exc() 
            return False
            
    
   
                

