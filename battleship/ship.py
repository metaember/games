from common import *

class PlacementError(Exception):
    """Exception raised for errors in the ship placement.

    Attributes:
        message -- explanation of the error
    """

    def __init__(self, message):
        self.message = message


class Ship ():
    members = []

    def __init__(self, x=None, y=None, size=None, direction=None, owner=None):
        self.x = x
        self.y = y
        self.size = size
        self.direction = direction
        self.members.append(self)
        self.owner = owner

        if self.x is None or self.y is None or self.direction is None:
            self.x = int(input("\tX coord ? "))
            self.y = int(input("\tY coord ? "))
            self.direction = input("\tDirection (NSEW) ? ").upper()

        if self.size is None:
            self.size = int(input("\tSize? "))

        self.cells = [0 for x in range(self.size)]

    def is_sunk(self):
        return 0 not in self.cells

    def touch(self, dist_from_origin):
        self.cells[dist_from_origin] = "pre pull"

    def add_to_board(self, board):
        try:
            startX = self.x
            startY = self.y
            direction = self.direction
            shipSize = self.size

            if direction == 'N':
                endX = startX
                startX = startX - shipSize + 1

                if SHIPCHAR in list(board.loc[startX:endX, startY]):
                    raise PlacementError("Ship collision!")

                elif NOSHIPCHAR in list(board.loc[startX:endX, startY]):
                    raise PlacementError("Ships Touching!")

                board.loc[startX-1:endX+1, startY-1:startY+1] = NOSHIPCHAR
                board.loc[startX:endX, startY] = [SHIPCHAR for i in range(shipSize)]

            elif direction == "S":

                endX = startX + shipSize - 1
                if SHIPCHAR in list(board.loc[startX:endX,startY]):
                    raise PlacementError("Ship collision!")

                elif NOSHIPCHAR in list(board.loc[startX:endX,startY]):
                    raise PlacementError("Ships Touching!")

                board.loc[startX-1:endX+1, startY-1:startY+1] = NOSHIPCHAR
                board.loc[startX:endX, startY] = [SHIPCHAR for i in range(shipSize)]

            elif direction == "E":
                endY = startY + shipSize - 1

                if SHIPCHAR in list(board.loc[startX, startY:endY]):
                    raise PlacementError("Ship collision!")

                elif NOSHIPCHAR in list(board.loc[startX,startY:endY]):
                    raise PlacementError("Ships Touching!")

                board.loc[startX-1:startX+1, startY-1:endY+1] = NOSHIPCHAR
                board.loc[startX,startY:endY] = [SHIPCHAR for i in range(shipSize)]

            elif direction == "W":
                endY = startY
                startY = startY - shipSize + 1

                if SHIPCHAR in list(board.loc[startX, startY:endY]):
                    raise PlacementError("Ship collision!")

                elif NOSHIPCHAR in list(board.loc[startX,startY:endY]):
                    raise PlacementError("Ships Touching!")

                board.loc[startX-1:startX+1, startY-1:endY+1] = NOSHIPCHAR
                board.loc[startX, startY:endY] = [SHIPCHAR for i in range(shipSize)]

            else:
                print("Direction nust be one of the following : N, S, E, W")
        except ValueError as err:
            print ("Ship cannot fit in this location!")
