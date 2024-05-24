from .Animal import Animal
from .Lynx import Lynx
from Position import Position
import random
from Action import Action
from ActionEnum import ActionEnum

class Antelope(Animal):

    def __init__(self, antelope=None, position=None, world=None):
        super(Antelope, self).__init__(antelope, position, world)

    def clone(self):
        return Antelope(self, None, None)

    def initParams(self):
        self.power = 4
        self.initiative = 3
        self.liveLength = 11
        self.powerToReproduce = 5
        self.sign = 'A'

    def getNeighboringPosition(self):
        return self.world.filterPositionsWithoutAnimals(self.world.getNeighboringPositions(self.position))

    def move(self):
        result = []
        pomPositions = self.getNeighboringPosition()
        newPosition = None

        if pomPositions:
            for pos in pomPositions:
                organism = self.world.getOrganismFromPosition(pos)
                if isinstance(organism, Lynx):
                    # Run away from Lynx
                    x_diff = self.position.x - organism.position.x
                    y_diff = self.position.y - organism.position.y
                    new_x = self.position.x + (2 * x_diff)
                    new_y = self.position.y + (2 * y_diff)
                    newPosition = Position(new_x, new_y)
                    break
            else:
                # Normal move
                newPosition = random.choice(pomPositions)

            if newPosition and self.world.positionOnBoard(newPosition):
                result.append(Action(ActionEnum.A_MOVE, newPosition, 0, self))
                self.lastPosition = self.position
                metOrganism = self.world.getOrganismFromPosition(newPosition)
                if metOrganism is not None:
                    result.extend(metOrganism.consequences(self))
        return result