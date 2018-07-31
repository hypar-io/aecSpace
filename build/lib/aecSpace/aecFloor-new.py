import traceback

from random import randint

from aecSpace.aecCorridor import aecCorridor
from aecSpace.aecGeometry import aecGeometry
from aecSpace.aecPoint import aecPoint
from aecSpace.aecShaper import aecShaper
from aecSpace.aecSpace import aecSpace
from aecSpace.aecSpaceGroup import aecSpaceGroup
from aecSpace.aecSpacer import aecSpacer

class aecFloor():
    """
    Represents the spatial configuration of a single floor.
    """ 
    __dimensionError = "Critical corridor dimension exceeds floor boundary."
    __minSpace = 1000
    __geometry = aecGeometry()
    __shaper = aecShaper() 
    __spacer = aecSpacer() 
    
    __slots__ = \
    [
        '__corridor',
        '__floor',
        '__rooms'
    ]   

    def __init__(self):
        self.__corridor = aecCorridor()
        self.__floor = aecSpace()
        self.__rooms = aecSpaceGroup()      
        points = self.__shaper.makeBox(xSize = 15000, ySize = 10000) 
        if points: 
            self.__floor.boundary = points
            self.__floor.height = 4000
            self.__floor.level = 0.0
            self.__corridor.space.height = 4000

    @property
    def corridor(self) -> aecSpace:
        """
        Returns the corridor space..
        Returns None on failure.
        """
        try:
            return self.__corridor
        except Exception:
            traceback.print_exc()
            return None
               
    @property
    def floor(self) -> aecSpace:
        """
        Returns the floor space..
        Returns None on failure.
        """
        try:
            return self.__floor
        except Exception:
            traceback.print_exc() 
            return None
        
    @property
    def rooms(self) -> aecSpaceGroup:
        """
        Returns the spaceGroup containing all the occupiable spaces.
        Returns None on failure.
        """
        try:
            return self.__rooms
        except Exception:
            traceback.print_exc() 
            return None
        
    def makeI(self, offset: float = 0,
                    rotation: float = 0,
                    roomsWest: int = 2,
                    roomsEast: int = 2,
                    roomsNorth: int = 0,
                    roomsNorthSize: float = 3000,
                    roomsSouth: int = 0,
                    roomsSouthSize: float = 3000) -> bool:
        """
        Sets the corridor to a centered box shape within the specified
        north and south margins of the delivered floor's bounding box.
        Populates the perimeter of the cooridor with the specified
        number of rooms in each compass quadrant and records the 
        list of room spaces in anticlockwise order, starting either
        from the southwestern room (if it exists) or the southeastern room.
        Returns None on Failure.
        """
        try:
            # Copy the incomming floor to avoid changing the original
            
            floor = self.__spacer.copy(self.floor)
            
            # Room types
            
            roomTypes = ['Office', 'Bathroom', 'Conference', 'Kitchen', 'Incubator']
            
            # Test and perform initial rotation.
                        
            rotate = 0
            if abs(rotation) <= aecGeometry.pi * 2: rotation = aecGeometry.toDegrees(rotation)
            if rotation < 0: rotate = abs(rotation)
            if rotation > 0: rotate = 0.0 - rotation
            if rotate != 0: floor.rotate(rotate)            
            if self.corridor.width >= floor.size_x: raise ValueError
            
            # Test proposed room quantities for feasibility
            
            roomsWest = abs(int(roomsWest))
            roomsEast = abs(int(roomsEast))
            roomsNorth = abs(int(roomsNorth))
            roomsSouth = abs(int(roomsSouth))
            if roomsNorth <= 0: 
                roomsNorth = 0
                roomsNorthSize = 0
            if roomsSouth <= 0: 
                roomsSouth = 0
                roomsSouthSize = 0
            if roomsNorth > 2: roomsNorth = 2
            if roomsSouth > 2: roomsSouth = 2   
            if roomsNorth > 0 and roomsNorthSize < self.__minSpace: roomsNorthSize = self.__minSpace
            if roomsSouth > 0 and roomsSouthSize < self.__minSpace: roomsSouthSize = self.__minSpace
            if floor.size_y <= (roomsNorthSize + roomsSouthSize): raise ValueError
            
            # Determine corridor origin
            
            floorBox = floor.points_box
            xPnt = self.__geometry.getMidpoint(floorBox.SW, floorBox.SE).x - (self.corridor.width * 0.5)
            xMin = floorBox.SW.x
            xMax = floorBox.SE.x - (self.corridor.width + self.__minSpace)
            xPnt += offset
            if xPnt < xMin: xPnt = xMin
            if xPnt > xMax: xPnt = xMax
            if xPnt == xMin: roomsWest = 0
            if xPnt == xMax: roomsEast = 0
            yPnt = floorBox.SW.y
            if roomsSouth > 0: yPnt += roomsSouthSize
            
            # Create the corridor
            
            self.corridor.space.level = floor.level
            origin = aecPoint(xPnt, yPnt)
            if roomsNorth > 0: ySize = abs((floorBox.NW.y - roomsNorthSize) - yPnt)
            else: ySize = abs(floorBox.NW.y - yPnt)
            points = self.__shaper.makeBox(origin = origin, 
                                           xSize = self.corridor.width, 
                                           ySize = ySize)
            if not points: raise Exception
            self.corridor.space.boundary = points
            if not self.corridor.space.fitWithin(floor.points_floor): return None
            
            # Create the Western rooms
            
            westRooms = None
            if roomsWest > 0:
                xRoom = abs(origin.x - floorBox.SW.x)
                yRoom = ySize / roomsWest
                xPnt = floorBox.SW.x
                yPnt = origin.y
                oRoom = aecPoint(xPnt, yPnt)
                points = self.__shaper.makeBox(origin = oRoom, 
                                               xSize = xRoom, 
                                               ySize = yRoom) 
                if not points: raise Exception
                room = aecSpace()
                room.boundary = points
                westRooms = [room] + self.__spacer.place(room, roomsWest - 1, y = yRoom)
                westRooms.reverse()
                for room in westRooms: room.name = roomTypes[randint(0, 4)]
            
            # Create the Eastern rooms
                
            eastRooms = None
            if roomsEast > 0:
                xRoom = abs(floorBox.SE.x - (origin.x + self.corridor.width))
                yRoom = ySize / roomsEast            
                xPnt = origin.x + self.corridor.width
                oRoom = aecPoint(xPnt, yPnt)
                points = self.__shaper.makeBox(origin = oRoom, 
                                               xSize = xRoom, 
                                               ySize = yRoom) 
                if not points: raise Exception
                room = aecSpace()
                room.boundary = points
                eastRooms = [room] + self.__spacer.place(room, roomsEast - 1, y = yRoom)
                for room in eastRooms: room.name = roomTypes[randint(0, 4)]
            
            # Create the North rooms
            
            northRooms = None
            if roomsNorth > 0:
                xPnt = floorBox.NW.x
                yPnt = floorBox.NW.y - roomsNorthSize
                oRoom = aecPoint(xPnt, yPnt)
                xRoom = abs(floorBox.NE.x - floorBox.NW.x)
                yRoom = roomsNorthSize
                if roomsNorth == 2: xRoom *= 0.5
                points = self.__shaper.makeBox(origin = oRoom, 
                                               xSize = xRoom, 
                                               ySize = yRoom)                 
                if not points: raise Exception
                room = aecSpace()
                room.boundary = points
                room.name = 'Lobby'
                northRooms = []
                northRooms.append(room)
                if roomsNorth == 2: 
                    northRooms.append(self.__spacer.copy(room, x = xRoom))
                    northRooms.reverse()
                    
            # Create the South rooms    
                 
            southRooms = None
            if roomsSouth > 0:
                xPnt = floorBox.SW.x
                yPnt = floorBox.SW.y
                oRoom = aecPoint(xPnt, yPnt)
                xRoom = abs(floorBox.NE.x - floorBox.NW.x)
                yRoom = roomsSouthSize
                if roomsSouth == 2: xRoom *= 0.5
                points = self.__shaper.makeBox(origin = oRoom, 
                                               xSize = xRoom, 
                                               ySize = yRoom)                 
                if not points: raise Exception
                room = aecSpace()
                room.boundary = points
                southRooms = []
                southRooms.append(room)
                if roomsSouth == 2: southRooms.append(self.__spacer.copy(room, x = xRoom))
                for room in southRooms: room.name = roomTypes[randint(0, 4)]
            
            # Create list of all rooms
            
            testRooms = []
            if southRooms: testRooms += southRooms
            if eastRooms: testRooms += eastRooms
            if northRooms: testRooms += northRooms
            if westRooms:  testRooms += westRooms
            
            # Test all rooms for inclusion in floor boundary and corridor adjacency
            
            finalRooms = []
            index = 0
            while index < len(testRooms):
                if not self.__geometry.areAdjacent(testRooms[index].points_floor, 
                                                   self.corridor.space.points_floor) or \
                                                   testRooms[index].area < self.__minSpace:
                   testRooms[(index + 1) % len(testRooms)].add(testRooms[index].points_floor)
                index += 1
            for room in testRooms:
                if room.fitWithin(floor.points_floor) and \
                self.__geometry.areAdjacent(room.points_floor, self.corridor.space.points_floor) and \
                room.area >= self.__minSpace:
                    finalRooms.append(room)            
            self.rooms.clear
            self.rooms.add(finalRooms)
            
            # Complete corridor rotation
            
            if rotation != 0:
                self.corridor.space.rotate(rotation, floor.center_floor)
                self.rooms.rotate(rotation, floor.center_floor)
            return True
        except ValueError:
            print(self.__dimensionError)
            if rotate != 0: floor.rotate(rotate)  
            return None
        except Exception:
            traceback.print_exc() 
            return None        
    