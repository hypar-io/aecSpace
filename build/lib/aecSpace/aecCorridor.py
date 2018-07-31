import traceback

from typing import List

from aecSpace.aecGeometry import aecGeometry
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer

class aecCorridor():
    """
    Represents architectural corridors of various configurations.
    """
    __dimensionError = "Critical corridor dimension exceeds floor boundary."
    __minPersons = 3
    __personWidth = 570
    __geometry = aecGeometry()
    __shaper = aecShaper() 
    __spacer = aecSpacer()
    
    # Defines a series of constants indicating corridor types.
    
    Unknown, H, I, L, T, U, X  = range(0, 7)
    
    __slots__ = \
    [
        '__compass',   
        '__corridor',
        '__persons',
        '__shape',
        '__space',
        '__width'
    ]   
    
    def __init__(self, corridor: int = 1,
                       origin: aecPoint = aecPoint(),
                       xSize: float = 1700, 
                       ySize: float = 1700, 
                       persons: int = 3):
        """
        Constructor       
        """
        self.__compass = self.__geometry.compass
        self.__corridor = aecSpace()
        self.__persons = self.__minPersons
        self.__shape = self.Unknown
        self.__width = self.__minPersons * self.__personWidth
        if persons > self.__minPersons: 
            self.__persons = persons = int(persons)
            persons -= self.__minPersons
            self.__width += (persons * self.__personWidth)
        self.__space = aecSpace()

    @property
    def persons(self) -> int:
        """
        Returns the capacity of the corridor as the quantity of 
        persons who can pass along its length simultaneously.
        Returns None on failure.
        """
        try:
            return self.__persons
        except Exception:
            traceback.print_exc() 
            return None
        
    @persons.setter
    def persons(self, value: int = 3) -> int:
        """
        Sets the capacity of the corridor as the quantity of 
        persons who can pass along its length simultaneously.
        Returns None on failure.
        """
        try:
            value = abs(int(value))
            if value < self.__minPersons: value = self.__minPersons
            self.__persons = value
            if value > self.__minPersons: value -= self.__minPersons
            self.__width += self.__personWidth * value
        except Exception:
            traceback.print_exc() 
            
    @property
    def space(self) -> aecSpace:
        """
        Returns the aecSpace object.
        Returns None on failure.
        """
        try:
            return self.__space
        except Exception:
            traceback.print_exc() 
            return None
        
    @property
    def width(self) -> float:
        """
        Returns the corridor width.
        Returns None on failure.
        """
        try:
            return self.__width
        except Exception:
            traceback.print_exc() 
            return None        

    def addLobby(self, lobby: aecSpace) -> bool:
        """
        Attempts to join a lobby to the corridor
        """
               
    def makeH(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to an H shape within the specified
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if (self.width * 2) >= floor.size_x or \
                self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeH(origin = origin,
                                         xSize = xSize,
                                         ySize = ySize,
                                         xWidth1 = self.width,
                                         xWidth2 = self.width,
                                         yDepth = self.width)
            if not points: raise Exception
            self.__space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)                
        except ValueError:
            print(self.__dimensionError)
            return False        
        except Exception:
            traceback.print_exc() 
            return False
        
    def makeL(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to an L shape within the specified
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if self.width >= floor.size_x or \
               self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeL(origin = origin,
                                         xSize = xSize,
                                         ySize = ySize,
                                         xWidth = self.width,
                                         yDepth = self.width)
            if not points: raise Exception
            self.__space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)            
        except ValueError:
            print(self.__dimensionError)
            return False
        except Exception:
            traceback.print_exc() 
            return False        

       
    def makeT(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to an T shape within the specified
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if self.width >= floor.size_x or \
               self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeT(origin = origin,
                                         xSize = xSize,
                                         ySize = ySize,
                                         xWidth = self.width,
                                         yDepth = self.width)
            if not points: raise Exception
            self.__space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)            
        except ValueError:
            print(self.__dimensionError)
            return False
        except Exception:
            traceback.print_exc() 
            return False                
           
    def makeU(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to a U shape within the specified
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if (self.width * 2) >= floor.size_x or \
                self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeU(origin = origin,
                                         xSize = xSize,
                                         ySize = ySize,
                                         xWidth1 = self.width,
                                         xWidth2 = self.width,
                                         yDepth = self.width)
            if not points: raise Exception
            self.__space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)                
        except ValueError:
            print(self.__dimensionError)
            return False
        except Exception:
            traceback.print_exc() 
            return False       
        
    def makeX(self, floor: aecSpace, margin: float = 0.0, rotate: float = 0.0) -> bool:
        """
        Sets the corridor to a cross shape within the
        margin of the delivered floor's bounding box.
        Returns True on success.
        Returns False on Failure.
        """
        try:
            if self.width >= floor.size_x or \
               self.width >= floor.size_y: raise ValueError
            self.space.height = floor.height- 0.25
            self.space.level = floor.level
            floorBox = floor.points_box
            xPnt = floorBox.SW.x + margin
            yPnt = floorBox.SW.y + margin
            origin = aecPoint(xPnt, yPnt)
            xSize = abs((floorBox.SE.x - margin) - xPnt)
            ySize = abs((floorBox.NW.y - margin) - yPnt)
            points = self.__shaper.makeCross(origin = origin,
                                             xSize = xSize,
                                             ySize = ySize,
                                             xWidth = self.width,
                                             yDepth = self.width)
            if not points: raise Exception
            self.space.boundary = points
            self.space.rotate(rotate)
            return self.space.fitWithin(floor.points_floor)
        except ValueError:
            print(self.__dimensionError)
            return False        
        except Exception:
            traceback.print_exc() 
            return False       
        
